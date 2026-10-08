# -*- coding: utf-8 -*-
"""House style shared by every JACR document builder.

python-docx's default template draws Title and Heading styles in blue theme
fonts (Calibri Light) and puts a rule under Title. A manuscript should not look
like that, so the heading styles are reset to black in the document's own font
and the rule is removed. The manuscript additionally gets page numbers and
continuous line numbers, which reviewers use to cite locations.
"""
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

_THEME_ATTRS = ('w:asciiTheme', 'w:hAnsiTheme', 'w:eastAsiaTheme', 'w:cstheme')


def _font(style, name, size, bold, italic=False):
    style.font.name = name
    style.font.size = Pt(size)
    style.font.bold = bold
    style.font.italic = italic
    style.font.color.rgb = RGBColor(0, 0, 0)
    rPr = style.element.get_or_add_rPr()
    rf = rPr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts')
        rPr.insert(0, rf)
    for a in _THEME_ATTRS:
        rf.attrib.pop(qn(a), None)
    for a in ('w:ascii', 'w:hAnsi', 'w:eastAsia', 'w:cs'):
        rf.set(qn(a), name)
    color = rPr.find(qn('w:color'))
    if color is not None:
        for a in ('w:themeColor', 'w:themeShade', 'w:themeTint'):
            color.attrib.pop(qn(a), None)


def apply_house_style(doc, font='Times New Roman'):
    normal = doc.styles['Normal']
    normal.font.name = font
    normal.element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'), font)
    _font(doc.styles['Title'], font, 16, True)
    pPr = doc.styles['Title'].element.pPr
    if pPr is not None:
        bdr = pPr.find(qn('w:pBdr'))
        if bdr is not None:
            pPr.remove(bdr)
    _font(doc.styles['Heading 1'], font, 13, True)
    _font(doc.styles['Heading 2'], font, 12, True, italic=True)
    return doc


def add_page_numbers(doc):
    for section in doc.sections:
        p = section.footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        fld = OxmlElement('w:fldSimple')
        fld.set(qn('w:instr'), 'PAGE')
        r = OxmlElement('w:r')
        t = OxmlElement('w:t')
        t.text = '1'
        r.append(t)
        fld.append(r)
        p._p.append(fld)


def add_line_numbers(doc):
    for section in doc.sections:
        sectPr = section._sectPr
        if sectPr.find(qn('w:lnNumType')) is not None:
            continue
        ln = OxmlElement('w:lnNumType')
        ln.set(qn('w:countBy'), '1')
        ln.set(qn('w:restart'), 'continuous')
        ln.set(qn('w:distance'), '284')
        # schema order: ... pgSz, pgMar, paperSrc, pgBorders, lnNumType, pgNumType, cols ...
        anchor = None
        for tag in ('w:pgBorders', 'w:paperSrc', 'w:pgMar', 'w:pgSz'):
            anchor = sectPr.find(qn(tag))
            if anchor is not None:
                break
        anchor.addnext(ln)
