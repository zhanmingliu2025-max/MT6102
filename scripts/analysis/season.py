import pandas as pd, numpy as np, sys
pd.set_option('display.width', 220); pd.set_option('display.max_columns', 30); pd.set_option('display.max_rows', 200)
R = '/home/user/MT6102/data/raw/'
def ser(f, col):
    d = pd.read_csv(R + f + '_20260912.csv', parse_dates=['Date']).set_index('Date')
    return d.iloc[:, col - 1].dropna().astype(float)

km_spot = ser('L5', 1)        # 533288 Kamsarmax Eco weekly
mr_eco = ser('L5', 3)         # 543759 MR Eco weekly
mr_2010 = ser('C4', 2)        # 545055 MR c2010 weekly
km_tc = ser('B5', 1)          # 540614 monthly
mr_tc = ser('B1', 1)          # 541552 monthly

def monthly(s):
    return s.resample('MS').mean()

def season(name, spot, tc, y0, y1):
    print('\n' + '=' * 100 + '\n' + name)
    m = monthly(spot)
    rows = []
    for y in range(y0, y1 + 1):
        yr = spot[str(y)]
        q4 = spot[f'{y}-10-01':f'{y}-12-31']
        q1n = spot[f'{y+1}-01-01':f'{y+1}-03-31']
        q3 = spot[f'{y}-07-01':f'{y}-09-30']
        sep_spot = m.get(pd.Timestamp(f'{y}-09-01'), np.nan)
        tc_sep = tc.get(pd.Timestamp(f'{y}-09-01'), np.nan)
        tc_oct = tc.get(pd.Timestamp(f'{y}-10-01'), np.nan)
        rows.append(dict(year=y, ann=yr.mean(), q3=q3.mean(), q4=q4.mean(), q1next=q1n.mean() if len(q1n) else np.nan,
                         sep_spot=sep_spot, tc_sep=tc_sep, tc_oct=tc_oct))
    t = pd.DataFrame(rows).set_index('year')
    t['q4_vs_ann_%'] = (t.q4 / t.ann - 1) * 100
    t['q4_vs_q1n_%'] = (t.q4 / t.q1next - 1) * 100
    t['q4_vs_q3_%'] = (t.q4 / t.q3 - 1) * 100
    t['q4_minus_tcSep'] = t.q4 - t.tc_sep
    print(t.round(0).to_string())
    full = t.dropna(subset=['ann'])
    print(f"Q4 > annual avg: {(full.q4 > full.ann).sum()}/{len(full)}; mean Q4 vs annual {full['q4_vs_ann_%'].mean():.1f}%, median {full['q4_vs_ann_%'].median():.1f}%; mean $ diff {(full.q4-full.ann).mean():,.0f}")
    q1 = t.dropna(subset=['q1next'])
    print(f"Q4 > next Q1: {(q1.q4 > q1.q1next).sum()}/{len(q1)}; mean Q4 vs next Q1 {q1['q4_vs_q1n_%'].mean():.1f}%, median {q1['q4_vs_q1n_%'].median():.1f}%")
    print(f"Q4 > Q3 same yr: {(full.q4 > full.q3).sum()}/{len(full)}; mean {full['q4_vs_q3_%'].mean():.1f}%, median {full['q4_vs_q3_%'].median():.1f}%")
    tt = t.dropna(subset=['tc_sep'])
    print(f"Q4 spot > Sep 1-yr TC: {(tt.q4 > tt.tc_sep).sum()}/{len(tt)}; mean diff {tt.q4_minus_tcSep.mean():,.0f}, median {tt.q4_minus_tcSep.median():,.0f}")
    # same test for every quarter vs TC at end of previous quarter (controls for Eco-vs-TC basis)
    qs = []
    for y in range(y0, y1 + 1):
        for q, (ms, me, tcm) in enumerate([((1, 1), (3, 31), (y - 1, 12)), ((4, 1), (6, 30), (y, 3)), ((7, 1), (9, 30), (y, 6)), ((10, 1), (12, 31), (y, 9))], 1):
            s = spot[f'{y}-{ms[0]:02d}-01':f'{y}-{me[0]:02d}-{me[1]}']
            tcv = tc.get(pd.Timestamp(f'{tcm[0]}-{tcm[1]:02d}-01'), np.nan)
            if len(s) and not np.isnan(tcv):
                qs.append(dict(year=y, q=q, spot=s.mean(), tc_prev=tcv, ann=spot[str(y)].mean()))
    qd = pd.DataFrame(qs)
    qd['beat'] = qd.spot > qd.tc_prev
    qd['diff'] = qd.spot - qd.tc_prev
    qd['vs_ann'] = (qd.spot / qd.ann - 1) * 100
    g = qd.groupby('q').agg(n=('beat', 'size'), beat=('beat', 'sum'), mean_diff=('diff', 'mean'), median_diff=('diff', 'median'), mean_vs_ann_pct=('vs_ann', 'mean'))
    print('Each quarter: avg spot vs 1-yr TC at end of previous quarter; and quarter vs annual avg')
    print(g.round(1).to_string())
    # monthly seasonal index
    mm = m[str(y0):str(y1)].to_frame('v')
    mm['y'] = mm.index.year; mm['mo'] = mm.index.month
    mm['idx'] = mm.v / mm.groupby('y').v.transform('mean')
    si = mm.groupby('mo').idx.agg(['mean', 'median', lambda x: (x > 1).mean()])
    si.columns = ['mean_idx', 'median_idx', 'share_above_1']
    print('Monthly seasonal index (month avg / calendar-year avg)')
    print(si.round(3).T.to_string())
    return t

kt = season('KAMSARMAX Eco spot 533288 vs 1-yr TC 540614', km_spot, km_tc, 2010, 2025)
mt = season('MR c2010 spot 545055 vs MR Eco 1-yr TC 541552', mr_2010, mr_tc, 2009, 2025)
me = season('MR Eco spot 543759 vs MR Eco 1-yr TC 541552', mr_eco, mr_tc, 2020, 2025)

# Basis check: average spot minus TC over full overlapping period
for nm, sp, tc in [('KM', km_spot, km_tc), ('MR2010', mr_2010, mr_tc), ('MReco', mr_eco, mr_tc)]:
    mo = monthly(sp).to_frame('spot').join(tc.rename('tc'), how='inner').dropna()
    print(nm, 'overlap', mo.index.min().date(), mo.index.max().date(), 'mean spot', round(mo.spot.mean()), 'mean tc', round(mo.tc.mean()), 'mean spot-tc', round((mo.spot - mo.tc).mean()), 'share months spot>tc', round((mo.spot > mo.tc).mean(), 3))
