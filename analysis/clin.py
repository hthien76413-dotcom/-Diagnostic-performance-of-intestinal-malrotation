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
# longest gastrointestinal-symptom duration stated in the chief complaint of the operative admission
import re
SYM=r'呕吐|吐奶|呕奶|干呕|吐|腹痛|腹胀|腹部不适|便血|血便|哭吵|哭闹|体重不增|便秘|纳差|拒奶|腹泻'
NONSYM=r'产检|产前|孕期|胎儿|发现|提示|术后|CT|B超|彩超|检查|立位片|造影'   # clauses dating a finding, not a symptom
DIG={'一':1,'二':2,'两':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9}
def cn(n):
    if re.fullmatch(r'\d+(\.\d+)?',n): return float(n)
    if n=='半': return 0.5
    if n=='数': return 3.0
    if '十' in n:
        a,_,b=n.partition('十')
        return (DIG.get(a,1) if a else 1)*10+(DIG.get(b,0) if b else 0)
    return float(DIG.get(n[0],1))
DUR=r'(\d+(?:\.\d+)?|[一二两三四五六七八九十半数]+)\s*余?\s*(?:个)?\s*(小时|h|天|日|周|月|年)'
UNIT={'小时':1/24,'h':1/24,'天':1,'日':1,'周':7,'月':30,'年':365}
def symptom_days(text):
    best=None
    for cl in re.split(r'[，,；;。\s]+',str(text)):
        if not re.search(SYM,cl) or re.search(NONSYM,cl): continue
        for m in re.finditer(DUR,cl):
            d=cn(m.group(1))*UNIT[m.group(2)]
            best=d if best is None else max(best,d)
    return best
_cc=adm.merge(pat[['科研患者编号','科研就诊编号']],on=['科研患者编号','科研就诊编号'],how='inner')
assert _cc['科研患者编号'].is_unique and len(_cc)==len(pat)
_cc['sym_days']=_cc['主诉'].map(symptom_days)
print('chief complaint with a GI-symptom duration:',_cc['sym_days'].notna().sum(),'| >=30 days:',(_cc['sym_days']>=30).sum())
feat=feat.merge(_cc[['科研患者编号','sym_days']],on='科研患者编号',how='left')
feat['symptoms_1m']=(feat['sym_days']>=30).values
feat=feat.drop(columns='sym_days')
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
      **{c:f"{d[c].sum()} ({d[c].mean()*100:.1f}%)" for c in ['vomit','bilious','bloody_stool','distension','abd_pain','shock','symptoms_1m']}))
t=pd.DataFrame(rows).set_index('group').T
print(t.to_string())
t.to_csv('tab_bygroup.csv')
pat2.to_csv('pat2.csv',index=False)
