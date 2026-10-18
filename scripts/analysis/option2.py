import pandas as pd, numpy as np
pd.set_option('display.width', 220)
R = '/home/user/MT6102/data/raw/'
def ser(f, col):
    d = pd.read_csv(R + f + '_20260912.csv', parse_dates=['Date']).set_index('Date')
    return d.iloc[:, col - 1].dropna().astype(float)
km_spot = ser('L5', 1); mr_eco = ser('L5', 3); mr_2010 = ser('C4', 2)
km_tc = ser('B5', 1); mr_tc = ser('B1', 1)
FS = 92 / 365; FT = 273 / 365

def roll(name, spot, tc, start, months=None):
    m = spot.resample('MS').mean()
    rows = []
    for t0 in tc[start:].index:
        if months and t0.month not in months: continue
        t3 = t0 + pd.DateOffset(months=3)
        if t3 not in tc.index: continue
        sp = spot[t0 + pd.DateOffset(months=1): t3 + pd.DateOffset(months=1) - pd.Timedelta(days=1)]
        if len(sp) < 10 or t0 not in m.index: continue
        A = tc[t0]; B = FS * sp.mean() + FT * tc[t3]
        rows.append(dict(t0=t0, ratio=m[t0] / A, gain=B - A, sp=FS * (sp.mean() - A), tcp=FT * (tc[t3] - A), tcchg=(tc[t3] / A - 1) * 100))
    d = pd.DataFrame(rows).set_index('t0')
    for lab, s in [('all', d), ('spot<=TC', d[d.ratio <= 1]), ('spot>TC', d[d.ratio > 1]), ('spot/TC>1.15', d[d.ratio > 1.15])]:
        if len(s):
            print(f'{name} {lab}: n={len(s)} years={s.index.year.nunique()} wins {(s.gain>0).mean():.2f} mean {s.gain.mean():,.0f} median {s.gain.median():,.0f} | spot part {s.sp.mean():,.0f} tc part {s.tcp.mean():,.0f} | mean TC chg {s.tcchg.mean():+.1f}% share TC up {(s.tcchg>0).mean():.2f}')
    return d

print('--- quarterly non-overlapping starts (Mar, Jun, Sep, Dec)')
roll('KM', km_spot, km_tc, '2010', [3, 6, 9, 12])
roll('MR c2010', mr_2010, mr_tc, '2014-05', [3, 6, 9, 12])
roll('MR Eco', mr_eco, mr_tc, '2020', [3, 6, 9, 12])
print('--- Sep and Oct starts only')
for mo in [9, 10]:
    roll(f'KM m{mo}', km_spot, km_tc, '2010', [mo])
    roll(f'MRc2010 m{mo}', mr_2010, mr_tc, '2014-05', [mo])
    roll(f'MREco m{mo}', mr_eco, mr_tc, '2020', [mo])
print('--- excluding Sep-Nov starts (non-seasonal months)')
roll('KM ex SepOctNov', km_spot, km_tc, '2010', [1, 2, 3, 4, 5, 6, 7, 8, 12])

# 12 months full spot from Oct vs Sep 1-yr TC
print('\n--- full 12-month spot (Oct Y to Sep Y+1) vs Sep Y 1-yr TC')
for nm, sp, tc, y0 in [('KM', km_spot, km_tc, 2010), ('MRc2010', mr_2010, mr_tc, 2014), ('MREco', mr_eco, mr_tc, 2020)]:
    r = []
    for y in range(y0, 2026):
        s = sp[f'{y}-10-01':f'{y+1}-09-30']
        if len(s) < 50: continue
        r.append((y, s.mean() - tc[pd.Timestamp(f'{y}-09-01')]))
    g = pd.Series(dict(r))
    print(nm, f'spot12 beats TC {int((g>0).sum())}/{len(g)} mean {g.mean():,.0f} median {g.median():,.0f}', ' '.join(f'{k}:{v:+,.0f}' for k, v in g.items()))

# break-even probability for 2026
print('\n--- 2026 break-even')
pcs = {}
for nm, tc in [('KM', km_tc['2010':]), ('MR', mr_tc)]:
    pc = (tc.shift(-3) / tc - 1).dropna() * 100
    pcs[nm] = pc
for nm, spot_now, tc_now in [('KM', 23389, 19750), ('MR', 53741, 43000)]:
    pc = pcs[nm]; sd = pc[pc.index.month == 9]
    for q4f in [1.0, 0.9, 0.8, tc_now / spot_now]:
        q4 = spot_now * q4f
        be = (tc_now - FS * q4) / FT; bep = (be / tc_now - 1) * 100
        print(f'{nm} Q4 spot {q4:,.0f}: break-even Dec TC {be:,.0f} ({bep:+.1f}%); hist share 3m TC change below that: all months {(pc < bep).mean():.2f}, Sep->Dec {(sd < bep).sum()}/{len(sd)}')

# 2026 monthly averages
for nm, s in [('KM spot', km_spot), ('MR eco spot', mr_eco), ('MR c2010', mr_2010)]:
    print(nm, ' '.join(f'{d:%b}:{v:,.0f}' for d, v in s['2026'].resample('MS').mean().items()))
print('KM TC 2026', ' '.join(f'{d:%b}:{v:,.0f}' for d, v in km_tc['2026'].items()))
print('MR TC 2026', ' '.join(f'{d:%b}:{v:,.0f}' for d, v in mr_tc['2026'].items()))
