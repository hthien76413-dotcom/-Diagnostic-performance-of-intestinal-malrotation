# -*- coding: utf-8 -*-
"""Final Table 2 and Table 4 on the pooled examination-episode index units."""
exec(open('usaudit4.py').read().split('ROWS=')[0])
import statsmodels.formula.api as smf, numpy as np, json

D=json.load(open('tables123.json')); D.update(json.load(open('tables456.json')))
# --- Table 2: drop the whirlpool row (a prevalence, not a detection rate) ---
T2=[r for r in D['T2'] if 'whirlpool' not in str(r[0]).lower()]
# sensitivity analysis: count as detected only positive episodes whose pooled
# conclusion names malrotation (旋转不良) without a preceding negation, so that a
# conclusion naming volvulus alone, or a sign alone, does not count
from statsmodels.stats.proportion import proportion_confint as pci
def names_malrotation(t):
    for c in re.split(r'[。；;\n]+',str(t)):
        for m in re.finditer(r'旋转不良',c):
            if not re.search(r'未见|未探及|未显示|未发现|无明显|不明显|不考虑',c[max(0,m.start()-12):m.start()]): return True
    return False
NAMED={}
for mod in ['UGI','CT','US']:
    d=IX[IX['mod']==mod].merge(long[long['mod']==mod][['科研患者编号','detected']],on='科研患者编号')
    named=(d['detected']==1)&d['concl'].map(names_malrotation)
    k=int(named.sum()); n=len(d); lo,hi=pci(k,n,method='wilson')
    NAMED[mod]=f'{100*k/n:.1f} ({100*lo:.1f}–{100*hi:.1f})'
    print(f'{mod}: positive and naming malrotation {k}/{n}; positive without naming it {int(d.detected.sum())-k}')
T2[0]=T2[0]+['Detection counting only conclusions naming malrotation, % (95% CI)']
ROWMOD={'UGI series':'UGI','Abdominal CT (all)':'CT','Ultrasound':'US'}
for r in T2[1:]: r.append(NAMED.get(ROWMOD.get(r[0]),'–'))

# --- Table 4: era models on pooled episodes, with average marginal effects ---
def model(d,content=None):
    m1=smf.logit('det ~ late',data=d).fit(disp=0)
    r={'crude':m1}
    if content: r['adj']=smf.logit(f'det ~ late + {content}',data=d).fit(disp=0)
    return r
def orci(m,t):
    ci=m.conf_int().loc[t]
    return f'{np.exp(m.params[t]):.2f} ({np.exp(ci[0]):.2f}–{np.exp(ci[1]):.2f}), p={m.pvalues[t]:.3f}'.replace('p=0.000','p<0.001')
def ame(m,d):
    a=d.copy(); a['late']=0; b=d.copy(); b['late']=1
    return 100*(m.predict(b).mean()-m.predict(a).mean())

rows=[['Modality','Detection 2012–2018','Detection 2019–2026','Era odds ratio (95% CI)',
       'Era odds ratio adjusted for the covariate','Covariate added, odds ratio (95% CI)',
       'Average marginal effect of later era, percentage points (95% CI), crude → adjusted']]
AM=json.load(open('addstats.json'))['AME']
def amci(key):
    pt,ci,_=AM[key]; return f'{pt:+.1f} ({ci[0]:+.1f} to {ci[1]:+.1f})'.replace('-', '−')
AMEKEY={'UGI':('UGI series, crude',None),'CT':('CT, crude','CT, adjusted for contrast enhancement'),
        'US':('Ultrasound, crude','Ultrasound, adjusted for great-vessel session')}
spec=[('UGI','UGI series',None,None),
      ('CT','Abdominal CT','enh','Intravenous contrast enhancement'),
      ('US','Ultrasound','ves','Session included a great-vessel study')]
for mod,lab,cvar,cname in spec:
    d=IX[IX['mod']==mod].merge(mat[['科研患者编号',mod+'_detected']],on='科研患者编号',how='left') \
                        .merge(pat[['科研患者编号','era_late','op_year']],on='科研患者编号',how='left')
    d['det']=d[mod+'_detected'].astype(int); d['late']=d['era_late'].astype(int)
    d['enh']=d['名称'].astype(str).str.contains('增强').astype(int)
    d['ves']=d['名称'].astype(str).str.contains('腹部大血管').astype(int)
    a=d[d.late==0]; b=d[d.late==1]
    M=model(d,cvar)
    r=[lab,f"{int(a['det'].sum())}/{len(a)} ({100*a['det'].mean():.1f}%)",
           f"{int(b['det'].sum())}/{len(b)} ({100*b['det'].mean():.1f}%)",orci(M['crude'],'late')]
    if cvar:
        r+= [orci(M['adj'],'late'), f"{cname} {orci(M['adj'],cvar)}",
             f"{amci(AMEKEY[mod][0])} → {amci(AMEKEY[mod][1])}"]
        assert abs(AM[AMEKEY[mod][0]][0]-ame(M['crude'],d))<0.05 and abs(AM[AMEKEY[mod][1]][0]-ame(M['adj'],d))<0.05
    else:
        r+= ['–','None fitted',amci(AMEKEY[mod][0])]
        assert abs(AM[AMEKEY[mod][0]][0]-ame(M['crude'],d))<0.05
    rows.append(r)
json.dump({'T2':T2,'T4':rows},open('tables24_final.json','w'),ensure_ascii=False,indent=1)
for r in rows: print(' | '.join(r))
print()
print('Table 2 rows kept:',len(T2))
