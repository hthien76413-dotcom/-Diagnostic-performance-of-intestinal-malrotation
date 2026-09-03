# -*- coding: utf-8 -*-
"""Analyses added after statistical review:
  (1) bootstrap CIs for the average marginal effect of era
  (2) paired proportion differences with CIs in the three-modality subgroup
  (3) Firth penalised logistic for the separated volvulus contrast
  (4) era x examination-content interaction
"""
exec(open('usaudit4.py').read().split('ROWS=')[0])
import numpy as np, json, statsmodels.formula.api as smf
from statsmodels.stats.contingency_tables import mcnemar
from statsmodels.stats.proportion import proportion_confint as pci
from firth import firth_logit
rng=np.random.default_rng(20260903)
B=2000

# ---------- (1) AME with bootstrap CI ----------
def _irls(X,y,maxit=60,tol=1e-9):
    b=np.zeros(X.shape[1])
    for _ in range(maxit):
        mu=1/(1+np.exp(-(X@b))); w=np.clip(mu*(1-mu),1e-10,None)
        z=X@b+(y-mu)/w
        nb=np.linalg.solve(X.T@(X*w[:,None]),X.T@(w*z))
        if np.max(np.abs(nb-b))<tol: b=nb; break
        b=nb
    return b
def ame(d,extra):
    cols=['late']+([extra] if extra else [])
    X=np.column_stack([np.ones(len(d))]+[d[c].to_numpy(float) for c in cols])
    y=d['det'].to_numpy(float)
    b=_irls(X,y)
    X0=X.copy(); X0[:,1]=0; X1=X.copy(); X1[:,1]=1
    f=lambda M:(1/(1+np.exp(-(M@b)))).mean()
    return 100*(f(X1)-f(X0))
def boot_ame(d,extra,B=B):
    out=[]; n=len(d); idxs=np.arange(n)
    for _ in range(B):
        s=d.iloc[rng.choice(idxs,n,replace=True)]
        if s['det'].nunique()<2 or s['late'].nunique()<2: continue
        if extra and s[extra].nunique()<2: continue
        try: out.append(ame(s,extra))
        except Exception: pass
    return np.percentile(out,[2.5,97.5]), len(out)

u['ves']=u['vessel_us'].astype(int); u['late']=u['era_late'].astype(int)
AME={}
for lab,d,extra in [('Ultrasound, crude',u,None),('Ultrasound, adjusted for great-vessel session',u,'ves')]:
    pt=ame(d,extra); ci,k=boot_ame(d,extra)
    AME[lab]=(pt,ci,k); print(f'{lab:48s} AME {pt:+.1f} pp (95% CI {ci[0]:+.1f} to {ci[1]:+.1f}; {k} resamples)')

ct=IX[IX['mod']=='CT'].merge(mat[['科研患者编号','CT_detected']],on='科研患者编号',how='left') \
                      .merge(pat[['科研患者编号','era_late']],on='科研患者编号',how='left')
ct['det']=ct['CT_detected'].astype(int); ct['late']=ct['era_late'].astype(int)
ct['enh']=ct['名称'].astype(str).str.contains('增强').astype(int)
for lab,extra in [('CT, crude',None),('CT, adjusted for contrast enhancement','enh')]:
    pt=ame(ct,extra); ci,k=boot_ame(ct,extra)
    AME[lab]=(pt,ci,k); print(f'{lab:48s} AME {pt:+.1f} pp (95% CI {ci[0]:+.1f} to {ci[1]:+.1f}; {k} resamples)')

# ---------- (2) paired differences ----------
print()
p=mat[mat[['US_detected','CT_detected','UGI_detected']].notna().all(axis=1)].copy()
PAIR=[]
for a,b,la,lb in [('UGI_detected','CT_detected','UGI series','CT'),
                  ('UGI_detected','US_detected','UGI series','ultrasound'),
                  ('CT_detected','US_detected','CT','ultrasound')]:
    A=p[a].astype(int).values; Bv=p[b].astype(int).values; n=len(A)
    d_hat=100*(A.mean()-Bv.mean())
    bs=[100*(A[i].mean()-Bv[i].mean()) for i in (rng.choice(n,n,replace=True) for _ in range(B))]
    lo,hi=np.percentile(bs,[2.5,97.5])
    n10=int(((A==1)&(Bv==0)).sum()); n01=int(((A==0)&(Bv==1)).sum())
    pv=mcnemar([[int(((A==0)&(Bv==0)).sum()),n01],[n10,int(((A==1)&(Bv==1)).sum())]],exact=True).pvalue
    PAIR.append([f'{la} vs {lb}',f'{100*A.mean():.1f}% vs {100*Bv.mean():.1f}%',
                 f'{d_hat:+.1f} ({lo:+.1f} to {hi:+.1f})',f'{n10}/{n01}',f'{pv:.3f}'])
    print(f'  {la:11s} vs {lb:11s} difference {d_hat:+.1f} pp (95% CI {lo:+.1f} to {hi:+.1f}); discordant {n10}/{n01}; exact McNemar p={pv:.4f}')

# ---------- (3) Firth for the separated contrast ----------
print()
us=IX[IX['mod']=='US'].merge(mat[['科研患者编号','US_detected']],on='科研患者编号',how='left') \
                      .merge(pat[['科研患者编号','volvulus','era_late','neonate']],on='科研患者编号',how='left')
y=us['US_detected'].astype(float).values
V=us['volvulus'].astype(float).values
print('  ultrasound detection by volvulus: volvulus %d/%d, no volvulus %d/%d'%(
      int(y[V==1].sum()),int((V==1).sum()),int(y[V==0].sum()),int((V==0).sum())))
for k,n,lab in [(int(y[V==1].sum()),int((V==1).sum()),'volvulus present'),
                (int(y[V==0].sum()),int((V==0).sum()),'volvulus absent')]:
    lo,hi=pci(k,n,method='wilson'); print(f'    {lab:17s} {k}/{n} = {100*k/n:.1f}% (Wilson {100*lo:.1f}-{100*hi:.1f})')
X=np.column_stack([np.ones(len(us)),V])
b,se=firth_logit(X,y)
orv=np.exp(b[1]); lo=np.exp(b[1]-1.96*se[1]); hi=np.exp(b[1]+1.96*se[1])
print(f'  Firth penalised OR for detection given volvulus: {orv:.2f} ({lo:.2f}-{hi:.2f})')
FIRTH=(orv,lo,hi)

# ---------- (4) era x content interaction ----------
print()
INT=[]
for lab,d,c in [('Ultrasound: era x great-vessel session',u,'ves'),('CT: era x contrast enhancement',ct,'enh')]:
    m=smf.logit(f'det ~ late * {c}',data=d).fit(disp=0)
    t=f'late:{c}'
    ci=m.conf_int().loc[t]
    INT.append([lab,f'{np.exp(m.params[t]):.2f} ({np.exp(ci[0]):.2f}–{np.exp(ci[1]):.2f})',f'{m.pvalues[t]:.3f}'])
    print(f'  {lab:42s} interaction OR {np.exp(m.params[t]):.2f} ({np.exp(ci[0]):.2f}-{np.exp(ci[1]):.2f}) p={m.pvalues[t]:.3f}')

json.dump({'AME':{k:[v[0],list(v[1]),v[2]] for k,v in AME.items()},
           'PAIR':PAIR,'FIRTH':list(FIRTH),'INT':INT},
          open('addstats.json','w'),ensure_ascii=False,indent=1)
