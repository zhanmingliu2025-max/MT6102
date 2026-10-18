import re
from copy import deepcopy
from lxml import etree
A='http://schemas.openxmlformats.org/drawingml/2006/main'
P='http://schemas.openxmlformats.org/presentationml/2006/main'
NS={'a':A,'p':P}
E=914400
def q(t): return '{%s}%s'%(A,t)
def qp(t): return '{%s}%s'%(P,t)
def ptext(p): return ''.join(t.text or '' for t in p.iter(q('t')))

def parse(marked):
    out=[]; bold=False
    for i,part in enumerate(marked.split('**')):
        if part: out.append((part, i%2==1))
    return out

def style_rpr(rpr, sz=None, b=None, i=None, color=None, font=None):
    if sz is not None: rpr.set('sz', str(sz))
    if b is not None: rpr.set('b','1' if b else '0')
    if i is not None: rpr.set('i','1' if i else '0')
    if color:
        sf=rpr.find(q('solidFill'))
        if sf is None:
            sf=etree.Element(q('solidFill'))
            ln=rpr.find(q('ln'))
            if ln is not None: ln.addnext(sf)
            else: rpr.insert(0,sf)
        for c in list(sf): sf.remove(c)
        etree.SubElement(sf,q('srgbClr')).set('val',color)
    if font:
        for tag in ('latin','ea','cs'):
            e=rpr.find(q(tag))
            if e is not None: e.set('typeface',font)

def set_para(p, marked=None, sz=None, color=None, font=None, base_b=None, i=None, bold_color=None):
    if marked is None: marked=ptext(p)
    runs=p.findall(q('r'))
    tmpl=deepcopy(runs[0].find(q('rPr')))
    for r in runs+p.findall(q('br')): p.remove(r)
    end=p.find(q('endParaRPr'))
    segs=parse(marked)
    assert ''.join(s for s,_ in segs).count('**')==0
    for text,bold in segs:
        r=etree.Element(q('r')); rp=deepcopy(tmpl)
        style_rpr(rp, sz=sz, b=(True if bold else base_b), i=i, color=(bold_color if (bold and bold_color) else color), font=font)
        r.append(rp); t=etree.SubElement(r,q('t')); t.text=text
        if end is not None: end.addprevious(r)
        else: p.append(r)
    if end is not None and sz: end.set('sz',str(sz))
    return p

class Slide:
    def __init__(self, path):
        self.path=path; self.tree=etree.parse(path); self.root=self.tree.getroot(); self.log=[]
    def paras(self): return list(self.root.iter(q('p')))
    def find(self, old, startswith=False):
        hits=[p for p in self.paras() if (ptext(p).startswith(old) if startswith else ptext(p)==old)]
        assert len(hits)==1, f'{self.path}: {len(hits)} hits for {old[:70]!r}'
        return hits[0]
    def edit(self, old, new=None, **kw):
        p=self.find(old); set_para(p, new, **kw); self.log.append((old, ptext(p))); return p
    def shape_of(self, p):
        e=p
        while e is not None and e.tag not in (qp('sp'),q('tc')): e=e.getparent()
        return e
    def table(self, idx=0):
        return list(self.root.iter(q('tbl')))[idx]
    def cell(self, r, c, idx=0):
        return self.table(idx).findall(q('tr'))[r].findall(q('tc'))[c]
    def cell_paras(self, r, c, idx=0):
        return [p for p in self.cell(r,c,idx).iter(q('p')) if p.findall(q('r'))]
    def next_id(self):
        return max(int(e.get('id')) for e in self.root.iter(qp('cNvPr')))+1
    def set_xfrm(self, sp, x=None, y=None, w=None, h=None):
        off=sp.find('.//a:off',NS); ext=sp.find('.//a:ext',NS)
        if x is not None: off.set('x',str(round(x*E)))
        if y is not None: off.set('y',str(round(y*E)))
        if w is not None: ext.set('cx',str(round(w*E)))
        if h is not None: ext.set('cy',str(round(h*E)))
    def clone_sp(self, sp, name, marked, x=None, y=None, w=None, h=None, algn=None, **kw):
        n=deepcopy(sp)
        c=n.find('.//p:cNvPr',NS); c.set('id',str(self.next_id())); c.set('name',name)
        ps=n.findall('.//a:p',NS)
        for extra in ps[1:]: extra.getparent().remove(extra)
        set_para(ps[0], marked, **kw)
        if algn:
            ppr=ps[0].find(q('pPr'))
            ppr.set('algn',algn)
        self.set_xfrm(n,x,y,w,h)
        sp.addnext(n)
        self.log.append(('NEW '+name, ptext(ps[0])))
        return n
    def save(self):
        self.tree.write(self.path, xml_declaration=True, encoding='UTF-8', standalone=True)

def set_cell_fill(tc, color):
    tcpr=tc.find(q('tcPr'))
    sf=tcpr.find(q('solidFill'))
    sf.find(q('srgbClr')).set('val',color)

def set_notes(path, text):
    t=etree.parse(path); root=t.getroot()
    body=None
    for sp in root.iter(qp('sp')):
        ph=sp.find('.//p:ph',NS)
        if ph is not None and ph.get('type')=='body': body=sp
    tx=body.find(qp('txBody'))
    old=tx.findall(q('p'))
    tmpl=old[0]
    for p in old: tx.remove(p)
    parts=[s.strip() for s in re.split(r'(?=If asked)', text) if s.strip()]
    for s in parts:
        p=deepcopy(tmpl)
        for r in p.findall(q('r'))[1:]: p.remove(r)
        p.find(q('r')).find(q('t')).text=s
        tx.append(p)
    t.write(path, xml_declaration=True, encoding='UTF-8', standalone=True)
