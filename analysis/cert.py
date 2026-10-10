exec(open('core.py').read())
# The index unit is the pooled examination episode (usaudit4.py): every report of
# the modality issued on the index day. The tier is read from the pooled
# conclusion. Reading only the single closest report (idx_audit.csv, as this
# script once did) picked a negative companion report's conclusion in four
# positive episodes, which then defaulted to "definite".
rep['day']=rep['检查时间'].dt.normalize()
_first=rep.sort_values('gap').groupby(['科研患者编号','mod']).first().reset_index()[['科研患者编号','mod','day']]
_pool=rep.merge(_first,on=['科研患者编号','mod','day'],how='inner')
ix=(_pool.groupby(['科研患者编号','mod']).agg(concl=('concl','\n'.join)).reset_index()
       .merge(long[['科研患者编号','mod','detected']].rename(columns={'detected':'det'}),on=['科研患者编号','mod'],how='inner'))
assert len(ix)==len(long)
POSS=r'可疑|可能|\?|？|不除外|不排除|待排|待除外|建议.{0,10}(除外|排除|进一步)|似'
PROB=r'多考虑|首先考虑|考虑|倾向|符合.{0,6}表现'
def tier(s):
    if re.search(POSS,s): return 'possible'
    if re.search(PROB,s): return 'probable'
    return 'definite'
pos=ix[ix['det']==1].copy()
pos['tier']=pos['concl'].fillna('').astype(str).map(tier)
print('=== certainty tier of POSITIVE index reports (conclusion wording) ===')
ct=pd.crosstab(pos['mod'],pos['tier'])
ct=ct[[c for c in ['definite','probable','possible'] if c in ct]]
print(ct.to_string()); print((ct.div(ct.sum(1),axis=0)*100).round(1).to_string())
print('\ntotal positives',len(pos))
# Would restricting to definite+probable change the ranking?
for mod,tot in ix['mod'].value_counts().reindex(['UGI','CT','US']).items():
    d=pos[pos['mod']==mod]
    strict=(d['tier']!='possible').sum()
    print(f'  {mod}: all-positive {len(d)}/{tot}={len(d)/tot*100:.1f}%   excluding "possible" wording {strict}/{tot}={strict/tot*100:.1f}%')
pos.to_csv('pos_tier.csv',index=False)
