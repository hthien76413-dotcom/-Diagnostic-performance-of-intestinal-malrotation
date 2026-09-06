# -*- coding: utf-8 -*-
"""Temporal models on the pooled examination-episode index units."""
exec(open('usaudit4.py').read().split('ROWS=')[0])
import statsmodels.formula.api as smf, numpy as np, json

def fit(d,extra=None):
    fml='det ~ late'+(' + '+extra if extra else '')
    m=smf.logit(fml,data=d).fit(disp=0)
    out={}
    for t in m.params.index:
        if t=='Intercept': continue
        ci=m.conf_int().loc[t]
        out[t]=(np.exp(m.params[t]),np.exp(ci[0]),np.exp(ci[1]),m.pvalues[t])
    a=d.copy(); a['late']=0; b=d.copy(); b['late']=1
    out['_ame']=100*(m.predict(b).mean()-m.predict(a).mean())
    return out
def fmt(t): return f'{t[0]:.2f} ({t[1]:.2f}–{t[2]:.2f}), p={t[3]:.3f}'

u['ves']=u['vessel_us'].astype(int)
print('=== ULTRASOUND (n=%d episodes) ==='%len(u))
print('detection %d/%d -> %d/%d'%(u[u.late==0]['det'].sum(),(u.late==0).sum(),
                                  u[u.late==1]['det'].sum(),(u.late==1).sum()))
print('great-vessel session %.1f%% -> %.1f%%'%(100*u[u.late==0]['ves'].mean(),100*u[u.late==1]['ves'].mean()))
m1=fit(u); m2=fit(u,'ves')
print('  era alone      :',fmt(m1['late']),' AME %+.1f pp'%m1['_ame'])
print('  era + vessel   :',fmt(m2['late']),' AME %+.1f pp'%m2['_ame'])
print('  vessel term    :',fmt(m2['ves']))
print('  strata: ',end='')
for e in [0,1]:
    for v in [1,0]:
        t=u[(u.late==e)&(u.ves==v)]; print(f'era{e}/ves{v} {int(t["det"].sum())}/{len(t)}  ',end='')
print()
print('  era cut-point sensitivity:')
for cut in [2019,2020,2021,2022]:
    d=u.copy(); d['late']=(d['op_year']>=cut).astype(int)
    a=fit(d); b=fit(d,'ves')
    print(f'   {cut}: n {int((d.late==0).sum())}/{int((d.late==1).sum())}  era {fmt(a["late"])}'
          f'  -> adj {fmt(b["late"])}  vessel {fmt(b["ves"])}  AME {a["_ame"]:+.1f} -> {b["_ame"]:+.1f} pp')

# ---- CT and UGI pooled content audits ----
print()
print('=== CT / UGI content audit on pooled episodes ===')
OUT={}
for mod,lab,items in [
  ('CT','Abdominal CT',[('Contrast enhancement',None,r'增强'),
                        ('Mesenteric whirl','txt',r'漩涡|旋涡|涡流|螺旋'),
                        ('Duodenum mentioned','txt',r'十二指肠'),
                        ('Mesenteric-vessel relationship','txt',r'肠系膜上动、?静脉|肠系膜上动静脉|肠系膜上动脉|肠系膜上静脉|系膜血管|SMA|SMV'),
                        ('Three-dimensional reconstruction',None,r'三维重建')]),
  ('UGI','Upper gastrointestinal series',[('Duodenojejunal junction','txt',r'空肠曲|屈氏|Treitz|悬韧带|十二指肠[-—与和]?空肠交界'),
                        ('Corkscrew / spring appearance','txt',r'弹簧|螺旋|绞索|盘曲'),
                        ('Jejunal position','txt',r'空肠[^。；\n]{0,10}(?:位于|居|偏)'),
                        ('Caecal position','txt',r'回盲'),
                        ('Whole-gastrointestinal study',None,r'全消化道'),
                        ('Barium used',None,r'钡')])]:
    d=IX[IX['mod']==mod].merge(mat[['科研患者编号',mod+'_detected']],on='科研患者编号',how='left')
    d['det']=d[mod+'_detected'].astype(int)
    rows=[]
    for name,field,rx in items:
        src=d['txt'] if field=='txt' else d['名称']
        s=src.astype(str).str.contains(rx,regex=True)
        rows.append([f'{lab} (n={len(d)})',name,f'{int(s.sum())} ({100*s.mean():.1f})',
                     f'{int(d[s]["det"].sum())}/{int(s.sum())} ({100*d[s]["det"].mean():.0f}%)' if s.sum()>=10 else f'{int(d[s]["det"].sum())}/{int(s.sum())}',
                     f'{int(d[~s]["det"].sum())}/{int((~s).sum())} ({100*d[~s]["det"].mean():.0f}%)' if (~s).sum()>=10 else f'{int(d[~s]["det"].sum())}/{int((~s).sum())}'])
        print('   '+' | '.join(rows[-1]))
    OUT[mod]=rows
S3=[['Modality','Documented content','n (%) of reports','Detection when documented','Detection when not documented']]+OUT['CT']+OUT['UGI']
json.dump({'S3':S3},open('or3_pooled.json','w'),ensure_ascii=False,indent=1)
