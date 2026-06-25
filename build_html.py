#!/usr/bin/env python3
"""Build a clean, editorial reading website for the GRE lexicon handbook.
   No tests, no study markers, no emojis — just the words, organised by root and
   meaning, each with example / synonym / antonym / root. One cohesive theme,
   a collapsible sidebar, and section-at-a-time navigation. Testing lives on the
   separate /test page (test.html)."""
import re, subprocess, html

MD = "GRE-Lexicon-Master-Handbook.md"
OUTS = ["index.html", "GRE-Lexicon-Master-Handbook.html"]

body = subprocess.run(
    ["pandoc", MD, "-f", "gfm", "-t", "html", "--syntax-highlighting=none"],
    capture_output=True, text=True, check=True).stdout

# one-line description per section (no icons, no per-section colours)
DESC = {
    "1":  "How the handbook works, and the method to learn any word.",
    "2":  "The 250 words that matter most — start here if you're short on time.",
    "3":  "Words learned in root families — the highest-leverage way to remember.",
    "4":  "Words grouped by meaning, so you can tell close synonyms apart.",
    "5":  "Ready-made synonym pairs for Sentence Equivalence.",
    "6":  "Positive / negative / neutral logic for Text Completion.",
    "7":  "Look-alike words the GRE deliberately uses as traps.",
    "8":  "Every thematic word group, fully listed.",
    "9":  "Active-recall flashcards.",
    "10": "A day-by-day spaced-revision schedule.",
    "11": "All 775 words A–Z in full detail, with instant search.",
}
def secnum(text):
    m = re.match(r'\s*(\d+)\.', text); return m.group(1) if m else None
def strip_num(text):
    return re.sub(r'^\s*\d+\.\s*', '', text).strip()

# live-search bar after the glossary heading
SEARCH_BAR = (
    '\n<div class="gloss-search">'
    '<input id="glossSearch" type="search" autocomplete="off" '
    'placeholder="Search the glossary — type a word or part of a meaning…">'
    '<span class="cnt" id="glossCount"></span></div>\n'
)
body = re.sub(r'(<h2 id="11-master-az-glossary-every-word">.*?</h2>)',
              r'\1' + SEARCH_BAR.replace('\\', '\\\\'), body, count=1, flags=re.S)

# split body into sections at each <h2>, wrap each as a routed .page
parts = re.split(r'(<h2 id="[^"]+">.*?</h2>)', body, flags=re.S)
title_m = re.search(r'<h1[^>]*>(.*?)</h1>', parts[0], re.S)
SITE_TITLE = re.sub(r'<[^>]+>', '', title_m.group(1)).strip() if title_m else "GRE Lexicon Master Handbook"

nav_items, pages_html = [], []
i = 1
while i < len(parts):
    h2html, content = parts[i], parts[i+1] if i+1 < len(parts) else ""
    hid = re.search(r'id="([^"]+)"', h2html).group(1)
    text = re.sub(r'<[^>]+>', '', re.search(r'<h2[^>]*>(.*?)</h2>', h2html, re.S).group(1)).strip()
    i += 2
    if hid == "table-of-contents":
        continue
    n = secnum(text)
    desc = DESC.get(n, "")
    nav_items.append((hid, n, text))
    h2disp = re.sub(r'(<h2[^>]*>)\s*\d+\.\s*', r'\1', h2html)  # drop "3." — the kicker shows it
    head = (f'<div class="kicker">Section {n}</div>'
            f'{h2disp}'
            f'<p class="ph-desc">{html.escape(desc)}</p>'
            f'<div class="page-rule"></div>')
    pages_html.append(f'<section class="page" id="page-{hid}">{head}{content}</section>')

# sidebar nav
nav_links = ['<li><a class="nav-link active" href="#" data-page="page-home">Home</a></li>']
for hid, n, text in nav_items:
    nav_links.append(
        f'<li><a class="nav-link" href="#{hid}" data-page="page-{hid}">'
        f'<span class="nl-num">{n}</span><span class="nl-txt">{html.escape(strip_num(text))}</span></a></li>')
nav_html = "\n".join(nav_links)

# home
STATS = [("775", "words"), ("215", "high-priority"), ("36", "root families"), ("31", "word lists")]
stat_html = "".join(f'<div class="stat"><span class="num">{v}</span><span class="lab">{l}</span></div>'
                    for v, l in STATS)
idx_rows = "".join(
    f'<a href="#{hid}"><span class="n">{n}</span><span class="t">{html.escape(strip_num(text))}</span>'
    f'<span class="d">{html.escape(DESC.get(n, ""))}</span></a>'
    for hid, n, text in nav_items)
