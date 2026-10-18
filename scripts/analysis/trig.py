import pandas as pd, numpy as np
R='/home/user/MT6102/data/raw/'
def ser(f,col):
    d=pd.read_csv(R+f+'_20260912.csv',parse_dates=['Date']).set_index('Date'); return d.iloc[:,col-1].dropna().astype(float)
mr_eco=ser('L5',3); mr_tc=ser('B1',1); km_tc=ser('B5',1); km_spot=ser('L5',1)
bdi=ser('C1',1)
# MR trigger: weekly MR Eco < 20000 for 8 consecutive weeks
b=(mr_eco<20000).astype(int); run=b.groupby((b!=b.shift()).cumsum()).cumsum()*b
fires=run[run==8]
print('MR Eco trigger fires:',[(d.date(), round(mr_tc.asof(d))) for d in fires.index])
# also c2010
mr10=ser('C4',2); b=(mr10<20000).astype(int); run=b.groupby((b!=b.shift()).cumsum()).cumsum()*b
f2=run[run==8]; print('MR c2010 trigger fires (since 2014):',[(d.date(), round(mr_tc.asof(d))) for d in f2['2014':].index])
# BDI weekly (Friday) below 2000 for 8 consecutive weeks: use daily: 40 consecutive trading days
b=(bdi<2000).astype(int); run=b.groupby((b!=b.shift()).cumsum()).cumsum()*b
f3=run[run==40]; print('BDI<2000 40 trading days fires:',[(d.date(), round(km_tc.asof(d)), round(km_spot.asof(d))) for d in f3.index])
print('BDI 2023-2026 share of days <2000:', round((bdi<2000).mean(),2), 'by year', (bdi<2000).groupby(bdi.index.year).mean().round(2).to_dict())
print('BDI monthly mean 2025-2026', bdi['2025':].resample('MS').mean().round(0).to_dict())
