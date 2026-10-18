import pandas as pd, numpy as np
pd.set_option('display.width', 250)
R = '/home/user/MT6102/data/raw/'
L5 = pd.read_csv(R + 'L5_20260912.csv', parse_dates=['Date']).set_index('Date')
C4 = pd.read_csv(R + 'C4_20260912.csv', parse_dates=['Date']).set_index('Date')
B1 = pd.read_csv(R + 'B1_20260912.csv', parse_dates=['Date']).set_index('Date').iloc[:, 0].dropna()
B5 = pd.read_csv(R + 'B5_20260912.csv', parse_dates=['Date']).set_index('Date').iloc[:, 0].dropna()
C1 = pd.read_csv(R + 'C1_20260912.csv', parse_dates=['Date']).set_index('Date').iloc[:, 0].dropna()

KM = L5.iloc[:, 0].dropna()     # 533288 Kamsarmax c2015 Eco, col 2
MRE = L5.iloc[:, 2].dropna()    # 543759 MR c2015 Eco, col 4
MRC = C4.iloc[:, 1].dropna()    # 545055 MR c2010, col 3
print('KM', KM.name, KM.index.min().date(), KM.index.max().date(), len(KM))
print('MRE', MRE.name, MRE.index.min().date(), MRE.index.max().date(), len(MRE))
print('MRC', MRC.name, MRC.index.min().date(), MRC.index.max().date(), len(MRC))

CAP = 250e6; D = 350; OPEX = 36560 * D
LOCK = (30000 + 40000 + 22000) * D
print('locked income', LOCK, 'opex', OPEX)

def roll52(s):
    # forward-looking window: value at t = mean of weeks t..t+51 ; label by start and end
    r = s.rolling(52).mean().dropna()
    end = r.index
    start = s.index[np.searchsorted(s.index, end) - 51]
    return pd.DataFrame({'start': start, 'end': end, 'avg': r.values})

def stats(df, label):
    v = df.avg
    i_min, i_max = v.idxmin(), v.idxmax()
    p10 = v.quantile(0.10); med = v.median()
    # window nearest p10 / median
    out = dict(series=label, n=len(v),
               worst=v[i_min], worst_win=f"{df.start[i_min].date()} to {df.end[i_min].date()}",
               p10=p10, median=med,
               best=v[i_max], best_win=f"{df.start[i_max].date()} to {df.end[i_max].date()}")
    return out

rows = []
rMRE = roll52(MRE); rMRC = roll52(MRC); rKM = roll52(KM)
rKM15 = rKM[rKM.start >= '2015-01-01'].reset_index(drop=True)
rMRC14 = rMRC[rMRC.start >= '2014-05-01'].reset_index(drop=True)
rMRC10 = rMRC[rMRC.start >= '2010-01-01'].reset_index(drop=True)
for df, lab in [(rMRE, 'MR Eco 543759 (2020+)'), (rMRC, 'MR c2010 545055 (2009+)'),
                (rMRC10, 'MR c2010 545055 (2010+)'),
                (rKM, 'Kamsarmax Eco 533288 (2010+)'), (rKM15, 'Kamsarmax Eco 533288 (2015+)')]:
    rows.append(stats(df, lab))
T1 = pd.DataFrame(rows)
print('\n=== TASK 1: rolling 52-week average spot ($/day) ===')
print(T1.round(0).to_string())

# percentile windows lookups
for df, lab in [(rMRE, 'MRE'), (rMRC, 'MRC'), (rKM, 'KM'), (rKM15, 'KM15')]:
    p10 = df.avg.quantile(.1)
    j = (df.avg - p10).abs().idxmin()
    print(lab, 'p10 example window', df.start[j].date(), df.end[j].date(), round(df.avg[j]))
    # share of windows below thresholds
    print('   share windows below 20k', round((df.avg < 20000).mean(), 3), 'below 12k', round((df.avg < 12000).mean(), 3))

