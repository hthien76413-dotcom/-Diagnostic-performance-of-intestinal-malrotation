exec(open('core.py').read())
noimg=sorted(ids-set(mat['科研患者编号']))
xr = x.parse('X线报告'); xr['检查时间']=pd.to_datetime(xr['检查时间'],errors='coerce')
usall=x.parse('超声报告').rename(columns={'超声检查时间':'检查时间','超声报告名称':'报告名称'}); usall['检查时间']=pd.to_datetime(usall['检查时间'],errors='coerce')
ctall=x.parse('CT报告'); ctall['检查时间']=pd.to_datetime(ctall['检查时间'],errors='coerce')
def preop(d):
    d=d[d['科研患者编号'].isin(ids)].merge(coh[['科研患者编号','op_dt']],on='科研患者编号',how='left')
    return d[d['检查时间'].dt.normalize()<=d['op_dt'].dt.normalize()]
xr,usall,ctall=preop(xr),preop(usall),preop(ctall)
S=set(noimg)
enema=set(xr[xr['报告名称'].astype(str).str.contains('灌肠')]['科研患者编号'])&S
plain=set(xr[~xr['报告名称'].astype(str).str.contains('造影|灌肠')]['科研患者编号'])&S
otherus=set(usall['科研患者编号'])&S; otherct=set(ctall['科研患者编号'])&S
none_=S-(enema|plain|otherus|otherct)
print('55 breakdown (non-mutually-exclusive): plain film %d, contrast enema %d, other-region US %d, other-region CT %d, none in-hospital %d'%(len(plain),len(enema),len(otherus),len(otherct),len(none_)))
# hierarchy
h_enema=enema; h_plain=plain-enema; h_us=otherus-enema-plain; h_ct=otherct-enema-plain-otherus
print('hierarchical: enema %d | plain-only(+US/CT other) %d | US-only %d | CT-only %d | none %d'%(len(h_enema),len(h_plain),len(h_us),len(h_ct),len(none_)))
adm=pd.concat([x.parse('儿科入院记录'),x.parse('新生儿科入院记录')],ignore_index=True)
adm=adm[adm['科研患者编号'].isin(S)]
col='门诊及院外重要辅助检查'; adm[col]=adm[col].fillna('').astype(str)
adm['hist']=adm['现病史'].fillna('').astype(str)
def outside(g):
    t=' '.join(g[col])+' '+' '.join(g['hist'])
    return bool(re.search(r'(造影|彩超|超声|B超|CT|X线|拍片|平片)',t))
def outside_mal(g):
    t=' '.join(g[col])+' '+' '.join(g['hist'])
    return bool(re.search(r'(旋转不良|肠扭转|中肠扭转|扭转)',t)) and bool(re.search(r'(造影|彩超|超声|B超|CT)',t))
o=adm.groupby('科研患者编号').apply(outside,include_groups=False); om=adm.groupby('科研患者编号').apply(outside_mal,include_groups=False)
print('with admission note: %d; documenting prior/outside imaging: %d; that imaging reported malrotation/volvulus: %d'%(len(o),o.sum(),om.sum()))
print('the %d with no in-hospital preop imaging:'%len(none_), sorted(none_))
sub=adm[adm['科研患者编号'].isin(none_)]
for pid,g in sub.groupby('科研患者编号'):
    print(' *',pid,(' '.join(g[col])+' | '+' '.join(g['hist']))[:200].replace('\n',' '))
# indication proxies: bilious vomiting etc among 55 vs 410
