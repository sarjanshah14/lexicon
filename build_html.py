#!/usr/bin/env python3
"""Wrap pandoc's HTML body in a clean, white, reading-friendly page with a sticky sidebar."""
import re, subprocess, html

MD = "GRE-Lexicon-Master-Handbook.md"
# index.html = Vercel entry point (served at the site root); the second is a friendly local copy
OUTS = ["index.html", "GRE-Lexicon-Master-Handbook.html"]

body = subprocess.run(
    ["pandoc", MD, "-f", "gfm", "-t", "html", "--syntax-highlighting=none"],
    capture_output=True, text=True, check=True).stdout

# Build sidebar from H2 headings (skip the in-page Table of Contents heading itself)
nav_items = []
for m in re.finditer(r'<h2 id="([^"]+)">(.*?)</h2>', body, re.S):
    hid, text = m.group(1), re.sub(r'<[^>]+>', '', m.group(2)).strip()
    if hid == "table-of-contents":
        continue
    nav_items.append((hid, text))

nav_html = "\n".join(
    f'      <li><a href="#{hid}">{html.escape(t)}</a></li>' for hid, t in nav_items
)

# inject a live-search bar right after the §11 glossary heading
SEARCH_BAR = (
    '\n<div class="gloss-search">'
    '<input id="glossSearch" type="search" autocomplete="off" '
    'placeholder="Search the glossary — type a word or part of a meaning…">'
    '<span class="cnt" id="glossCount"></span></div>\n'
)
body = re.sub(
    r'(<h2 id="11-master-az-glossary-every-word">.*?</h2>)',
    r'\1' + SEARCH_BAR.replace('\\', '\\\\'),
    body, count=1, flags=re.S,
)

