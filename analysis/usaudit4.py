# -*- coding: utf-8 -*-
"""Ultrasound report-content audit (definitive).

Two corrections over usaudit2.py:
  * Index unit = the examination EPISODE closest to operation. All reports of the
    modality issued on that calendar day are pooled, because the department
    routinely issues separate reports for the gastrointestinal and the
    great-vessel study of one session; taking a single report could select the
    negative companion report of a positive session.
  * Patterns are clause-aware where the element is a FINDING (whirlpool, study
    adequacy) and mention-level where it is a TECHNIQUE element (an examination
    that states the vessel relationship is normal did address the vessels).
"""
exec(open('core.py').read())
import re, json, numpy as np, pandas as pd

rep['day']=rep['检查时间'].dt.normalize()
first=rep.sort_values('gap').groupby(['科研患者编号','mod']).first().reset_index()[['科研患者编号','mod','day']]
pool=rep.merge(first,on=['科研患者编号','mod','day'],how='inner')
IX=pool.groupby(['科研患者编号','mod']).agg(txt=('txt','\n'.join),concl=('concl','\n'.join),
        名称=('报告名称',lambda s:' | '.join(sorted(set(s)))),nrep=('txt','size'),
        检查时间=('检查时间','min')).reset_index()

u=IX[IX['mod']=='US'].merge(mat[['科研患者编号','US_detected','US_whirlpool']],on='科研患者编号',how='left') \
                     .merge(pat[['科研患者编号','era_late','op_year','volvulus']],on='科研患者编号',how='left')
T=u['txt'].astype(str); N=u['名称'].astype(str)
f=lambda rx: T.str.contains(rx,regex=True)
CLAUSE=r'[。；;\n]+'
def clause_both(a,b):
    return T.map(lambda t: any(re.search(a,c) and re.search(b,c) for c in re.split(CLAUSE,t)))
NEG=r'未见|未探及|未显示|未发现|无明显|不明显|未闻'
def reported(rx):
    """True if the pattern occurs at least once without a negation in the 12
    characters preceding it within the same clause (Chinese negation precedes)."""
    def g(t):
        for c in re.split(CLAUSE,str(t)):
            for m in re.finditer(rx,c):
                if not re.search(NEG,c[max(0,m.start()-12):m.start()]): return True
        return False
    return T.map(g)

VESSEL = r'肠系膜上动、?静脉|肠系膜上动静脉|肠系膜上动脉|肠系膜上静脉|肠系膜血管|系膜血管|SMA|SMV'
RENAL  = r'左肾静脉|胡桃夹|肾静脉受压'
GAS    = r'肠气|积气|气体干扰|气体遮挡|气体遮盖|气体较多|气强反射|充满气体'
LIMIT  = r'干扰|遮挡|遮盖|显示不清|显示欠清|探及?不满意|不满意'
WHIRL  = r'漩涡|旋涡|涡流|螺旋'

u['d3']       = f(r'十二指肠水平部|十二指肠水平段|十二指肠横部|十二指肠第三段|(?<![弓])横部|水平部')
u['djj']      = f(r'十二指肠空肠曲|屈氏|Treitz|十二指肠悬韧带|十二指肠[-—与和]?空肠交界')
u['d3_or_djj']= u['d3']|u['djj']
u['duodenum'] = f(r'十二指肠')
u['sma_smv']  = f(VESSEL) & ~(f(RENAL) & ~f(WHIRL))
u['inversion']= f(r'(?:静脉|动脉)[^。；\n]{0,10}(?:换位|反位|倒置|关系异常|异常关系)|静脉位于[^。；\n]{0,8}左|动脉位于[^。；\n]{0,8}右')
u['fluid']    = f(r'饮水|口服[^。；\n]{0,6}(?:水|液|造影剂)|注水|注入|胃内注|温开水|经胃管')
u['dynamic']  = f(r'动态|实时观察|连续观察')
u['compress'] = f(r'加压|探头压|压迫探查')
u['whirl_any']= f(WHIRL)
u['whirl_pos']= reported(WHIRL)
u['gas_limit']= clause_both(GAS,LIMIT)
u['cecum']    = f(r'回盲')
u['doppler']  = f(r'CDFI|彩色多普勒|多普勒')
u['vessel_us']= N.str.contains('腹部大血管'); u['gi_us']=N.str.contains('胃肠道')
u['pyloric']  = N.str.contains('幽门');       u['bedside']=N.str.contains('床旁')
u['det']=u['US_detected'].astype(int); u['late']=u['era_late'].astype(int)
u.to_csv('us_audit4.csv',index=False)

ROWS=[('d3_or_djj','Third portion of duodenum or duodenojejunal junction'),
      ('duodenum','Duodenum mentioned in any form'),
      ('sma_smv','Superior mesenteric artery–vein relationship'),
      ('inversion','Explicit statement of vessel inversion'),
      ('fluid','Enteric fluid administration recorded'),
      ('dynamic','Dynamic (real-time) assessment'),
      ('compress','Graded compression'),
      ('cecum','Caecal position'),
      ('doppler','Colour Doppler used'),
      ('whirl_pos','Whirlpool, swirl or spiral appearance reported'),
      ('gas_limit','Bowel gas explicitly limiting the study'),
      ('vessel_us','Booked as abdominal great-vessel study'),
      ('gi_us','Booked as gastrointestinal ultrasound'),
      ('pyloric','Booked as pyloric ultrasound'),
      ('bedside','Performed at the bedside')]
e0=u[u['late']==0]; e1=u[u['late']==1]
T3=[['Documented content of the ultrasound examination',f'n (%) of {len(u)}',
     f'2012–2018 (n={len(e0)})',f'2019–2026 (n={len(e1)})',
     'Detection when documented','Detection when not documented']]
def cell(d):
    if len(d)==0: return '–'
    s=f"{int(d['det'].sum())}/{len(d)}"
    return s+f" ({100*d['det'].mean():.0f}%)" if len(d)>=10 else s
for k,lab in ROWS:
    s=u[k].astype(bool)
    T3.append([lab,f"{int(s.sum())} ({100*s.mean():.1f})",str(int(e0[k].sum())),str(int(e1[k].sum())),
               cell(u[s]),cell(u[~s])])
json.dump({'T3':T3},open('table3_final.json','w'),ensure_ascii=False,indent=1)
for r in T3: print(' | '.join(r))

print()
NAMED=r'肠旋转不良|中肠旋转不良|旋转不良|中肠扭转|肠扭转|肠系膜扭转|小肠扭转'
w=u[u['whirl_pos']]
print('whirlpool reported n=%d; conclusion names malrotation/volvulus in %d'%(
      len(w),int(w['concl'].astype(str).str.contains(NAMED,regex=True).sum())))
print('agreement with adjudicated whirlpool variable: %d/%d'%(
      int((u['whirl_pos']==(u['US_whirlpool']==1)).sum()),len(u)))
v=u[u['volvulus'].astype(bool)]
print('whirlpool reported among %d children with operative volvulus: %d (%.1f%%)'%(
      len(v),int(v['whirl_pos'].sum()),100*v['whirl_pos'].mean()))
print('exam items: vessel %d, gastrointestinal %d, pyloric %d, both GI+vessel %d'%(
      int(u['vessel_us'].sum()),int(u['gi_us'].sum()),int(u['pyloric'].sum()),
      int((u['vessel_us']&u['gi_us']).sum())))
