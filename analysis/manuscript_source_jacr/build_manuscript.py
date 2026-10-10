import docx, json, re, os
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from threeline import make_three_line_table
from usspell import us, us_table, ama_p
from docstyle import apply_house_style, add_page_numbers, add_line_numbers

def _blank_props(doc):
    """Strip python-docx's default authorship before saving.

    These files go out for double-blind review, so no document property may
    name an author, a reviser or the generator.
    """
    c = doc.core_properties
    for f in ('author', 'last_modified_by', 'title', 'subject', 'comments',
              'category', 'keywords', 'content_status', 'identifier',
              'language', 'version'):
        setattr(c, f, '')
    return doc


AN='/home/user/-Diagnostic-performance-of-intestinal-malrotation/analysis/'
OUT='/home/user/-Diagnostic-performance-of-intestinal-malrotation/'
D=json.load(open(AN+'tables123.json')); D.update(json.load(open(AN+'tables456.json')))
D.update(json.load(open(AN+'table3_final.json')))
D.update(json.load(open(AN+'tables24_final.json')))
T={k:us_table(D['T'+k]) for k in '1234'}
N_COH=D['T1'][1][1]; N_NONE=D['T1'][1][5]; N_US=re.search(r'\d+',D['T3'][0][1]).group()
AG=json.load(open(AN+'review_agreement.json')); OV=D['T3_overlap']
TITLES={
 '1':('Table 1',f'Characteristics of the {N_COH} children with surgically confirmed intestinal malrotation, overall and according to which preoperative index test they received',
   f'Groups overlap, because a child could receive more than one index test; columns therefore do not sum to the cohort total. Age at operation was calculated as age at admission for the operative encounter plus the interval from admission to operation. Presenting features were extracted from admission records by text search and are documentation rates, not verified prevalences. Symptom duration is the longest duration of a gastrointestinal symptom stated in the chief complaint of the operative admission; a child whose chief complaint stated none was counted as not having symptoms for 1 month or longer. The rightmost column shows the {N_NONE} children who received none of the three index tests; all of them nonetheless had other preoperative imaging (Figure 1). IQR interquartile range, UGI upper gastrointestinal.'),
 '2':('Table 2','Report-level detection of intestinal malrotation among surgically confirmed children, with the certainty of the wording used in positive conclusions',
   'Wilson 95% confidence intervals. Denominators differ between modalities and are drawn from overlapping but non-identical, indication-selected groups of children; the rates are not directly comparable between modalities and are not sensitivities. Certainty tiers were assigned from the conclusion text: definite (unqualified statement), probable ("most likely", "first consideration"), possible ("suspected", "cannot be excluded", "?"). The penultimate column repeats the detection rate after reclassifying all possible-tier conclusions as negative; the last counts as detected only positive examinations whose conclusion named malrotation, so that a conclusion naming volvulus alone or describing a sign alone does not count. Percentages for certainty tiers are of positive reports; detection rates are of all index reports of that modality. Contrast-enhanced and unenhanced CT were performed for different indications and in children of different ages, so their comparison is confounded and is presented as an exploratory subgroup only. UGI, upper gastrointestinal.'),
 '3':('Table 3',f'Documented content of the {N_US} routine ultrasound index examinations, and report-level detection conditional on that content',
   f'The index examination is the examination episode closest to operation, pooling all reports of that modality issued that day. Content was coded from the findings and conclusion text by two readers, an ultrasound physician and a pediatric surgeon, both authors who had reported none of the examinations, working independently against written criteria; {AG["disagreeing_cells"]} of {AG["cells"]:,} item codes differed and were adjudicated against the criteria (Supplement 1, Section K). This is an audit of what was recorded and is a lower bound on what was performed: an element assessed but not documented cannot be distinguished from one never assessed. Technique elements count as documented whether the finding was normal or abnormal; the artery–vein relationship counts only where the position of the two vessels relative to each other was stated, and the whirlpool sign only where it was described as present. Enteric fluid administration counts only examinations stating that fluid was given (oral contrast or nasogastric instillation); observed luminal fluid without a stated route was not counted. Booking categories were coded from the examination name and are not mutually exclusive: {OV["gi_vessel"]} sessions were booked as both gastrointestinal and great-vessel studies, {OV["gi_pyloric"]} as gastrointestinal and pyloric, and {OV["vessel_pyloric"]} as great-vessel and pyloric. Denominators of fewer than 10 are shown without a percentage.'),
 '4':('Table 4','Change in report-level detection between eras, before and after adding one covariate per modality (exploratory)',
   'Modality-specific logistic models; exploratory, the covariates having been chosen after inspection of the data. For ultrasound the covariate is whether the examination session included an abdominal great-vessel study; this is a booking label, not a record of technique. For CT it is intravenous contrast enhancement. No covariate was fitted for the UGI series. Odds ratios and average marginal effects are both shown because a conditional odds ratio attenuates when a predictive covariate is added even in the absence of mediation (non-collapsibility), so the marginal effect is the more interpretable measure of how far the era difference changes when the covariate is added. The covariates were not randomized and are themselves confounded by indication: a child suspected of volvulus is both more likely to be booked for a great-vessel study and more likely to have a whirlpool to find. These models are descriptive, not causal. Sensitivity analyses moving the era boundary from 2019 to 2022 are in Supplement 2. Marginal-effect intervals are percentile bootstrap intervals (2,000 resamples of children). UGI, upper gastrointestinal.'),
}
FIGS={'1':(OUT+'Fig1_study_flow.png',6.4),'2':(OUT+'Fig2_detection_by_modality.png',6.4),'3':(OUT+'Fig3_ultrasound_report_audit.png',6.6)}
doc=docx.Document()
st=doc.styles['Normal']; st.font.name='Times New Roman'; st.font.size=Pt(11)
for s in doc.sections: s.left_margin=s.right_margin=Inches(1.0)
def para(text,style=None,size=None,italic=False,space_after=8):
    p=doc.add_paragraph(style=style)
    text=ama_p(text)
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
    doc.add_page_break()
    p=para(f'{tag}. {title}'); p.runs[0].bold=True; p.paragraph_format.keep_with_next=True
    make_three_line_table(doc,data)
    para(foot,italic=True,size=8.5)
