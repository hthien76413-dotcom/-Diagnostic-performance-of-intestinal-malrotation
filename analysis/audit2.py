exec(open('core.py').read())
ix=idx.merge(mat,on='科研患者编号',how='left').merge(pat[['科研患者编号','era_late','op_year','volvulus','neonate']],on='科研患者编号',how='left')
ix['det']=np.where(ix['mod']=='US',ix['US_detected'],np.where(ix['mod']=='CT',ix['CT_detected'],ix['UGI_detected']))
def f(d,rx): return d['txt'].str.contains(rx,regex=True)
# ---- CT ----
c=ix[ix['mod']=='CT'].copy()
c['enhanced']=c['报告名称'].astype(str).str.contains('增强')
c['whirl']=f(c,r'漩涡|旋涡|涡流|螺旋')
c['duod']=f(c,r'十二指肠')
c['sma_smv']=f(c,r'肠系膜上动脉|肠系膜上静脉|系膜血管')
c['recon3d']=c['报告名称'].astype(str).str.contains('三维重建')
print('=== CT audit n=%d ==='%len(c))
for k in ['enhanced','whirl','duod','sma_smv','recon3d']:
    print(f'  {k:9s} {c[k].sum():4d} ({c[k].mean()*100:5.1f}%)  det|yes {c[c[k]]["det"].mean()*100:5.1f}%  det|no {c[~c[k]]["det"].mean()*100:5.1f}%')
print('  enhanced n=%d det %.1f%% | unenhanced n=%d det %.1f%%'%(c['enhanced'].sum(),c[c['enhanced']]['det'].mean()*100,(~c['enhanced']).sum(),c[~c['enhanced']]['det'].mean()*100))
print('  enhanced share by era: early %.1f%% late %.1f%%'%(c[~c['era_late']]['enhanced'].mean()*100,c[c['era_late']]['enhanced'].mean()*100))
# ---- UGI ----
g=ix[ix['mod']=='UGI'].copy()
g['full']=g['报告名称'].astype(str).str.contains('全消化道')
g['upper']=g['报告名称'].astype(str).str.contains('上消化道')
g['barium']=g['报告名称'].astype(str).str.contains('钡')
g['djj']=f(g,r'十二指肠空肠曲|屈氏|Treitz|十二指肠.{0,6}空肠')
g['corkscrew']=f(g,r'弹簧|螺旋|绞索|corkscrew|盘曲')
g['jej_pos']=f(g,r'空肠.{0,10}(位于|居|偏)')
g['cecum']=f(g,r'回盲部')
print('\n=== UGI audit n=%d ==='%len(g))
for k in ['full','upper','barium','djj','corkscrew','jej_pos','cecum']:
    print(f'  {k:10s} {g[k].sum():4d} ({g[k].mean()*100:5.1f}%)  det|yes {g[g[k]]["det"].mean()*100:5.1f}%  det|no {g[~g[k]]["det"].mean()*100:5.1f}%')
# ---- equivocal phrasing ----
EQ=r'可疑|可能|多考虑|考虑|首先考虑|不除外|不排除|待排|待除外|建议.{0,8}除外|？|\?'
POSK=r'旋转不良|中肠扭转|肠扭转|漩涡|旋涡|弹簧征|螺旋征'
print('\n=== equivocal (hedged) phrasing in the CONCLUSION of positive index reports ===')
for mod in ['UGI','CT','US']:
    d=ix[(ix['mod']==mod)&(ix['det']==1)].copy()
    hedge=d['concl'].str.contains(EQ,regex=True)
    definite=~hedge
    print(f'  {mod:4s} positive n={len(d):3d}: hedged {hedge.sum():3d} ({hedge.mean()*100:.1f}%)  unhedged {definite.sum():3d} ({definite.mean()*100:.1f}%)')
print('\n=== conclusion mentions malrotation keyword at all, by modality/label ===')
for mod in ['UGI','CT','US']:
    d=ix[ix['mod']==mod]
    kw=d['concl'].str.contains(POSK,regex=True)
    print(f'  {mod:4s} n={len(d):3d} concl-keyword {kw.sum():3d}; det={int(d["det"].sum())}; keyword&det {int((kw&(d["det"]==1)).sum())}; keyword&~det {int((kw&(d["det"]==0)).sum())}')
ix.to_csv('idx_audit.csv',index=False)
