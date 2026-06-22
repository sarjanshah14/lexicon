#!/usr/bin/env python3
import re, json, sys
from collections import Counter

lines = open('GRE-Lexicon-2024.txt', encoding='utf-8').read().split('\n')
region = list(enumerate(lines))[104:2890]

def is_noise(ln):
    s = ln.strip()
    if not s: return True
    if re.fullmatch(r'\d+', s): return True
    if s.startswith('GRE'): return True
    if re.match(r'^Wordlist \d+', s): return True
    if s in ('Sr.', 'No'): return True
    if 'Word Classes / Meaning' in ln: return True
    if 'Centre for' in s or s.startswith('International') or s == 'Education': return True
    if s.startswith('IMS-'): return True
    return False

blocks = []; cur = []
for idx, ln in region:
    if 'Word Classes / Meaning' in ln:
        if cur: blocks.append(cur); cur = []
        continue
    if is_noise(ln): continue
    cur.append((idx, ln))
if cur: blocks.append(cur)

entry_re = re.compile(r'^\s*(\d{1,2})\s+([A-Za-zâàéíﬁﬂﬀﬃﬄ])')

def col_starts(blk):
    starts = Counter()
    for _, l in blk:
        for i in range(2, len(l)):
            if l[i] != ' ' and l[i-1] == ' ' and l[i-2] == ' ':
                starts[i] += 1
    peaks = sorted([c for c, n in starts.items() if n >= 3])
    def pick(lo, hi, default):
        cand = [c for c in peaks if lo <= c <= hi]
        return min(cand) if cand else default
    mean_c = pick(14, 40, 20)
    syn_c  = pick(78, 102, 88)
    ant_c  = pick(106, 128, 115)
    return mean_c, syn_c, ant_c

def fix(s):
    return (s.replace('ﬁ','fi').replace('ﬂ','fl').replace('ﬀ','ff')
             .replace('ﬃ','ffi').replace('ﬄ','ffl').replace('’',"'")
             .replace('‘',"'").replace('–','-').replace('“','"').replace('”','"')
             .replace('ﬅ','ft'))

def gaps(line):
    return [(mm.start(), mm.end()) for mm in re.finditer(r' {2,}', line)]

def snap_space(line, c):
    """Return a field-start boundary near column c that never falls inside a word.
    Prefer a real 2+-space gutter within range; otherwise snap to the nearest single
    space and return the start of the following field (whole words preserved)."""
    if c >= len(line):
        return len(line)
    # prefer a real gutter whose END is closest to c
    g = [e for (s, e) in gaps(line) if abs(e - c) <= 14]
    if g:
        return min(g, key=lambda e: abs(e - c))
    # else snap to nearest space character
    best = None
    for j in range(len(line)):
        if line[j] == ' ':
            if best is None or abs(j - c) < abs(best - c):
                best = j
    if best is None:
        return c
    j = best
    while j < len(line) and line[j] == ' ':
        j += 1
    return j

def split_line(l, mc, sc, ac):
    s2 = snap_space(l, sc)
    a2 = snap_space(l, ac)
    s2 = max(s2, mc)
    if a2 <= s2:
        a2 = len(l)
    return l[mc:s2].strip(), l[s2:a2].strip(), l[a2:].strip()

all_entries = []
for blk in blocks:
    mc, sc, ac = col_starts(blk)
    cur = None
    for idx, l in blk:
        m = entry_re.match(l)
        indent = len(l) - len(l.lstrip())
        if m and indent < mc:
            if cur: all_entries.append(cur)
            # word = leading token after the number, up to the first 2+ space gap
            after_num = re.sub(r'^\s*\d{1,2}\s+', '', l)
            offset = len(l) - len(after_num)
            gg = gaps(after_num)
            wcol = mc - offset  # width of the word column in this row
            if gg and gg[0][0] <= wcol + 6:
                # normal row: the first real gutter ends the headword
                word_part = after_num[:gg[0][0]].strip()
            else:
                # collapsed gutter: headword = first token (+ one extra lowercase token
                # for 2-word headwords like "faux pas"); stop at the capitalized meaning.
                toks = after_num.split()
                wtoks = toks[:1]
                if len(toks) > 1 and toks[1][:1].isalpha() and toks[1][:1].islower():
                    wtoks.append(toks[1])
                word_part = ' '.join(wtoks).strip()
            mp, sp, ap = split_line(l, mc, sc, ac)
            cur = {'word': word_part, 'mean': [mp], 'syn': [sp], 'ant': [ap]}
        else:
            if cur is None: continue
            mp, sp, ap = split_line(l, mc, sc, ac)
            cur['mean'].append(mp); cur['syn'].append(sp); cur['ant'].append(ap)
    if cur: all_entries.append(cur)

def clean_join(parts):
    return re.sub(r'\s+', ' ', ' '.join(p for p in parts if p)).strip()

out = []
for e in all_entries:
    word = fix(e['word'])
    star = '*' in word
    wc = word.replace('*', '').strip()
    if not wc or not re.match(r'^[A-Za-z]', wc): continue
    mean = fix(clean_join(e['mean']))
    syn = fix(clean_join(e['syn'])).strip(' ,-')
    ant = fix(clean_join(e['ant'])).strip(' ,-')
    out.append({'word': wc, 'star': star, 'mean': mean, 'syn': syn, 'ant': ant})

# de-dup exact word repeats (keep first)
seen = {}
final = []
for e in out:
    k = e['word'].lower()
    if k in seen:
        continue
    seen[k] = True
    final.append(e)

print(f"TOTAL: {len(out)}  UNIQUE: {len(final)}", file=sys.stderr)
json.dump(final, open('glossary.json', 'w'), indent=1)
for e in final[:6] + final[200:204]:
    print((e['word']+('*' if e['star'] else '')).ljust(15), '|', e['mean'][:48])
    print(' '*15, ' S:', e['syn'][:42], '| A:', e['ant'][:30])
