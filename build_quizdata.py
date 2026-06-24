#!/usr/bin/env python3
"""Generate quizdata.js (window.QUIZ) from the handbook's own data:
   - words   : every glossary word with a concise meaning + syn/ant (for auto MCQs)
   - roots   : each §3 root family -> its testable member words (for 'test only studied roots')
   - clusters: each §4 semantic cluster -> its member words (for SE / odd-one-out)
All answers come straight from the source, so nothing is invented."""
import re, json

g = json.load(open("glossary.json"))
md = open("GRE-Lexicon-Master-Handbook.md", encoding="utf-8").read()

WORDSET = {e["word"].lower() for e in g}

def short_mean(m):
    m = re.sub(r'\b\d\]\s*', '', m).strip()          # drop "1] " sense markers
    m = m.split(';')[0]
    # keep just the first sense/sentence when several are concatenated
    sent = re.split(r'(?<=[a-z])\.\s+(?=[A-Z])', m)
    if sent and len(sent[0]) >= 18:
        m = sent[0]
    ci = m.find(':')
    if ci > 18: m = m[:ci]                            # cut an illustrative ": example"
    m = m.strip(' ;.,-')
    if len(m) > 95:
        m = m[:95].rsplit(' ', 1)[0] + '…'
    return m

def split_list(s):
    out = []
    for t in re.split(r'[,;]', s or ""):
        t = t.strip(' .')
        if len(t) >= 2 and re.search(r'[a-zA-Z]', t):
            out.append(t)
    return out

# ---- words ----
words = []
for e in g:
    words.append({
        "w": e["word"],
        "m": short_mean(e["mean"]),
        "s": split_list(e.get("syn", ""))[:4],
        "a": split_list(e.get("ant", ""))[:4],
        "hf": bool(e.get("star")),
    })

# ---- roots (§3) ----
s3 = md[md.index("## 3."):md.index("## 4.")]
roots = []
for m in re.finditer(r'^### (.+)$', s3, re.M):
    header = m.group(1)
    if '=' not in header:        # skip "Additional high-yield mini-roots" sub-header
        continue
    # block = from this header to the next ### / ## / end
    start = m.end()
    nxt = re.search(r'^#{2,3} ', s3[start:], re.M)
    block = s3[start: start + (nxt.start() if nxt else len(s3))]
    label = re.sub(r'`', '', header.split('=')[0]).strip(' /')
    mean  = header.split('=', 1)[1].strip()
    mean  = re.sub(r'\s*\*.*$', '', mean).strip()       # drop trailing "— note"
    # member words = bolded tokens that exist in the glossary
    members = []
    for b in re.findall(r'\*\*([^*]+)\*\*', block):
        for tok in re.findall(r"[A-Za-z][A-Za-z'-]+", b):
            lw = tok.lower()
            if lw in WORDSET and lw not in members:
                members.append(lw)
    # keep every root family (even one with no glossary member words) so the on-page
    # "studied up to here" markers line up 1:1 with this list
    roots.append({"root": label, "mean": mean, "words": members})

# ---- clusters (§4) ----
s4 = md[md.index("## 4."):md.index("## 5.")]
clusters = []
for m in re.finditer(r'^### (4\.\d+) (.+)$', s4, re.M):
    name = m.group(2).strip()
    start = m.end()
    nxt = re.search(r'^### ', s4[start:], re.M)
    block = s4[start: start + (nxt.start() if nxt else len(s4))]
    wm = re.search(r'\*\*Words:\*\*\s*(.+)', block)
    if not wm: continue
    raw = re.sub(r'\*', '', wm.group(1))
    members = [t for t in split_list(raw) if t.lower() in WORDSET]
    if len(members) >= 4:
        clusters.append({"name": name.title(), "words": [w.lower() for w in members]})

data = {"words": words, "roots": roots, "clusters": clusters}
js = "window.QUIZ = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n"
open("quizdata.js", "w", encoding="utf-8").write(js)
print(f"quizdata.js: {len(words)} words, {len(roots)} roots, {len(clusters)} clusters")
print("roots:", ", ".join(r["root"] for r in roots))
