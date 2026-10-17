exec(open('core.py').read())
import statsmodels.api as sm, statsmodels.formula.api as smf
long['modality']=pd.Categorical(long['mod'],categories=['UGI','CT','US'])
long=long.sort_values('科研患者编号')
def fit(f,data=None):
    d=long if data is None else data
    return smf.gee(f,'科研患者编号',data=d,family=sm.families.Binomial(),cov_struct=sm.cov_struct.Exchangeable()).fit()
def show(m):
    p,ci,pv=m.params,m.conf_int(),m.pvalues
    for k in p.index:
        if k=='Intercept': continue
        print(f'  {k:42s} OR {np.exp(p[k]):.2f} ({np.exp(ci.loc[k,0]):.2f}-{np.exp(ci.loc[k,1]):.2f})  p={pv[k]:.4g}')
sub=long[long['mod'].isin(['UGI','CT'])].copy()
sub['modality']=pd.Categorical(sub['mod'],categories=['UGI','CT'])
print('=== UGI vs CT interaction with volvulus (no separation) ===')
m=fit('detected ~ C(modality)*volvulus + era_late + neonate',sub); show(m)
print('  n obs',m.nobs)
print()
print('=== adjusted incl. age group instead of neonate ===')
long['agegrp']=pd.cut(long['age_days'],[-1,28,365,1e5],labels=['neonate','1-12mo','>1y'])
m=fit('detected ~ C(modality) + era_late + C(agegrp, Treatment(reference="neonate"))'); show(m)
print()
print('=== adjusted + volvulus main effect ===')
m=fit('detected ~ C(modality) + era_late + neonate + volvulus'); show(m)
