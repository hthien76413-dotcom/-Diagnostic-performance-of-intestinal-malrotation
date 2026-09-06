exec(open('core.py').read())
import json
from statsmodels.stats.proportion import proportion_confint as pci
p2=pd.read_csv('pat2.csv'); ixf=pd.read_csv('ix_full.csv'); u=pd.read_csv('us_audit.csv')
img=set(mat['科研患者编号']); noidx=ids-img
G={'UGI':set(mat[mat['UGI_detected'].notna()]['科研患者编号']),'CT':set(mat[mat['CT_detected'].notna()]['科研患者编号']),
   'US':set(mat[mat['US_detected'].notna()]['科研患者编号']),'none':noidx}
def pc(k,n): return f'{k} ({k/n*100:.1f})'
def med(d): return f"{d['age_days'].median():.0f} ({d['age_days'].quantile(.25):.0f}–{d['age_days'].quantile(.75):.0f})"
rows=[]
cols=['Overall','UGI','CT','US','none']
sets={'Overall':ids,**G}
def row(lab,fn): rows.append([lab]+[fn(p2[p2['科研患者编号'].isin(sets[c])]) for c in cols])
row('Children, n',lambda d:str(len(d)))
row('Age at operation, median (IQR), days',med)
row('Neonate ≤28 days, n (%)',lambda d:pc(int(d['neonate'].sum()),len(d)))
row('Age >1 year, n (%)',lambda d:pc(int((d['age_days']>365).sum()),len(d)))
row('Male, n (%)',lambda d:pc(int(d['male'].sum()),len(d)))
row('Operated 2019–2026, n (%)',lambda d:pc(int(d['era_late'].sum()),len(d)))
row('Midgut volvulus at operation, n (%)',lambda d:pc(int(d['volvulus'].sum()),len(d)))
for c,lab in [('vomit','Vomiting documented, n (%)'),('bilious','Bilious vomiting documented, n (%)'),
              ('distension','Abdominal distension, n (%)'),('bloody_stool','Blood in stool, n (%)'),
              ('abd_pain','Abdominal pain, n (%)'),('duration_chronic','Recurrent/intermittent symptoms, n (%)'),
              ('shock','Shock or poor perfusion, n (%)')]:
    row(lab,lambda d,c=c:pc(int(d[c].sum()),len(d)))
T1=[['Characteristic','All children','Received UGI series','Received CT','Received ultrasound','Received none of the three']]+rows
# Table 2
def wr(k,n):
    lo,hi=pci(k,n,method='wilson'); return f'{k}/{n}',f'{k/n*100:.1f} ({lo*100:.1f}–{hi*100:.1f})'
tier=pd.read_csv('pos_tier.csv')
T2=[['Index test','Positive/total','Detection rate, % (95% CI)','Definite wording, n (%)','Probable wording, n (%)','Possible wording, n (%)','Detection excluding possible wording, %']]
for mod,lab in [('UGI','UGI contrast series'),('CT','Abdominal CT (all)'),('US','Gastrointestinal ultrasound')]:
    d=ixf[ixf['mod']==mod]; k=int(d['det'].sum()); n=len(d); a,b=wr(k,n)
    t=tier[tier['mod']==mod]['tier'].value_counts()
    de,pr,po=int(t.get('definite',0)),int(t.get('probable',0)),int(t.get('possible',0))
    T2.append([lab,a,b,f'{de} ({de/k*100:.1f})',f'{pr} ({pr/k*100:.1f})',f'{po} ({po/k*100:.1f})',f'{(k-po)/n*100:.1f}'])
c=ixf[ixf['mod']=='CT'].copy(); c['enh']=c['报告名称'].astype(str).str.contains('增强')
for sel,lab in [(c[c['enh']],'  CT, contrast-enhanced'),(c[~c['enh']],'  CT, unenhanced')]:
    k=int(sel['det'].sum()); n=len(sel); a,b=wr(k,n); T2.append([lab,a,b,'–','–','–','–'])
k=int(u['US_whirlpool'].sum()); n=len(u); a,b=wr(k,n); T2.append(['  Ultrasound, whirlpool sign recorded',a,b,'–','–','–','–'])
# Table 3 US content
T3=[['Documented content of the ultrasound report','n (%) of 119 reports','2012–2018 (n=39), %','2019–2026 (n=80), %','Detection when documented, %','Detection when not documented, %']]
items=[('d3','Third portion of duodenum or duodenojejunal junction'),('duodenum','Duodenum mentioned in any form'),
 ('sma_smv','Superior mesenteric artery–vein relationship'),('inversion','Explicit statement of vessel inversion'),
 ('fluid','Enteric fluid administered'),('cecum','Caecal position'),('whirl_txt','Whirlpool, swirl or spiral appearance'),
 ('gas_limit','Bowel gas explicitly limiting the study'),('vessel_us','Recorded as abdominal great-vessel study'),
 ('gi_us','Recorded as gastrointestinal ultrasound'),('bedside','Performed at the bedside')]
for k_,lab in items:
    s=u[k_].astype(bool); n=len(u)
    dy=f"{u[s]['US_detected'].mean()*100:.1f}" if s.sum() else '–'
    dn=f"{u[~s]['US_detected'].mean()*100:.1f}" if (~s).sum() else '–'
    T3.append([lab,f'{int(s.sum())} ({s.mean()*100:.1f})',f"{u[~u['era_late']][k_].mean()*100:.1f}",f"{u[u['era_late']][k_].mean()*100:.1f}",dy,dn])
s=(u['US_whirlpool']==1); 
T3.append(['Whirlpool sign (adjudicated variable)',f'{int(s.sum())} ({s.mean()*100:.1f})',
           f"{u[~u['era_late']]['US_whirlpool'].mean()*100:.1f}",f"{u[u['era_late']]['US_whirlpool'].mean()*100:.1f}",
           f"{u[s]['US_detected'].mean()*100:.1f}",f"{u[~s]['US_detected'].mean()*100:.1f}"])
json.dump({'T1':T1,'T2':T2,'T3':T3},open('tables123.json','w'),ensure_ascii=False,indent=1)
for T in (T1,T2,T3):
    print('\n'.join(' | '.join(r) for r in T)); print('---')
