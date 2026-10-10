exec(open('core.py').read())
ix=pd.read_csv('ix_full.csv')
ix['era']=np.where(ix['era_late'],'2019-2026','2012-2018')
print('=== examinations and detection by era ===')
for mod in ['UGI','CT','US']:
    d=ix[ix['mod']==mod]
    for e in ['2012-2018','2019-2026']:
        s=d[d['era']==e]
        print(f'  {mod:4s} {e}: n={len(s):3d} detected {int(s["det"].sum()):3d} ({s["det"].mean()*100:.1f}%)')
print('\n=== cohort size and modality utilisation by era ===')
pt=pat.copy(); pt['era']=np.where(pt['era_late'],'2019-2026','2012-2018')
for e in ['2012-2018','2019-2026']:
    s=set(pt[pt['era']==e]['科研患者编号']); n=len(s)
    row=f'  {e}: patients {n}'
    for mod in ['UGI','CT','US']:
        k=ix[(ix['mod']==mod)&(ix['科研患者编号'].isin(s))]['科研患者编号'].nunique()
        row+=f' | {mod} {k} ({k/n*100:.0f}%)'
    print(row)
print('\n=== ultrasound: content drivers of the era difference ===')
u=pd.read_csv('us_audit.csv')
for c in ['gi_us','vessel_us','bedside','sma_smv','whirl_txt','gas_limit']:
    a=u[~u['era_late']][c].mean()*100; b=u[u['era_late']][c].mean()*100
    print(f'  {c:10s} early {a:5.1f}%  late {b:5.1f}%')
from scipy.stats import fisher_exact
tab=pd.crosstab(u['era_late'],u['vessel_us']).values
print('  vessel-US label by era Fisher p=%.4g'%fisher_exact(tab)[1])
# stratified detection: does era effect persist within whirlpool-documented?
print('\n  US detection by era within vessel-US label:')
for v in [True,False]:
    s=u[u['vessel_us']==v]
    if len(s): print(f'    vessel_us={v}: early {s[~s["era_late"]]["US_detected"].mean()*100:.1f}% (n={(~s["era_late"]).sum()}), late {s[s["era_late"]]["US_detected"].mean()*100:.1f}% (n={s["era_late"].sum()})')
print('\n  US whirlpool documented (matrix) by era: early %.1f%% late %.1f%%'%(u[~u['era_late']]['US_whirlpool'].mean()*100,u[u['era_late']]['US_whirlpool'].mean()*100))
print('\n=== CT enhanced share by era ===')
c=ix[ix['mod']=='CT'].copy(); c['enh']=c['报告名称'].astype(str).str.contains('增强')
for e in ['2012-2018','2019-2026']:
    s=c[c['era']==e]; print(f'  {e}: enhanced {int(s["enh"].sum())}/{len(s)} ({s["enh"].mean()*100:.1f}%)')
print('\n=== per-year detection (all modalities) ===')
pv=ix.pivot_table(index='op_year',columns='mod',values='det',aggfunc=['size','mean'])
print(pv.round(2).to_string())
