exec(open('core.py').read())
adm=pd.concat([x.parse('儿科入院记录'),x.parse('新生儿科入院记录')],ignore_index=True)
adm=adm[adm['科研患者编号'].isin(ids)]
for c in ['主诉','现病史','体格检查','初步诊断','病史小结']:
    if c in adm: adm[c]=adm[c].fillna('').astype(str)
    else: adm[c]=''
adm['all']=adm['主诉']+' '+adm['现病史']+' '+adm['病史小结']+' '+adm['初步诊断']
g=adm.groupby('科研患者编号')['all'].apply(lambda s:' '.join(s))
def has(pat_,s): return s.str.contains(pat_,regex=True)
feat=pd.DataFrame({'科研患者编号':g.index})
S=g.values
import numpy as np
def flag(rx): return pd.Series(S).str.contains(rx,regex=True).values
feat['vomit']=flag(r'呕吐|吐奶|呕奶')
feat['bilious']=flag(r'胆汁|黄绿|绿色液|草绿')
feat['bloody_stool']=flag(r'血便|便血|果酱')
feat['distension']=flag(r'腹胀')
feat['abd_pain']=flag(r'腹痛')
feat['poor_feed']=flag(r'拒奶|纳差|喂养困难')
feat['shock']=flag(r'休克|循环衰竭|面色苍白|皮肤花纹')
feat['duration_chronic']=flag(r'反复|间断|间歇|数月|年余|余月')
pat2=pat.merge(feat,on='科研患者编号',how='left')
for c in feat.columns[1:]: pat2[c]=pat2[c].fillna(False)
pat2['has_note']=pat2['科研患者编号'].isin(g.index)
print('with admission note:',pat2['has_note'].sum(),'of',len(pat2))
groups={'UGI':set(mat[mat['UGI_detected'].notna()]['科研患者编号']),
        'CT':set(mat[mat['CT_detected'].notna()]['科研患者编号']),
        'US':set(mat[mat['US_detected'].notna()]['科研患者编号']),
        'none':ids-set(mat['科研患者编号'])}
rows=[]
for k,s in groups.items():
    d=pat2[pat2['科研患者编号'].isin(s)]
    rows.append(dict(group=k,n=len(d),
      age_med=round(d['age_days'].median(),1),
      age_iqr=f"{d['age_days'].quantile(.25):.1f}-{d['age_days'].quantile(.75):.1f}",
      neonate=f"{d['neonate'].sum()} ({d['neonate'].mean()*100:.1f}%)",
      infant=f"{d['infant'].sum()} ({d['infant'].mean()*100:.1f}%)",
      male=f"{d['male'].sum()} ({d['male'].mean()*100:.1f}%)",
      volvulus=f"{d['volvulus'].sum()} ({d['volvulus'].mean()*100:.1f}%)",
      late_era=f"{d['era_late'].sum()} ({d['era_late'].mean()*100:.1f}%)",
      **{c:f"{d[c].sum()} ({d[c].mean()*100:.1f}%)" for c in ['vomit','bilious','bloody_stool','distension','abd_pain','shock','duration_chronic']}))
t=pd.DataFrame(rows).set_index('group').T
print(t.to_string())
t.to_csv('tab_bygroup.csv')
pat2.to_csv('pat2.csv',index=False)
