import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-MT6102/0b8c27c0-7c61-5386-8dfe-5f85d183f1af/scratchpad')
import term_premium as T, pandas as pd, numpy as np
def nw(x,L=12):
    x=np.asarray(x)-np.mean(x); n=len(x); g0=(x@x)/n; s=g0
    for l in range(1,L+1): s+=2*(1-l/(L+1))*(x[l:]@x[:-l])/n
    return np.sqrt(s/n)
for name,tc,sp in [('MR c2010',T.tc_mr,T.sp_mr10),('MR Eco',T.tc_mr,T.sp_mreco),('KMX LR',T.tc_km,T.sp_km),('KMX Atl',T.tc_km_atl,T.sp_km),('KMX Pac2014+',T.tc_km_pac,T.sp_km)]:
    df=T.build(tc,sp)
    m=df.prem_pct.mean(); se=nw(df.prem_pct)
    print(f'{name}: n={len(df)} mean prem% {m:+.1f} NW-se {se:.1f} t={m/se:.2f}; beat {(df.prem>0).mean()*100:.0f}% median {df.prem_pct.median():+.1f}%')
    for th in [10,25]:
        s=df[df.back_pct>th]
        print(f'   >{th}%: n={len(s)} beat {(s.prem>0).mean()*100:.0f}% mean {s.prem_pct.mean():+.1f}% median {s.prem_pct.median():+.1f}% mean$ {s.prem.mean():+,.0f} med$ {s.prem.median():+,.0f}')
    s=df[df.back_pct<=0]; print(f'   <=0: n={len(s)} beat {(s.prem>0).mean()*100:.0f}% mean {s.prem_pct.mean():+.1f}% median {s.prem_pct.median():+.1f}%')
# KMX excluding pre-2014 / MR c2010 restricted to 2020+ for apples to apples with Eco
df=T.build(T.tc_mr,T.sp_mr10); d2=df[df.index>='2020-02-01']
print('MR c2010 2020-02+: n',len(d2),'beat',round((d2.prem>0).mean()*100),'mean',round(d2.prem_pct.mean(),1),'median',round(d2.prem_pct.median(),1))
s=d2[d2.back_pct>10]; print('  >10 n',len(s),'beat',round((s.prem>0).mean()*100),'mean',round(s.prem_pct.mean(),1),'med',round(s.prem_pct.median(),1))
# excluding 2022 Russia windows (t in 2021-03..2022-12) and COVID (2019-10..2020-12) to see dependence
for name,tc,sp in [('MR c2010',T.tc_mr,T.sp_mr10),('MR Eco',T.tc_mr,T.sp_mreco),('KMX',T.tc_km,T.sp_km)]:
    df=T.build(tc,sp)
    ex=df[~((df.index>='2021-03-01')&(df.index<='2022-12-01'))]
    for th in [10,25]:
        s=ex[ex.back_pct>th]
        if len(s): print(f'{name} ex-2021/22 starts >{th}%: n={len(s)} beat {(s.prem>0).mean()*100:.0f}% mean {s.prem_pct.mean():+.1f}% median {s.prem_pct.median():+.1f}%')
    a=ex; print(f'{name} ex-2021/22 ALL: n={len(a)} beat {(a.prem>0).mean()*100:.0f}% mean {a.prem_pct.mean():+.1f}% median {a.prem_pct.median():+.1f}%')
# MR Eco >25% list
df=T.build(T.tc_mr,T.sp_mreco)
print(df[df.back_pct>25][['tc','spot_now','fwd','prem','prem_pct','back_pct']].round(0).to_string())
df=T.build(T.tc_km,T.sp_km)
print(df[df.back_pct>25][['tc','spot_now','fwd','prem','prem_pct','back_pct']].round(0).to_string())
df=T.build(T.tc_mr,T.sp_mr10)
print(df[df.back_pct>25][['tc','spot_now','fwd','prem','prem_pct','back_pct']].round(0).to_string())
