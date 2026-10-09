exec(open('core.py').read())
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from statsmodels.stats.proportion import proportion_confint as pci
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
OUT='/home/user/-Diagnostic-performance-of-intestinal-malrotation/'
C={'UGI':'#B22222','CT':'#E08214','US':'#2C7FB8','US2':'#7FC0E8','grey':'#7a7a7a'}

# ---------- Figure 1: flow ----------
import json
A55=json.load(open('a55b.json'))
ops0=pd.read_excel(BASE+'诊断效能_手术确诊队列_465例.xlsx', sheet_name='手术记录明细_503条')
opsall=x.parse('住院病历手术记录'); n_db=x.parse('病案首页基本信息')['科研患者编号'].nunique()
_ch=REV[REV['kind']=='child']['reason']
n_nc=int(_ch.str.startswith('malrotation not confirmed').sum()); n_re=int(_ch.str.startswith('anchor operation was a reoperation').sum())
rep['day']=rep['检查时间'].dt.normalize()
_f=rep.sort_values('gap').groupby(['科研患者编号','mod']).first().reset_index()[['科研患者编号','mod','day']]
_m=rep.merge(_f,on=['科研患者编号','mod'],suffixes=('','_ix')); _in=_m['day']==_m['day_ix']
n_rep,n_ixrep,n_early=len(rep),int(_in.sum()),int((~_in).sum())
_rr=REV[(REV['kind']=='report')&~REV['科研患者编号'].isin(_drop)]; n_rm=len(_rr)
nmod=idx['mod'].value_counts(); n_img=idx['科研患者编号'].nunique(); n_ep=len(idx)
n_three=int(mat[['US_detected','CT_detected','UGI_detected']].notna().all(axis=1).sum())
n_none=len(coh)-n_img; assert n_none==A55['n']
fig,ax=plt.subplots(figsize=(10.5,10.0)); ax.axis('off'); ax.set_xlim(0,100); ax.set_ylim(20,132)
def box(x,y,w,h,txt,fc='#f4f6f8',ec='#333',fs=10.5,weight='normal'):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.6',fc=fc,ec=ec,lw=1.1))
    ax.text(x+w/2,y+h/2,txt,ha='center',va='center',fontsize=fs,fontweight=weight,linespacing=1.45)
def arrow(x1,y1,x2,y2):
    ax.annotate('',xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle='-|>',lw=1.2,color='#333'))
