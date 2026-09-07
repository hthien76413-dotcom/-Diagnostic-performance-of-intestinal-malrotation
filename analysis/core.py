import pandas as pd, numpy as np, re, warnings
warnings.filterwarnings('ignore')
BASE='/home/user/-Diagnostic-performance-of-intestinal-malrotation/'
x = pd.ExcelFile(BASE+'全部肠旋转不良数据.xlsx')
coh = pd.read_excel(BASE+'诊断效能_手术确诊队列_465例.xlsx', sheet_name='患者队列_465例')
ops = pd.read_excel(BASE+'诊断效能_手术确诊队列_465例.xlsx', sheet_name='手术记录明细_503条')
mat = pd.read_excel(BASE+'诊断效能_逐患者矩阵_当前版v3.xlsx')
# Corrections agreed after the two-directional label audit (labelaudit.py).
# The raw export is left untouched; every correction is listed, with its reason,
# in label_corrections.csv, and each was checked against the source reports.
_fix = pd.read_csv('label_corrections.csv')
for _r in _fix.itertuples():
    _m = mat['科研患者编号'] == _r.科研患者编号
    assert _m.sum() == 1 and mat.loc[_m, _r.column].iloc[0] == _r.old, \
        f'label_corrections.csv no longer matches the matrix at {_r.科研患者编号}'
    mat.loc[_m, _r.column] = _r.new
coh['op_dt']=pd.to_datetime(coh['首次手术日期及时间']); ids=set(coh['科研患者编号'])
ops['op_dt']=pd.to_datetime(ops['手术日期及时间'])
ops['dx']=ops['术中诊断'].fillna('').astype(str); ops['pr']=ops['手术经过'].fillna('').astype(str)
first_op = ops.sort_values('op_dt').groupby('科研患者编号').first().reset_index()
visits = x.parse('患者就诊信息')[['科研患者编号','科研就诊编号','年龄（岁）','入院时间','入院科室']].drop_duplicates(['科研患者编号','科研就诊编号'])
sexdf  = x.parse('病案首页基本信息')[['科研患者编号','性别']].drop_duplicates('科研患者编号')
pat = first_op[['科研患者编号','科研就诊编号','op_dt']].merge(visits,on=['科研患者编号','科研就诊编号'],how='left').merge(sexdf,on='科研患者编号',how='left')
pat = pat[pat['科研患者编号'].isin(ids)].drop_duplicates('科研患者编号').reset_index(drop=True)
pat['adm']=pd.to_datetime(pat['入院时间'])
pat['age_days']=pat['年龄（岁）']*365 + (pat['op_dt']-pat['adm']).dt.total_seconds()/86400
pat['neonate']=pat['age_days']<=28
pat['infant']=pat['age_days']<=365
pat['male']=pat['性别'].astype(str).str.contains('男')
pat['era_late']=pat['op_dt'].dt.year>=2019
pat['op_year']=pat['op_dt'].dt.year
# volvulus: adjudicated matrix where available, keyword rule otherwise
EXC=r'(?:胃|睾丸|卵巢|附件|大网膜|精索|阑尾)扭转'
def vrule(g):
    t=re.sub(EXC,'',' '.join(g['dx'])+' || '+' '.join(g['pr']))
    return ('扭转' in t) or bool(re.search(r'旋转[^。；;]{0,8}\d+\s*[°度]',t))
vk=ops[ops['科研患者编号'].isin(ids)].groupby('科研患者编号').apply(vrule,include_groups=False).rename('volv_rule')
pat=pat.merge(vk,on='科研患者编号',how='left').merge(mat[['科研患者编号','intraop_volvulus']],on='科研患者编号',how='left')
pat['volvulus']=pat['intraop_volvulus'].fillna(pat['volv_rule']).astype(bool)
# degree of rotation
def deg(g):
    t=' '.join(g['dx'])+' '+' '.join(g['pr'])
    d=[int(v) for v in re.findall(r'旋转[^。；;]{0,8}?(\d{2,4})\s*[°度]',t)]
    return max(d) if d else np.nan
pat=pat.merge(ops[ops['科研患者编号'].isin(ids)].groupby('科研患者编号').apply(deg,include_groups=False).rename('rot_deg'),on='科研患者编号',how='left')

# ---- index-test reports ----
us = x.parse('超声报告').rename(columns={'超声报告名称':'报告名称','超声检查时间':'检查时间','超声检查所见':'检查所见','超声检查结论':'检查结论'})
xr = x.parse('X线报告'); ctr = x.parse('CT报告')
for d in (us,xr,ctr): d['检查时间']=pd.to_datetime(d['检查时间'],errors='coerce')
sel={'US':lambda n:('胃肠道' in n) or ('腹部大血管' in n) or ('幽门' in n),
     'UGI':lambda n:('造影' in n) and ('消化道' in n),
     'CT':lambda n:('CT' in n) and any(k in n for k in ['腹盆','腹部','上腹','下腹','全腹'])}
def prep(df,mod):
    d=df[df['报告名称'].astype(str).map(sel[mod])].copy(); d['mod']=mod
    d=d[d['科研患者编号'].isin(ids)].merge(coh[['科研患者编号','op_dt']],on='科研患者编号',how='left')
    d=d[d['检查时间'].notna() & (d['检查时间'].dt.normalize()<=d['op_dt'].dt.normalize())]
    return d[['科研患者编号','mod','报告名称','检查时间','检查所见','检查结论','op_dt']]
rep=pd.concat([prep(us,'US'),prep(xr,'UGI'),prep(ctr,'CT')],ignore_index=True)
rep=rep.drop_duplicates(subset=['科研患者编号','mod','检查时间','报告名称','检查结论'])
rep['txt']=(rep['检查所见'].fillna('')+'\n'+rep['检查结论'].fillna('')).astype(str)
rep['concl']=rep['检查结论'].fillna('').astype(str)
# index test = closest preoperative exam per modality
rep['gap']=(rep['op_dt']-rep['检查时间']).dt.total_seconds()/86400
idx=rep.sort_values('gap').groupby(['科研患者编号','mod']).first().reset_index()
# long-format detection from adjudicated matrix
lab={'US':'US_detected','CT':'CT_detected','UGI':'UGI_detected'}
long=[]
for mod,c in lab.items():
    s=mat[mat[c].notna()][['科研患者编号',c]].rename(columns={c:'detected'}); s['mod']=mod; long.append(s)
long=pd.concat(long,ignore_index=True)
long=long.merge(pat[['科研患者编号','neonate','era_late','volvulus','age_days','male','op_year']],on='科研患者编号',how='left')
long['detected']=long['detected'].astype(int)