CSS = """
:root{
  --ink:#161616; --muted:#5a5a5a; --line:#d6d6d2; --bg:#e7e7e3;
  --accent:#111111; --accent-soft:#e9e9e6; --code-bg:#efefec;
  --zebra:#f6f6f3; --thead:#ececea; --panel:#ffffff;
  --sidebar:#1a1a1a; --sidebar-ink:#cfcfca; --sidebar-hover:#2b2b2b;
  --content-width:880px; --sidebar-width:300px;
  --head-top:18px;        /* gap kept above a frozen header row */
}
*{box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{
  margin:0; background:var(--bg); color:var(--ink);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  font-size:17px; line-height:1.72; -webkit-font-smoothing:antialiased;
}
a{color:var(--accent); text-decoration:underline; text-underline-offset:2px;}
a:hover{opacity:.7;}

/* layout */
.layout{display:flex; align-items:flex-start;}
.sidebar{
  width:var(--sidebar-width); flex:0 0 auto;
  position:sticky; top:0; height:100vh; overflow-x:hidden; overflow-y:auto;
  background:var(--sidebar); border-right:1px solid #000;
  transition:width .28s ease, border-color .28s ease;
}
.sidebar-inner{
  width:var(--sidebar-width); box-sizing:border-box;
  padding:62px 18px 60px;   /* top padding clears the fixed toggle button */
}
.sidebar h1{font-size:17px; margin:4px 8px 16px; line-height:1.4; color:#fff;}
.sidebar .sub{font-size:12.5px; color:#8a8a85; margin:0 8px 18px; font-weight:400;}
.sidebar ol{list-style:none; margin:0; padding:0; counter-reset:nav;}
.sidebar li{margin:0;}
.sidebar li a{
  display:block; padding:7px 10px; border-radius:6px; text-decoration:none;
  color:var(--sidebar-ink); font-size:14px; line-height:1.35;
}
.sidebar li a:hover{background:var(--sidebar-hover); color:#fff; opacity:1;}
.sidebar li a.active{background:#fff; color:#111; font-weight:600;}

.content{flex:1 1 auto; min-width:0; display:flex; justify-content:center; padding:0 32px;}
.content-inner{
  width:100%; max-width:var(--content-width); margin:34px 0 80px;
  background:var(--panel); border:1px solid var(--line); border-radius:10px;
  padding:48px 56px 90px; box-shadow:0 1px 3px rgba(0,0,0,.06);
  transition:max-width .28s ease, width .28s ease;
}

/* typography */
h1,h2,h3,h4{line-height:1.3; font-weight:700; scroll-margin-top:calc(var(--head-top) + 12px);}
.content-inner > h1:first-child{font-size:2.1rem; margin:0 0 .2em;}
h2{font-size:1.6rem; margin:2.4em 0 .8em; padding-bottom:.3em; border-bottom:2px solid var(--line);}
h3{font-size:1.22rem; margin:1.8em 0 .6em; color:#111;}
h4{font-size:1.04rem; margin:1.4em 0 .5em; color:var(--muted);}
p{margin:.7em 0;}
ul,ol{padding-left:1.5em;}
li{margin:.25em 0;}
hr{border:0; border-top:1px solid var(--line); margin:2.4em 0;}

strong{color:#111; font-weight:700;}

/* blockquote = study tip callout */
blockquote{
  margin:1.2em 0; padding:.8em 1.1em; background:var(--accent-soft);
  border-left:4px solid var(--accent); border-radius:0 8px 8px 0; color:#2a2a2a;
}
blockquote p{margin:.4em 0;}

/* code */
code{
  background:var(--code-bg); padding:.12em .4em; border-radius:5px;
  font-family:"SF Mono",SFMono-Regular,Consolas,"Liberation Mono",Menlo,monospace;
  font-size:.86em; color:#222; border:1px solid var(--line);
}

/* tables — NOT inside an overflow box, so sticky headers track the PAGE scroll.
   border-collapse:separate is required so the header's borders stay attached while it floats. */
table{
  border-collapse:separate; border-spacing:0; width:100%; margin:1.2em 0; font-size:15px;
  table-layout:auto; border-top:1px solid var(--line); border-left:1px solid var(--line);
}
th,td{
  border-right:1px solid var(--line); border-bottom:1px solid var(--line);
  padding:8px 11px; vertical-align:top;
  /* keep whole words intact — wrap only at spaces, never split a word into characters */
  overflow-wrap:normal; word-break:normal; hyphens:none;
}
/* sticky header row: freezes a little BELOW the top of the viewport (--head-top) while its
   table is in view, then releases once the table has scrolled past. The downward box-shadow
   in panel colour masks any rows passing through the gap above the frozen header. */
thead th{
  background:var(--thead); text-align:left; font-weight:700;
  position:-webkit-sticky; position:sticky; top:var(--head-top); z-index:5;
  box-shadow:inset 0 1px 0 var(--line), 0 calc(-1 * var(--head-top) - 2px) 0 var(--panel);
}
tbody tr:nth-child(even){background:var(--zebra);}
tbody tr:hover{background:#e9e9e6;}

/* in-page ToC list (right after first h2) gets a card look via class added by JS */
.toc-card{background:#f6f6f3; border:1px solid var(--line); border-radius:10px; padding:8px 22px;}

/* glossary live-search bar (sticky just below the top gap, masks rows above it) */
.gloss-search{
  position:-webkit-sticky; position:sticky; top:var(--head-top); z-index:7;
  background:var(--panel); padding:10px 0; border-bottom:1px solid var(--line);
  display:flex; gap:12px; align-items:center; margin-bottom:6px;
  box-shadow:0 calc(-1 * var(--head-top) - 2px) 0 var(--panel);
}
.gloss-search input{
  flex:1; padding:9px 13px; font-size:16px; border:1px solid #b5b5b5;
  border-radius:8px; background:#fff; color:var(--ink);
}
.gloss-search input:focus{outline:2px solid #555; border-color:#555;}
.gloss-search .cnt{font-size:12.5px; color:var(--muted); white-space:nowrap;}
/* frozen glossary headers sit just below the sticky search bar */
table.gloss thead th{top:calc(var(--head-top) + 52px);}

/* nav toggle button (always visible) */
.nav-toggle{
  position:fixed; top:14px; left:14px; z-index:60;
  width:40px; height:40px; border-radius:8px; border:1px solid #000;
  background:#1a1a1a; color:#fff; font-size:18px; cursor:pointer; line-height:1;
  display:flex; align-items:center; justify-content:center;
  box-shadow:0 1px 4px rgba(0,0,0,.25);
}
.nav-toggle:hover{background:#000;}

/* desktop collapsed state: sidebar slides/clips away smoothly, content widens to ~90% */
body.nav-collapsed .sidebar{width:0; border-right-color:transparent;}
body.nav-collapsed .content{padding:0;}
body.nav-collapsed .content-inner{max-width:none; width:90%;}

/* back to top */
#toTop{
  position:fixed; right:22px; bottom:22px; width:42px; height:42px; border-radius:50%;
  background:var(--accent); color:#fff; border:none; font-size:20px; cursor:pointer;
  box-shadow:0 2px 10px rgba(0,0,0,.18); opacity:0; pointer-events:none; transition:opacity .2s;
}
#toTop.show{opacity:.9; pointer-events:auto;}
#toTop:hover{opacity:1;}

.backdrop{display:none;}

/* desktop: leave room at top-left of content for the floating toggle */
.content-inner{position:relative;}

/* tablet / phone */
@media (max-width:900px){
  :root{--head-top:54px;}   /* clear the floating menu button on small screens */
  .sidebar{
    position:fixed; left:0; top:0; z-index:50; width:84vw; max-width:320px;
    transform:translateX(-100%); transition:transform .25s ease;
    box-shadow:2px 0 18px rgba(0,0,0,.3);
  }
  .sidebar.open{transform:translateX(0);}
  .sidebar-inner{width:100%;}
  .content{padding:0 12px;}
  .content-inner{
    margin:16px 0 70px; padding:58px 18px 70px; border-radius:8px;
  }
  body{font-size:16px;}
  .content-inner > h1:first-child{font-size:1.7rem;}
  h2{font-size:1.4rem;}
  h3{font-size:1.12rem;}
  table{font-size:13.5px;}
  th,td{padding:6px 8px;}
  blockquote{padding:.7em .9em;}
  .backdrop{
    position:fixed; inset:0; background:rgba(0,0,0,.4); z-index:45; display:none;
  }
  .backdrop.show{display:block;}
}

/* small phones */
@media (max-width:480px){
  body{font-size:15px;}
  .content{padding:0 6px;}
  .content-inner{padding:54px 12px 60px;}
  table{font-size:12.5px;}
  th,td{padding:5px 6px;}
  code{font-size:.8em;}
}

/* ===== Card view (toggleable per section) =====
   A row becomes a self-contained card; column names become inline labels.
   On wide screens cards flow as a grid; on phones they stack one per row. */
table.cards{display:block; border:0; margin:1.2em 0;}
table.cards thead{display:none;}
table.cards tbody{
  display:grid; gap:14px;
  grid-template-columns:repeat(auto-fill, minmax(280px, 1fr));
}
table.cards tbody tr{
  display:flex; flex-direction:column; background:var(--panel) !important;
  border:1px solid var(--line); border-radius:10px; padding:10px 14px;
  box-shadow:0 1px 2px rgba(0,0,0,.05);
}
table.cards tbody td{
  border:0; padding:4px 0; display:flex; gap:8px; align-items:baseline;
}
table.cards tbody td::before{
  content:attr(data-label); font-weight:700; color:var(--muted);
  flex:0 0 92px; font-size:.85em; text-transform:uppercase; letter-spacing:.02em;
}
table.cards tbody td:empty{display:none;}

/* per-section view toggle, appears on the right edge while a wide table is in view */
#viewToggle{
  position:fixed; right:14px; top:50%; transform:translateY(-50%);
  z-index:55; display:none; flex-direction:column; gap:6px;
  background:#1a1a1a; color:#fff; padding:8px; border-radius:12px;
  box-shadow:0 3px 14px rgba(0,0,0,.3); font-size:12px;
}
#viewToggle.show{display:flex;}
#viewToggle .lbl{font-size:10px; text-align:center; color:#9a9a95; letter-spacing:.04em;}
#viewToggle button{
  border:0; border-radius:7px; padding:7px 12px; cursor:pointer;
  background:#333; color:#ddd; font-size:12px; font-weight:600;
}
#viewToggle button.on{background:#fff; color:#111;}
#viewToggle button:hover{background:#4a4a4a; color:#fff;}
#viewToggle button.on:hover{background:#fff; color:#111;}
"""

