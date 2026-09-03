exec(open('core.py').read())
import re, numpy as np, pandas as pd, statsmodels.api as sm
import statsmodels.formula.api as smf

print('='*70); print('A. Flow: eligible preoperative reports vs index tests')
t=pd.DataFrame({'eligible':rep['mod'].value_counts(),'index':idx['mod'].value_counts()})
t['discarded']=t['eligible']-t['index']; print(t.loc[['UGI','CT','US']]); print('total',t.sum().to_dict())

print('='*70); print('B. Do repeat reports change the patient-level label?')
NAMED=r'肠旋转不良|中肠旋转不良|旋转不良|中肠扭转|肠扭转|肠系膜扭转|小肠扭转'
rep['named']=rep['concl'].astype(str).str.contains(NAMED,regex=True)
idx['named']=idx['concl'].astype(str).str.contains(NAMED,regex=True)
for mod in ['US','CT','UGI']:
    r=rep[rep['mod']==mod]; multi=r.groupby('科研患者编号').size()
    m=set(multi[multi>1].index)
    sub=r[r['科研患者编号'].isin(m)]
    ix=idx[(idx['mod']==mod)&(idx['科研患者编号'].isin(m))].set_index('科研患者编号')['named']
    anyn=sub.groupby('科研患者编号')['named'].any()
    disc=int((anyn & ~ix.reindex(anyn.index).fillna(False)).sum())
    print(f'  {mod}: {len(m)} children with >1 preop report; index negative but another report named it: {disc}')

print('='*70); print('C. Ultrasound content audit: closest-to-operation vs earliest')
u_first=rep[rep['mod']=='US'].sort_values('gap',ascending=False).groupby('科研患者编号').first().reset_index()
def content(d):
    T=d['txt'].astype(str)
    f=lambda rx:T.str.contains(rx,regex=True)
    return {'D3 or DJJ':f(r'十二指肠水平部|十二指肠水平段|十二指肠横部|十二指肠第三段|(?<![弓])横部|水平部|十二指肠空肠曲|屈氏|Treitz|十二指肠悬韧带').sum(),
            'SMA-SMV':f(r'肠系膜上动脉|肠系膜上静脉|系膜血管|SMA|SMV').sum(),
            'fluid':f(r'饮水|口服[^。；\n]{0,6}(?:水|液|造影剂)|注水|注入|胃内注|温开水|经胃管').sum(),
            'whirl_txt':f(r'漩涡|旋涡|涡流|螺旋').sum(),
            'n':len(d)}
print('  closest :',content(idx[idx['mod']=='US']))
print('  earliest:',content(u_first))

print('='*70); print('D. Ultrasound examination-item overlap')
u=idx[idx['mod']=='US'].copy(); N=u['报告名称'].astype(str)
u['gi']=N.str.contains('胃肠道'); u['ves']=N.str.contains('腹部大血管'); u['pyl']=N.str.contains('幽门')
print('  gastrointestinal',int(u['gi'].sum()),' great-vessel',int(u['ves'].sum()),' pyloric',int(u['pyl'].sum()))
print('  gi & vessel',int((u['gi']&u['ves']).sum()),' pyloric only',int((u['pyl']&~u['gi']&~u['ves']).sum()))
print('  none of the three',int((~u['gi']&~u['ves']&~u['pyl']).sum()))

print('='*70); print('E. Era cut point sensitivity (ultrasound)')
us=idx[idx['mod']=='US'][['科研患者编号','报告名称','检查时间']].merge(
    mat[['科研患者编号','US_detected']],on='科研患者编号',how='left').merge(
    pat[['科研患者编号','op_year']],on='科研患者编号',how='left')
us['ves']=us['报告名称'].astype(str).str.contains('腹部大血管').astype(int)
us['det']=us['US_detected'].astype(int)
for cut in [2019,2020,2021,2022]:
    us['late']=(us['op_year']>=cut).astype(int)
    a=us[us['late']==0]; b=us[us['late']==1]
    m1=smf.logit('det ~ late',data=us).fit(disp=0)
    m2=smf.logit('det ~ late + ves',data=us).fit(disp=0)
    or1=np.exp(m1.params['late']); ci1=np.exp(m1.conf_int().loc['late'])
    or2=np.exp(m2.params['late']); ci2=np.exp(m2.conf_int().loc['late'])
    orv=np.exp(m2.params['ves']); civ=np.exp(m2.conf_int().loc['ves'])
    print(f'  cut {cut}: n {len(a)}/{len(b)}  det {100*a["det"].mean():.1f}%/{100*b["det"].mean():.1f}%  '
          f'era OR {or1:.2f} ({ci1[0]:.2f}-{ci1[1]:.2f}) p={m1.pvalues["late"]:.3f}  '
          f'-> adj {or2:.2f} ({ci2[0]:.2f}-{ci2[1]:.2f}) p={m2.pvalues["late"]:.3f}  '
          f'vessel OR {orv:.2f} ({civ[0]:.2f}-{civ[1]:.2f}) p={m2.pvalues["ves"]:.4f}')

print('='*70); print('F. Marginal (risk-difference) version of the ultrasound era model')
us['late']=(us['op_year']>=2019).astype(int)
m2=smf.logit('det ~ late + ves',data=us).fit(disp=0)
d0=us.copy(); d0['late']=0; d1=us.copy(); d1['late']=1
rd=(m2.predict(d1).mean()-m2.predict(d0).mean())
m1=smf.logit('det ~ late',data=us).fit(disp=0)
e0=us.copy(); e0['late']=0; e1=us.copy(); e1['late']=1
rd_un=(m1.predict(e1).mean()-m1.predict(e0).mean())
print(f'  unadjusted average marginal effect of later era: {100*rd_un:+.1f} percentage points')
print(f'  adjusted for great-vessel coding:                {100*rd:+.1f} percentage points')

print('='*70); print('G. Volvulus definition sensitivity')
print('  volvulus (as used):',int(pat['volvulus'].sum()),'/',len(pat))
print('  explicit 扭转 wording only:',int(pat['volv_rule'].sum()))
print('  rotation degree documented:',int(pat['rot_deg'].notna().sum()))
print(pat['rot_deg'].value_counts().sort_index().to_string())
strict=pat['intraop_volvulus'].fillna(False).astype(bool)
print('  adjudicated intraop_volvulus non-missing:',int(pat['intraop_volvulus'].notna().sum()))
deg=pat['rot_deg']
byrule_only = pat['volvulus'] & ~pat['intraop_volvulus'].fillna(False).astype(bool)
print('  positive by keyword rule where adjudication absent/negative:',int(byrule_only.sum()))
lt360 = pat['volvulus'] & pat['rot_deg'].notna() & (pat['rot_deg']<360)
print('  volvulus-positive with a documented rotation <360 deg:',int(lt360.sum()))