box(20,119,60,10,f'Clinical research database, 1 Dec 2012 - 30 Jun 2026:\n{n_db} children with a recorded diagnosis of intestinal malrotation;\n{len(opsall)} operative records in {opsall["科研患者编号"].nunique()} operated children, all read',fc='#e8eef5',weight='bold')
arrow(50,119,50,102.5)
arrow(50,110.5,64.5,110.5)
box(65,106,33,9,f'Operation did not meet the criterion\n{len(opsall)-len(ops0)} records in {opsall["科研患者编号"].nunique()-ops0["科研患者编号"].nunique()} children\n(operative diagnosis unrelated to malrotation)',fc='#faf1e8',fs=9.0)
box(22,93,56,9,f'Operative diagnosis named malrotation or procedure was a Ladd procedure\n{len(ops0)} records in {ops0["科研患者编号"].nunique()} children',fc='#e8eef5')
arrow(50,93,50,80.5)
arrow(50,86.5,64.5,86.5)
box(65,81.5,33,10,f'Excluded after review of the anchor operation\nn = {n_nc+n_re}\n  malrotation not confirmed at that operation  {n_nc}\n  reoperation after earlier malrotation surgery  {n_re}',fc='#faf1e8',fs=9.0)
box(22,71,56,9,f'Surgically confirmed intestinal malrotation\n{len(ops)} records in n = {len(coh)} children (reference standard)',fc='#e8eef5',weight='bold')
arrow(50,71,50,67)
box(4,50,44,17,f'At least one preoperative index test\nn = {n_img}  ({n_ep} index examinations)\n\nUGI series {nmod["UGI"]}   Abdominal CT {nmod["CT"]}\nUltrasound {nmod["US"]}\nAll three modalities {n_three}',fc='#eef5ee',fs=10.5)
arrow(48,58.5,54,58.5)
box(54,36,44,31,f'None of the three index tests\nn = {n_none} ({100*n_none/len(coh):.1f}%)\n\nbut every one had other preoperative imaging:\n  abdominal / chest radiograph            {A55["plain"]}\n  contrast enema of the colon             {A55["enema"]}\n  ultrasound of another region            {A55["otherus"]}\n  CT of another region                      {A55["otherct"]}\n  no in-hospital study                       {A55["none"]}\n     (all {A55["none"]} with documented outside imaging)\n\nOutside or outpatient imaging documented in {A55["outside"]};\nalready reporting malrotation or volvulus in {A55["outside_mal"]}',fc='#faf1e8',fs=9.3)
assert A55['none_outside']==A55['none']
arrow(26,50,26,45.5)
box(3,22,46,23,f'Index examination = examination episode closest to operation\n{n_rep} eligible preoperative reports  \u2192  {n_ep} episodes\n(same-day reports of one modality pooled; {n_early} earlier\nrepeat examinations not audited; {n_rm} reports issued after\nthe operation or for an unrelated illness removed)\n\nEach episode classified as positive or negative by\nrule-based algorithm + surgeon adjudication, and\nseparately audited for documented technical content',fc='#eef5ee',fs=9.3)
plt.tight_layout(); plt.savefig(OUT+'Fig1_study_flow.png',dpi=300,bbox_inches='tight',facecolor='white'); plt.close()
print('figure 1: cohort %d (%d records), excluded %d+%d, imaged %d, episodes %d from %d reports (%d in index episodes, %d earlier), none %d'%(
      len(coh),len(ops),n_nc,n_re,n_img,n_ep,n_rep,n_ixrep,n_early,n_none))

# ---------- Figure 3: detection with prominent denominators ----------
ixf=pd.read_csv('ix_full.csv'); u=pd.read_csv('us_audit.csv')
rows=[]
for mod,lab,col in [('UGI','UGI series',C['UGI']),('CT','Abdominal CT (all)',C['CT']),('US','Ultrasound',C['US'])]:
    d=ixf[ixf['mod']==mod]; k=int(d['det'].sum()); n=len(d); lo,hi=pci(k,n,method='wilson')
    rows.append((lab,k,n,k/n*100,lo*100,hi*100,col))
fig,ax=plt.subplots(figsize=(11,4.6))
y=np.arange(len(rows))[::-1]
for i,(lab,k,n,r,lo,hi,col) in enumerate(rows):
    ax.plot([lo,hi],[y[i],y[i]],color=col,lw=3.2,solid_capstyle='round')
    ax.plot(r,y[i],'o',color=col,ms=11,zorder=3)
    ax.text(103,y[i],f'{r:.1f}%',va='center',ha='right',fontsize=12,fontweight='bold',color=col)
    ax.text(106,y[i],f'{k} of {n}',va='center',ha='left',fontsize=11,color='#333')
ax.set_yticks(y); ax.set_yticklabels([f'{lab}\n' + r'$\bf{denominator\ n=%d}$'%n for lab,k,n,*_ in rows],fontsize=11)
ax.set_xlim(0,126); ax.set_xticks(range(0,101,20)); ax.set_xlabel('Report-level detection among surgically confirmed malrotation (%), Wilson 95% CI')
ax.grid(axis='x',color='#dddddd'); ax.set_axisbelow(True)
plt.tight_layout(); plt.savefig(OUT+'Fig2_detection_by_modality.png',dpi=300,bbox_inches='tight',facecolor='white'); plt.close()
print('fig1, fig3 done')
