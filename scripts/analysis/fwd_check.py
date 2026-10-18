import numpy as np

def brentq(f,a,b):
    fa=f(a)
    for _ in range(200):
        m=(a+b)/2; fm=f(m)
        if (fm>0)==(fa>0): a,fa=m,fm
        else: b=m
    return (a+b)/2
def lin(S1,S3):
    y23=(3*S3-S1)/2
    b=(S1-y23)/18; a=S1+6*b
    return a,b,y23
for name,S0,S1,S3 in [("MR",53741,43000,26250),("KM",23389,19750,17250)]:
    a,b,y23=lin(S1,S3)
    f=lambda t0: a-b*(t0+6)
    print(name,"linear a=%.0f b=%.0f y23=%.0f"%(a,b,y23),
          "spot avg m0-3 %.0f"%(a-1.5*b),"fwd1y from m0.5 %.0f"%f(0.5),"from m2.5 %.0f"%f(2.5),"from m3 %.0f"%f(3))
    # exponential with S0 fixed: s(m)=L+(S0-L)exp(-k m)
    def avg(L,k,t0,t1): return L+(S0-L)*(np.exp(-k*t0)-np.exp(-k*t1))/(k*(t1-t0))
    def eqs(k):
        # solve L from 1y avg, then check 3y
        e=(1-np.exp(-k*12))/(k*12)
        L=(S1-S0*e)/(1-e)
        return avg(L,k,0,36)-S3
    try:
        k=brentq(eqs,1e-4,5)
        e=(1-np.exp(-k*12))/(k*12); L=(S1-S0*e)/(1-e)
        print("  exp k=%.3f L=%.0f"%(k,L),"spot avg m0-2.5 %.0f"%avg(L,k,0,2.5),"fwd1y m2.5-14.5 %.0f"%avg(L,k,2.5,14.5),"fwd1y m0.5-12.5 %.0f"%avg(L,k,0.5,12.5))
        # plan value MR: 92d spot then 273 at fwd
        if name=="MR":
            plan=92*avg(L,k,0,3)+273*avg(L,k,3,15); print("  plan 92/273 per-day %.0f vs fix now %d"%(plan/365,S1))
    except Exception as ex: print("  exp fail",ex)
