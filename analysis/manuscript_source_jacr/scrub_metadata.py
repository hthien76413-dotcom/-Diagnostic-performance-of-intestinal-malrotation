# -*- coding: utf-8 -*-
"""Clean the file properties of the submission documents.

For every JACR_*.docx in the repository root this script
  * leaves author, last modified by, comments, title, subject and keywords empty,
  * writes the current time into the created and modified fields (python-docx's
    template carries a 2013 date),
  * replaces docProps/app.xml, which describes the template (Word for Mac, zero
    words), with a minimal one,
  * drops the template's docProps/thumbnail.jpeg,
  * re-encodes embedded PNG figures without their text chunks (matplotlib writes a
    "Software" chunk) and without changing a pixel,
  * stamps every zip entry with the current time.
It then sets the modification time of all files in the package to the same moment.

The builders call scrub_docx() after each save; run `python3 scrub_metadata.py`
after any rebuild to finish the whole package.
"""
import datetime, glob, io, os, re, sys, time, zipfile
from PIL import Image

ROOT = '/home/user/-Diagnostic-performance-of-intestinal-malrotation/'
PACKAGE_EXTRA = ['Supplement_1_classifier.py', 'JACR_Figure1.tif', 'JACR_Figure2.tif', 'JACR_Figure3.tif',
                 'JACR_英文稿_全文纯文本.txt', '参考文献_28条.ris', '参考文献_28条_DOI清单.txt', '参考文献_28条_编号对照.txt']

APP_XML = ("<?xml version='1.0' encoding='UTF-8' standalone='yes'?>\n"
           '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
           'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
           '<DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop><LinksUpToDate>false</LinksUpToDate>'
           '<SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged></Properties>')

EMPTY_FIELDS = ['dc:title', 'dc:subject', 'dc:creator', 'cp:keywords', 'dc:description', 'cp:lastModifiedBy',
                'cp:category', 'cp:contentStatus', 'dc:identifier', 'dc:language', 'cp:version']


def _core(xml, stamp):
    for tag in EMPTY_FIELDS:
        xml, n = re.subn(rf'<{tag}>.*?</{tag}>|<{tag}/>', f'<{tag}></{tag}>', xml, flags=re.S)
    for tag in ('dcterms:created', 'dcterms:modified', 'cp:lastPrinted'):
        xml = re.sub(rf'(<{tag}[^>]*>)[^<]*(</{tag}>)', rf'\g<1>{stamp}\g<2>', xml)
    return xml


def _png(data):
    im = Image.open(io.BytesIO(data))
    im.load()
    out = io.BytesIO()
    kw = {}
    if 'dpi' in im.info:
        kw['dpi'] = im.info['dpi']
    im.save(out, format='PNG', **kw)
    return out.getvalue()


def scrub_docx(path, now=None):
    now = now or time.time()
    t = time.gmtime(now)
    stamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', t)
    zt = time.localtime(now)[:6]
    src = zipfile.ZipFile(path)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as dst:
        for info in src.infolist():
            name, data = info.filename, src.read(info.filename)
            if name == 'docProps/thumbnail.jpeg':
                continue
            if name == 'docProps/core.xml':
                data = _core(data.decode('utf-8'), stamp).encode('utf-8')
            elif name == 'docProps/app.xml':
                data = APP_XML.encode('utf-8')
            elif name == '_rels/.rels':
                data = re.sub(rb'<Relationship [^>]*metadata/thumbnail[^>]*/>', b'', data)
            elif name.startswith('word/media/') and name.lower().endswith('.png'):
                data = _png(data)
            zi = zipfile.ZipInfo(name, date_time=zt)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            dst.writestr(zi, data)
    src.close()
    with open(path, 'wb') as f:
        f.write(buf.getvalue())
    os.utime(path, (now, now))


def scrub_all(now=None):
    now = now or time.time()
    for p in sorted(glob.glob(ROOT + 'JACR_*.docx')):
        scrub_docx(p, now)
    for n in PACKAGE_EXTRA:
        p = ROOT + n
        if os.path.exists(p):
            os.utime(p, (now, now))
    return now


if __name__ == '__main__':
    n = scrub_all()
    print('scrubbed', len(glob.glob(ROOT + 'JACR_*.docx')), 'documents at', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(n)))