home_html = f"""
<section class="page home active" id="page-home">
  <div class="hero">
    <div class="kicker">GRE Verbal · Text Completion · Sentence Equivalence</div>
    <h1>The GRE Lexicon</h1>
    <p class="sub">775 high-frequency words, organised the way the test actually rewards —
       in root families and meaning clusters, each with its meaning, an example, synonyms,
       antonyms, and its root where one exists.</p>
    <div class="cta">
      <a class="btn primary" href="#3-root-word-encyclopedia">Browse by root</a>
      <a class="btn ghost" href="#11-master-az-glossary-every-word">A–Z glossary</a>
      <a class="btn link" href="test.html">Practice tests &rarr;</a>
    </div>
    <div class="stats">{stat_html}</div>
  </div>
  <h2 class="home-h">Contents</h2>
  <div class="idx">{idx_rows}</div>
</section>
"""

CSS = """
:root{
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif;
  --bg:#f5f4f0; --surface:#ffffff; --ink:#211f1a; --muted:#6b665d; --faint:#938d82;
  --line:#e7e3da; --accent:#35487a; --accent-d:#27375f; --accent-soft:#eef1f8; --gold:#9a7b2e;
  --sidebar-w:272px; --content-w:1060px; --head-top:14px;
  --shadow:0 1px 2px rgba(30,28,22,.04),0 10px 26px rgba(30,28,22,.06);
}
*{box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{margin:0; background:var(--bg); color:var(--ink); font-family:var(--sans);
  font-size:16.5px; line-height:1.72; -webkit-font-smoothing:antialiased;}
a{color:var(--accent); text-decoration:none;}
a:hover{text-decoration:underline;}

/* ===== layout + collapsible sidebar ===== */
.layout{display:flex; align-items:flex-start;}
.sidebar{width:var(--sidebar-w); flex:0 0 auto; position:sticky; top:0; height:100vh;
  overflow-y:auto; background:var(--surface); border-right:1px solid var(--line);
  padding:20px 14px 40px; margin-left:0; transition:margin-left .26s ease;}
.sb-head{display:flex; align-items:center; justify-content:space-between; padding:4px 8px 14px;}
.brand{font-family:var(--serif); font-weight:800; font-size:17px; color:var(--ink); line-height:1.15;}
.brand:hover{text-decoration:none;}
.brand span{display:block; font-family:var(--sans); font-weight:500; font-size:11.5px; color:var(--faint);}
.icon-btn{width:30px; height:30px; border-radius:8px; border:1px solid var(--line); background:var(--surface);
  color:var(--muted); cursor:pointer; font-size:15px; line-height:1; display:grid; place-items:center;}
.icon-btn:hover{background:var(--accent-soft); color:var(--accent); border-color:var(--accent);}
.sidebar .heading{font-size:10.5px; text-transform:uppercase; letter-spacing:.09em; color:var(--faint); margin:10px 10px 6px;}
.sidebar ul{list-style:none; margin:0; padding:0;}
.nav-link{display:flex; align-items:center; gap:11px; padding:8px 11px; border-radius:9px;
  color:var(--muted); font-size:14px; line-height:1.3; border-left:3px solid transparent;}
.nav-link:hover{background:var(--accent-soft); color:var(--accent-d); text-decoration:none;}
.nav-link .nl-num{font-size:11px; font-weight:700; color:var(--faint); width:18px; text-align:center; flex:0 0 auto;}
.nav-link.active{background:var(--accent-soft); color:var(--accent-d); font-weight:700; border-left-color:var(--accent);}
.nav-link.active .nl-num{color:var(--accent);}
.sb-test{margin:16px 8px 4px; display:block; text-align:center; padding:10px; border-radius:10px;
  background:var(--accent); color:#fff; font-weight:600; font-size:13.5px;}
.sb-test:hover{background:var(--accent-d); text-decoration:none;}

body.nav-collapsed .sidebar{margin-left:calc(-1 * var(--sidebar-w));}
#openBtn{display:none; position:fixed; top:14px; left:14px; z-index:60; width:42px; height:42px;
  border-radius:11px; border:none; background:var(--accent); color:#fff; font-size:18px; cursor:pointer;
  box-shadow:var(--shadow); align-items:center; justify-content:center;}
body.nav-collapsed #openBtn{display:flex;}

.content{flex:1 1 auto; min-width:0; display:flex; justify-content:center; padding:0 40px;}
.content-inner{width:100%; max-width:var(--content-w); margin:38px 0 90px;}

/* ===== pages ===== */
.page{display:none; animation:fade .26s ease;}
.page.active{display:block;}
@keyframes fade{from{opacity:0; transform:translateY(6px);}to{opacity:1; transform:none;}}

/* ===== home ===== */
.kicker{font-size:11.5px; font-weight:700; text-transform:uppercase; letter-spacing:.09em; color:var(--accent); margin-bottom:8px;}
.hero{padding:14px 0 6px;}
.hero h1{font-family:var(--serif); font-size:3.1rem; line-height:1.04; font-weight:800; margin:0 0 16px;}
.hero .sub{font-size:1.12rem; color:var(--muted); max-width:60ch; margin:0;}
.cta{display:flex; flex-wrap:wrap; gap:12px; align-items:center; margin:26px 0 2px;}
.btn{padding:11px 21px; border-radius:11px; font-size:15px; font-weight:600; cursor:pointer; border:1px solid transparent;}
.btn.primary{background:var(--accent); color:#fff;}
.btn.primary:hover{background:var(--accent-d); text-decoration:none;}
.btn.ghost{background:var(--surface); border-color:var(--line); color:var(--ink);}
.btn.ghost:hover{border-color:var(--accent); color:var(--accent); text-decoration:none;}
.btn.link{color:var(--accent); padding:11px 6px;}
.stats{display:flex; flex-wrap:wrap; gap:38px; margin-top:30px; padding-top:24px; border-top:1px solid var(--line);}
.stat .num{display:block; font-family:var(--serif); font-size:1.9rem; font-weight:800; color:var(--accent); line-height:1;}
.stat .lab{font-size:11.5px; text-transform:uppercase; letter-spacing:.05em; color:var(--faint);}
.home-h{font-family:var(--serif); font-size:1.5rem; margin:42px 2px 16px; font-weight:800; border:none; padding:0;}
.idx{border:1px solid var(--line); border-radius:16px; overflow:hidden; background:var(--surface); box-shadow:var(--shadow);}
.idx a{display:flex; gap:18px; align-items:baseline; padding:15px 22px; border-bottom:1px solid var(--line); color:var(--ink);}
.idx a:last-child{border-bottom:none;}
.idx a:hover{background:var(--accent-soft); text-decoration:none;}
.idx .n{font-weight:700; font-size:13px; color:var(--accent); width:26px; flex:0 0 auto;}
.idx .t{font-family:var(--serif); font-weight:700; font-size:1.08rem;}
.idx .d{color:var(--muted); font-size:13.5px; margin-left:auto; text-align:right; max-width:50%;}

/* ===== section pages ===== */
.page > h2{font-family:var(--serif); font-size:2.2rem; font-weight:800; margin:.12em 0 .12em; border:none; padding:0;}
.ph-desc{color:var(--muted); font-size:1.04rem; margin:0;}
.page-rule{height:2px; background:linear-gradient(90deg,var(--accent),transparent 55%); margin:16px 0 26px; opacity:.5;}

/* ===== typography ===== */
h3{font-family:var(--serif); font-size:1.32rem; font-weight:700; margin:1.8em 0 .55em; color:var(--ink);
  scroll-margin-top:calc(var(--head-top) + 12px);}
h4{font-size:1.02rem; margin:1.4em 0 .5em; color:var(--muted);}
p{margin:.7em 0;}
ul,ol{padding-left:1.4em;}
li{margin:.28em 0;}
hr{border:0; border-top:1px solid var(--line); margin:2.2em 0;}
strong{color:var(--ink); font-weight:700;}

blockquote{margin:1.3em 0; padding:1em 1.2em; background:var(--accent-soft);
  border-left:4px solid var(--accent); border-radius:0 12px 12px 0; color:#2a2c34;}
blockquote p{margin:.4em 0;}
blockquote strong{color:var(--accent-d);}

code{background:var(--accent-soft); color:var(--accent-d); padding:.12em .45em; border-radius:6px;
  font-family:"SF Mono",SFMono-Regular,Consolas,Menlo,monospace; font-size:.85em; font-weight:600;}

/* ===== tables (sticky headers; NO overflow:hidden) ===== */
table{border-collapse:separate; border-spacing:0; width:100%; margin:1.3em 0; font-size:14.5px;
  background:var(--surface); border:1px solid var(--line); border-radius:12px; box-shadow:var(--shadow);}
th,td{border-bottom:1px solid var(--line); border-right:1px solid var(--line); padding:9px 12px; vertical-align:top; overflow-wrap:break-word;}
tr td:last-child, tr th:last-child{border-right:none;}
tbody tr:last-child td{border-bottom:none;}
thead th:first-child{border-top-left-radius:12px;}
thead th:last-child{border-top-right-radius:12px;}
tbody tr:last-child td:first-child{border-bottom-left-radius:12px;}
tbody tr:last-child td:last-child{border-bottom-right-radius:12px;}
table.wide{table-layout:fixed;}
table.wide th, table.wide td{word-break:break-word; padding:8px 9px;}
table.numbered th:nth-child(1), table.numbered td:nth-child(1){width:2.6em; white-space:nowrap;}
table.numbered th:nth-child(3), table.numbered td:nth-child(3){width:3em;}
table.gloss th:nth-child(1), table.gloss td:nth-child(1){width:11%;}
table.gloss th:nth-child(2), table.gloss td:nth-child(2){width:3.4em;}
table.gloss th:nth-child(3), table.gloss td:nth-child(3){width:19%;}
table.gloss th:nth-child(4), table.gloss td:nth-child(4){width:15%;}
table.gloss th:nth-child(5), table.gloss td:nth-child(5){width:5%;}
table.gloss th:nth-child(6), table.gloss td:nth-child(6){width:18%;}
table.gloss th:nth-child(7), table.gloss td:nth-child(7){width:15%;}
table.gloss th:nth-child(8), table.gloss td:nth-child(8){width:13%;}
thead th{background:var(--accent-soft); color:var(--accent-d); text-align:left; font-weight:700;
  position:-webkit-sticky; position:sticky; top:var(--head-top); z-index:5;}
thead th::before{content:""; position:absolute; left:0; right:0; bottom:100%;
  height:calc(var(--head-top) + 2px); background:var(--bg);}
tbody tr:nth-child(even){background:#faf9f6;}
tbody tr:hover{background:var(--accent-soft);}

.gloss-search{position:-webkit-sticky; position:sticky; top:var(--head-top); z-index:7;
  background:var(--bg); padding:10px 0; display:flex; gap:12px; align-items:center; margin-bottom:6px;}
.gloss-search::before{content:""; position:absolute; left:0; right:0; bottom:100%;
  height:calc(var(--head-top) + 2px); background:var(--bg);}
.gloss-search input{flex:1; padding:11px 15px; font-size:15.5px; border:1px solid var(--line);
  border-radius:11px; background:var(--surface); color:var(--ink); box-shadow:var(--shadow);}
.gloss-search input:focus{outline:2px solid var(--accent); border-color:var(--accent);}
.gloss-search .cnt{font-size:12.5px; color:var(--muted); white-space:nowrap;}
table.gloss thead th{top:calc(var(--head-top) + 58px);}

.backdrop{display:none;}
#toTop{position:fixed; right:22px; bottom:22px; width:46px; height:46px; border-radius:50%;
  background:var(--accent); color:#fff; border:none; font-size:21px; cursor:pointer;
  box-shadow:var(--shadow); opacity:0; pointer-events:none; transition:.2s; z-index:55;}
#toTop.show{opacity:1; pointer-events:auto;}
#toTop:hover{background:var(--accent-d);}

/* ===== responsive ===== */
@media (max-width:900px){
  .sidebar{position:fixed; left:0; top:0; z-index:50; width:80vw; max-width:300px; margin-left:0;
    transform:translateX(-100%); transition:transform .26s ease; box-shadow:4px 0 24px rgba(0,0,0,.25);}
  .sidebar.open{transform:translateX(0);}
  body.nav-collapsed .sidebar{margin-left:0;}
  #openBtn{display:flex !important;}
  .backdrop{position:fixed; inset:0; background:rgba(0,0,0,.42); z-index:45;}
  .backdrop.show{display:block;}
  .content{padding:0 16px;}
  .content-inner{margin:64px 0 70px;}
  .hero h1{font-size:2.3rem;}
  .page > h2{font-size:1.7rem;}
  .idx .d{display:none;}
  table{font-size:13px;}
  th,td{padding:7px 9px;}
}
@media (max-width:480px){
  body{font-size:15.5px;}
  .hero h1{font-size:2rem;}
  .stats{gap:22px;}
  table{font-size:12.5px;}
}
"""