JS = """
const sb=document.getElementById('sidebar');
const bd=document.getElementById('backdrop');
const body=document.body;
const mobile=()=>window.innerWidth<=900;
function closeMobile(){sb.classList.remove('open');bd.classList.remove('show');}
function toggle(){
  if(mobile()){ sb.classList.toggle('open'); bd.classList.toggle('show'); }
  else { body.classList.toggle('nav-collapsed'); }
}
document.getElementById('navToggle').addEventListener('click',toggle);
bd.addEventListener('click',closeMobile);
sb.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{if(mobile())closeMobile();}));
// reset overlay state when crossing the breakpoint
addEventListener('resize',()=>{ if(!mobile()) closeMobile(); });

// active section highlight
const links=[...sb.querySelectorAll('a')];
const map={}; links.forEach(a=>map[a.getAttribute('href').slice(1)]=a);
const heads=[...document.querySelectorAll('h2[id]')];
const obs=new IntersectionObserver((es)=>{
  es.forEach(e=>{if(e.isIntersecting){links.forEach(l=>l.classList.remove('active'));
    const a=map[e.target.id]; if(a)a.classList.add('active');}});
},{rootMargin:'-10% 0px -80% 0px'});
heads.forEach(h=>obs.observe(h));

// give the in-page Table of Contents list a card look
const tocH=document.getElementById('table-of-contents');
if(tocH){let n=tocH.nextElementSibling; if(n&&n.tagName==='OL')n.classList.add('toc-card');}

// glossary live search
const gh=document.getElementById('11-master-az-glossary-every-word');
const gInput=document.getElementById('glossSearch');
const gCount=document.getElementById('glossCount');
if(gh && gInput){
  let els=[]; let n=gh.nextElementSibling;
  while(n){els.push(n); n=n.nextElementSibling;}
  const tables=els.filter(e=>e.tagName==='TABLE');
  tables.forEach(t=>t.classList.add('gloss'));
  const filter=()=>{
    const q=gInput.value.trim().toLowerCase();
    let shown=0;
    tables.forEach(t=>{
      let vis=0;
      const tb=t.tBodies[0];
      if(tb){[...tb.rows].forEach(r=>{
        const hit = q==='' || r.textContent.toLowerCase().includes(q);
        r.style.display = hit ? '' : 'none';
        if(hit) vis++;
      });}
      t.style.display = vis ? '' : 'none';
      const h=t.previousElementSibling;
      if(h && h.tagName==='H3') h.style.display = vis ? '' : 'none';
      shown+=vis;
    });
    gCount.textContent = q ? (shown + ' match' + (shown===1?'':'es')) : '';
  };
  gInput.addEventListener('input', filter);
}

// ===== per-section Table/Cards view toggle (only for tables with 4+ columns) =====
(function(){
  const all=[...document.querySelectorAll('table')];
  const wide=all.filter(t=>{
    const h=t.tHead||t.querySelector('thead');
    return h && h.rows[0] && h.rows[0].cells.length>=4;
  });
  if(!wide.length) return;
  // tag each wide table with its section (nearest preceding h2) + add data-labels
  const sectionOf=t=>{
    let n=t;
    while(n){ if(n.tagName==='H2') return n.id||'_'; n=n.previousElementSibling
      || (n.parentElement && n.parentElement!==document.body ? n.parentElement : null); }
    return '_';
  };
  const groups={};   // sectionId -> [tables]
  wide.forEach(t=>{
    t.classList.add('switchable');
    const heads=[...(t.tHead?t.tHead.rows[0].cells:[])].map(c=>c.textContent.trim());
    [...t.tBodies].forEach(tb=>[...tb.rows].forEach(r=>{
      [...r.cells].forEach((c,i)=>{ if(heads[i]) c.setAttribute('data-label', heads[i]); });
    }));
    const sec=sectionOf(t);
    t.dataset.section=sec;
    (groups[sec]=groups[sec]||[]).push(t);
  });
  const mode={};     // sectionId -> 'table' | 'cards'  (default table)
  Object.keys(groups).forEach(s=>mode[s]='table');

  const tgl=document.getElementById('viewToggle');
  const bT=document.getElementById('vtTable'), bC=document.getElementById('vtCards');
  let active=null;
  const reflect=()=>{
    if(!active){tgl.classList.remove('show'); return;}
    tgl.classList.add('show');
    const m=mode[active];
    bT.classList.toggle('on', m==='table');
    bC.classList.toggle('on', m==='cards');
  };
  const apply=(sec)=>{
    groups[sec].forEach(t=>t.classList.toggle('cards', mode[sec]==='cards'));
  };
  bT.addEventListener('click',()=>{ if(active){mode[active]='table'; apply(active); reflect();} });
  bC.addEventListener('click',()=>{ if(active){mode[active]='cards'; apply(active); reflect();} });

  // track which wide table is currently most in view -> its section is active
  const vis=new Map();
  const io=new IntersectionObserver((es)=>{
    es.forEach(e=>vis.set(e.target, e.isIntersecting?e.intersectionRatio:0));
    let best=null,br=0;
    vis.forEach((r,t)=>{ if(r>br){br=r; best=t;} });
    const sec = best && br>0 ? best.dataset.section : null;
    if(sec!==active){ active=sec; reflect(); }
  },{threshold:[0,0.01,0.15,0.4,0.75]});
  wide.forEach(t=>io.observe(t));
})();

// back to top
const btn=document.getElementById('toTop');
addEventListener('scroll',()=>{btn.classList.toggle('show',scrollY>600);});
btn.addEventListener('click',()=>scrollTo({top:0,behavior:'smooth'}));
"""

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GRE Lexicon Master Handbook</title>
<style>{CSS}</style>
</head>
<body>
<button id="navToggle" class="nav-toggle" aria-label="Show / hide menu" title="Show / hide menu">&#9776;</button>
<div class="backdrop" id="backdrop"></div>
<div class="layout">
  <aside class="sidebar" id="sidebar">
    <div class="sidebar-inner">
      <h1>GRE Lexicon<br>Master Handbook</h1>
      <div class="sub">Text Completion &middot; Sentence Equivalence &middot; RC vocab</div>
      <nav><ol>
{nav_html}
      </ol></nav>
    </div>
  </aside>
  <main class="content">
    <article class="content-inner">
{body}
    </article>
  </main>
</div>
<div id="viewToggle" role="group" aria-label="Table view switch">
  <span class="lbl">VIEW</span>
  <button id="vtTable" type="button">Table</button>
  <button id="vtCards" type="button">Cards</button>
</div>
<button id="toTop" aria-label="Back to top">&#8593;</button>
<script>{JS}</script>
</body>
</html>
"""

for out in OUTS:
    open(out, "w", encoding="utf-8").write(page)
print(f"Wrote {', '.join(OUTS)} with {len(nav_items)} sidebar sections.")
