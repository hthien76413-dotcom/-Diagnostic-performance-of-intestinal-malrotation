# -*- coding: utf-8 -*-
"""Render the built manuscript as plain text, tables included.

Reads the .docx rather than the .md sources so that what is exported is exactly
what was built. Regenerate after any rebuild:  python3 export_plaintext.py
"""
import docx, io, os
from docx.table import Table
from docx.text.paragraph import Paragraph

ROOT = '/home/user/-Diagnostic-performance-of-intestinal-malrotation/'
SRC  = ROOT + '诊断效能_英文稿_InsightsIntoImaging投稿版_v4.docx'
DST  = ROOT + '诊断效能_英文稿_全文纯文本.txt'

d = docx.Document(SRC)
out = []
for ch in d.element.body.iterchildren():
    if ch.tag.endswith('}p'):
        p = Paragraph(ch, d); t = p.text.strip()
        if not t: continue
        st = p.style.name
        if st == 'Title':                out.append('# ' + t)
        elif st.startswith('Heading 1'): out.append('\n## ' + t)
        elif st.startswith('Heading 2'): out.append('\n### ' + t)
        else:                            out.append(t)
    elif ch.tag.endswith('}tbl'):
        rows = [[c.text.strip() for c in r.cells] for r in Table(ch, d).rows]
        w = [max(len(r[i]) for r in rows) for i in range(len(rows[0]))]
        out.append('```')
        for k, r in enumerate(rows):
            out.append('  '.join(x.ljust(w[i]) for i, x in enumerate(r)).rstrip())
            if k == 0: out.append('  '.join('-' * w[i] for i in range(len(w))))
        out.append('```')

txt = '\n\n'.join(out)
io.open(DST, 'w', encoding='utf-8').write(txt)
print(f'{os.path.basename(DST)}: {len(txt.split())} words, {len(txt)} chars')
