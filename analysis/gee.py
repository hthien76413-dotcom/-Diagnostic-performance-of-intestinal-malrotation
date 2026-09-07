exec(open('core.py').read())
import statsmodels.api as sm, statsmodels.formula.api as smf
long['modality']=pd.Categorical(long['mod'],categories=['UGI','CT','US'])
long=long.sort_values('科研患者编号')
def fit(f):
    m=smf.gee(f,'科研患者编号',data=long,family=sm.families.Binomial(),cov_struct=sm.cov_struct.Exchangeable()).fit()
    return m
def show(m,keys=None):
    p=m.params; ci=m.conf_int(); pv=m.pvalues
    for k in p.index:
        if k=='Intercept': continue
        print(f'  {k:45s} OR {np.exp(p[k]):.2f} ({np.exp(ci.loc[k,0]):.2f}-{np.exp(ci.loc[k,1]):.2f})  p={pv[k]:.3g}')
print('=== unadjusted ==='); m1=fit('detected ~ C(modality)'); show(m1)
print('=== adjusted (era, neonate) ==='); m2=fit('detected ~ C(modality) + era_late + neonate'); show(m2)
print('=== interaction ==='); m3=fit('detected ~ C(modality)*volvulus + era_late + neonate'); show(m3)
import numpy as np
names=[k for k in m3.params.index if ':' in k]
print('interaction terms:',names)
R=np.zeros((len(names),len(m3.params)))
for i,n in enumerate(names): R[i,list(m3.params.index).index(n)]=1
w=m3.wald_test(R,scalar=True)
print('GLOBAL Wald interaction: chi2=%.3f df=%d p=%.4f'%(w.statistic,len(names),w.pvalue))
