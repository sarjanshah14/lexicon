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
  --head-top:12px;        /* small gap kept above a frozen header row */
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
   table is in view, then releases once the table has scrolled past. */
thead th{
  background:var(--thead); text-align:left; font-weight:700;
  position:-webkit-sticky; position:sticky; top:var(--head-top); z-index:5;
  box-shadow:inset 0 1px 0 var(--line);
}
/* mask the small gap above a frozen header so rows don't peek through.
   The block sits directly above each header cell and travels with it. */
thead th::before{
  content:""; position:absolute; left:-1px; right:-1px; bottom:100%;
  height:calc(var(--head-top) + 2px); background:var(--panel);
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
}
.gloss-search::before{
  content:""; position:absolute; left:0; right:0; bottom:100%;
  height:calc(var(--head-top) + 2px); background:var(--panel);
}
.gloss-search input{
  flex:1; padding:9px 13px; font-size:16px; border:1px solid #b5b5b5;
  border-radius:8px; background:#fff; color:var(--ink);
}
.gloss-search input:focus{outline:2px solid #555; border-color:#555;}
.gloss-search .cnt{font-size:12.5px; color:var(--muted); white-space:nowrap;}
/* frozen glossary headers sit just below the sticky search bar */
table.gloss thead th{top:calc(var(--head-top) + 56px);}

/* a too-wide table is auto-wrapped in this scroll frame (JS) so columns are never
   cut off; the header stays frozen at the top of the frame, and you scroll the table
   sideways/vertically inside it. */
.tscroll{
  overflow:auto; max-height:82vh; margin:1.2em 0;
  border:1px solid var(--line); border-radius:8px;
  -webkit-overflow-scrolling:touch;
}
.tscroll table{margin:0; border-top:0; border-left:0;}
.tscroll thead th{top:0;}              /* freeze to the frame top (no page offset) */
.tscroll thead th::before{display:none;}/* no gap mask needed inside the frame */

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
  /* move the menu button to the BOTTOM-left so it never overlaps a frozen header */
  .nav-toggle{top:auto; bottom:18px; left:16px;}
  .sidebar{
    position:fixed; left:0; top:0; z-index:50; width:84vw; max-width:320px;
    transform:translateX(-100%); transition:transform .25s ease;
    box-shadow:2px 0 18px rgba(0,0,0,.3);
  }
  .sidebar.open{transform:translateX(0);}
  .sidebar-inner{width:100%;}
  .content{padding:0 12px;}
  .content-inner{
    margin:16px 0 70px; padding:26px 16px 70px; border-radius:8px;
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
  .content-inner{padding:24px 12px 60px;}
  table{font-size:12.5px;}
  th,td{padding:5px 6px;}
  code{font-size:.8em;}
}

"""

JS = """
const sb=document.getElementById('sidebar');
const bd=document.getElementById('backdrop');
const body=document.body;
const mobile=()=>window.innerWidth<=900;
function closeMobile(){sb.classList.remove('open');bd.classList.remove('show');}
function toggle(){
  if(mobile()){ sb.classList.toggle('open'); bd.classList.toggle('show'); }
  else { body.classList.toggle('nav-collapsed'); setTimeout(()=>refitTables(), 320); }
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
      // a table may be wrapped in a .tscroll frame; hide the frame + its letter heading
      const host = (t.parentElement && t.parentElement.classList.contains('tscroll'))
                   ? t.parentElement : t;
      host.style.display = vis ? '' : 'none';
      const h=host.previousElementSibling;
      if(h && h.tagName==='H3') h.style.display = vis ? '' : 'none';
      shown+=vis;
    });
    gCount.textContent = q ? (shown + ' match' + (shown===1?'':'es')) : '';
  };
  gInput.addEventListener('input', filter);
}

// ===== auto-fit wide tables: wrap any table that overflows its width in a scroll frame
// (keeps the header frozen at the frame top); unwrap again if it fits after a resize =====
function refitTables(){
  document.querySelectorAll('table').forEach(t=>{
    const pane = t.parentElement && t.parentElement.classList.contains('tscroll')
                 ? t.parentElement : null;
    const overflowing = t.scrollWidth > t.clientWidth + 1;
    if(overflowing && !pane){
      const w=document.createElement('div'); w.className='tscroll';
      t.parentNode.insertBefore(w, t); w.appendChild(t);
    }else if(!overflowing && pane){
      pane.parentNode.insertBefore(t, pane); pane.remove();
    }
  });
}
let _rt; addEventListener('resize',()=>{clearTimeout(_rt); _rt=setTimeout(refitTables,150);});
refitTables();

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
<button id="toTop" aria-label="Back to top">&#8593;</button>
<script>{JS}</script>
</body>
</html>
"""

for out in OUTS:
    open(out, "w", encoding="utf-8").write(page)
print(f"Wrote {', '.join(OUTS)} with {len(nav_items)} sidebar sections.")
