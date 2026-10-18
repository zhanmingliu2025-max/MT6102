import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-MT6102/0b8c27c0-7c61-5386-8dfe-5f85d183f1af/scratchpad')
import term_premium as T, pandas as pd, numpy as np
from pandas.tseries.offsets import DateOffset
# Eco premium MR
a=T.sp_mreco; b=T.sp_mr10; j=pd.concat([a,b],axis=1,keys=['eco','c10']).dropna()
print('MR eco/c2010 overlap', j.index.min().date(), j.index.max().date(), 'mean ratio', (j.eco/j.c10).mean().round(3), 'median', (j.eco/j.c10).median().round(3), 'mean diff', (j.eco-j.c10).mean().round(0))
for y,g in j.groupby(j.index.year): print(' ',y, round((g.eco/g.c10).mean(),3), round((g.eco-g.c10).mean()))
# KMX long run vs Pacific
k=pd.concat([T.tc_km,T.tc_km_pac,T.tc_km_atl],axis=1,keys=['lr','pac','atl']).dropna()
print('KMX LR==Pac share', (abs(k.lr-k.pac)<1).mean(), 'LR==Atl', (abs(k.lr-k.atl)<1).mean(), 'LR==avg', (abs(k.lr-(k.pac+k.atl)/2)<1).mean())
print(k.tail(5))
# clean variant: TC month t, spot_now = weeks in month t, forward = [t+1m, t+13m)
def clean(tc, sp):
    rows=[]
    for t,v in tc.items():
        s=t+DateOffset(months=1); e=t+DateOffset(months=13)
        w=sp[(sp.index>=s)&(sp.index<e)]
        if len(w)<48 or w.index.min()>s+pd.Timedelta(days=7) or w.index.max()<e-pd.Timedelta(days=7): continue
        p=sp[(sp.index>=t)&(sp.index<s)]
        if len(p)<3: continue
        rows.append(dict(t=t,tc=v,spot_now=p.mean(),fwd=w.mean()))
    df=pd.DataFrame(rows).set_index('t'); df['prem']=df.fwd-df.tc; df['prem_pct']=df.prem/df.tc*100; df['back_pct']=(df.spot_now/df.tc-1)*100
    return df
for name,tc,sp in [('MR c2010',T.tc_mr,T.sp_mr10),('MR Eco',T.tc_mr,T.sp_mreco),('KMX',T.tc_km,T.sp_km)]:
    df=clean(tc,sp); print('\n== CLEAN (spot in month t, fwd t+1..t+13)',name)
    T.stats(df,'ALL'); T.stats(df[df.back_pct>10],'>10%'); T.stats(df[df.back_pct>25],'>25%'); T.stats(df[df.back_pct<=0],'<=0')
# current readings from repo data (pull 12 Sep 2026)
for name,tc,sp in [('MR c2010',T.tc_mr,T.sp_mr10),('MR Eco',T.tc_mr,T.sp_mreco),('KMX',T.tc_km,T.sp_km)]:
    t=pd.Timestamp('2026-09-01'); p=sp[(sp.index<t)].tail(4)
    print(name,'Sep-2026 TC',tc[t],'prior4w spot',round(p.mean()),'back%',round((p.mean()/tc[t]-1)*100,1), 'last wk', sp.index[-1].date(), round(sp.iloc[-1]), round((sp.iloc[-1]/tc[t]-1)*100,1))
print('Oct facts: MR', round((53741/43000-1)*100,1), 'MR 2wk avg', round(((53741+64189)/2/43000-1)*100,1), 'KMX', round((23389/19750-1)*100,1))
