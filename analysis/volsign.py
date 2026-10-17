exec(open('core.py').read())
from statsmodels.stats.proportion import proportion_confint as pci
from statsmodels.stats.contingency_tables import mcnemar, cochrans_q
ix=idx.merge(pat[['科研患者编号','volvulus','era_late','op_year','neonate']],on='科研患者编号',how='left')
ix=ix.merge(mat,on='科研患者编号',how='left')
ix['det']=np.where(ix['mod']=='US',ix['US_detected'],np.where(ix['mod']=='CT',ix['CT_detected'],ix['UGI_detected']))
VS=r'漩涡|旋涡|涡流|螺旋|弹簧征|扭转'
ix['vsign']=ix['txt'].str.contains(VS,regex=True) & ~ix['txt'].str.contains(r'胃扭转',regex=True)
v=ix[ix['volvulus']==True]
print('=== volvulus-specific sign among confirmed volvulus (my rule) ===')
for mod in ['UGI','US','CT']:
    d=v[v['mod']==mod]; k=int(d['vsign'].sum()); n=len(d); lo,hi=pci(k,n,method='wilson')
    print(f'  {mod:4s} {k:3d}/{n:3d} = {k/n*100:5.1f}% ({lo*100:.1f}-{hi*100:.1f})')
print('published Table 6: UGI 131/268 48.9, US 59/113 52.2, CT 116/281 41.3')
# paired volvulus cohort
pid=set(mat[mat[['US_detected','CT_detected','UGI_detected']].notna().all(axis=1)]['科研患者编号'])
pv=v[v['科研患者编号'].isin(pid)].pivot_table(index='科研患者编号',columns='mod',values='vsign',aggfunc='first')
pv=pv.dropna()
print('\npaired volvulus cohort n=%d'%len(pv))
for mod in ['UGI','US','CT']: print(f'  {mod}: {int(pv[mod].sum())}/{len(pv)} = {pv[mod].mean()*100:.1f}%')
M=pv[['UGI','CT','US']].astype(int).values
q=cochrans_q(M); print('  Cochran Q p=%.4f'%q.pvalue)
for a,b in [('US','CT'),('UGI','US'),('UGI','CT')]:
    tab=pd.crosstab(pv[a].astype(int),pv[b].astype(int)).reindex(index=[0,1],columns=[0,1],fill_value=0).values
    print(f'  {a} vs {b}: {int(tab[1,0])}/{int(tab[0,1])} exact p={mcnemar(tab,exact=True).pvalue:.4f}')
ix.to_csv('ix_full.csv',index=False)
