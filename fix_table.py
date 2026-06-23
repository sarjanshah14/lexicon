#!/usr/bin/env python3
"""Convert the Top 101-250 numbered list in the handbook into a clean Markdown table."""
import re

path = "GRE-Lexicon-Master-Handbook.md"
doc = open(path, encoding="utf-8").read()
lines = doc.split("\n")

# find the numbered entries 101..250
start = next(i for i, l in enumerate(lines) if l.startswith("These extend the priority set."))
end = next(i for i, l in enumerate(lines) if re.match(r'^250\.\s', l))

rows = []
for l in lines[start:end+1]:
    m = re.match(r'^(\d+)\.\s+(.*)$', l)
    if not m:
        continue
    num, rest = m.group(1), m.group(2).strip()
    # word
    wm = re.match(r'^\*\*(.+?)\*\*', rest)
    word = wm.group(1).strip() if wm else ""
    rest2 = rest[wm.end():].strip() if wm else rest
    # cross-reference rows: "— *(see #39)*"
    see = re.search(r'\(see #(\d+)\)', rest2)
    # POS
    pos = ""
    pm = re.match(r'^\((.*?)\)', rest2)
    if pm:
        pos = pm.group(1).strip()
        rest2 = rest2[pm.end():].strip()
    # drop leading dash
    rest2 = re.sub(r'^[—\-]\s*', '', rest2).strip()
    if see and "—" not in rest2 and "·" not in rest2:
        rows.append((num, word, pos, f"see entry #{see.group(1)} for full treatment", "", ""))
        continue
    # split by middle dot
    segs = [s.strip() for s in rest2.split("·") if s.strip()]
    meaning = segs[0] if segs else ""
    root = ""
    synant = ""
    notes = []
    for s in segs[1:]:
        if "→" in s:
            synant = s
        elif "CP:" in s or s.startswith("(CP"):
            notes.append(s.strip("()"))
        elif re.search(r'\*.*\*', s) or "(" in s and not root:
            root = s
        elif not root:
            root = s
        else:
            notes.append(s)
    root = root.replace("*", "")
    if notes:
        meaning = meaning + " — " + "; ".join(n.replace("*", "") for n in notes)
    # tidy syn → ant: keep the arrow
    synant = synant.replace("→ —", "→ —")
    rows.append((num, word, pos, meaning, root, synant))

# build table
out = []
out.append("These are the **next 150 highest-value words** (ranks 101–250). Same priority logic as the Top 100: frequency, usefulness across TC/SE/RC, and memorability. **How to read a row:** learn the *meaning* first, anchor it with the *root/hook*, then use *synonyms → antonyms* to lock the word into its meaning-family (that pairing is exactly what Sentence Equivalence tests). `*` = high-frequency. **CP** = a commonly-confused look-alike (see §7).")
out.append("")
out.append("| # | Word | POS | Meaning | Root / hook | Synonyms → Antonyms |")
out.append("|---|---|---|---|---|---|")
for num, word, pos, meaning, root, synant in rows:
    w = f"**{word}**"
    out.append(f"| {num} | {w} | {pos} | {meaning} | {root} | {synant} |")

new_block = "\n".join(out)
old_block = "\n".join(lines[start:end+1])
doc = doc.replace(old_block, new_block, 1)
open(path, "w", encoding="utf-8").write(doc)
print(f"Replaced list with table: {len(rows)} rows.")
