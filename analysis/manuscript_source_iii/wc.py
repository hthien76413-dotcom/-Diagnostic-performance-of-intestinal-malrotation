import io,re,sys
def body(path,start=None,end=None):
    ls=io.open(path,encoding='utf-8').read().split('\n')
    a=0; b=len(ls)
    if start: a=[i for i,l in enumerate(ls) if l.strip()==start][0]
    if end:   b=[i for i,l in enumerate(ls) if l.strip()==end][0]
    return ls[a:b]
ls=body('iii/p1.md','#H1 Introduction')+body('iii/p2.md')+body('iii/p3.md',None,'#H1 Abbreviations')
n=0
for l in ls:
    l=l.strip()
    if not l or l.startswith('#TAB') or l.startswith('#FIG'): continue
    t=re.sub(r'^#(H1|H2|N)\s*','',l)
    t=re.sub(r'\*+','',t)
    n+=len(t.split())
print(n)
