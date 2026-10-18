import pandas as pd, numpy as np
R='/home/user/MT6102/data/raw/'
L5=pd.read_csv(R+'L5_20260912.csv',parse_dates=['Date']).set_index('Date')
C4=pd.read_csv(R+'C4_20260912.csv',parse_dates=['Date']).set_index('Date')
KM=L5.iloc[:,0].dropna(); MRE=L5.iloc[:,2].dropna(); MRC=C4.iloc[:,1].dropna()
D=350; OPEX=36560*D; CAP=250e6
def joint(mr, km, fixed, n_mr, n_km, start='2010-01-01'):
    df=pd.concat([mr.rename('mr'),km.rename('km')],axis=1).dropna()
    r=df.rolling(52).mean().dropna()
    st=df.index[np.searchsorted(df.index,r.index)-51]
    r=r[st>=pd.Timestamp(start)]; st=st[st>=pd.Timestamp(start)]
    inc=(fixed+n_mr*r.mr+n_km*r.km)*D
    i=inc.values.argmin()
    return st[i].date(), r.index[i].date(), round(r.mr.iloc[i]), round(r.km.iloc[i]), round(inc.iloc[i]/CAP*100,2), round((inc.iloc[i]-OPEX)/CAP*100,2)
cfg={'1 fixed Afra':(40000,2,2),'2 fixed Afra+MR1':(70000,1,2),'2 fixed Afra+KM1':(62000,2,1),'3 fixed':(92000,1,1),
     '2 fixed Oct Afra37.5+MR43':(80500,1,2),'3 fixed Oct':(100250,1,1)}
for k,(f,nm,nk) in cfg.items():
    print(k,'MRc2010',joint(MRC,KM,f,nm,nk),'MREco',joint(MRE,KM,f,nm,nk,'2020-01-01'))
