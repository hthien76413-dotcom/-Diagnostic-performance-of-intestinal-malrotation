exec(open('core.py').read())
ix=pd.read_csv('idx_audit.csv')
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
for mod,tot in [('UGI',301),('CT',320),('US',119)]:
    d=pos[pos['mod']==mod]
    strict=(d['tier']!='possible').sum()
    print(f'  {mod}: all-positive {len(d)}/{tot}={len(d)/tot*100:.1f}%   excluding "possible" wording {strict}/{tot}={strict/tot*100:.1f}%')
pos.to_csv('pos_tier.csv',index=False)
