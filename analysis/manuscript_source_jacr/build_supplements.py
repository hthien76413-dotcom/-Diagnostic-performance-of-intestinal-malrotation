import docx, json, re, os
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from threeline import make_three_line_table
from usspell import us, us_table, ama_p
from docstyle import apply_house_style, add_page_numbers
import shutil

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
D.update(json.load(open(AN+'or_tables.json'))); D.update(json.load(open(AN+'or_h.json')))
D.update(json.load(open(AN+'or3_pooled.json'))); D.update(json.load(open(AN+'or_sens.json'))); D.update(json.load(open(AN+'or_add.json')))
D.update(json.load(open(AN+'us_coding_agreement.json')))
TAB={'H':('Table S1','Report-content audit patterns',D['H']),
     'K':('Table S2','Agreement of the two independent readers on the twelve ultrasound content items, and agreement of the text patterns with their consensus',D['K']),
     'S1':('Table S3','Distribution of algorithmic labels and certainty tiers, by modality',D['S1']),
     'G':('Table S4','Between-modality comparison of report-level detection (generalized estimating equation)',D['T4']),
     'P':('Table S5','Report-level detection in the selected subgroup receiving all three examinations, overall and restricted to examinations performed close together in time',D['T5']),
     'S2':('Table S6','Report-level detection stratified by midgut volvulus and by age category',D['S2']),
     'S2B':('Table S7','Detection of a volvulus-specific sign among children with surgically confirmed midgut volvulus',D['S2b']),
     'S3':('Table S8','Documented content of the CT and upper gastrointestinal series index examinations',D['S3']),
     'S4':('Table S9','Ultrasound temporal model with the era boundary placed at 2019, 2020, 2021 and 2022',D['S4']),
     'S5':('Table S10','Ultrasound content audit taking the earliest rather than the closest preoperative examination episode as the index unit',D['S5']),
     'S6':('Table S11','Prevalence of midgut volvulus, and the whirlpool sign among those children, under three definitions of volvulus',D['S6']),
     'S11':('Table S12','Average marginal effect of later era, with bootstrap confidence intervals',D['S11']),
     'S12':('Table S13','Paired differences in detection in the subgroup receiving all three examinations',D['S12']),
     'S13':('Table S14','Interaction terms, and the separated volvulus contrast under penalized likelihood',D['S13'])}
def make(src,outfile,figs=None):
    doc=docx.Document(); apply_house_style(doc); add_page_numbers(doc)
    st=doc.styles['Normal']; st.font.name='Times New Roman'; st.font.size=Pt(11)
    for s in doc.sections: s.left_margin=s.right_margin=Inches(1.0)
    def para(t,style=None,size=None,italic=False):
        p=doc.add_paragraph(style=style)
        t=ama_p(t)
        for pt in re.split(r'(\*\*[^*]+\*\*|\*[^*\s][^*]*\*)',t):
            if not pt: continue
            if pt.startswith('**') and pt.endswith('**'): r=p.add_run(pt[2:-2]); r.bold=True
            elif pt.startswith('*') and pt.endswith('*') and len(pt)>2: r=p.add_run(pt[1:-1]); r.italic=True
            else: r=p.add_run(pt)
            if italic: r.italic=True
            if size: r.font.size=Pt(size)
        p.paragraph_format.space_after=Pt(8); return p
    def table(key):
        tag,title,data=TAB[key]
        p=para(f'{tag}. {title}'); p.runs[0].bold=True
        make_three_line_table(doc,us_table(data))
        para('')
    for ln in open(src).read().split('\n'):
        ln=ln.strip()
        if not ln: continue
        if ln.startswith('#T '): para(ln[3:],style='Title')
        elif ln.startswith('#H1 '): doc.add_heading(ln[4:],level=1)
        elif ln.startswith('#N '): para(ln[3:])
        elif ln.startswith('#FIG'):
            doc.add_picture(OUT+'FigS1_paired_subgroup.png',width=Inches(6.2)); doc.paragraphs[-1].alignment=WD_ALIGN_PARAGRAPH.CENTER
        elif ln.startswith('#TAB'): table(ln[4:])
        else: para(ln)
    _blank_props(doc).save(OUT+outfile); print('saved',outfile)
make('supp1.md','JACR_Supplement_1_NLP_and_report_audit.docx')
make('supp2.md','JACR_Supplement_2_models_and_subgroups.docx')
make('supp3.md','JACR_Supplement_3_CT_and_UGI_content_audit.docx')
# the runnable rule set deposited with Supplement 1 is the analysis copy, unchanged
shutil.copyfile(AN+'classifier.py',OUT+'Supplement_1_classifier.py'); print('saved Supplement_1_classifier.py')