# Layout for review: text double-spaced with continuous line numbers and page
# numbers. JACR's guide asks for figure legends after the references and for
# tables and figures to be included in the manuscript at initial submission, so
# the order at the end is References, Figure Legends, then each table and each
# figure on its own page. Separate figure files (TIFF, >=300 dpi) are needed
# only at revision.
apply_house_style(doc)
DOUBLE=2.0
tables=[]; figs=[]
text=''.join(open(f).read()+'\n' for f in ['p1.md','p2.md','p3.md'])
for ln in text.split('\n'):
    ln=ln.strip()
    if not ln: continue
    if ln.startswith('#T '): para(ln[3:],style='Title')
    elif ln == '#H1 Figure legends':
        doc.add_page_break(); doc.add_heading('Figure Legends',level=1)
    elif ln.startswith('#H1 '): doc.add_heading(ln[4:],level=1)
    elif ln.startswith('#H2 '): doc.add_heading(ln[4:],level=2)
    elif ln.startswith('#N '): para(ln[3:]).paragraph_format.line_spacing=DOUBLE
    elif ln.startswith('#R '): para(ln[3:],size=10,space_after=3).paragraph_format.line_spacing=DOUBLE
    elif ln.startswith('#TAB'): tables.append(ln[4:])
    elif ln.startswith('#FIG'): figs.append(ln[4:])
    else: para(ln)
for k in tables: add_table(k)
for k in figs:
    doc.add_page_break()
    p=para(f'Figure {k}'); p.runs[0].bold=True; p.paragraph_format.keep_with_next=True
    path,w=FIGS[k]
    doc.add_picture(path,width=Inches(min(w,6.5))); doc.paragraphs[-1].alignment=WD_ALIGN_PARAGRAPH.CENTER
assert figs==['1','2','3'], figs
assert tables==['1','2','3','4'], tables
add_page_numbers(doc); add_line_numbers(doc)
_blank_props(doc).save(OUT+'JACR_3_Manuscript_masked.docx'); print('saved JACR_3_Manuscript_masked.docx')

# At revision JACR takes figures as separate TIFF, JPEG or EPS files of at least
# 300 dpi, so each figure is also written as an RGB, LZW-compressed, 300 dpi
# TIFF flattened onto white.
from PIL import Image
for k,(path,_) in FIGS.items():
    im=Image.open(path)
    if im.mode in ('RGBA','LA'):
        bg=Image.new('RGB',im.size,'white'); bg.paste(im,mask=im.split()[-1]); im=bg
    im.convert('RGB').save(OUT+f'JACR_Figure{k}.tif',compression='tiff_lzw',dpi=(300,300))
    print(f'saved JACR_Figure{k}.tif')
