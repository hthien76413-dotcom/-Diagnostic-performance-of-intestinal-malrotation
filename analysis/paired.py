exec(open('core.py').read())
from scipy import stats
from statsmodels.stats.contingency_tables import mcnemar
p=mat[mat[['US_detected','CT_detected','UGI_detected']].notna().all(axis=1)].copy()
pid=set(p['科研患者编号'])
t=idx[idx['科研患者编号'].isin(pid)].pivot_table(index='科研患者编号',columns='mod',values='检查时间',aggfunc='first')
t['span']=(t.max(axis=1)-t.min(axis=1)).dt.total_seconds()/86400
p=p.merge(t[['span']],on='科研患者编号',how='left').merge(pat[['科研患者编号','era_late','neonate','volvulus','age_days']],on='科研患者编号')
print('paired n=%d ; span median %.2f d, IQR %.2f-%.2f ; within2d %d (%.0f%%), >2d %d'%(
    len(p),p['span'].median(),p['span'].quantile(.25),p['span'].quantile(.75),(p['span']<=2).sum(),(p['span']<=2).mean()*100,(p['span']>2).sum()))
def wilson(k,n):
    if n==0: return (np.nan,np.nan)
    from statsmodels.stats.proportion import proportion_confint
    return proportion_confint(k,n,method='wilson')
def block(d,lab):
    print(f'\n--- {lab} (n={len(d)}) ---')
    for c,nm in [('UGI_detected','UGI'),('US_detected','US'),('CT_detected','CT'),('US_whirlpool','US-whirl')]:
        k=int(d[c].sum()); n=len(d); lo,hi=wilson(k,n)
        print(f'   {nm:9s} {k:3d}/{n:3d} = {k/n*100:5.1f}% ({lo*100:.1f}-{hi*100:.1f})')
    # Cochran Q
    M=d[['UGI_detected','CT_detected','US_detected']].values.astype(int)
    from statsmodels.stats.contingency_tables import cochrans_q
    q=cochrans_q(M); print(f'   Cochran Q = {q.statistic:.3f}, p = {q.pvalue:.4f}')
    for a,b in [('UGI_detected','CT_detected'),('UGI_detected','US_detected'),('CT_detected','US_detected')]:
        tab=pd.crosstab(d[a],d[b]).reindex(index=[0.0,1.0],columns=[0.0,1.0],fill_value=0).values
        r=mcnemar(tab,exact=True)
        print(f'   {a[:3]} vs {b[:3]}: discordant {int(tab[1,0])}/{int(tab[0,1])}, exact McNemar p={r.pvalue:.4f}')
block(p,'ALL paired')
block(p[p['span']<=2],'paired, all three within 2 days')
block(p[p['span']<=1],'paired, within 1 day')
# order of tests
o=idx[idx['科研患者编号'].isin(pid)].sort_values('检查时间').groupby('科研患者编号')['mod'].apply(list)
print('\nfirst test in paired cohort:',pd.Series([v[0] for v in o]).value_counts().to_dict())
print('last  test in paired cohort:',pd.Series([v[-1] for v in o]).value_counts().to_dict())
# characteristics: paired vs non-paired imaged
np_=mat[~mat['科研患者编号'].isin(pid)].merge(pat,on='科研患者编号')
pp=p
print('\npaired vs other imaged: neonate %.0f%% vs %.0f%%; volvulus %.0f%% vs %.0f%%; late era %.0f%% vs %.0f%%; age med %.0f vs %.0f d'%(
 pp['neonate'].mean()*100,np_['neonate'].mean()*100,pp['volvulus'].mean()*100,np_['volvulus'].mean()*100,
 pp['era_late'].mean()*100,np_['era_late'].mean()*100,pp['age_days'].median(),np_['age_days'].median()))
# time from first imaging to operation
gap=idx.groupby('科研患者编号')['gap'].max()
print('\ndays from FIRST preoperative index test to operation: median %.1f (IQR %.1f-%.1f)'%(gap.median(),gap.quantile(.25),gap.quantile(.75)))
gp=gap[gap.index.isin(pid)]
print('paired cohort: median %.1f (IQR %.1f-%.1f)'%(gp.median(),gp.quantile(.25),gp.quantile(.75)))
