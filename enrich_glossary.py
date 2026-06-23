#!/usr/bin/env python3
"""Rebuild §11 as a full-detail glossary: every word gets POS, Root, Tags, Memory hook
(merged from §2 where it exists, else from the authored extra1/2/3 batches)."""
import re, json
from collections import defaultdict
import extra1, extra2, extra3

g = json.load(open("glossary.json"))
enr = json.load(open("enr2.json"))
EXTRA = {}
for mod in (extra1, extra2, extra3):
    EXTRA.update(mod.D)

# CP set: words that appear in §7 Common Confusing Words
md = open("GRE-Lexicon-Master-Handbook.md", encoding="utf-8").read()
s7 = md[md.index("## 7."):md.index("## 8.")]
cp = set(w.lower() for w in re.findall(r'\*([a-zA-Zé -]+)\*', s7))

def short_mean(m):
    m = re.sub(r'\b\d\]\s*', '', m).strip()
    ci = m.find(':')
    if ci > 18: m = m[:ci]
    m = m.strip(' ;.,-')
    if len(m) > 110:
        m = m[:110].rsplit(' ', 1)[0] + '…'
    return m

def cell(x): return (x or "").replace("|", "/").strip()

rows = []
missing = []
for e in g:
    w = e["word"]; key = w.lower()
    star = e["star"]
    pos = root = hook = ""
    tags = []
    if key in enr:
        d = enr[key]
        pos = d.get("pos", ""); root = d.get("root", ""); hook = d.get("hook", "")
        if d.get("tags"): tags.append(d["tags"])
    elif key in EXTRA:
        pos, root, hook = EXTRA[key]
    else:
        missing.append(w)
    # tags: ensure HF for starred, add CP if a confusing-pair word
    tagstr = "·".join(t for t in tags if t).strip("·")
    if star and "HF" not in tagstr:
        tagstr = ("HF·" + tagstr).strip("·") if tagstr else "HF"
    if key in cp and "CP" not in tagstr:
        tagstr = (tagstr + "·CP").strip("·") if tagstr else "CP"
    if not tagstr:
        tagstr = "—"
    rows.append({
        "word": w + ("\\*" if star else ""),
        "pos": cell(pos) or "—",
        "mean": cell(short_mean(e["mean"])),
        "root": cell(root) or "(possible root)",
        "tags": cell(tagstr),
        "hook": cell(hook) or "—",
        "syn": cell(e["syn"]) or "—",
        "ant": cell(e["ant"]) or "—",
        "sort": key,
    })

print("rows:", len(rows), " unmatched:", len(missing))
if missing: print("UNMATCHED:", missing[:30])

rows.sort(key=lambda r: r["sort"])
buckets = defaultdict(list)
for r in rows:
    buckets[r["word"][0].upper()].append(r)

star_total = sum(1 for r in rows if "\\*" in r["word"])
out = []
out.append("## 11. Master A–Z Glossary (Every Word)\n")
out.append(f"> **Every one of the {len(rows)} words, in full detail** — the same columns the high-priority words get: **POS, Short meaning, Root, Tags, Memory hook, Synonyms, Antonyms**. Meanings/synonyms/antonyms are taken faithfully from the source; roots and memory hooks are added for every word, and any etymology that isn't certain is marked **\"(possible root)\"** rather than invented. `*` = high-frequency. **Tags:** HF = high-frequency · CP = part of a classic confusing pair (§7). The table is wide — drag it sideways inside its frame; the header stays frozen.\n")
out.append(f"**Total words: {len(rows)}  ·  High-frequency (\\*): {star_total}**\n")
for letter in sorted(buckets):
    out.append(f"### {letter}\n")
    out.append("| Word | POS | Short meaning | Root | Tags | Memory hook | Synonyms | Antonyms |")
    out.append("|---|---|---|---|---|---|---|---|")
    for r in buckets[letter]:
        out.append(f"| **{r['word']}** | {r['pos']} | {r['mean']} | {r['root']} | {r['tags']} | {r['hook']} | {r['syn']} | {r['ant']} |")
    out.append("")
out.append("---\n")
out.append("*End of the GRE Lexicon Master Handbook. Every source word is represented above with full detail. Good luck — now go drill the leech deck.*\n")

new_s11 = "\n".join(out)
# replace existing §11 (it is the last section)
idx = md.index("## 11. Master")
md = md[:idx] + new_s11
open("GRE-Lexicon-Master-Handbook.md", "w", encoding="utf-8").write(md)
print("Rebuilt §11 with full detail.")
