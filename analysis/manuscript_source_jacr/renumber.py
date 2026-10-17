# -*- coding: utf-8 -*-
"""Renumber references into order of first citation (Springer numbered style).

Rewrites the in-text markers in p1/p2/p3.md and reorders the #R list in p3.md.
Idempotent: running it again is a no-op once the list is already in order.
"""
import io, re, sys

FILES=['p1.md','p2.md','p3.md']
CITE=re.compile(r'\[((?:\d+\s*[–-]\s*\d+|\d+)(?:\s*,\s*(?:\d+\s*[–-]\s*\d+|\d+))*)\]')

def expand(g):
    out=[]
    for part in [p.strip() for p in g.split(',')]:
        m=re.match(r'^(\d+)\s*[–-]\s*(\d+)$',part)
        if m: out+=list(range(int(m.group(1)),int(m.group(2))+1))
        else: out.append(int(part))
    return out

def render(nums):
    """Collapse a sorted list into ranges: 5,6,7,9 -> '5-7, 9' (en dash)."""
    nums=sorted(set(nums)); parts=[]; i=0
    while i<len(nums):
        j=i
        while j+1<len(nums) and nums[j+1]==nums[j]+1: j+=1
        run=j-i+1
        if run==1: parts.append(str(nums[i]))
        elif run==2: parts += [str(nums[i]), str(nums[j])]   # a run of two stays a list
        else: parts.append(f'{nums[i]}–{nums[j]}')
        i=j+1
    return '['+', '.join(parts)+']'

text={f: io.open(f,encoding='utf-8').read() for f in FILES}
refs={}
for line in text['p3.md'].split('\n'):
    m=re.match(r'^#R (\d+)\.\s+(.*)$',line)
    if m: refs[int(m.group(1))]=m.group(2)

# first-appearance order over body text only (reference list excluded)
order=[]
for f in FILES:
    body=text[f].split('#H1 References')[0]
    for m in CITE.finditer(body):
        for n in expand(m.group(1)):
            if n not in order: order.append(n)

missing=[n for n in order if n not in refs]
uncited=[n for n in refs if n not in order]
if missing or uncited:
    sys.exit(f'ABORT missing={missing} uncited={uncited}')

mp={old:new for new,old in enumerate(order,1)}
for f in FILES:
    head,sep,tail=text[f].partition('#H1 References')
    head=CITE.sub(lambda m: render([mp[n] for n in expand(m.group(1))]), head)
    text[f]=head+sep+tail

newlist='\n'.join(f'#R {mp[old]}. {refs[old]}' for old in sorted(refs,key=lambda o:mp[o]))
text['p3.md']=re.sub(r'(?m)^#R \d+\..*(?:\n#R \d+\..*)*$', newlist, text['p3.md'], count=1)

for f in FILES: io.open(f,'w',encoding='utf-8').write(text[f])
changed=sum(1 for o in mp if mp[o]!=o)
print(f'renumbered {len(mp)} references, {changed} changed position')
for old in sorted(mp):
    if mp[old]!=old: print(f'  [{old}] -> [{mp[old]}]  {refs[old][:60]}')
