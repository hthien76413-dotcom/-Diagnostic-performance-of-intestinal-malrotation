# -*- coding: utf-8 -*-
"""Ultrasound report-content audit.

Index unit = the examination episode closest to operation: all reports of that
modality issued on that calendar day are pooled, because the department routinely
issues a separate report for the gastrointestinal and the great-vessel study of
the same session. Superseded usaudit2.py, which took a single report and could
therefore pick the negative companion report of a positive session."""
exec(open('core.py').read())
import re, json, numpy as np, pandas as pd

rep['day']=rep['检查时间'].dt.normalize()
first=rep.sort_values('gap').groupby(['科研患者编号','mod']).first().reset_index()[['科研患者编号','mod','day']]
pool=rep.merge(first,on=['科研患者编号','mod','day'],how='inner')
IX=pool.groupby(['科研患者编号','mod']).agg(txt=('txt','\n'.join),concl=('concl','\n'.join),
                                          名称=('报告名称',lambda s:' | '.join(s)),
                                          nrep=('txt','size'),检查时间=('检查时间','min')).reset_index()
IX.to_csv('index_units.csv',index=False)

u=IX[IX['mod']=='US'].merge(mat[['科研患者编号','US_detected','US_whirlpool']],on='科研患者编号',how='left') \
                     .merge(pat[['科研患者编号','era_late','op_year','volvulus']],on='科研患者编号',how='left')
T=u['txt'].astype(str); N=u['名称'].astype(str)
f=lambda rx: T.str.contains(rx,regex=True)
u['d3']       = f(r'十二指肠水平部|十二指肠水平段|十二指肠横部|十二指肠第三段|(?<![弓])横部|水平部')
u['djj']      = f(r'十二指肠空肠曲|屈氏|Treitz|十二指肠悬韧带|十二指肠[-—与和]?空肠交界')
u['d3_or_djj']= u['d3']|u['djj']
u['duodenum'] = f(r'十二指肠')
u['sma_smv']  = f(r'肠系膜上动脉|肠系膜上静脉|系膜血管|SMA|SMV')
u['inversion']= f(r'(?:静脉|动脉)[^。；\n]{0,10}(?:换位|反位|倒置|关系异常|异常关系)|静脉位于[^。；\n]{0,8}左|动脉位于[^。；\n]{0,8}右')
u['fluid']    = f(r'饮水|口服[^。；\n]{0,6}(?:水|液|造影剂)|注水|注入|胃内注|温开水|经胃管')
u['dynamic']  = f(r'动态|实时观察|连续观察')
u['compress'] = f(r'加压|探头压|压迫探查')
u['whirl_txt']= f(r'漩涡|旋涡|涡流|螺旋')
u['gas_limit']= f(r'气体干扰|肠气干扰|气体较多|积气[^。；\n]{0,10}(?:干扰|遮挡)|显示欠清|显示不清|声窗')
u['cecum']    = f(r'回盲')
u['doppler']  = f(r'CDFI|彩色多普勒|多普勒')
u['vessel_us']= N.str.contains('腹部大血管'); u['gi_us']=N.str.contains('胃肠道')
u['pyloric']  = N.str.contains('幽门');       u['bedside']=N.str.contains('床旁')
u['det']=u['US_detected'].astype(int)
u.to_csv('us_audit3.csv',index=False)

ROWS=[('d3_or_djj','Third portion of duodenum or duodenojejunal junction'),
      ('sma_smv','Superior mesenteric artery–vein relationship'),
      ('inversion','Explicit statement of vessel inversion'),
      ('fluid','Enteric fluid administration recorded'),
      ('dynamic','Dynamic (real-time) assessment'),
      ('compress','Graded compression'),
      ('duodenum','Duodenum mentioned in any form'),
      ('cecum','Caecal position'),
      ('whirl_txt','Whirlpool, swirl or spiral appearance'),
      ('doppler','Colour Doppler used'),
      ('gas_limit','Bowel gas explicitly limiting the study'),
      ('vessel_us','Recorded as abdominal great-vessel study'),
      ('gi_us','Recorded as gastrointestinal ultrasound'),
      ('pyloric','Recorded as pyloric ultrasound'),
      ('bedside','Performed at the bedside')]
e0=u[~u['era_late'].astype(bool)]; e1=u[u['era_late'].astype(bool)]
T3=[['Documented content of the ultrasound examination','n (%) of 119 examinations',
     f'2012–2018 (n={len(e0)}), n','2019–2026 (n={}), n'.format(len(e1)),
     'Detection when documented','Detection when not documented']]
for k,lab in ROWS:
    s=u[k].astype(bool)
    dy=f"{int(u[s]['det'].sum())}/{int(s.sum())}" if s.sum() else '–'
    dn=f"{int(u[~s]['det'].sum())}/{int((~s).sum())}" if (~s).sum() else '–'
    if s.sum()>=10: dy+=f" ({100*u[s]['det'].mean():.0f}%)"
    if (~s).sum()>=10: dn+=f" ({100*u[~s]['det'].mean():.0f}%)"
    T3.append([lab,f"{int(s.sum())} ({100*s.mean():.1f})",str(int(e0[k].sum())),str(int(e1[k].sum())),dy,dn])
json.dump({'T3':T3},open('table3_pooled.json','w'),ensure_ascii=False,indent=1)

print('=== pooled index units: %d ultrasound examinations from %d reports ==='%(len(u),int(u['nrep'].sum())))
for r in T3: print('  '+' | '.join(r))
print()
print('whirlpool text vs adjudicated:'); print(pd.crosstab(u['whirl_txt'],u['US_whirlpool']).to_string())
print()
NAMED=r'肠旋转不良|中肠旋转不良|旋转不良|中肠扭转|肠扭转|肠系膜扭转|小肠扭转'
w=u[u['whirl_txt']]
print('whirlpool documented n=%d ; conclusion names the diagnosis in %d'%(
    len(w),int(w['concl'].astype(str).str.contains(NAMED,regex=True).sum())))
print('detection | whirlpool documented %d/%d ; not documented %d/%d'%(
    int(w['det'].sum()),len(w),int(u[~u['whirl_txt']]['det'].sum()),int((~u['whirl_txt']).sum())))
print()
print('the D3/DJJ examinations:')
for _,r in u[u['d3_or_djj']].iterrows():
    print('  %d detected=%d  %s'%(r['op_year'],r['det'],r['名称'][:50]))