JS = """
const sb=document.getElementById('sidebar'), bd=document.getElementById('backdrop'), bodyEl=document.body;
const mobile=()=>window.matchMedia('(max-width:900px)').matches;
function closeDrawer(){sb.classList.remove('open');bd.classList.remove('show');}
function openDrawer(){sb.classList.add('open');bd.classList.add('show');}
function setCollapsed(c){bodyEl.classList.toggle('nav-collapsed',c); try{localStorage.setItem('gre_sb',c?'1':'0');}catch(e){}}
document.getElementById('collapseBtn').addEventListener('click',()=>{ mobile()?closeDrawer():setCollapsed(true); });
document.getElementById('openBtn').addEventListener('click',()=>{ mobile()?openDrawer():setCollapsed(false); });
bd.addEventListener('click',closeDrawer);
try{ if(!mobile() && localStorage.getItem('gre_sb')==='1') bodyEl.classList.add('nav-collapsed'); }catch(e){}

// ----- page router (one section at a time) -----
const pages=[...document.querySelectorAll('.page')];
const navlinks=[...document.querySelectorAll('[data-page]')];
function setActive(pid){
  pages.forEach(p=>p.classList.toggle('active',p.id===pid));
  navlinks.forEach(a=>a.classList.toggle('active',a.dataset.page===pid));
}
function pageFor(id){ const el=id&&document.getElementById(id); const pg=el?el.closest('.page'):null; return pg?pg.id:'page-home'; }
function go(id){
  const pid=pageFor(id); setActive(pid);
  const el=id&&document.getElementById(id);
  if(el && el.tagName!=='H2' && !el.classList.contains('page') && el.id!==pid){ el.scrollIntoView({block:'start'}); }
  else { (document.scrollingElement||document.documentElement).scrollTop=0; }
  if(mobile()) closeDrawer();
}
document.addEventListener('click',e=>{
  const a=e.target.closest('a[href^="#"]'); if(!a) return;
  e.preventDefault(); const id=a.getAttribute('href').slice(1);
  history.replaceState(null,'', id?('#'+id):'#'); go(id);
});
addEventListener('hashchange',()=>go(location.hash.slice(1)));
go(location.hash.slice(1));

// ----- glossary live search -----
const gh=document.getElementById('11-master-az-glossary-every-word');
const gInput=document.getElementById('glossSearch'), gCount=document.getElementById('glossCount');
if(gh && gInput){
  let els=[], n=gh.nextElementSibling; while(n){els.push(n); n=n.nextElementSibling;}
  const tables=els.filter(e=>e.tagName==='TABLE'); tables.forEach(t=>t.classList.add('gloss'));
  gInput.addEventListener('input',()=>{
    const q=gInput.value.trim().toLowerCase(); let shown=0;
    tables.forEach(t=>{
      let vis=0; const tb=t.tBodies[0];
      if(tb){[...tb.rows].forEach(r=>{const hit=q===''||r.textContent.toLowerCase().includes(q);
        r.style.display=hit?'':'none'; if(hit)vis++;});}
      t.style.display=vis?'':'none';
      const h=t.previousElementSibling; if(h&&h.tagName==='H3')h.style.display=vis?'':'none';
      shown+=vis;
    });
    gCount.textContent=q?(shown+' match'+(shown===1?'':'es')):'';
  });
}

// ----- lock wide tables to container width -----
document.querySelectorAll('table').forEach(t=>{
  const h=t.tHead||t.querySelector('thead');
  if(h && h.rows[0] && h.rows[0].cells.length>=6){ t.classList.add('wide');
    if(h.rows[0].cells[0].textContent.trim()==='#') t.classList.add('numbered'); }
});

// ----- back to top -----
const btn=document.getElementById('toTop');
addEventListener('scroll',()=>{btn.classList.toggle('show',scrollY>500);});
btn.addEventListener('click',()=>scrollTo({top:0,behavior:'smooth'}));
"""

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(SITE_TITLE)}</title>
<style>{CSS}</style>
</head>
<body>
<button id="openBtn" aria-label="Open menu">&#9776;</button>
<div class="backdrop" id="backdrop"></div>
<div class="layout">
  <aside class="sidebar" id="sidebar">
    <div class="sb-head">
      <a class="brand" href="#">GRE Lexicon<span>Master Handbook</span></a>
      <button id="collapseBtn" class="icon-btn" aria-label="Collapse menu" title="Collapse">&#10094;</button>
    </div>
    <a class="sb-test" href="test.html">Practice tests &rarr;</a>
    <div class="heading">Sections</div>
    <nav><ul>
{nav_html}
    </ul></nav>
  </aside>
  <main class="content">
    <article class="content-inner">
{home_html}
{''.join(pages_html)}
    </article>
  </main>
</div>
<button id="toTop" aria-label="Back to top">&#8593;</button>
<script>{JS}</script>
</body>
</html>
"""

for out in OUTS:
    open(out, "w", encoding="utf-8").write(page)
print(f"Wrote {', '.join(OUTS)} — {len(nav_items)} sections, clean theme, no tests/markers/emojis.")
