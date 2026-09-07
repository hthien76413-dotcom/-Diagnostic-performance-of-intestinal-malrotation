exec(open('core.py').read())
import json
from statsmodels.stats.proportion import proportion_confint as pci
ixf=pd.read_csv('ix_full.csv'); u=pd.read_csv('us_audit.csv'); tier=pd.read_csv('pos_tier.csv')
def W(k,n):
    lo,hi=pci(k,n,method='wilson'); return f'{k}/{n} = {k/n*100:.1f} ({lo*100:.1f}–{hi*100:.1f})'
# OR1 T: label distribution
S1=[['Modality','Index reports','Classified positive','Classified negative','Positive with definite wording','Positive with probable wording','Positive with possible wording']]
for mod,lab in [('UGI','UGI contrast series'),('CT','Abdominal CT'),('US','Gastrointestinal ultrasound')]:
    d=ixf[ixf['mod']==mod]; k=int(d['det'].sum()); n=len(d)
    t=tier[tier['mod']==mod]['tier'].value_counts()
    S1.append([lab,str(n),f'{k} ({k/n*100:.1f}%)',f'{n-k} ({(n-k)/n*100:.1f}%)',
               str(int(t.get('definite',0))),str(int(t.get('probable',0))),str(int(t.get('possible',0)))])
_tot={t:sum(int(r[i]) for r in S1[1:]) for i,t in ((4,'definite'),(5,'probable'),(6,'possible'))}
S1.append(['All three','740',f"{int(ixf['det'].sum())}",f"{740-int(ixf['det'].sum())}",
           str(_tot['definite']),str(_tot['probable']),str(_tot['possible'])])
assert sum(_tot.values())==int(ixf['det'].sum()), 'certainty tiers do not sum to the positives'
# OR2 stratified
pat['agegrp']=pd.cut(pat['age_days'],[-1,28,365,1e9],labels=['≤28 days','29 days–1 year','>1 year'])
ix2=ixf.merge(pat[['科研患者编号','agegrp']],on='科研患者编号',how='left')
S2=[['Index test','Stratum','Detected / total','Detection rate % (95% CI)']]
for mod,lab in [('UGI','UGI contrast series'),('CT','Abdominal CT'),('US','Gastrointestinal ultrasound')]:
    d=ix2[ix2['mod']==mod]
    for v,sl in [(True,'Midgut volvulus present'),(False,'Midgut volvulus absent')]:
        s=d[d['volvulus'].astype(bool)==v]; k=int(s['det'].sum()); n=len(s)
        lo,hi=pci(k,n,method='wilson'); S2.append([lab,sl,f'{k}/{n}',f'{k/n*100:.1f} ({lo*100:.1f}–{hi*100:.1f})'])
    for g in ['≤28 days','29 days–1 year','>1 year']:
        s=d[d['agegrp']==g]; k=int(s['det'].sum()); n=len(s)
        lo,hi=pci(k,n,method='wilson'); S2.append([lab,'Age '+g,f'{k}/{n}',f'{k/n*100:.1f} ({lo*100:.1f}–{hi*100:.1f})'])
# OR2b (volvulus-specific sign) is produced by volsign2.py, which applies the
# modality-specific, negation-aware rules. It is not duplicated here.
# OR3 CT and UGI content
c=ixf[ixf['mod']=='CT'].copy(); g=ixf[ixf['mod']=='UGI'].copy()
def f(d,rx): return d['txt'].astype(str).str.contains(rx,regex=True)
c['Contrast enhancement']=c['报告名称'].astype(str).str.contains('增强')
c['Mesenteric whirl']=f(c,r'漩涡|旋涡|涡流|螺旋')
c['Duodenum mentioned']=f(c,r'十二指肠')
c['Mesenteric-vessel relationship']=f(c,r'肠系膜上动脉|肠系膜上静脉|系膜血管')
c['Three-dimensional reconstruction']=c['报告名称'].astype(str).str.contains('三维重建')
g['Duodenojejunal junction']=f(g,r'十二指肠空肠曲|屈氏|Treitz|十二指肠.{0,6}空肠')
g['Corkscrew / spring appearance']=f(g,r'弹簧|螺旋|绞索|盘曲')
g['Jejunal position']=f(g,r'空肠.{0,10}(位于|居|偏)')
g['Caecal position']=f(g,r'回盲部')
g['Whole-gastrointestinal study']=g['报告名称'].astype(str).str.contains('全消化道')
g['Barium used']=g['报告名称'].astype(str).str.contains('钡')
S3=[['Modality','Documented content','n (%) of reports','Detection when documented, %','Detection when not documented, %']]
for d,lab,keys in [(c,'Abdominal CT (n=320)',['Contrast enhancement','Mesenteric whirl','Duodenum mentioned','Mesenteric-vessel relationship','Three-dimensional reconstruction']),
                   (g,'UGI contrast series (n=301)',['Duodenojejunal junction','Corkscrew / spring appearance','Jejunal position','Caecal position','Whole-gastrointestinal study','Barium used'])]:
    for k_ in keys:
        s=d[k_].astype(bool)
        S3.append([lab,k_,f'{int(s.sum())} ({s.mean()*100:.1f})',f"{d[s]['det'].mean()*100:.1f}" if s.sum() else '–',f"{d[~s]['det'].mean()*100:.1f}" if (~s).sum() else '–'])
json.dump({'S1':S1,'S2':S2,'S3':S3},open('or_tables.json','w'),ensure_ascii=False,indent=1)
for T in (S1,S2,S3): print('\n'.join(' | '.join(map(str,r)) for r in T)); print('---')
