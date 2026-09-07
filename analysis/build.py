import pandas as pd, numpy as np, re
BASE='/home/user/-Diagnostic-performance-of-intestinal-malrotation/'
x = pd.ExcelFile(BASE+'全部肠旋转不良数据.xlsx')
coh = pd.read_excel(BASE+'诊断效能_手术确诊队列_465例.xlsx', sheet_name='患者队列_465例')
ops = pd.read_excel(BASE+'诊断效能_手术确诊队列_465例.xlsx', sheet_name='手术记录明细_503条')
coh['op_dt']=pd.to_datetime(coh['首次手术日期及时间'])
ids=set(coh['科研患者编号'])
ops['op_dt']=pd.to_datetime(ops['手术日期及时间'])
# visit id of first operation
first_op = ops.sort_values('op_dt').groupby('科研患者编号').first().reset_index()[['科研患者编号','科研就诊编号','op_dt','术中诊断','手术经过']]
visits = x.parse('患者就诊信息')
pat = first_op.merge(visits[['科研患者编号','科研就诊编号','年龄（岁）','入院时间','入院科室']],on=['科研患者编号','科研就诊编号'],how='left')
base = x.parse('病案首页基本信息')[['科研患者编号','科研就诊编号','性别']].drop_duplicates()
pat = pat.merge(base,on=['科研患者编号','科研就诊编号'],how='left')
pat = pat[pat['科研患者编号'].isin(ids)].drop_duplicates('科研患者编号')
pat['age_days']=pat['年龄（岁）']*365
pat['neonate']=pat['age_days']<=28
pat['male']=pat['性别'].astype(str).str.contains('男')
pat['era']=np.where(pat['op_dt'].dt.year<=2018,'2012-2018','2019-2026')
pat['op_year']=pat['op_dt'].dt.year
