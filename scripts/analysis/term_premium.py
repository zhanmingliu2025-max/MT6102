import pandas as pd, numpy as np, sys
from pandas.tseries.offsets import DateOffset

R = '/home/user/MT6102/data/raw/'

def load(f, c):
    d = pd.read_csv(R + f, parse_dates=['Date'])
    s = d.iloc[:, [0, c]].dropna()
    s.columns = ['Date', 'v']
    return s.set_index('Date')['v'].sort_index()

tc_mr = load('B1_20260912.csv', 1)        # 541552 MR 1yr TC Eco, monthly
sp_mr10 = load('C4_20260912.csv', 2)      # 545055 MR c.2010 earnings, weekly
sp_mreco = load('L5_20260912.csv', 3)     # 543759 MR c2015 Eco, weekly
tc_km = load('B5_20260912.csv', 1)        # 540614 Panamax/Kamsarmax 1yr TC long run
tc_km_atl = load('B5_20260912.csv', 2)    # 551145 82k Atlantic
tc_km_pac = load('B5_20260912.csv', 3)    # 551149 82k Pacific
sp_km = load('L5_20260912.csv', 1)        # 533288 Kamsarmax c2015 Eco, weekly


def build(tc, sp, nowdef='prior4w'):
    rows = []
    for t, tcv in tc.items():
        end = t + DateOffset(months=12)
        w = sp[(sp.index >= t) & (sp.index < end)]
        if len(w) < 48:
            continue
        if w.index.min() > t + pd.Timedelta(days=7) or w.index.max() < end - pd.Timedelta(days=7):
            continue
        if nowdef == 'prior4w':
            p = sp[(sp.index < t) & (sp.index >= t - pd.Timedelta(days=35))].tail(4)
        else:  # weeks inside month t (contemporaneous with monthly TC assessment)
            p = sp[(sp.index >= t) & (sp.index < t + DateOffset(months=1))]
        if len(p) < 4 and nowdef == 'prior4w':
            continue
        if len(p) == 0:
            continue
        fwd = w.mean()
        rows.append(dict(t=t, tc=tcv, spot_now=p.mean(), fwd=fwd, nweeks=len(w)))
    df = pd.DataFrame(rows).set_index('t')
    df['prem'] = df.fwd - df.tc
    df['prem_pct'] = df.prem / df.tc * 100
    df['back_pct'] = (df.spot_now / df.tc - 1) * 100
    return df


def episodes(idx):
    # count runs of consecutive months
    if len(idx) == 0:
        return 0, []
    idx = sorted(idx)
    runs = []
    start = prev = idx[0]
    for d in idx[1:]:
        if (d.year - prev.year) * 12 + d.month - prev.month == 1:
            prev = d
            continue
        runs.append((start, prev))
        start = prev = d
    runs.append((start, prev))
    return len(runs), runs


def stats(df, label):
    if len(df) == 0:
        print(f'  {label}: n=0')
        return
    w = df.prem.idxmin(); b = df.prem.idxmax()
    ne, runs = episodes(list(df.index))
    print(f'  {label}: n={len(df)} months ({df.index.min():%Y-%m}..{df.index.max():%Y-%m}), episodes={ne}')
    print(f'    spot beat TC: {(df.prem>0).mean()*100:.1f}%  ({(df.prem>0).sum()}/{len(df)})')
    print(f'    mean prem ${df.prem.mean():,.0f}/day ({df.prem_pct.mean():+.1f}%), median ${df.prem.median():,.0f}/day ({df.prem_pct.median():+.1f}%)')
    print(f'    worst {w:%Y-%m}: TC {df.tc[w]:,.0f} spot_now {df.spot_now[w]:,.0f} fwd12 {df.fwd[w]:,.0f} prem {df.prem[w]:+,.0f} ({df.prem_pct[w]:+.1f}%)')
    print(f'    best  {b:%Y-%m}: TC {df.tc[b]:,.0f} spot_now {df.spot_now[b]:,.0f} fwd12 {df.fwd[b]:,.0f} prem {df.prem[b]:+,.0f} ({df.prem_pct[b]:+.1f}%)')
    wp = df.prem_pct.idxmin(); bp = df.prem_pct.idxmax()
    print(f'    worst% {wp:%Y-%m} {df.prem_pct[wp]:+.1f}% ; best% {bp:%Y-%m} {df.prem_pct[bp]:+.1f}%')
    if ne <= 12:
        print('    runs: ' + '; '.join(f'{a:%Y-%m}..{z:%Y-%m}' for a, z in runs))
    # per-episode mean premium
    if ne <= 12:
        out = []
        for a, z in runs:
            sub = df.loc[a:z]
            out.append(f'{a:%Y-%m}..{z:%Y-%m}: n={len(sub)} beat {(sub.prem>0).mean()*100:.0f}% mean {sub.prem_pct.mean():+.1f}%')
        print('    by episode: ' + ' | '.join(out))


