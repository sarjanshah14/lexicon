#!/usr/bin/env python3
"""Repair rows where the high-frequency '*' leaked into the Meaning column."""
import re
path = "GRE-Lexicon-Master-Handbook.md"
lines = open(path, encoding="utf-8").read().split("\n")
fixed = 0
for i, l in enumerate(lines):
    if not l.startswith("| ") or l.count("|") != 7:
        continue
    cells = [c.strip() for c in l.strip().strip("|").split("|")]
    if len(cells) != 6:
        continue
    num, word, pos, meaning, root, synant = cells
    m = re.match(r'^\*\s*\((.*?)\)\s*[—\-]\s*(.*)$', meaning)
    if m:
        pos = m.group(1).strip()
        meaning = m.group(2).strip()
        # add star to the word (inside the bold)
        if word.endswith("**") and not word.endswith("\\***"):
            word = word[:-2] + "\\*" + "**"
        fixed += 1
        lines[i] = f"| {num} | {word} | {pos} | {meaning} | {root} | {synant} |"
open(path, "w", encoding="utf-8").write("\n".join(lines))
print("Fixed rows:", fixed)
