exec(open('core.py').read())
ix=pd.read_csv('ix_full.csv')
ix['检查时间']=pd.to_datetime(ix['检查时间'])
multi=ix[ix.groupby('科研患者编号')['mod'].transform('size')>1]
o=multi.sort_values('检查时间').groupby('科研患者编号')['mod'].apply(list)
print('patients with >1 modality:',len(o))
print('first modality:',pd.Series([v[0] for v in o]).value_counts().to_dict())
print('last  modality:',pd.Series([v[-1] for v in o]).value_counts().to_dict())
print()
# position of each modality relative to operation
print('=== gap from examination to operation (days), by modality ===')
for mod in ['UGI','CT','US']:
    d=ix[ix['mod']==mod]['gap']
    print(f'  {mod:4s} median {d.median():.2f} (IQR {d.quantile(.25):.2f}-{d.quantile(.75):.2f}); same-day {int((d<1).sum())} ({(d<1).mean()*100:.0f}%)')
print()
# is it the LAST test before surgery?
lastmod=multi.sort_values('检查时间').groupby('科研患者编号')['mod'].last()
det=multi.set_index(['科研患者编号','mod'])['det']
rows=[]
for mod in ['UGI','CT','US']:
    d=multi[multi['mod']==mod].merge(lastmod.rename('lastmod'),on='科研患者编号')
    isl=d['mod']==d['lastmod']
    rows.append((mod,int(isl.sum()),len(d),d[isl]['det'].mean()*100,d[~isl]['det'].mean()*100))
print('=== detection when the modality was the LAST preoperative test vs earlier ===')
for r in rows: print('  %-4s last in %d/%d (%.0f%%): detection %.1f%% when last vs %.1f%% when earlier'%(r[0],r[1],r[2],r[1]/r[2]*100,r[3],r[4]))
print()
# US as first-line
usp=set(ix[ix['mod']=='US']['科研患者编号'])
o2=ix.sort_values('检查时间').groupby('科研患者编号')['mod'].apply(list)
usfirst=sum(1 for p,v in o2.items() if p in usp and v[0]=='US')
print('ultrasound was the FIRST index test in %d/%d (%.0f%%) of children who had one'%(usfirst,len(usp),usfirst/len(usp)*100))
# by era
late=set(pat[pat['era_late']]['科研患者编号'])
for lab,S in [('2012-2018',set(pat[~pat['era_late']]['科研患者编号'])),('2019-2026',late)]:
    sub=[p for p in usp if p in S]
    k=sum(1 for p in sub if o2[p][0]=='US')
    print(f'   {lab}: {k}/{len(sub)} ({k/len(sub)*100:.0f}%)')
