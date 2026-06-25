#!/usr/bin/env python3
"""Build a real multi-page website from the handbook Markdown:
   - a home page (hero + colourful section cards),
   - one routed "page" per section (no more endless scroll),
   - colour-coded section headers, cards, badges, restyled sidebar.
   The quiz launchers and study markers are preserved (h2 ids + sibling order intact)."""
import re, subprocess, html, json

MD = "GRE-Lexicon-Master-Handbook.md"
OUTS = ["index.html", "GRE-Lexicon-Master-Handbook.html"]

body = subprocess.run(
    ["pandoc", MD, "-f", "gfm", "-t", "html", "--syntax-highlighting=none"],
    capture_output=True, text=True, check=True).stdout

# ---------- per-section presentation metadata ----------
META = {
    "1":  ("How to Use",     "🧭", "How the handbook works, and the 4-step method to learn any word."),
    "2":  ("High-Priority",  "⭐", "The 250 words that matter most — start here if you're short on time."),
    "3":  ("Roots",          "🌳", "Learn words in root families — the single highest-leverage method."),
    "4":  ("Clusters",       "🧩", "Words grouped by meaning, so you can tell close synonyms apart."),
    "5":  ("SE Pairs",       "🔗", "Ready-made synonym pairs built for Sentence Equivalence."),
    "6":  ("TC Polarity",    "⚖️", "Positive / negative / neutral logic for Text Completion."),
    "7":  ("Confusing",      "⚠️", "Look-alike words the GRE deliberately uses as traps."),
    "8":  ("Word Groups",    "🗂️", "Every thematic word group, fully listed for broad coverage."),
    "9":  ("Flashcards",     "🎴", "Active-recall flashcards — test yourself, don't reread."),
    "10": ("Revision",       "📅", "A day-by-day spaced-revision schedule to lock words in."),
    "11": ("Glossary",       "📚", "All 775 words A–Z in full detail, with instant search."),
}
ACCENTS = {
    "1":("#3b82f6","#ebf2fe"), "2":("#f59e0b","#fef3e2"), "3":("#10b981","#e5f7f1"),
    "4":("#8b5cf6","#f1ecfe"), "5":("#ec4899","#fdebf4"), "6":("#14b8a6","#e5f7f5"),
    "7":("#ef4444","#fdeceb"), "8":("#6366f1","#ecedfd"), "9":("#f97316","#fef0e6"),
    "10":("#0ea5e9","#e6f5fd"), "11":("#22c55e","#e8f9ef"),
}
def secnum(text):
    m = re.match(r'\s*(\d+)\.', text); return m.group(1) if m else None
def strip_num(text):
    return re.sub(r'^\s*\d+\.\s*', '', text).strip()

# ---------- live-search bar after the glossary heading ----------
SEARCH_BAR = (
    '\n<div class="gloss-search">'
    '<input id="glossSearch" type="search" autocomplete="off" '
    'placeholder="Search the glossary — type a word or part of a meaning…">'
    '<span class="cnt" id="glossCount"></span></div>\n'
)
body = re.sub(r'(<h2 id="11-master-az-glossary-every-word">.*?</h2>)',
              r'\1' + SEARCH_BAR.replace('\\', '\\\\'), body, count=1, flags=re.S)

# ---------- inject "Test now" launchers after each section heading ----------
def launcher(scope, label):
    return (f'\n<button class="quiz-launch" data-scope="{scope}">'
            f'<span class="ic">&#128221;</span> {label}</button>\n')
def after_h2(num_prefix, btn):
    global body
    body = re.sub(r'(<h2 id="' + num_prefix + r'-[^"]*">.*?</h2>)',
                  lambda m: m.group(1) + btn, body, count=1, flags=re.S)
after_h2("2",  launcher("hf",         "Test these high-priority words"))
after_h2("3",  launcher("roots",      "Test these roots"))
after_h2("4",  launcher("clusters",   "Test these clusters"))
after_h2("5",  launcher("se",         "Test these SE groups"))
after_h2("6",  launcher("polarity",   "Test this polarity bank"))
after_h2("7",  launcher("confusing",  "Test the confusing words"))
after_h2("8",  launcher("wordgroups", "Test these word groups"))
after_h2("11", launcher("glossary",   "Test glossary words"))

