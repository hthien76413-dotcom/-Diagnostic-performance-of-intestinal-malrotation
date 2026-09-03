exec(open('core.py').read())
import re
u=idx[idx['mod']=='US'].copy()
u=u.merge(mat[['科研患者编号','US_detected','US_whirlpool']],on='科研患者编号',how='left')
u=u.merge(pat[['科研患者编号','era_late','op_year']],on='科研患者编号',how='left')
T=u['txt'].astype(str); N=u['报告名称'].astype(str)
def f(rx): return T.str.contains(rx,regex=True)

# --- 语料驱动的修正模式 ---
u['d3']       = f(r'十二指肠水平部|十二指肠水平段|十二指肠横部|十二指肠第三段|(?<![弓])横部|水平部')
u['djj']      = f(r'十二指肠空肠曲|屈氏|Treitz|十二指肠悬韧带')
u['d3_or_djj']= u['d3'] | u['djj']
u['duodenum'] = f(r'十二指肠')
u['sma_smv']  = f(r'肠系膜上动脉|肠系膜上静脉|系膜血管|SMA|SMV')
u['inversion']= f(r'(?:静脉|动脉)[^。；\n]{0,10}(?:换位|反位|倒置|关系异常|异常关系)|静脉位于[^。；\n]{0,8}左|动脉位于[^。；\n]{0,8}右')

u['fluid']    = f(r'饮水|口服[^。；\n]{0,6}(?:水|液|造影剂)|注水|注入|胃内注|温开水|经胃管')
u['dynamic']  = f(r'动态|实时观察|连续观察')
u['compress'] = f(r'加压|探头压|压迫探查')
u['whirl_txt']= f(r'漩涡|旋涡|涡流|螺旋')
u['gas_limit']= f(r'气体干扰|肠气干扰|气体较多|积气[^。；\n]{0,10}(?:干扰|遮挡)|显示欠清|显示不清|声窗')
u['cecum']    = f(r'回盲')
u['vessel_us']= N.str.contains('腹部大血管'); u['gi_us']=N.str.contains('胃肠道')
u['bedside']  = N.str.contains('床旁')
u['doppler']  = f(r'CDFI|彩色多普勒|多普勒')
u.to_csv('us_audit2.csv',index=False)

print('=== 修正后的超声报告内容审计 (n=%d) ==='%len(u))
items=[('d3_or_djj','D3 或十二指肠空肠曲'),('d3','  其中 D3（水平部/横部）'),('djj','  其中 十二指肠空肠曲'),
       ('duodenum','十二指肠（任何提及）'),('sma_smv','肠系膜上动/静脉关系'),('inversion','明确写出动静脉换位'),
       ('fluid','使用肠腔内液体'),('dynamic','动态观察'),('compress','加压探查'),
       ('cecum','回盲部'),('whirl_txt','漩涡/螺旋征象'),('gas_limit','肠气影响显示'),('doppler','彩色多普勒'),
       ('vessel_us','按大血管项目开单'),('gi_us','按胃肠道项目开单'),('bedside','床旁检查')]
for k,lab in items:
    s=u[k].astype(bool)
    dy=f"{u[s]['US_detected'].mean()*100:5.1f}" if s.sum() else '  –  '
    dn=f"{u[~s]['US_detected'].mean()*100:5.1f}" if (~s).sum() else '  –  '
    print(f'  {lab:24s} {int(s.sum()):3d} ({s.mean()*100:5.1f}%)   检出|有 {dy}%  检出|无 {dn}%')
print()
print('=== 那 2 份记录了 D3 的报告 ===')
for _,r in u[u['d3']].iterrows():
    print(f"  检出={int(r['US_detected'])} 漩涡={int(r['US_whirlpool'])} 年={r['op_year']} 项目={r['报告名称'][:28]}")
    for m in re.finditer(r'.{0,50}(水平部|横部).{0,50}', str(r['txt'])):
        print('    …'+m.group(0).replace('\n',' ')+'…')
