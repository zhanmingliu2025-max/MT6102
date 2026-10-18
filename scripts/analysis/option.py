import pandas as pd, numpy as np
pd.set_option('display.width', 220); pd.set_option('display.max_columns', 30); pd.set_option('display.max_rows', 300)
R = '/home/user/MT6102/data/raw/'
def ser(f, col):
    d = pd.read_csv(R + f + '_20260912.csv', parse_dates=['Date']).set_index('Date')
    return d.iloc[:, col - 1].dropna().astype(float)
km_spot = ser('L5', 1); mr_eco = ser('L5', 3); mr_2010 = ser('C4', 2)
km_tc = ser('B5', 1); mr_tc = ser('B1', 1)
FS = 92 / 365; FT = 273 / 365   # Oct-Dec share of 12 months, Jan-Sep share

def tc_changes(name, tc, start=None):
    t = tc[start:] if start else tc
    ch = (t.shift(-3) - t).dropna(); pc = (t.shift(-3) / t - 1).dropna() * 100
    q = lambda s: ' '.join(f'p{int(p*100)}={s.quantile(p):,.0f}' for p in [.05, .1, .25, .5, .75, .9, .95])
    print(f'\n{name} 1-yr TC 3-month change, all start months {t.index.min().date()}..{t.index.max().date()} n={len(ch)}')
    print('  $/day: mean', f'{ch.mean():,.0f}', 'sd', f'{ch.std():,.0f}', q(ch))
    print('  %    : mean', f'{pc.mean():.1f}', 'sd', f'{pc.std():.1f}', 'mean |chg|', f'{pc.abs().mean():.1f}', q(pc).replace(',', ''))
    print('  share rises', round((ch > 0).mean(), 3), 'share |chg|>10%', round((pc.abs() > 10).mean(), 3), 'share falls>10%', round((pc < -10).mean(), 3), 'share falls>15%', round((pc < -15).mean(), 3), 'share falls>20%', round((pc < -20).mean(), 3))
    sd = pc[pc.index.month == 9]
    print('  Sep->Dec only: n', len(sd), 'mean %', round(sd.mean(), 1), 'median', round(sd.median(), 1), 'share rises', round((sd > 0).mean(), 3), 'min', round(sd.min(), 1), 'max', round(sd.max(), 1))
    print('  Sep->Dec by year (%):', ' '.join(f'{d.year}:{v:+.0f}' for d, v in sd.items() if d.year >= 2009))
    return pc

kpc = tc_changes('KAMSARMAX', km_tc)
kpc10 = tc_changes('KAMSARMAX since 2010', km_tc, '2010')
mpc = tc_changes('MR Eco', mr_tc)

def wait_test(name, spot, tc, basis_adj=0.0):
    m = spot.resample('MS').mean()
    rows = []
    for y in range(2009, 2026):
        tsep = tc.get(pd.Timestamp(f'{y}-09-01')); tdec = tc.get(pd.Timestamp(f'{y}-12-01'))
        q4 = spot[f'{y}-10-01':f'{y}-12-31']
        if tsep is None or tdec is None or len(q4) < 10: continue
        q4m = q4.mean() - basis_adj
        A = tsep; B = FS * q4m + FT * tdec
        rows.append(dict(year=y, tc_sep=tsep, sep_spot=m.get(pd.Timestamp(f'{y}-09-01')), q4_spot=q4m, tc_dec=tdec, fix_now=A, wait=B, gain=B - A,
                         spot_part=FS * (q4m - tsep), tc_part=FT * (tdec - tsep)))
    d = pd.DataFrame(rows).set_index('year')
    d['backw'] = d.sep_spot > d.tc_sep
    print(f'\n{name}: fix 12m at Sep 1-yr TC vs spot Oct-Dec then fix 9m at Dec 1-yr TC (basis adj {basis_adj:,.0f})')
    print(d.round(0).to_string())
    print(f'  waiting wins {int((d.gain>0).sum())}/{len(d)}; mean gain {d.gain.mean():,.0f} $/day; median {d.gain.median():,.0f}; min {d.gain.min():,.0f} max {d.gain.max():,.0f}; mean spot part {d.spot_part.mean():,.0f}, mean tc part {d.tc_part.mean():,.0f}')
    for flag, lab in [(True, 'Sep spot > Sep TC'), (False, 'Sep spot <= Sep TC')]:
        s = d[d.backw == flag]
        if len(s): print(f'  {lab}: n={len(s)} wins {int((s.gain>0).sum())} mean gain {s.gain.mean():,.0f} median {s.gain.median():,.0f}')
    return d

