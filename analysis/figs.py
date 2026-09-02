exec(open('core.py').read())
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from statsmodels.stats.proportion import proportion_confint as pci
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
OUT='/home/user/-Diagnostic-performance-of-intestinal-malrotation/'
C={'UGI':'#B22222','CT':'#E08214','US':'#2C7FB8','US2':'#7FC0E8','grey':'#7a7a7a'}

# ---------- Figure 1: flow ----------
fig,ax=plt.subplots(figsize=(10.5,8.2)); ax.axis('off'); ax.set_xlim(0,100); ax.set_ylim(0,100)
def box(x,y,w,h,txt,fc='#f4f6f8',ec='#333',fs=10.5,weight='normal'):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.6',fc=fc,ec=ec,lw=1.1))
    ax.text(x+w/2,y+h/2,txt,ha='center',va='center',fontsize=fs,fontweight=weight,linespacing=1.45)
def arrow(x1,y1,x2,y2):
    ax.annotate('',xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle='-|>',lw=1.2,color='#333'))
box(22,88,56,9,'Children undergoing surgery for intestinal malrotation\n1 December 2012 - 30 June 2026',fc='#e8eef5',weight='bold')
arrow(50,88,50,82.5)
box(22,73,56,9,'Surgically confirmed intestinal malrotation\nn = 465  (reference standard: operative diagnosis)',fc='#e8eef5',weight='bold')
arrow(50,73,50,67)
box(4,50,44,17,'At least one preoperative index test\nn = 410  (740 index examinations)\n\nUGI series 301   Abdominal CT 320\nGastrointestinal ultrasound 119\nAll three modalities 59',fc='#eef5ee',fs=10.5)
arrow(48,58.5,54,58.5)
box(54,36,44,31,'None of the three index tests\nn = 55 (11.8%)\n\nbut every one had other preoperative imaging:\n  abdominal / chest radiograph            46\n  contrast enema of the colon             12\n  ultrasound of another region            22\n  CT of another region                      7\n  no in-hospital study                       5\n     (all 5 with documented outside imaging)\n\nOutside or outpatient imaging documented in 33;\nalready reporting malrotation or volvulus in 19',fc='#faf1e8',fs=9.3)
arrow(26,50,26,44)
box(4,26,44,18,'Analysis of report-level detection\n\nEach report classified as positive or negative\nby rule-based algorithm + surgeon adjudication\n\nEach report separately audited for\ndocumented technical content',fc='#eef5ee',fs=10)
ax.text(50,15,'Detection rates are computed among children with surgically confirmed malrotation.\nThe cohort contains no test-negative children, so sensitivity, specificity and predictive values are not estimable.',
        ha='center',va='center',fontsize=9.8,style='italic',color='#444',
        bbox=dict(boxstyle='round,pad=0.6',fc='#fff8e1',ec='#d9b34a'))
plt.tight_layout(); plt.savefig(OUT+'Fig1_study_flow.png',dpi=300,bbox_inches='tight',facecolor='white'); plt.close()

# ---------- Figure 3: detection with prominent denominators ----------
ixf=pd.read_csv('ix_full.csv'); u=pd.read_csv('us_audit.csv')
rows=[]
for mod,lab,col in [('UGI','UGI contrast series',C['UGI']),('CT','Abdominal CT (all)',C['CT']),('US','Gastrointestinal ultrasound',C['US'])]:
    d=ixf[ixf['mod']==mod]; k=int(d['det'].sum()); n=len(d); lo,hi=pci(k,n,method='wilson')
    rows.append((lab,k,n,k/n*100,lo*100,hi*100,col))
k=int(u['US_whirlpool'].sum()); n=len(u); lo,hi=pci(k,n,method='wilson')
rows.append(('Ultrasound: whirlpool sign recorded',k,n,k/n*100,lo*100,hi*100,C['US2']))
fig,ax=plt.subplots(figsize=(11,5.4))
y=np.arange(len(rows))[::-1]
for i,(lab,k,n,r,lo,hi,col) in enumerate(rows):
    ax.plot([lo,hi],[y[i],y[i]],color=col,lw=3.2,solid_capstyle='round')
    ax.plot(r,y[i],'o',color=col,ms=11,zorder=3)
    ax.text(103,y[i],f'{r:.1f}%',va='center',ha='right',fontsize=12,fontweight='bold',color=col)
    ax.text(106,y[i],f'{k} of {n}',va='center',ha='left',fontsize=11,color='#333')
ax.set_yticks(y); ax.set_yticklabels([f'{lab}\n' + r'$\bf{denominator\ n=%d}$'%n for lab,k,n,*_ in rows],fontsize=11)
ax.set_xlim(0,126); ax.set_xticks(range(0,101,20)); ax.set_xlabel('Report-level detection among surgically confirmed malrotation (%), Wilson 95% CI')
ax.grid(axis='x',color='#dddddd'); ax.set_axisbelow(True)
ax.set_title('Each bar has a DIFFERENT denominator drawn from a DIFFERENT, indication-selected group of children.\nThese are not sensitivities and must not be compared with one another as if they were.',
             fontsize=10.5,color='#8a1c1c',pad=14,fontweight='bold')
plt.tight_layout(); plt.savefig(OUT+'Fig2_detection_by_modality.png',dpi=300,bbox_inches='tight',facecolor='white'); plt.close()
print('fig1, fig3 done')
