# -*- coding: utf-8 -*-
"""Draw the proposal mind map (left-right tree) from scratchpad/mindmap.mmd."""
import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch
from matplotlib.path import Path as MPath
import matplotlib.patches as mpatches

MMD, OUT, FONTDIR = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
for f in FONTDIR.glob("NotoSansSC-*.ttf"):
    font_manager.fontManager.addfont(str(f))
plt.rcParams["font.family"] = "Noto Sans SC"
plt.rcParams["text.parse_math"] = False

# ---------- parse indented mindmap ----------
class N:
    def __init__(s, t, d): s.t, s.d, s.kids, s.y = t, d, [], 0.0
lines = [l for l in MMD.read_text(encoding="utf-8").splitlines() if l.strip() and l.strip() != "mindmap"]
root_txt = lines[0].strip()
root_txt = root_txt.replace("root)", "").rstrip("(").strip()
root = N(root_txt, 0); stack = [root]
for l in lines[1:]:
    d = (len(l) - len(l.lstrip(" "))) // 2 - 1   # branch = depth 1
    node = N(l.strip(), d)
    while stack and stack[-1].d >= d: stack.pop()
    stack[-1].kids.append(node); stack.append(node)

def leaves(n): return 1 if not n.kids else sum(leaves(k) for k in n.kids)

# ---------- split sides ----------
branches = root.kids
right, left = [], []
for b in branches:              # greedy balance by leaf count
    (right if sum(leaves(x) for x in right) <= sum(leaves(x) for x in left) else left).append(b)

PAL = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948", "#6b7480"]
color = {b.t: PAL[i] for i, b in enumerate(branches)}

# ---------- layout ----------
SLOT = 0.56           # vertical unit per leaf
def assign_y(nodes, top):
    y = top
    for n in nodes:
        if n.kids:
            assign_y(n.kids, y); n.y = sum(k.y for k in n.kids) / len(n.kids); y -= leaves(n) * SLOT
        else:
            n.y = y - SLOT / 2; y -= SLOT
for side in (right, left):
    total = sum(leaves(b) for b in side) * SLOT
    assign_y(side, total / 2)
    # add small gaps between branches
    gap_acc = 0.0
    def shift(n, dy):
        n.y += dy
        for k in n.kids: shift(k, dy)
    for i, b in enumerate(side):
        shift(b, -gap_acc); gap_acc += 0.38
    # recenter
    allnodes = []
    def collect(n): allnodes.append(n); [collect(k) for k in n.kids]
    for b in side: collect(b)
    mid = (max(n.y for n in allnodes) + min(n.y for n in allnodes)) / 2
    for n in allnodes: n.y -= mid

def est_w(t, fs):
    w = 0
    for ch in t:
        w += fs * (1.0 if ord(ch) > 0x2E7F else 0.56)
    return w / 72 * 1.0 + 0.35   # inches incl. padding

FS = {1: 13, 2: 11, 3: 10.2}
X_GAP = 0.55
def depth_x(side):
    xs = {0: 0.0}
    cur = est_w(root.t, 16) / 2 + X_GAP
    maxw = {}
    def walk(n):
        maxw[n.d] = max(maxw.get(n.d, 0), est_w(n.t, FS.get(n.d, 9.6)))
        for k in n.kids: walk(k)
    for b in side: walk(b)
    for d in sorted(maxw):
        xs[d] = cur; cur += maxw[d] + X_GAP
    return xs
xr, xl = depth_x(right), depth_x(left)

# ---------- draw ----------
H = max(sum(leaves(b) for b in right) * SLOT + 0.38 * len(right), sum(leaves(b) for b in left) * SLOT + 0.38 * len(left))
W = (max(xr.values()) + max(est_w(n.t, 9.6) for n in [root]) + 3.2) + (max(xl.values()) + 3.2)
fig = plt.figure(figsize=(W, H + 1.2), dpi=150)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(-(max(xl.values()) + 3.3), max(xr.values()) + 3.3); ax.set_ylim(-H / 2 - 0.6, H / 2 + 0.6); ax.axis("off")

def box(x, y, t, fs, fc, ec, tc, align, bold=False):
    ha = "left" if align > 0 else "right"
    ax.text(x, y, t, fontsize=fs, ha=ha, va="center", color=tc, fontweight="bold" if bold else "normal",
            bbox=dict(boxstyle="round,pad=0.32,rounding_size=0.25", fc=fc, ec=ec, lw=1.0), zorder=3)

def curve(x0, y0, x1, y1, c, lw):
    mx = (x0 + x1) / 2
    p = MPath([(x0, y0), (mx, y0), (mx, y1), (x1, y1)], [MPath.MOVETO, MPath.CURVE4, MPath.CURVE4, MPath.CURVE4])
    ax.add_patch(mpatches.PathPatch(p, fc="none", ec=c, lw=lw, zorder=1, alpha=0.9))

def lighten(hexc, f=0.85):
    r, g, b = int(hexc[1:3], 16), int(hexc[3:5], 16), int(hexc[5:7], 16)
    return "#%02x%02x%02x" % tuple(int(v + (255 - v) * f) for v in (r, g, b))

def draw(n, side, xs, c, parent_anchor=None):
    sgn = 1 if side is right else -1
    x = sgn * xs[n.d]
    w = est_w(n.t, FS.get(n.d, 9.6))
    if n.d == 1:
        box(x, n.y, n.t, FS[1], c, c, "white", sgn, bold=True)
    elif n.d == 2:
        box(x, n.y, n.t, FS[2], lighten(c, 0.82), c, "#182430", sgn, bold=True)
    else:
        box(x, n.y, n.t, FS[3], "#ffffff", lighten(c, 0.4), "#2b3540", sgn)
    if parent_anchor:
        curve(parent_anchor[0], parent_anchor[1], x - sgn * 0.05, n.y, c, 2.2 if n.d == 1 else 1.3)
    my_anchor = (x + sgn * (w - 0.1), n.y)
    for k in n.kids: draw(k, side, xs, c, my_anchor)

for b in right: draw(b, right, xr, color[b.t], (est_w(root.t, 16) / 2 - 0.1, 0))
for b in left: draw(b, left, xl, color[b.t], (-(est_w(root.t, 16) / 2 - 0.1), 0))
ax.text(0, 0, root.t, fontsize=16, ha="center", va="center", color="white", fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.6,rounding_size=0.4", fc="#182430", ec="#182430"), zorder=4)
ax.text(ax.get_xlim()[0] + 0.3, ax.get_ylim()[0] + 0.25,
        "MT6102 Maritime Economics · 方案思维导图 · 数据 Clarksons SIN，2026-09-12 提取 · 叶子节点均对应数据版 PDF 章节",
        fontsize=8.5, color="#6b7480", ha="left", va="bottom")
fig.savefig(OUT, dpi=150, facecolor="white")
print("saved", OUT, f"{W:.1f}x{H+1.6:.1f} in")
