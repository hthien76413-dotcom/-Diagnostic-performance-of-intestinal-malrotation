import docx, json, re, os
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
AN='/tmp/claude-0/-home-user--Diagnostic-performance-of-intestinal-malrotation/4998e6b2-e14c-57b0-80b5-41a1fb987d43/scratchpad/an/'
OUT='/home/user/-Diagnostic-performance-of-intestinal-malrotation/'
D=json.load(open(AN+'tables123.json')); D.update(json.load(open(AN+'tables456.json')))
T={'1':D['T1'],'2':D['T2'],'3':D['T3'],'4':D['T6']}
TITLES={
 '1':('Table 1','Characteristics of the 465 children with surgically confirmed intestinal malrotation, overall and according to which preoperative index test they received',
   'Groups overlap, because a child could receive more than one index test; columns therefore do not sum to the cohort total. Age at operation was calculated as age at admission for the operative encounter plus the interval from admission to operation. Presenting features were extracted from admission records by text search and are documentation rates, not verified prevalences. The rightmost column shows the 55 children who received none of the three index tests; all of them nonetheless had other preoperative imaging (Fig. 1). IQR interquartile range, UGI upper gastrointestinal.'),
 '2':('Table 2','Report-level detection of intestinal malrotation among surgically confirmed children, with the certainty of the wording used in positive conclusions',
   'Wilson 95% confidence intervals. Denominators differ between modalities and are drawn from overlapping but non-identical, indication-selected groups of children; the rates are not directly comparable between modalities and are not sensitivities. Certainty tiers were assigned from the conclusion text: definite (unqualified statement), probable ("most likely", "first consideration"), possible ("suspected", "cannot be excluded", "?"). The final column repeats the detection rate after reclassifying all possible-tier conclusions as negative. Percentages for certainty tiers are of positive reports; detection rates are of all index reports of that modality. Contrast-enhanced and unenhanced CT were performed for different indications and in children of different ages, so their comparison is confounded and is presented as an exploratory subgroup only.'),
 '3':('Table 3','Documented content of the 119 routine gastrointestinal ultrasound index reports, and report-level detection conditional on that content',
   'Content was coded from the findings and conclusion text of each index report by pre-specified patterns (Online Resource 1). This is an audit of what was recorded, and is a lower bound on what was performed: an element assessed but not documented cannot be distinguished here from one never assessed. The whirlpool sign appears twice because the adjudicated study variable and the text-pattern variable differ slightly (59 vs 57 reports); both are shown for transparency. Examination-type categories are not mutually exclusive.'),
 '4':('Table 4','Change in report-level detection between eras, and the examination-content variables that account for it',
   'Modality-specific logistic models. For ultrasound the content variable is whether the examination was booked and reported under the abdominal great-vessel item rather than the gastrointestinal ultrasound item (great-vessel-coded); this is an ordering and reporting label, not a record of technique. For CT the variable is intravenous contrast enhancement. Attenuation of the era odds ratio after the content variable is added indicates that the temporal change operated through what the examination was rather than through calendar time. The content variables were not randomly assigned and are themselves confounded by indication; these models are explanatory rather than causal.'),
}
FIGS={'1':(OUT+'Fig1_study_flow.png',6.4),'2':(OUT+'Fig2_detection_by_modality.png',6.4),'3':(OUT+'Fig3_ultrasound_report_audit.png',6.6)}
doc=docx.Document()
st=doc.styles['Normal']; st.font.name='Times New Roman'; st.font.size=Pt(11)
for s in doc.sections: s.left_margin=s.right_margin=Inches(1.0)
def para(text,style=None,size=None,italic=False,space_after=8):
    p=doc.add_paragraph(style=style)
    for pt in re.split(r'(\*\*[^*]+\*\*|\*[^*]+\*)',text):
        if not pt: continue
        if pt.startswith('**') and pt.endswith('**'): r=p.add_run(pt[2:-2]); r.bold=True
        elif pt.startswith('*') and pt.endswith('*') and len(pt)>2: r=p.add_run(pt[1:-1]); r.italic=True
        else: r=p.add_run(pt)
        if italic: r.italic=True
        if size: r.font.size=Pt(size)
    p.paragraph_format.space_after=Pt(space_after); return p
def add_table(k):
    tag,title,foot=TITLES[k]; data=T[k]
    p=para(f'{tag}. {title}'); p.runs[0].bold=True
    t=doc.add_table(rows=len(data),cols=len(data[0])); t.style='Light Grid Accent 1'
    for i,row in enumerate(data):
        for j,c in enumerate(row):
            cell=t.cell(i,j); cell.text=''
            r=cell.paragraphs[0].add_run(str(c)); r.font.size=Pt(8.5); r.font.name='Times New Roman'
            if i==0: r.bold=True
    para(foot,italic=True,size=8.5)
def add_fig(k):
    path,w=FIGS[k]
    doc.add_picture(path,width=Inches(w)); doc.paragraphs[-1].alignment=WD_ALIGN_PARAGRAPH.CENTER
text=''.join(open(f).read()+'\n' for f in ['p1.md','p2.md','p3.md'])
for ln in text.split('\n'):
    ln=ln.strip()
    if not ln: continue
    if ln.startswith('#T '): para(ln[3:],style='Title')
    elif ln.startswith('#H1 '): doc.add_heading(ln[4:],level=1)
    elif ln.startswith('#H2 '): doc.add_heading(ln[4:],level=2)
    elif ln.startswith('#N '): para(ln[3:])
    elif ln.startswith('#R '): para(ln[3:],size=10,space_after=3)
    elif ln.startswith('#TAB'): add_table(ln[4:])
    elif ln.startswith('#FIG'): add_fig(ln[4:])
    else: para(ln)
doc.save(OUT+'诊断效能_英文稿_InsightsIntoImaging投稿版_v4.docx'); print('saved')