# ---------- split body into sections at each <h2>, wrap each as a routed .page ----------
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
    ac, acbg = ACCENTS.get(n, ("#2f6d5b", "#e7f1ee"))
    ico, desc = (META[n][1], META[n][2]) if n in META else ("📄", "")
    nav_items.append((hid, n, text))
    head = (f'<div class="page-head" style="--ac:{ac};--ac-bg:{acbg}">'
            f'<span class="ph-ico">{ico}</span>'
            f'<div class="ph-meta"><span class="ph-num">Section {n}</span>'
            f'<span class="ph-desc">{html.escape(desc)}</span></div></div>')
    pages_html.append(
        f'<section class="page" id="page-{hid}" style="--ac:{ac};--ac-bg:{acbg}">'
        f'{head}{h2html}{content}</section>')

# ---------- sidebar nav ----------
nav_links = ['<li><a class="nav-link active" href="#" data-page="page-home">'
             '<span class="nl-ico">🏠</span><span class="nl-txt">Home</span></a></li>']
for hid, n, text in nav_items:
    ac, _ = ACCENTS.get(n, ("#2f6d5b", ""))
    ico = META.get(n, ("", "📄"))[1]
    nav_links.append(
        f'<li><a class="nav-link" href="#{hid}" data-page="page-{hid}" style="--ac:{ac}">'
        f'<span class="nl-ico">{ico}</span>'
        f'<span class="nl-num">{n}</span>'
        f'<span class="nl-txt">{html.escape(strip_num(text))}</span></a></li>')
nav_html = "\n".join(nav_links)

# ---------- home page ----------
g = json.load(open("glossary.json"))
STATS = [("775", "words"), ("215", "high-priority"), ("36", "root families"), ("11", "sections")]
stat_html = "".join(f'<div class="stat"><span class="num">{v}</span><span class="lab">{l}</span></div>'
                    for v, l in STATS)
cards = []
for hid, n, text in nav_items:
    ac, acbg = ACCENTS.get(n, ("#2f6d5b", "#e7f1ee"))
    ico, desc = (META[n][1], META[n][2]) if n in META else ("📄", "")
    cards.append(
        f'<a class="card" href="#{hid}" style="--ac:{ac};--ac-bg:{acbg}">'
        f'<span class="card-ico">{ico}</span>'
        f'<span class="card-num">Section {n}</span>'
        f'<h3>{html.escape(strip_num(text))}</h3>'
        f'<p>{html.escape(desc)}</p>'
        f'<span class="card-go">Open &rarr;</span></a>')
home_html = f"""
<section class="page home active" id="page-home">
  <div class="hero">
    <span class="hero-badge">GRE Verbal &middot; Text Completion &middot; Sentence Equivalence</span>
    <h1>GRE Lexicon<br><span>Master Handbook</span></h1>
    <p class="hero-sub">Every high-frequency GRE word, learned the way the test actually rewards —
       in <b>root families</b> and <b>meaning clusters</b>, not as a flat list to forget.
       Then drill it: tap <b>Test</b> in any section to quiz yourself on exactly what you've studied.</p>
    <div class="hero-actions">
      <button class="quiz-launch hero-cta" data-scope=""><span class="ic">&#128221;</span> Test me now</button>
      <a class="hero-ghost" href="#3-root-word-encyclopedia">Start with roots &rarr;</a>
    </div>
    <div class="stats">{stat_html}</div>
  </div>
  <h2 class="home-h">Explore the handbook</h2>
  <div class="card-grid">{''.join(cards)}</div>
</section>
"""

