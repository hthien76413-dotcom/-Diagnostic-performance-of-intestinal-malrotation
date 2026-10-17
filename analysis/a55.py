exec(open('core.py').read())
noimg=sorted(ids-set(mat['科研患者编号']))
print('N no index imaging:',len(noimg))
p55=pat[pat['科研患者编号'].isin(noimg)]
p410=pat[~pat['科研患者编号'].isin(noimg)]
def desc(d,lab):
    print(f'{lab:8s} n={len(d):3d} age_med={d["age_days"].median():7.1f}d neonate={d["neonate"].sum():3d}({d["neonate"].mean()*100:.0f}%) male={d["male"].mean()*100:.0f}% volv={d["volvulus"].mean()*100:.0f}% lateEra={d["era_late"].mean()*100:.0f}%')
desc(p55,'no-index'); desc(p410,'imaged')
# plain radiographs preop
xr = x.parse('X线报告'); xr['检查时间']=pd.to_datetime(xr['检查时间'],errors='coerce')
xr=xr[xr['科研患者编号'].isin(ids)].merge(coh[['科研患者编号','op_dt']],on='科研患者编号',how='left')
xr=xr[xr['检查时间'].dt.normalize()<=xr['op_dt'].dt.normalize()]
plain=xr[~xr['报告名称'].astype(str).str.contains('造影|灌肠')]
abd = plain[plain['报告名称'].astype(str).str.contains('腹')]
print('\n--- among the no-index 55 ---')
print('any preop plain radiograph:',plain[plain['科研患者编号'].isin(noimg)]['科研患者编号'].nunique())
print('abdominal-containing plain film:',abd[abd['科研患者编号'].isin(noimg)]['科研患者编号'].nunique())
print('contrast enema only:',xr[xr['报告名称'].astype(str).str.contains('灌肠')&xr['科研患者编号'].isin(noimg)]['科研患者编号'].nunique())
# any US or CT of any type preop
usall=x.parse('超声报告').rename(columns={'超声检查时间':'检查时间','超声报告名称':'报告名称'}); usall['检查时间']=pd.to_datetime(usall['检查时间'],errors='coerce')
ctall=x.parse('CT报告'); ctall['检查时间']=pd.to_datetime(ctall['检查时间'],errors='coerce')
for nm,d in [('any US',usall),('any CT',ctall)]:
    d=d[d['科研患者编号'].isin(ids)].merge(coh[['科研患者编号','op_dt']],on='科研患者编号',how='left')
    d=d[d['检查时间'].dt.normalize()<=d['op_dt'].dt.normalize()]
    print(f'{nm} (any type) among 55:',d[d['科研患者编号'].isin(noimg)]['科研患者编号'].nunique())
# combined: any preop imaging of any kind
anyimg=set(plain['科研患者编号'])|set(xr['科研患者编号'])
u=usall[usall['科研患者编号'].isin(ids)].merge(coh[['科研患者编号','op_dt']],on='科研患者编号',how='left'); u=u[u['检查时间'].dt.normalize()<=u['op_dt'].dt.normalize()]
c=ctall[ctall['科研患者编号'].isin(ids)].merge(coh[['科研患者编号','op_dt']],on='科研患者编号',how='left'); c=c[c['检查时间'].dt.normalize()<=c['op_dt'].dt.normalize()]
anyimg|=set(u['科研患者编号'])|set(c['科研患者编号'])
print('\nno-index children with NO preoperative imaging of ANY kind:',len(set(noimg)-anyimg))
print('no-index children WITH some preoperative imaging:',len(set(noimg)&anyimg))
# what type of plain film
print('\nplain film names among 55:')
print(plain[plain['科研患者编号'].isin(noimg)]['报告名称'].astype(str).str.replace('\n','').value_counts().head(12).to_string())
# outside-hospital imaging mention
adm_recs=pd.concat([x.parse('儿科入院记录'),x.parse('新生儿科入院记录')],ignore_index=True)
adm_recs=adm_recs[adm_recs['科研患者编号'].isin(noimg)]
col='门诊及院外重要辅助检查'
t=adm_recs[col].fillna('').astype(str)
kw=t.str.contains('造影|超声|彩超|CT|B超|X线|片')
print('\nno-index children whose admission note documents outside/outpatient imaging:',adm_recs[kw]['科研患者编号'].nunique(),'of',adm_recs['科研患者编号'].nunique(),'with admission notes')
for s in t[kw].head(4): print('   *',s[:160].replace('\n',' '))
