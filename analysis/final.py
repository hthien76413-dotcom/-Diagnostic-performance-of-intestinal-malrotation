exec(open('core.py').read())
from statsmodels.stats.proportion import proportion_confint as pci
ix=pd.read_csv('ix_full.csv')
def rate(k,n):
    lo,hi=pci(k,n,method='wilson'); return f'{k}/{n} = {k/n*100:.1f}% ({lo*100:.1f}-{hi*100:.1f})'
print('=== detection in the subgroups the editor asks about ===')
pat['agegrp']=pd.cut(pat['age_days'],[-1,28,365,1e9],labels=['<=28d','29d-1y','>1y'])
ix2=ix.merge(pat[['科研患者编号','agegrp']],on='科研患者编号',how='left')
for mod in ['UGI','CT','US']:
    d=ix2[ix2['mod']==mod]
    print(f'  {mod}:')
    for g in ['<=28d','29d-1y','>1y']:
        s=d[d['agegrp']==g]
        if len(s): print(f'     age {g:7s} {rate(int(s["det"].sum()),len(s))}')
    for v,lab in [(True,'volvulus+'),(False,'volvulus-')]:
        s=d[d['volvulus']==v]
        if len(s): print(f'     {lab:9s} {rate(int(s["det"].sum()),len(s))}')
print()
print('=== children >1 year (the "older child" group) ===')
old=pat[pat['age_days']>365]
print('  n=%d (%.1f%% of cohort); volvulus %d (%.0f%%); imaged %d'%(len(old),len(old)/465*100,old['volvulus'].sum(),old['volvulus'].mean()*100,ix[ix['科研患者编号'].isin(old['科研患者编号'])]['科研患者编号'].nunique()))
print('=== children without volvulus ===')
nv=pat[~pat['volvulus']]
print('  n=%d (%.1f%%); median age %.0f d; neonates %d (%.0f%%)'%(len(nv),len(nv)/465*100,nv['age_days'].median(),nv['neonate'].sum(),nv['neonate'].mean()*100))
print()
print('=== US sensitivity: excluding pyloric-only examinations ===')
u=pd.read_csv('us_audit.csv')
s=u[~u['pyloric_only']]
print('  all US %s'%rate(int(u['US_detected'].sum()),len(u)))
print('  excl. pyloric-only %s'%rate(int(s['US_detected'].sum()),len(s)))
print('  gastrointestinal-US label only %s'%rate(int(u[u['gi_us']]['US_detected'].sum()),int(u['gi_us'].sum())))
print('  vessel-US label %s'%rate(int(u[u['vessel_us']]['US_detected'].sum()),int(u['vessel_us'].sum())))
print()
print('=== whirlpool documented vs detection (US) ===')
print('  whirlpool documented %s'%rate(int(u['US_whirlpool'].sum()),len(u)))
print('  detection | whirlpool documented: %s'%rate(int(u[u['US_whirlpool']==1]['US_detected'].sum()),int((u['US_whirlpool']==1).sum())))
print('  detection | whirlpool NOT documented: %s'%rate(int(u[u['US_whirlpool']==0]['US_detected'].sum()),int((u['US_whirlpool']==0).sum())))
print()
print('=== overall single-modality rates (verification) ===')
for mod in ['UGI','CT','US']:
    d=ix[ix['mod']==mod]; print(f'  {mod}: {rate(int(d["det"].sum()),len(d))}')
c=ix[ix['mod']=='CT'].copy(); c['enh']=c['报告名称'].astype(str).str.contains('增强')
print('  CT enhanced: %s ; unenhanced: %s'%(rate(int(c[c['enh']]['det'].sum()),int(c['enh'].sum())),rate(int(c[~c['enh']]['det'].sum()),int((~c['enh']).sum()))))
from scipy.stats import fisher_exact
tab=pd.crosstab(c['enh'],c['det']).values
orr,pv=fisher_exact(tab); print('  Fisher OR %.2f p=%.3g'%(orr,pv))
