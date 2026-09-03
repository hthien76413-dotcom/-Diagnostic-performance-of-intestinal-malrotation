# -*- coding: utf-8 -*-
"""Online Resource 2, section S2.5: robustness of the analytic choices."""
exec(open('usaudit4.py').read().split('ROWS=')[0])
import statsmodels.formula.api as smf, numpy as np, json, re
u['ves']=u['vessel_us'].astype(int)
def fit(d,extra=None):
    m=smf.logit('det ~ late'+(' + '+extra if extra else ''),data=d).fit(disp=0)
    a=d.copy(); a['late']=0; b=d.copy(); b['late']=1
    return m,100*(m.predict(b).mean()-m.predict(a).mean())
def f(m,t):
    ci=m.conf_int().loc[t]
    return f'{np.exp(m.params[t]):.2f} ({np.exp(ci[0]):.2f}–{np.exp(ci[1]):.2f}), p={m.pvalues[t]:.3f}'
S4=[['Era boundary','Examinations before / after','Detection before / after','Era odds ratio',
     'Era odds ratio adjusted for examination type','Examination-type odds ratio',
     'Average marginal effect of later era (crude → adjusted)']]
for cut in [2019,2020,2021,2022]:
    d=u.copy(); d['late']=(d['op_year']>=cut).astype(int)
    a=d[d.late==0]; b=d[d.late==1]
    m1,e1=fit(d); m2,e2=fit(d,'ves')
    S4.append([str(cut),f'{len(a)} / {len(b)}',
               f"{int(a['det'].sum())}/{len(a)} ({100*a['det'].mean():.1f}%) / {int(b['det'].sum())}/{len(b)} ({100*b['det'].mean():.1f}%)",
               f(m1,'late'),f(m2,'late'),f(m2,'ves'),f'{e1:+.1f} → {e2:+.1f} pp'])

# earliest vs closest index unit
rep['day']=rep['检查时间'].dt.normalize()
last=rep.sort_values('gap',ascending=False).groupby(['科研患者编号','mod']).first().reset_index()[['科研患者编号','mod','day']]
poolE=rep.merge(last,on=['科研患者编号','mod','day'],how='inner')
E=poolE[poolE['mod']=='US'].groupby('科研患者编号').agg(txt=('txt','\n'.join)).reset_index()
VESSEL=r'肠系膜上动、?静脉|肠系膜上动静脉|肠系膜上动脉|肠系膜上静脉|肠系膜血管|系膜血管|SMA|SMV'
RENAL=r'左肾静脉|胡桃夹|肾静脉受压'; WHIRL=r'漩涡|旋涡|涡流|螺旋'
NEG=r'未见|未探及|未显示|未发现|无明显|不明显|未闻'
def whirl_reported(t):
    for c in re.split(r'[。；;\n]+',str(t)):
        for m in re.finditer(WHIRL,c):
            if not re.search(NEG,c[max(0,m.start()-12):m.start()]): return True
    return False
def counts(series):
    S=series.astype(str)
    ves=S.str.contains(VESSEL,regex=True) & ~(S.str.contains(RENAL,regex=True) & ~S.str.contains(WHIRL,regex=True))
    return {'D3 or duodenojejunal junction':int(S.str.contains(r'十二指肠水平部|十二指肠水平段|十二指肠横部|十二指肠第三段|(?<![弓])横部|水平部|十二指肠空肠曲|屈氏|Treitz|十二指肠悬韧带|十二指肠[-—与和]?空肠交界',regex=True).sum()),
            'Superior mesenteric artery–vein relationship':int(ves.sum()),
            'Enteric fluid administration':int(S.str.contains(r'饮水|口服[^。；\n]{0,6}(?:水|液|造影剂)|注水|注入|胃内注|温开水|经胃管',regex=True).sum()),
            'Whirlpool, swirl or spiral appearance reported':int(S.map(whirl_reported).sum())}
A=counts(u['txt']); B=counts(E['txt'])
S5=[['Documented content','Closest preoperative episode (primary)','Earliest preoperative episode']]
for lab in A:
    S5.append([lab,f'{A[lab]}/119 ({100*A[lab]/119:.1f}%)',f'{B[lab]}/119 ({100*B[lab]/119:.1f}%)'])

strict=pat['volvulus'] & ~(pat['rot_deg'].notna() & (pat['rot_deg']<360))
us_ids=set(u['科研患者编号']); pu=pat[pat['科研患者编号'].isin(us_ids)]
pus=strict[pat['科研患者编号'].isin(us_ids)]
S6=[['Definition of midgut volvulus','Whole cohort (n=465)','Children who underwent ultrasound (n=119)'],
    ['Explicit operative statement of torsion, or any documented degree of rotation (primary)',
     f"{int(pat['volvulus'].sum())} ({100*pat['volvulus'].mean():.1f}%)",
     f"{int(pu['volvulus'].sum())} ({100*pu['volvulus'].mean():.1f}%)"],
    ['Restricted to a documented rotation of 360° or more',
     f"{int(strict.sum())} ({100*strict.mean():.1f}%)",
     f"{int(pus.sum())} ({100*pus.mean():.1f}%)"]]
json.dump({'S4':S4,'S5':S5,'S6':S6},open('or_sens.json','w'),ensure_ascii=False,indent=1)
for k,T in [('S4',S4),('S5',S5),('S6',S6)]:
    print('===',k)
    for r in T: print('  '+' | '.join(r))
