import re, sys
DRY = "--write" not in sys.argv

DEFAULT={
 'ab-':'away','abs-':'away','a-':'not','an-':'not','ambi-':'both','anti-':'against',
 'be-':'intensive','caco-':'bad','co-':'together','com-':'together','con-':'together',
 'de-':'down/away','dia-':'through','dis-':'apart','dif-':'apart','di-':'apart',
 'e-':'out','ex-':'out','ef-':'out','ec-':'out','en-':'in','em-':'in','epi-':'upon',
 'equi-':'equal','eu-':'good','il-':'not','ir-':'not','im-':'not','in-':'not',
 'mis-':'hate','ob-':'against/toward','op-':'against','of-':'against','per-':'through',
 'prae-':'before/forth','pre-':'before','pro-':'forward','re-':'back/again','sub-':'under',
 'trans-':'across','un-':'not','ana-':'up/back','prod-':'forth','aff-':'to','epi-':'upon',
}
# word -> gloss for its FIRST prefix (context-specific, overrides DEFAULT)
OVR={
 'implicit':'in','inchoate':'intensive','engender':'make','effrontery':'out',
 'belie':'intensive','obfuscate':'over','revere':'intensive',
 'contrite':'thoroughly','disinterested':'not','dissemble':'apart','exacerbate':'thoroughly',
 'amnesty':'not','desultory':'down','ephemeral':'on','erudite':'out','enmity':'in',
}

def norm_word(w):
    return w.replace('*','').replace('\\','').strip().lower()

def is_prefix(tok):
    t=tok.strip().strip('*')
    return bool(re.fullmatch(r'[a-z]{1,5}-', t)) and '(' not in tok

def prefix_key(tok):
    return tok.strip().strip('*')

lines=open("GRE-Lexicon-Master-Handbook.md",encoding="utf-8").read().split("\n")
s=next(i for i,l in enumerate(lines) if l.startswith("## 2."))
e=next(i for i,l in enumerate(lines) if l.startswith("## 3."))
changed=0
for i in range(s,e):
    l=lines[i]
    if not l.startswith("| ") or l.startswith("| #"): continue
    cells=[c for c in l.split("|")]
    # raw cells incl spaces; the actual fields are cells[1..]
    fields=[c.strip() for c in l.strip().strip("|").split("|")]
    if len(fields) not in (6,9): continue
    word=norm_word(fields[1]); root=fields[4]
    parts=root.split(" + ")
    first=True
    new=[]
    for p in parts:
        if is_prefix(p):
            key=prefix_key(p)
            gloss = OVR.get(word) if first else None
            if gloss is None: gloss = DEFAULT.get(key)
            if gloss:
                # keep italic wrapping if present
                if p.strip().startswith('*') and p.strip().endswith('*'):
                    p = p.strip()[:-1] + f" ({gloss})" if False else p  # keep simple
                p = re.sub(r'(\*?'+re.escape(key)+r'\*?)', r'\1 ('+gloss+')', p, count=1)
            first=False
        else:
            if not is_prefix(p): first=False
        new.append(p)
    newroot=" + ".join(new)
    if newroot!=root:
        # rebuild line preserving outer structure
        fields[4]=newroot
        lines[i]="| "+" | ".join(fields)+" |"
        changed+=1
        if DRY and changed<=90:
            print(f"{word:20} -> {newroot}")
print("rows changed:",changed, "(dry-run)" if DRY else "(written)")
if not DRY:
    open("GRE-Lexicon-Master-Handbook.md","w",encoding="utf-8").write("\n".join(lines))
