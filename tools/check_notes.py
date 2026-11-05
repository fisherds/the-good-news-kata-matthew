"""Check that each walkthrough table in translation/notes/*.md covers every Greek
word of the verse quoted above it (the "> ..." line under each "## c:v" heading).
Prints the words that no row's Greek column contains.

Usage: python3 tools/check_notes.py [notes files...]   (default: all notes)
"""
import re,sys,unicodedata
def norm(w):
    w=unicodedata.normalize('NFD',w); w=''.join(c for c in w if not unicodedata.combining(c))
    return re.sub(r'[^\w]','',w.lower().replace('ʼ','').replace('ς','σ'))
import glob, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for path in sys.argv[1:] or sorted(glob.glob(os.path.join(ROOT, "translation", "notes", "*.md"))):
    text=open(path).read()
    secs=re.split(r'\n(?=## )',text)
    for sec in secs:
        q=re.search(r'^> (.+)$',sec,re.M)
        if not q or not re.search(r'[Ͱ-Ͽἀ-῿]',q.group(1)): continue
        need=[norm(w) for w in q.group(1).split() if re.search(r'[Ͱ-Ͽἀ-῿]',w)]
        have=set()
        for row in re.findall(r'^\| ([^|]+) \|',sec,re.M):
            for w in row.split(): have.add(norm(w))
        miss=[]
        for w in need:
            if w and w not in have and w not in miss: miss.append(w)
        print(path.split('/')[-1], '|', sec.splitlines()[0], '| missing:', ' '.join(miss) or '—')
