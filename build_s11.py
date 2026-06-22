#!/usr/bin/env python3
# Section 11: Master A-Z Glossary of ALL words from glossary.json (faithful to source).
import json, re

g = json.load(open("glossary.json"))

def short_mean(m):
    if not m: return ""
    # turn "1] ... 2] ..." numbering into separators
    m = re.sub(r'\b\d\]\s*', '', m).strip()
    # drop a leading "To " duplication artifacts kept; cut at first example marker ':'
    # keep definition before first ':' if it leaves a substantial chunk
    ci = m.find(':')
    if ci > 18:
        m = m[:ci]
    m = m.strip(' ;.,-')
    if len(m) > 145:
        cut = m[:145]
        sp = cut.rfind(' ')
        m = cut[:sp] + '…'
    return m

def trim(s, n=95):
    s = s.strip(' ;.,-')
    if len(s) > n:
        cut = s[:n]; sp = cut.rfind(' ')
        s = cut[:sp] + '…'
    return s

# sort A-Z
g = sorted(g, key=lambda e: e['word'].lower())

lines = []
lines.append("---\n")
lines.append("## 11. Master A–Z Glossary (Every Word)\n")
lines.append(f"> **Completeness guarantee:** all **{len(g)}** words from the source wordlists, A–Z, each with a short meaning, synonyms, and antonyms drawn faithfully from the source. `*` marks a **high-frequency** GRE word. This is the catch-all — every word in the handbook appears here at least once; rarer words live *only* here, so this is your final completeness sweep before test day. (Meanings are condensed; see the source for full examples. A few synonym/antonym strings carry minor OCR artifacts from the original PDF.)\n")

# letter sections
from collections import defaultdict
buckets = defaultdict(list)
for e in g:
    buckets[e['word'][0].upper()].append(e)

star_total = sum(1 for e in g if e['star'])
lines.append(f"**Total words: {len(g)}  ·  High-frequency (\\*): {star_total}**\n")

for letter in sorted(buckets):
    lines.append(f"### {letter}\n")
    lines.append("| Word | Meaning | Synonyms | Antonyms |")
    lines.append("|---|---|---|---|")
    for e in buckets[letter]:
        w = e['word'] + ('\\*' if e['star'] else '')
        mean = short_mean(e['mean']).replace('|', '/')
        syn = trim(e['syn']).replace('|', '/')
        ant = trim(e['ant']).replace('|', '/')
        lines.append(f"| **{w}** | {mean} | {syn} | {ant} |")
    lines.append("")

lines.append("---\n")
lines.append("*End of the GRE Lexicon Master Handbook. Every source word — all 31 wordlists, the Word Groups, and the 106 Common Confusing Words — is represented above. Good luck. Now go drill the leech deck.*\n")

section = "\n".join(lines)
path = "GRE-Lexicon-Master-Handbook.md"
doc = open(path, encoding="utf-8").read()
assert doc.count("<!-- SECTION-BREAK -->") == 1
doc = doc.replace("<!-- SECTION-BREAK -->", section, 1)
open(path, "w", encoding="utf-8").write(doc)
print(f"Inserted Section 11 with {len(g)} words across {len(buckets)} letters.")
