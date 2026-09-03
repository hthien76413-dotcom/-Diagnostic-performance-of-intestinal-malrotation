# -*- coding: utf-8 -*-
"""Final Table 2 and Table 4 on the pooled examination-episode index units."""
exec(open('usaudit4.py').read().split('ROWS=')[0])
import statsmodels.formula.api as smf, numpy as np, json

D=json.load(open('tables123.json')); D.update(json.load(open('tables456.json')))
# --- Table 2: drop the whirlpool row (a prevalence, not a detection rate) ---
T2=[r for r in D['T2'] if 'whirlpool' not in str(r[0]).lower()]

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
       'Era odds ratio after adjustment for examination content','Examination-content variable, odds ratio (95% CI)',
       'Average marginal effect of later era, percentage points (crude → adjusted)']]
spec=[('UGI','UGI contrast series',None,None),
      ('CT','Abdominal CT','enh','Intravenous contrast enhancement'),
      ('US','Gastrointestinal ultrasound','ves','Session included a great-vessel study')]
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
             f"{ame(M['crude'],d):+.1f} → {ame(M['adj'],d):+.1f}"]
    else:
        r+= ['Not applicable (technique unchanged)','–',f"{ame(M['crude'],d):+.1f}"]
    rows.append(r)
json.dump({'T2':T2,'T4':rows},open('tables24_final.json','w'),ensure_ascii=False,indent=1)
for r in rows: print(' | '.join(r))
print()
print('Table 2 rows kept:',len(T2))
