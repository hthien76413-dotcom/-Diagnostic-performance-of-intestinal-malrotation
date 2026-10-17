exec(open('core.py').read())
import statsmodels.api as sm, statsmodels.formula.api as smf
u=pd.read_csv('us_audit.csv'); u['det']=u['US_detected']
def lg(f,d):
    m=smf.logit(f,data=d).fit(disp=0)
    p,ci,pv=m.params,m.conf_int(),m.pvalues
    for k in p.index:
        if k=='Intercept': continue
        print(f'   {k:26s} OR {np.exp(p[k]):.2f} ({np.exp(ci.loc[k,0]):.2f}-{np.exp(ci.loc[k,1]):.2f}) p={pv[k]:.4g}')
print('US detection ~ era'); lg('det ~ era_late',u)
print('US detection ~ era + vessel-US protocol label'); lg('det ~ era_late + vessel_us',u)
print('US detection ~ vessel-US label alone'); lg('det ~ vessel_us',u)
print('US detection ~ era + vessel + neonate'); lg('det ~ era_late + vessel_us + neonate',u)
c=pd.read_csv('ix_full.csv'); c=c[c['mod']=='CT'].copy(); c['enh']=c['报告名称'].astype(str).str.contains('增强').astype(int)
print('\nCT detection ~ era'); lg('det ~ era_late',c)
print('CT detection ~ era + contrast enhancement'); lg('det ~ era_late + enh',c)
g=pd.read_csv('ix_full.csv'); g=g[g['mod']=='UGI'].copy()
print('\nUGI detection ~ era'); lg('det ~ era_late',g)