# Eco premium over c2010 in overlap
ov = pd.concat([MRE, MRC], axis=1).dropna()
print('\nMR overlap', ov.index.min().date(), ov.index.max().date(), 'Eco mean', round(ov.iloc[:,0].mean()), 'c2010 mean', round(ov.iloc[:,1].mean()),
      'diff', round((ov.iloc[:,0]-ov.iloc[:,1]).mean()), 'ratio', round((ov.iloc[:,0]/ov.iloc[:,1]).mean(), 3),
      'ratio of means', round(ov.iloc[:,0].mean()/ov.iloc[:,1].mean(), 3))

def fleet(mr, km, lock=LOCK):
    inc = lock + (mr + km) * D
    return inc, inc / CAP, (inc - OPEX) / CAP

print('\n=== TASK 2: fleet return if MR#2 and KM#2 earn historical 52-wk outcomes ===')
print('(a) quantile-by-quantile pairing (each series own quantile, not same year)')
pairs = {}
for mrlab, rm in [('MR Eco', rMRE), ('MR c2010', rMRC)]:
    for kmlab, rk in [('KM 2010+', rKM), ('KM 2015+', rKM15)]:
        for q, f in [('worst', lambda v: v.min()), ('p10', lambda v: v.quantile(.1)), ('median', lambda v: v.median()), ('best', lambda v: v.max())]:
            mr, km = f(rm.avg), f(rk.avg)
            inc, rb, ra = fleet(mr, km)
            pairs[(mrlab, kmlab, q)] = (mr, km, inc / 1e6, rb * 100, ra * 100)
P = pd.DataFrame(pairs, index=['MR$/d', 'KM$/d', 'income $m', 'ret pre-OPEX %', 'ret post-OPEX %']).T
print(P.round(2).to_string())

print('\n(b) same-window joint history (both ships in the same 52 weeks)')
def joint(rm, rk, lab):
    j = pd.merge(rm, rk, on=['start', 'end'], suffixes=('_mr', '_km'))
    j['inc'] = LOCK + (j.avg_mr + j.avg_km) * D
    j['pre'] = j.inc / CAP * 100
    j['post'] = (j.inc - OPEX) / CAP * 100
    i = j.inc.idxmin(); k = j.inc.idxmax()
    q10 = j.inc.quantile(.1); med = j.inc.median()
    print(f"{lab}: n={len(j)} windows {j.start.min().date()}..{j.start.max().date()}")
    print(f"   worst window {j.start[i].date()} to {j.end[i].date()}: MR {j.avg_mr[i]:.0f} KM {j.avg_km[i]:.0f} income {j.inc[i]/1e6:.2f}m pre {j.pre[i]:.2f}% post {j.post[i]:.2f}%")
    print(f"   p10 income {q10/1e6:.2f}m pre {q10/CAP*100:.2f}% post {(q10-OPEX)/CAP*100:.2f}%")
    print(f"   median income {med/1e6:.2f}m pre {med/CAP*100:.2f}% post {(med-OPEX)/CAP*100:.2f}%")
    print(f"   best window {j.start[k].date()} to {j.end[k].date()}: MR {j.avg_mr[k]:.0f} KM {j.avg_km[k]:.0f} income {j.inc[k]/1e6:.2f}m pre {j.pre[k]:.2f}% post {j.post[k]:.2f}%")
    print(f"   share of windows with pre-OPEX < 15%: {(j.pre<15).mean():.3f}; < base 19.88%: {(j.pre<19.88).mean():.3f}; post-OPEX < 8%: {(j.post<8).mean():.3f}")
    return j
jE = joint(rMRE, rKM, 'MR Eco + KM (2020+)')
jC = joint(rMRC, rKM, 'MR c2010 + KM (2010+)')
jC15 = joint(rMRC[rMRC.start >= '2015-01-01'], rKM15, 'MR c2010 + KM (2015+)')

print('\n=== TASK 3: alternatives (deterministic) ===')
for lab, mr, km in [('Base mix (spot proxies 27k/23k)', 27000, 23000), ('A all fixed last-done 27k/23k', 27000, 23000),
                    ('B all fixed Oct 1-yr 43k/19.75k', 43000, 19750), ('Bear mix 2025 avg', 22950, 12880)]:
    inc, rb, ra = fleet(mr, km)
    print(f"{lab}: income {inc/1e6:.3f}m pre {rb*100:.2f}% post {ra*100:.2f}%")