CSS = """
:root{
  --bg:#eef1f6; --surface:#ffffff; --ink:#1b2330; --muted:#646e7e; --line:#e4e8ef;
  --brand:#1f6f5b; --brand-d:#175345; --brand-l:#e7f1ee;
  --sidebar-bg:#13201c; --sidebar-ink:#aab4ad; --sidebar-hover:#1e302a;
  --sidebar-w:268px; --content-w:1040px; --head-top:14px;
  --shadow:0 1px 2px rgba(20,30,40,.04),0 6px 20px rgba(20,30,40,.06);
  --ac:#1f6f5b; --ac-bg:#e7f1ee;
}
*{box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{margin:0; background:var(--bg); color:var(--ink);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  font-size:16.5px; line-height:1.7; -webkit-font-smoothing:antialiased;}
a{color:var(--brand); text-decoration:none;}
a:hover{text-decoration:underline;}

/* ===== layout ===== */
.layout{display:flex; align-items:flex-start;}
.sidebar{width:var(--sidebar-w); flex:0 0 auto; position:sticky; top:0; height:100vh;
  overflow-y:auto; background:var(--sidebar-bg); color:var(--sidebar-ink);
  padding:22px 14px 40px; transition:transform .25s ease;}
.brand{display:flex; align-items:center; gap:11px; padding:6px 8px 18px; color:#fff; text-decoration:none;}
.brand:hover{text-decoration:none;}
.brand .logo{width:40px; height:40px; border-radius:11px; flex:0 0 auto;
  background:linear-gradient(135deg,#2f9e7e,#175345); display:grid; place-items:center;
  font-size:20px; box-shadow:0 4px 12px rgba(0,0,0,.3);}
.brand .bt{font-weight:800; font-size:15px; line-height:1.2;}
.brand .bt span{display:block; font-weight:500; font-size:11.5px; color:#7f8c85;}
.sidebar .heading{font-size:11px; text-transform:uppercase; letter-spacing:.08em;
  color:#6b766f; margin:14px 10px 6px;}
.sidebar ul{list-style:none; margin:0; padding:0;}
.nav-link{display:flex; align-items:center; gap:10px; padding:8px 10px; border-radius:10px;
  color:var(--sidebar-ink); font-size:14px; line-height:1.25; transition:.13s;}
.nav-link:hover{background:var(--sidebar-hover); color:#fff; text-decoration:none;}
.nav-link .nl-ico{font-size:15px; width:20px; text-align:center;}
.nav-link .nl-num{margin-left:auto; font-size:11px; font-weight:700; color:#5f6b64;
  background:rgba(255,255,255,.06); border-radius:6px; padding:1px 7px;}
.nav-link.active{background:#fff; color:var(--brand-d); font-weight:700;}
.nav-link.active .nl-num{background:var(--ac,#1f6f5b); color:#fff;}
.nav-link.active .nl-ico{filter:none;}

.content{flex:1 1 auto; min-width:0; display:flex; justify-content:center; padding:0 34px;}
.content-inner{width:100%; max-width:var(--content-w); margin:30px 0 90px;}

/* ===== pages (one section visible at a time) ===== */
.page{display:none; animation:fade .25s ease;}
.page.active{display:block;}
@keyframes fade{from{opacity:0; transform:translateY(6px);}to{opacity:1; transform:none;}}

/* ===== home / hero ===== */
.hero{background:linear-gradient(135deg,#1f6f5b 0%,#15514360 100%),
  radial-gradient(120% 120% at 100% 0%,#2f9e7e33,transparent 60%),#163f35;
  color:#fff; border-radius:22px; padding:46px 44px 38px; box-shadow:var(--shadow);
  position:relative; overflow:hidden;}
.hero-badge{display:inline-block; font-size:12px; font-weight:600; letter-spacing:.02em;
  background:rgba(255,255,255,.14); padding:6px 13px; border-radius:30px; margin-bottom:16px;}
.hero h1{font-size:2.7rem; line-height:1.08; margin:0 0 14px; font-weight:800;}
.hero h1 span{color:#9fe9cf;}
.hero-sub{font-size:1.06rem; line-height:1.6; max-width:60ch; color:#e6f3ee; margin:0 0 24px;}
.hero-sub b{color:#fff;}
.hero-actions{display:flex; flex-wrap:wrap; gap:14px; align-items:center;}
.hero-cta{font-size:16px !important; padding:13px 24px !important; background:#fff !important;
  color:var(--brand-d) !important; border:none !important; box-shadow:0 6px 18px rgba(0,0,0,.22) !important;}
.hero-cta:hover{transform:translateY(-1px);}
.hero-ghost{color:#fff; font-weight:600; padding:12px 6px;}
.hero-ghost:hover{color:#9fe9cf; text-decoration:none;}
.stats{display:flex; flex-wrap:wrap; gap:30px; margin-top:30px; padding-top:24px;
  border-top:1px solid rgba(255,255,255,.16);}
.stat .num{display:block; font-size:1.8rem; font-weight:800; line-height:1;}
.stat .lab{font-size:12.5px; color:#bfe0d5; text-transform:uppercase; letter-spacing:.04em;}

.page > h2.home-h{font-size:1.4rem; margin:38px 4px 18px; font-weight:800; border:none; padding:0;}
.card-grid{display:grid; grid-template-columns:repeat(auto-fill,minmax(252px,1fr)); gap:18px;}
.card{display:flex; flex-direction:column; background:var(--surface); border:1px solid var(--line);
  border-radius:16px; padding:22px 20px; box-shadow:var(--shadow); transition:.16s; position:relative;
  overflow:hidden; color:var(--ink);}
.card::before{content:""; position:absolute; left:0; top:0; bottom:0; width:5px; background:var(--ac);}
.card:hover{transform:translateY(-4px); box-shadow:0 10px 30px rgba(20,30,40,.13); text-decoration:none; border-color:var(--ac);}
.card-ico{width:48px; height:48px; border-radius:13px; background:var(--ac-bg); color:var(--ac);
  display:grid; place-items:center; font-size:24px; margin-bottom:14px;}
.card-num{font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:.06em; color:var(--ac);}
.card h3{font-size:1.12rem; margin:3px 0 7px; color:var(--ink); border:none;}
.card p{font-size:13.6px; color:var(--muted); margin:0 0 16px; line-height:1.5; flex:1 1 auto;}
.card-go{font-size:13.5px; font-weight:700; color:var(--ac);}

/* ===== section page header ===== */
.page-head{display:flex; align-items:center; gap:15px; margin:2px 0 6px;}
.ph-ico{width:54px; height:54px; border-radius:15px; flex:0 0 auto; display:grid; place-items:center;
  font-size:27px; background:var(--ac); color:#fff; box-shadow:0 6px 16px color-mix(in srgb,var(--ac) 40%,transparent);}
.ph-meta{display:flex; flex-direction:column;}
.ph-num{font-size:11.5px; font-weight:800; text-transform:uppercase; letter-spacing:.07em; color:var(--ac);}
.ph-desc{font-size:14px; color:var(--muted); line-height:1.4;}

/* ===== typography ===== */
h1,h2,h3,h4{line-height:1.3; font-weight:800; scroll-margin-top:calc(var(--head-top) + 12px); color:var(--ink);}
.page > h2{font-size:1.95rem; margin:.1em 0 .7em; padding:0 0 .35em; border-bottom:3px solid var(--ac);}
h3{font-size:1.2rem; margin:1.7em 0 .55em;}
h4{font-size:1.02rem; margin:1.4em 0 .5em; color:var(--muted);}
p{margin:.7em 0;}
ul,ol{padding-left:1.4em;}
li{margin:.28em 0;}
hr{border:0; border-top:1px solid var(--line); margin:2.2em 0;}
strong{color:var(--ink); font-weight:700;}

/* callout */
blockquote{margin:1.3em 0; padding:1em 1.2em; background:var(--ac-bg);
  border:1px solid color-mix(in srgb,var(--ac) 22%,transparent); border-left:4px solid var(--ac);
  border-radius:0 12px 12px 0; color:#2a3a34;}
blockquote p{margin:.4em 0;}
blockquote strong{color:var(--ac);}

/* code / inline roots */
code{background:var(--ac-bg); color:var(--ac); padding:.12em .45em; border-radius:6px;
  font-family:"SF Mono",SFMono-Regular,Consolas,Menlo,monospace; font-size:.85em; font-weight:600;}

/* ===== tables ===== */
/* NOTE: no overflow:hidden here — it would break the sticky/frozen headers.
   Corners are rounded via the corner cells instead. */
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
thead th{background:var(--ac-bg); color:var(--ac); text-align:left; font-weight:700;
  position:-webkit-sticky; position:sticky; top:var(--head-top); z-index:5;}
thead th::before{content:""; position:absolute; left:0; right:0; bottom:100%;
  height:calc(var(--head-top) + 2px); background:var(--bg);}
tbody tr:nth-child(even){background:#f7f9fb;}
tbody tr:hover{background:var(--ac-bg);}

/* glossary search */
.gloss-search{position:-webkit-sticky; position:sticky; top:var(--head-top); z-index:7;
  background:var(--bg); padding:10px 0; display:flex; gap:12px; align-items:center; margin-bottom:6px;}
.gloss-search::before{content:""; position:absolute; left:0; right:0; bottom:100%;
  height:calc(var(--head-top) + 2px); background:var(--bg);}
.gloss-search input{flex:1; padding:11px 15px; font-size:15.5px; border:1px solid var(--line);
  border-radius:11px; background:var(--surface); color:var(--ink); box-shadow:var(--shadow);}
.gloss-search input:focus{outline:2px solid var(--brand); border-color:var(--brand);}
.gloss-search .cnt{font-size:12.5px; color:var(--muted); white-space:nowrap;}
table.gloss thead th{top:calc(var(--head-top) + 58px);}

/* ===== mobile nav button + backdrop ===== */
.nav-toggle{display:none; position:fixed; top:14px; left:14px; z-index:60; width:44px; height:44px;
  border-radius:12px; border:none; background:var(--brand); color:#fff; font-size:19px; cursor:pointer;
  box-shadow:0 4px 14px rgba(0,0,0,.25); align-items:center; justify-content:center;}
.backdrop{display:none;}

/* back to top */
#toTop{position:fixed; right:22px; bottom:22px; width:46px; height:46px; border-radius:50%;
  background:var(--brand); color:#fff; border:none; font-size:21px; cursor:pointer;
  box-shadow:0 6px 18px rgba(0,0,0,.22); opacity:0; pointer-events:none; transition:.2s; z-index:55;}
#toTop.show{opacity:1; pointer-events:auto;}
#toTop:hover{background:var(--brand-d);}

/* ===== responsive ===== */
@media (max-width:900px){
  .nav-toggle{display:flex;}
  .sidebar{position:fixed; left:0; top:0; z-index:50; width:80vw; max-width:300px;
    transform:translateX(-100%); box-shadow:4px 0 24px rgba(0,0,0,.35);}
  .sidebar.open{transform:translateX(0);}
  .backdrop{position:fixed; inset:0; background:rgba(0,0,0,.45); z-index:45;}
  .backdrop.show{display:block;}
  .content{padding:0 14px;}
  .content-inner{margin:64px 0 70px;}
  .hero{padding:34px 24px 30px;}
  .hero h1{font-size:2.1rem;}
  .page > h2{font-size:1.6rem;}
  table{font-size:13px;}
  th,td{padding:7px 9px;}
}
@media (max-width:480px){
  body{font-size:15.5px;}
  .hero h1{font-size:1.8rem;}
  .stats{gap:20px;}
  .ph-ico{width:46px; height:46px; font-size:23px;}
  .card-grid{grid-template-columns:1fr;}
  table{font-size:12.5px;}
}
"""

JS = """
const sb=document.getElementById('sidebar'), bd=document.getElementById('backdrop');
const mobile=()=>window.matchMedia('(max-width:900px)').matches;
function closeSb(){sb.classList.remove('open');bd.classList.remove('show');}
document.getElementById('navToggle').addEventListener('click',()=>{sb.classList.toggle('open');bd.classList.toggle('show');});
bd.addEventListener('click',closeSb);

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
  if(mobile()) closeSb();
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
<link rel="stylesheet" href="quiz.css">
</head>
<body>
<button id="navToggle" class="nav-toggle" aria-label="Menu">&#9776;</button>
<div class="backdrop" id="backdrop"></div>
<div class="layout">
  <aside class="sidebar" id="sidebar">
    <a class="brand" href="#">
      <span class="logo">📖</span>
      <span class="bt">GRE Lexicon<span>Master Handbook</span></span>
    </a>
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
<script src="quizdata.js"></script>
<script src="tcse.js"></script>
<script src="quiz.js"></script>
</body>
</html>
"""

for out in OUTS:
    open(out, "w", encoding="utf-8").write(page)
print(f"Wrote {', '.join(OUTS)} — {len(nav_items)} section pages + home.")
