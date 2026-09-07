exec(open('core.py').read())
import json, statsmodels.api as sm, statsmodels.formula.api as smf
from statsmodels.stats.proportion import proportion_confint as pci
from statsmodels.stats.contingency_tables import mcnemar, cochrans_q
long['modality']=pd.Categorical(long['mod'],categories=['UGI','CT','US'])
long['agegrp']=pd.cut(long['age_days'],[-1,28,365,1e9],labels=['neonate','29d-1y','>1y'])
long=long.sort_values('科研患者编号')
def gee(f):
    return smf.gee(f,'科研患者编号',data=long,family=sm.families.Binomial(),cov_struct=sm.cov_struct.Exchangeable()).fit()
m1=gee('detected ~ C(modality)'); m2=gee('detected ~ C(modality) + era_late + C(agegrp, Treatment(reference="neonate"))')
def o(m,k):
    if k not in m.params: return '–'
    ci=m.conf_int(); return f'{np.exp(m.params[k]):.2f} ({np.exp(ci.loc[k,0]):.2f}–{np.exp(ci.loc[k,1]):.2f})'
def pv(m,k): 
    p=m.pvalues[k]; return '<0.001' if p<0.001 else f'{p:.3f}'
K={'CT':'C(modality)[T.CT]','US':'C(modality)[T.US]','era':'era_late[T.True]',
   'a2':'C(agegrp, Treatment(reference="neonate"))[T.29d-1y]','a3':'C(agegrp, Treatment(reference="neonate"))[T.>1y]'}
T4=[['Effect','Unadjusted OR (95% CI)','Adjusted OR (95% CI)','p (adjusted)'],
    ['Abdominal CT vs UGI series',o(m1,K['CT']),o(m2,K['CT']),pv(m2,K['CT'])],
    ['Gastrointestinal ultrasound vs UGI series',o(m1,K['US']),o(m2,K['US']),pv(m2,K['US'])],
    ['Operated 2019–2026 vs 2012–2018','–',o(m2,K['era']),pv(m2,K['era'])],
    ['Age 29 days–1 year vs neonate','–',o(m2,K['a2']),pv(m2,K['a2'])],
    ['Age >1 year vs neonate','–',o(m2,K['a3']),pv(m2,K['a3'])]]
# Table 5 paired
p=mat[mat[['US_detected','CT_detected','UGI_detected']].notna().all(axis=1)].copy()
pid=set(p['科研患者编号'])
tt=idx[idx['科研患者编号'].isin(pid)].pivot_table(index='科研患者编号',columns='mod',values='检查时间',aggfunc='first')
p=p.merge(((tt.max(axis=1)-tt.min(axis=1)).dt.total_seconds()/86400).rename('span'),on='科研患者编号')
def blk(d):
    out={}
    for c in ['UGI_detected','US_detected','CT_detected','US_whirlpool']:
        k=int(d[c].sum()); n=len(d); lo,hi=pci(k,n,method='wilson'); out[c]=f'{k}/{n} ({k/n*100:.1f}; {lo*100:.1f}–{hi*100:.1f})'
    M=d[['UGI_detected','CT_detected','US_detected']].values.astype(int)
    out['Q']=cochrans_q(M).pvalue
    for a,b,nm in [('UGI_detected','CT_detected','UGI vs CT'),('UGI_detected','US_detected','UGI vs US'),('CT_detected','US_detected','CT vs US')]:
        tab=pd.crosstab(d[a],d[b]).reindex(index=[0.0,1.0],columns=[0.0,1.0],fill_value=0).values
        out[nm]=(int(tab[1,0]),int(tab[0,1]),mcnemar(tab,exact=True).pvalue)
    return out
def fp(x): return '<0.001' if x<0.001 else f'{x:.3f}'
cols=[('All (n=59)',p),('All three within 48 h (n=%d)'%int((p['span']<=2).sum()),p[p['span']<=2]),('All three within 24 h (n=%d)'%int((p['span']<=1).sum()),p[p['span']<=1])]
B=[(lab,blk(d)) for lab,d in cols]
T5=[['Measure']+[l for l,_ in B]]
for c,lab in [('UGI_detected','UGI contrast series, n/N (%; 95% CI)'),('US_detected','Gastrointestinal ultrasound, n/N (%; 95% CI)'),
              ('CT_detected','Abdominal CT, n/N (%; 95% CI)'),('US_whirlpool','Ultrasound whirlpool sign, n/N (%; 95% CI)')]:
    T5.append([lab]+[b[c] for _,b in B])
T5.append(["Cochran's Q, p"]+[fp(b['Q']) for _,b in B])
for nm in ['UGI vs CT','UGI vs US','CT vs US']:
    T5.append([f'Exact McNemar {nm}: discordant pairs, p']+[f'{b[nm][0]}/{b[nm][1]}, p={fp(b[nm][2])}' for _,b in B])
# Table 6 temporal
ixf=pd.read_csv('ix_full.csv'); u=pd.read_csv('us_audit.csv')
def lg(f,d,k):
    m=smf.logit(f,data=d).fit(disp=0); ci=m.conf_int()
    return f'{np.exp(m.params[k]):.2f} ({np.exp(ci.loc[k,0]):.2f}–{np.exp(ci.loc[k,1]):.2f})', ('<0.001' if m.pvalues[k]<0.001 else f'{m.pvalues[k]:.3f}')
c=ixf[ixf['mod']=='CT'].copy(); c['enh']=c['报告名称'].astype(str).str.contains('增强').astype(int)
g=ixf[ixf['mod']=='UGI'].copy(); u['det']=u['US_detected']
def pf(p): return 'p<0.001' if p=='<0.001' else f'p={p}'
T6=[['Modality','Detection 2012–2018','Detection 2019–2026','Era OR (95% CI)','Era OR after adjustment for examination content','Content variable OR (95% CI)']]
def dr(d):
    e=d[~d['era_late'].astype(bool)]; l=d[d['era_late'].astype(bool)]
    return f"{int(e['det'].sum())}/{len(e)} ({e['det'].mean()*100:.1f}%)", f"{int(l['det'].sum())}/{len(l)} ({l['det'].mean()*100:.1f}%)"
a,b=dr(g); e1,p1=lg('det ~ era_late',g,'era_late[T.True]')
T6.append(['UGI contrast series',a,b,f'{e1} ({pf(p1)})','Not applicable (technique unchanged)','–'])
a,b=dr(c); e1,p1=lg('det ~ era_late',c,'era_late[T.True]'); e2,p2=lg('det ~ era_late + enh',c,'era_late[T.True]'); e3,p3=lg('det ~ era_late + enh',c,'enh')
T6.append(['Abdominal CT',a,b,f'{e1} ({pf(p1)})',f'{e2} ({pf(p2)})',f'Contrast enhancement {e3} ({pf(p3)})'])
a,b=dr(u); e1,p1=lg('det ~ era_late',u,'era_late[T.True]'); e2,p2=lg('det ~ era_late + vessel_us',u,'era_late[T.True]'); e3,p3=lg('det ~ era_late + vessel_us',u,'vessel_us[T.True]')
T6.append(['Gastrointestinal ultrasound',a,b,f'{e1} ({pf(p1)})',f'{e2} ({pf(p2)})',f'Vessel-focused examination {e3} ({pf(p3)})'])
json.dump({'T4':T4,'T5':T5,'T6':T6},open('tables456.json','w'),ensure_ascii=False,indent=1)
for T in (T4,T5,T6): print('\n'.join(' | '.join(map(str,r)) for r in T)); print('---')