def report(name, tc, sp, nowdef='prior4w'):
    df = build(tc, sp, nowdef)
    print(f'\n===== {name}  (spot-now = {nowdef}) =====')
    stats(df, 'ALL')
    stats(df[df.back_pct > 10], 'spot_now > TC +10%')
    stats(df[df.back_pct > 25], 'spot_now > TC +25%')
    stats(df[(df.back_pct > 0) & (df.back_pct <= 10)], 'spot_now 0..+10% over TC')
    stats(df[df.back_pct <= 0], 'spot_now <= TC (contango/flat)')
    stats(df[df.back_pct < -10], 'spot_now < TC -10%')
    # regression prem_pct on back_pct
    x = df.back_pct; y = df.prem_pct
    sl, ic = np.polyfit(x, y, 1)
    print(f'  OLS prem_pct = {ic:.2f} + {sl:.3f}*back_pct  corr={np.corrcoef(x,y)[0,1]:.2f}')
    # how much of the spot excess persisted: fwd vs spot_now
    for th in [10, 25]:
        s = df[df.back_pct > th]
        if len(s):
            print(f'  >{th}%: avg spot_now ${s.spot_now.mean():,.0f}, avg TC ${s.tc.mean():,.0f}, avg fwd12 ${s.fwd.mean():,.0f}; fwd12 fell below spot_now in {(s.fwd<s.spot_now).mean()*100:.0f}% of months, avg fall {((s.fwd/s.spot_now-1)*100).mean():+.1f}%')
    # non-overlapping check: January starts only
    j = df[df.index.month == 1]
    print(f'  Non-overlapping Jan starts: n={len(j)} beat {(j.prem>0).mean()*100:.0f}% mean {j.prem_pct.mean():+.1f}% median {j.prem_pct.median():+.1f}%')
    jb = j[j.back_pct > 10]
    if len(jb):
        print(f'    Jan starts with back>10%: n={len(jb)} beat {(jb.prem>0).mean()*100:.0f}% mean {jb.prem_pct.mean():+.1f}% : ' + ', '.join(f'{d:%Y}:{v:+.0f}%' for d, v in jb.prem_pct.items()))
    # bins
    bins = [-100, -25, -10, 0, 10, 25, 50, 1000]
    df['bin'] = pd.cut(df.back_pct, bins)
    g = df.groupby('bin', observed=True).agg(n=('prem', 'size'), beat=('prem', lambda s: (s > 0).mean() * 100), mean_pct=('prem_pct', 'mean'), med_pct=('prem_pct', 'median'), mean_usd=('prem', 'mean'))
    print(g.round(1).to_string())
    return df


if __name__ == '__main__':
    pd.set_option('display.width', 200)
    a = report('MR: TC 541552 Eco vs spot 545055 c.2010', tc_mr, sp_mr10)
    b = report('MR: TC 541552 Eco vs spot 543759 c2015 Eco (2020+)', tc_mr, sp_mreco)
    c = report('KMX: TC 540614 long run vs spot 533288 c2015 Eco', tc_km, sp_km)
    # robustness
    report('MR Eco/Eco, spot-now = weeks inside month t', tc_mr, sp_mreco, 'inmonth')
    report('MR c2010, spot-now = weeks inside month t', tc_mr, sp_mr10, 'inmonth')
    report('KMX, spot-now = weeks inside month t', tc_km, sp_km, 'inmonth')
    report('KMX: TC 551149 82k Pacific vs spot 533288', tc_km_pac, sp_km)
    report('KMX: TC 551145 82k Atlantic vs spot 533288', tc_km_atl, sp_km)
    a.to_csv('/tmp/claude-0/-home-user-MT6102/0b8c27c0-7c61-5386-8dfe-5f85d183f1af/scratchpad/mr10.csv')
    b.to_csv('/tmp/claude-0/-home-user-MT6102/0b8c27c0-7c61-5386-8dfe-5f85d183f1af/scratchpad/mreco.csv')
    c.to_csv('/tmp/claude-0/-home-user-MT6102/0b8c27c0-7c61-5386-8dfe-5f85d183f1af/scratchpad/kmx.csv')