kd = wait_test('KAMSARMAX', km_spot, km_tc)
kd2 = wait_test('KAMSARMAX basis-adjusted (spot minus mean spot-TC basis -820 => +820)', km_spot, km_tc, basis_adj=-820)
md = wait_test('MR c2010 spot', mr_2010, mr_tc)
md2 = wait_test('MR Eco spot', mr_eco, mr_tc)

# All start months: wait 3 months on spot then fix 9 months vs fix 12 now; conditional on spot/TC at decision
def roll(name, spot, tc, start):
    m = spot.resample('MS').mean()
    rows = []
    for t0 in tc[start:].index:
        t3 = t0 + pd.DateOffset(months=3)
        if t3 not in tc.index: continue
        sp = spot[t0 + pd.DateOffset(months=1): t3 + pd.DateOffset(months=1) - pd.Timedelta(days=1)]  # next 3 months after decision month
        if len(sp) < 10 or t0 not in m.index: continue
        A = tc[t0]; B = FS * sp.mean() + FT * tc[t3]
        rows.append(dict(t0=t0, ratio=m[t0] / A, gain=B - A, gpct=(B / A - 1) * 100))
    d = pd.DataFrame(rows).set_index('t0')
    print(f'\n{name} rolling (decision month t0; spot months t0+1..t0+3; fix 9m at TC t0+3) n={len(d)}')
    print(f'  all: wins {(d.gain>0).mean():.3f} mean gain {d.gain.mean():,.0f} median {d.gain.median():,.0f} mean % {d.gpct.mean():.1f}')
    for lo, hi in [(0, 1.0), (1.0, 10), (1.1, 10), (1.15, 10), (1.25, 10)]:
        s = d[(d.ratio > lo) & (d.ratio <= hi)]
        if len(s): print(f'  spot/TC in ({lo},{hi}]: n={len(s)} wins {(s.gain>0).mean():.3f} mean gain {s.gain.mean():,.0f} median {s.gain.median():,.0f} mean % {s.gpct.mean():.1f} p10 {s.gain.quantile(.1):,.0f} p90 {s.gain.quantile(.9):,.0f}')
    return d
kr = roll('KAMSARMAX', km_spot, km_tc, '2010')
mr_r = roll('MR c2010', mr_2010, mr_tc, '2014-05')
mre_r = roll('MR Eco', mr_eco, mr_tc, '2020')

# 2026 application: break-even TC in Dec and historical analog outcomes
print('\n2026 application (fractions 92/365 spot, 273/365 fixed)')
for nm, spot_now, tc_now, d in [('KM', 23389, 19750, kd), ('MR', 53741, 43000, md2)]:
    for q4 in [spot_now, 0.8 * spot_now, tc_now]:
        be = (tc_now - FS * q4) / FT
        print(f'  {nm}: fix now {tc_now:,}; if Q4 spot avg {q4:,.0f} break-even Dec TC {be:,.0f} ({(be/tc_now-1)*100:+.1f}%)')
    # analog: scale history ratios
    a = d.dropna(subset=['sep_spot']).copy()
    a['q4r'] = a.q4_spot / a.sep_spot; a['tcr'] = a.tc_dec / a.tc_sep
    a['B'] = FS * spot_now * a.q4r + FT * tc_now * a.tcr; a['g'] = a.B - tc_now
    print(f'  {nm} historical-analog: wins {(a.g>0).sum()}/{len(a)} mean gain {a.g.mean():,.0f} median {a.g.median():,.0f} min {a.g.min():,.0f} max {a.g.max():,.0f}')
    print('   ', ' '.join(f'{y}:{g:+,.0f}' for y, g in a.g.items()))
