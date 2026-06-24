/* GRE Lexicon practice engine — simplified.
   Press a Test button -> one screen: choose how many questions -> go.
   All question types are mixed automatically. The pool is decided by the button
   plus your "studied up to here" markers (saved in your browser), so you're only
   ever tested on what you've studied. Nothing is sent anywhere; score is per-session. */
(function(){
"use strict";
var Q = window.QUIZ || {words:[],roots:[],clusters:[]};
var BANK = window.TCSE || [];
var WORDS = Q.words;
var BYWORD = {}; WORDS.forEach(function(w){ BYWORD[w.w.toLowerCase()] = w; });

/* ---------- helpers ---------- */
function rnd(n){ return Math.floor(Math.random()*n); }
function shuffle(a){ a=a.slice(); for(var i=a.length-1;i>0;i--){var j=rnd(i+1);var t=a[i];a[i]=a[j];a[j]=t;} return a; }
function sample(a,n){ return shuffle(a).slice(0,n); }
function cap(s){ return s.charAt(0).toUpperCase()+s.slice(1); }
function esc(s){ return (s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;"); }
var LAB = ["A","B","C","D","E","F"];

/* ---------- persisted "studied up to here" markers ---------- */
var LS_GLOSS="gre_gloss_studied";
function get(k,d){ try{ var v=localStorage.getItem(k); return v===null?d:v; }catch(e){ return d; } }
function set(k,v){ try{ localStorage.setItem(k,v); }catch(e){} }
function studiedGloss(){ return get(LS_GLOSS,""); }

/* ================= MODAL SHELL ================= */
var overlay = document.createElement("div");
overlay.className = "qz-overlay";
overlay.innerHTML =
  '<div class="qz-modal" role="dialog" aria-modal="true">'+
    '<div class="qz-head"><h3 id="qzTitle">Practice</h3><button class="qz-x" aria-label="Close">&times;</button></div>'+
    '<div class="qz-body" id="qzBody"></div>'+
  '</div>';
document.body.appendChild(overlay);
var body = overlay.querySelector("#qzBody");
var titleEl = overlay.querySelector("#qzTitle");
overlay.querySelector(".qz-x").addEventListener("click", close);
overlay.addEventListener("click", function(e){ if(e.target===overlay) close(); });
document.addEventListener("keydown", function(e){ if(e.key==="Escape" && overlay.classList.contains("open")) close(); });
function open(){ overlay.classList.add("open"); }
function close(){ overlay.classList.remove("open"); run=null; }

/* ================= POOL (decided by scope + per-section "studied" markers) ================= */
function allFmts(withRoot){ var f={def:true,rev:true,syn:true,ant:true,tc:true,se:true}; if(withRoot) f.root=true; return f; }
function glossPool(letter){
  if(!letter) return WORDS.slice();
  return WORDS.filter(function(w){ return w.w[0].toUpperCase() <= letter; });
}
function toWordObjs(keys){ return keys.map(function(k){ return BYWORD[k]; }).filter(Boolean); }

function poolFor(scope){
  if(scope==="glossary"){ var L=studiedGloss();
    return {pool:glossPool(L), label:(L?("glossary A–"+L):"the whole glossary"), fmts:allFmts(false)}; }
  if(scope==="hf"){ return {pool:WORDS.filter(function(w){return w.hf;}), label:"the high-priority words", fmts:allFmts(false)}; }
  if(scope===""){ // global: union of everything marked studied across all sections + glossary
    var set={};
    Object.keys(REG).forEach(function(s){ sectionWords(s,true).forEach(function(w){ set[w]=1; }); });
    var L2=studiedGloss(); if(L2) glossPool(L2).forEach(function(w){ set[w.w.toLowerCase()]=1; });
    var keys=Object.keys(set);
    if(keys.length) return {pool:toWordObjs(keys), label:"everything you've marked studied", fmts:allFmts(true)};
    return {pool:WORDS.filter(function(w){return w.hf;}),
            label:"the high-priority words (mark sections “studied up to here” to focus your tests)", fmts:allFmts(true)};
  }
  var rt=REG[scope];
  if(rt){
    var words=toWordObjs(sectionWords(scope,false));
    var n=mark(rt);
    var label = rt.whole ? ("the "+rt.noun)
              : (n ? ("your studied "+rt.noun+" (1–"+n+" of "+rt.heads.length+")")
                   : ("all "+rt.heads.length+" "+rt.noun));
    var f=allFmts(scope==="roots");
    if(rt.fullBank){ f.tc=true; f.se=true; }
    return {pool:words, label:label, fmts:f, fullBank:rt.fullBank};
  }
  return {pool:WORDS.filter(function(w){return w.hf;}), label:"the high-priority words", fmts:allFmts(true)};
}

/* ================= SETUP SCREEN (count only) ================= */
var current=null, lastScope="";
function showSetup(scope){
  lastScope = scope||"";
  current = poolFor(lastScope);
  titleEl.textContent = "Quick test";
  var pool=current.pool;
  var enough = pool.length>=4;
  var h='<div class="qz-set">';
  h+='<p class="qz-lead">Testing you on <b>'+esc(current.label)+'</b>'+
     (enough?(' — about <b>'+pool.length+'</b> words.'):'.')+'</p>';
  h+='<p class="qz-sub2">All question types — definitions, synonyms/antonyms, roots, Text Completion & Sentence Equivalence — are mixed in automatically.</p>';
  if(!enough){
    h+='<div class="qz-err">Not enough studied yet to build a test. Mark a few more as studied, or use a broader Test button.</div>';
    h+='<button class="qz-start" id="qzClose2">OK</button></div>';
    body.innerHTML=h; open();
    body.querySelector('#qzClose2').addEventListener('click',close);
    return;
  }
  h+='<h4>How many questions?</h4>';
  h+='<div class="qz-count" id="qzCount">'+
     [10,15,20,25].map(function(n,i){ return '<span class="qz-chip cnt'+(i===1?" on":"")+'" data-n="'+n+'">'+n+'</span>'; }).join("")+
     '</div>';
  h+='<button class="qz-start" id="qzStart">Start test</button>';
  h+='</div>';
  body.innerHTML=h;
  current.count=15;
  body.querySelectorAll('#qzCount .qz-chip').forEach(function(c){
    c.addEventListener('click',function(){
      body.querySelectorAll('#qzCount .qz-chip').forEach(function(x){x.classList.remove('on');});
      c.classList.add('on'); current.count=parseInt(c.getAttribute('data-n'),10);
    });
  });
  body.querySelector('#qzStart').addEventListener('click', start);
  open();
}

/* ================= QUESTION GENERATION ================= */
function withMeaning(pool){ return pool.filter(function(w){return w.m;}); }
function makeDef(pool){
  var src=withMeaning(pool); if(src.length<4) return null;
  var w=src[rnd(src.length)];
  var distract=sample(WORDS.filter(function(x){ return x.w!==w.w && x.m && x.m!==w.m && (w.s||[]).indexOf(x.w)<0; }),3);
  if(distract.length<3) return null;
  var opts=shuffle([w].concat(distract)).map(function(x){
    return { text:cap(x.m), correct:x.w===w.w,
             why:x.w===w.w?"This is the meaning of <b>"+esc(w.w)+"</b>.":"This is the meaning of <b>"+esc(x.w)+"</b>, not "+esc(w.w)+"." };
  });
  return { type:"Definition", stem:"Which is the best meaning of <b>"+esc(w.w)+"</b>?", opts:opts, multi:false };
}
function makeRev(pool){
  var src=withMeaning(pool); if(src.length<4) return null;
  var w=src[rnd(src.length)];
  var distract=sample(WORDS.filter(function(x){ return x.w!==w.w && x.m && x.m!==w.m; }),3);
  if(distract.length<3) return null;
  var opts=shuffle([w].concat(distract)).map(function(x){
    return { text:cap(x.w), correct:x.w===w.w,
             why:x.w===w.w?"<b>"+esc(w.w)+"</b> — "+esc(w.m)+".":"<b>"+esc(x.w)+"</b> means "+esc(x.m)+"." };
  });
  return { type:"Reverse", stem:"Which word means: <i>"+esc(w.m)+"</i>?", opts:opts, multi:false };
}
function makeSyn(pool){
  var src=pool.filter(function(w){ return w.s && w.s.length; }); if(src.length<1) return null;
  var w=src[rnd(src.length)];
  var ans=w.s[rnd(w.s.length)];
  var bad={}; (w.s||[]).forEach(function(x){bad[x.toLowerCase()]=1;}); bad[w.w.toLowerCase()]=1;
  var distract=sample(WORDS.filter(function(x){ return !bad[x.w.toLowerCase()]; }),3).map(function(x){return x.w;});
  if(distract.length<3) return null;
  var opts=shuffle([{t:ans,c:true}].concat(distract.map(function(d){return {t:d,c:false};}))).map(function(o){
    return { text:cap(o.t), correct:o.c, why:o.c?"<b>"+esc(ans)+"</b> is a listed synonym of "+esc(w.w)+" ("+esc(w.m)+").":"Not a synonym of "+esc(w.w)+"." };
  });
  return { type:"Synonym", stem:"Which word is closest in meaning to <b>"+esc(w.w)+"</b>?", opts:opts, multi:false, note:"<b>"+esc(w.w)+"</b> means "+esc(w.m)+"." };
}
function makeAnt(pool){
  var src=pool.filter(function(w){ return w.a && w.a.length; }); if(src.length<1) return null;
  var w=src[rnd(src.length)];
  var ans=w.a[rnd(w.a.length)];
  var bad={}; (w.a||[]).forEach(function(x){bad[x.toLowerCase()]=1;}); (w.s||[]).forEach(function(x){bad[x.toLowerCase()]=1;}); bad[w.w.toLowerCase()]=1;
  var distract=sample(WORDS.filter(function(x){ return !bad[x.w.toLowerCase()]; }),3).map(function(x){return x.w;});
  if(distract.length<3) return null;
  var opts=shuffle([{t:ans,c:true}].concat(distract.map(function(d){return {t:d,c:false};}))).map(function(o){
    return { text:cap(o.t), correct:o.c, why:o.c?"<b>"+esc(ans)+"</b> is a listed antonym of "+esc(w.w)+" ("+esc(w.m)+").":"Not an antonym of "+esc(w.w)+"." };
  });
  return { type:"Antonym", stem:"Which word is most nearly <i>opposite</i> to <b>"+esc(w.w)+"</b>?", opts:opts, multi:false, note:"<b>"+esc(w.w)+"</b> means "+esc(w.m)+"." };
}
function makeRoot(){
  if(Q.roots.length<4) return null;
  var r=Q.roots[rnd(Q.roots.length)];
  var distract=sample(Q.roots.filter(function(x){return x.root!==r.root;}),3);
  var opts=shuffle([r].concat(distract)).map(function(x){
    return { text:cap(x.mean), correct:x.root===r.root,
             why:x.root===r.root?("The root <b>"+esc(r.root)+"</b> means “"+esc(r.mean)+"” (e.g. "+esc((r.words||[]).slice(0,3).join(", "))+")."):("“"+esc(x.mean)+"” is the meaning of the root <b>"+esc(x.root)+"</b>.") };
  });
  return { type:"Root", stem:"What does the root <b>"+esc(r.root)+"</b> mean?", opts:opts, multi:false };
}
function bankInPool(b,poolNames,pool,fullBank){
  if(fullBank || pool.length===WORDS.length) return true;
  return (b.words||[]).some(function(w){ return poolNames[w.toLowerCase()]; });
}
function tcseCard(it){
  if(it.se){
    var b=it.se;
    var opts=b.opts.map(function(w,i){ return { text:cap(w), correct:b.ans.indexOf(i)>=0, why:b.expl[w]||"" }; });
    return { type:"Sentence Equivalence", stem:esc(b.stem), opts:opts, multi:true, note:b.pairNote||"", hint:"Select the TWO words that give the sentence the same meaning." };
  }
  if(it.tc){
    var t=it.tc, bl=t.blanks[it.bi];
    var stem=t.blanks.length>1
      ? esc(t.stem).replace(/\((i+)\)_{2,}/g,function(_,r){ return '<span class="bk">('+r+') ____</span>'; })
      : esc(t.stem).replace(/_{2,}/g,'<span class="bk">____</span>');
    var label = t.blanks.length>1 ? "Blank "+(it.bi===0?"(i)":it.bi===1?"(ii)":"(iii)")+" — choose the best word:" : null;
    var opts=bl.opts.map(function(w,i){ return { text:cap(w), correct:i===bl.ans, why:bl.expl[w]||"" }; });
    return { type:"Text Completion"+(t.blanks.length>1?" · double blank":""), stem:stem, opts:shuffle(opts), multi:false, hint:label };
  }
  return null;
}
function buildQueue(pool,fmts,count,fullBank){
  var poolNames={}; pool.forEach(function(w){poolNames[w.w.toLowerCase()]=1;});
  var gens=[];
  if(fmts.def) gens.push(function(){return makeDef(pool);});
  if(fmts.rev) gens.push(function(){return makeRev(pool);});
  if(fmts.syn) gens.push(function(){return makeSyn(pool);});
  if(fmts.ant) gens.push(function(){return makeAnt(pool);});
  if(fmts.root) gens.push(makeRoot);
  var bankItems=[];
  if(fmts.se) BANK.filter(function(b){return b.type==="SE" && bankInPool(b,poolNames,pool,fullBank);}).forEach(function(b){ bankItems.push({se:b}); });
  if(fmts.tc) BANK.filter(function(b){return b.type==="TC" && bankInPool(b,poolNames,pool,fullBank);}).forEach(function(b){
    b.blanks.forEach(function(bl,bi){ bankItems.push({tc:b,bi:bi}); });
  });
  bankItems=shuffle(bankItems);
  var queue=[], guard=0;
  var bankQuota = Math.min(bankItems.length, Math.round(count*(gens.length?0.4:1)));
  for(var i=0;i<bankQuota;i++){ var bq=tcseCard(bankItems[i]); if(bq) queue.push(bq); }
  while(queue.length<count && gens.length && guard++<count*40){
    var q=gens[rnd(gens.length)]();
    if(q && !dup(queue,q)) queue.push(q);
  }
  var bi2=bankQuota;
  while(queue.length<count && bi2<bankItems.length){ var c=tcseCard(bankItems[bi2++]); if(c) queue.push(c); }
  return shuffle(queue).slice(0,count);
}
function dup(queue,q){ return queue.some(function(x){return x.stem===q.stem;}); }

/* ================= RUN A TEST ================= */
var run=null;
function start(){
  var queue=buildQueue(current.pool, current.fmts, current.count||15, current.fullBank);
  if(!queue.length){ body.querySelector('.qz-start').insertAdjacentHTML('beforebegin','<div class="qz-err">Couldn\'t build questions for this pool — try a broader Test button.</div>'); return; }
  run = { queue:queue, i:0, score:0, streak:0, correct:0, missed:[] };
  titleEl.textContent = "Test in progress";
  renderQ();
}
function renderQ(){
  var q=run.queue[run.i];
  q._picked = q.multi ? [] : null; q._answered=false;
  var h='';
  h+='<div class="qz-bar"><span class="qz-score">Score <b>'+run.score+'</b></span>'+
     '<span>Q '+(run.i+1)+' / '+run.queue.length+'</span>'+
     '<span class="qz-streak">'+(run.streak>1?('🔥 '+run.streak+' streak'):'')+'</span></div>';
  h+='<div class="qz-prog"><i style="width:'+(run.i/run.queue.length*100)+'%"></i></div>';
  h+='<div class="qz-type">'+esc(q.type)+'</div>';
  h+='<div class="qz-stem">'+q.stem+'</div>';
  if(q.hint) h+='<div class="qz-hint">'+esc(q.hint)+'</div>';
  if(q.note) h+='<div class="qz-hint">Tip: '+q.note+'</div>';
  h+='<div class="qz-opts" id="qzOpts">'+
     q.opts.map(function(o,i){ return '<button class="qz-opt" data-i="'+i+'"><span class="lab">'+LAB[i]+'</span>'+esc(o.text)+'</button>'; }).join("")+'</div>';
  h+='<div class="qz-expl" id="qzExpl"></div>';
  h+='<div class="qz-actions">'+
     (q.multi?'<button class="qz-btn" id="qzCheck" disabled>Check answer</button>':'')+
     '<button class="qz-btn ghost" id="qzNext" style="display:none">'+(run.i+1<run.queue.length?'Next →':'See results')+'</button></div>';
  body.innerHTML=h;
  [].slice.call(body.querySelectorAll('.qz-opt')).forEach(function(el){
    el.addEventListener('click',function(){
      if(q._answered) return;
      var i=+el.getAttribute('data-i');
      if(q.multi){
        var pos=q._picked.indexOf(i);
        if(pos>=0){ q._picked.splice(pos,1); el.classList.remove('sel'); }
        else { if(q._picked.length>=2) return; q._picked.push(i); el.classList.add('sel'); }
        body.querySelector('#qzCheck').disabled = q._picked.length!==2;
      } else { grade(q,[i]); }
    });
  });
  if(q.multi) body.querySelector('#qzCheck').addEventListener('click',function(){ grade(q,q._picked.slice()); });
  body.querySelector('#qzNext').addEventListener('click', next);
}
function grade(q,picked){
  q._answered=true;
  var correctIdx=[]; q.opts.forEach(function(o,i){ if(o.correct) correctIdx.push(i); });
  var right = picked.length===correctIdx.length && picked.every(function(i){return q.opts[i].correct;});
  [].slice.call(body.querySelectorAll('.qz-opt')).forEach(function(el,i){
    el.disabled=true;
    if(q.opts[i].correct) el.classList.add('correct');
    else if(picked.indexOf(i)>=0) el.classList.add('wrong');
    else el.classList.add('muted');
  });
  var pts=0;
  if(right){ run.streak++; run.correct++; pts=10+(run.streak>1?(run.streak-1)*2:0); run.score+=pts; }
  else { run.streak=0; run.missed.push(q); }
  var ex=body.querySelector('#qzExpl');
  var lines=q.opts.map(function(o,i){ return '<div class="ln '+(o.correct?'r':'x')+'"><span class="w">'+LAB[i]+'. '+esc(o.text)+'</span> — '+(o.why||'')+'</div>'; }).join("");
  ex.innerHTML='<div class="verdict '+(right?'ok':'no')+'">'+(right?'✓ Correct  +'+pts+' pts':'✗ Not quite')+'</div>'+
    (q.note?'<div class="note">'+q.note+'</div>':'')+'<div class="lines">'+lines+'</div>';
  ex.classList.add('show');
  if(body.querySelector('#qzCheck')) body.querySelector('#qzCheck').style.display='none';
  body.querySelector('#qzNext').style.display='';
}
function next(){ run.i++; if(run.i>=run.queue.length){ results(); return; } renderQ(); }
function results(){
  titleEl.textContent="Results";
  var total=run.queue.length, pct=Math.round(run.correct/total*100);
  var msg=pct>=90?"Outstanding — these are locked in.":pct>=75?"Strong. Review the few you missed and move on.":pct>=50?"Getting there — re-drill the misses below.":"Early days. Re-study this batch and test again.";
  var h='<div class="qz-res"><div class="pct">You scored</div><div class="big">'+run.score+'</div>'+
        '<div class="pct">'+run.correct+' / '+total+' correct · '+pct+'%</div><div class="msg">'+msg+'</div></div>';
  if(run.missed.length){
    h+='<div class="qz-review"><h4>Review — '+run.missed.length+' to revisit</h4>'+
       run.missed.map(function(q){
         var ans=q.opts.filter(function(o){return o.correct;}).map(function(o){return o.text;}).join(" + ");
         var stem=q.stem.replace(/<[^>]+>/g,'');
         return '<div class="item">'+esc(stem.length>90?stem.slice(0,90)+'…':stem)+'<br>Answer: <b>'+esc(ans)+'</b></div>';
       }).join("")+'</div>';
  }
  h+='<div class="qz-actions"><button class="qz-btn" id="qzAgain">Test again</button><button class="qz-btn ghost" id="qzDone">Done</button></div>';
  body.innerHTML=h;
  body.querySelector('#qzAgain').addEventListener('click',function(){ showSetup(lastScope); });
  body.querySelector('#qzDone').addEventListener('click', close);
}

/* ================= STUDIED-MARKER UI (generic, every word-bearing section) ================= */
function sectionEls(h2id){
  var h2=document.getElementById(h2id); if(!h2) return [];
  var els=[], n=h2.nextElementSibling;
  while(n && n.tagName!=='H2'){ els.push(n); n=n.nextElementSibling; }
  return els;
}
// extract glossary words mentioned anywhere in an element's text
function tokWords(el){
  var set={}, m=el.textContent.toLowerCase().match(/[a-zé][a-zé'-]{2,}/g)||[];
  m.forEach(function(t){ if(BYWORD[t]) set[t]=1; });
  return Object.keys(set);
}
// the sections that get per-unit "studied up to here" markers
var SECTIONS = [
  {scope:"roots",      h2:"3-root-word-encyclopedia",        noun:"root families"},
  {scope:"clusters",   h2:"4-semantic--synonym-clusters",    noun:"meaning clusters"},
  {scope:"se",         h2:"5-sentence-equivalence-clusters",  noun:"SE groups",        fullBank:true},
  {scope:"polarity",   h2:"6-text-completion-polarity-map",   noun:"polarity banks",   fullBank:true},
  {scope:"confusing",  h2:"7-common-confusing-words",         noun:"confusing words"},
  {scope:"wordgroups", h2:"8-word-groups-rebuilt-for-memory", noun:"word groups"},
];
var REG = {};   // scope -> {def, heads:[{el,words}], whole:[words], noun, fullBank}
function mark(rt){ return parseInt(get("gre_sm_"+rt.def.scope,"0"),10)||0; }
function setMark(rt,v){ set("gre_sm_"+rt.def.scope, String(v)); }

function setupSection(def){
  var els=sectionEls(def.h2); if(!els.length) return;
  var heads=[], cur=null;
  els.forEach(function(e){
    if(e.tagName==="H3"){ cur={el:e, nodes:[e]}; heads.push(cur); }
    else if(cur){ cur.nodes.push(e); }
  });
  heads.forEach(function(hd){
    var set={}; hd.nodes.forEach(function(n){ tokWords(n).forEach(function(w){ set[w]=1; }); });
    hd.words=Object.keys(set);
  });
  heads=heads.filter(function(hd){ return hd.words.length>0; });
  var rt={def:def, heads:heads, noun:def.noun, fullBank:def.fullBank};
  if(!heads.length){
    var set2={}; els.forEach(function(n){ tokWords(n).forEach(function(w){ set2[w]=1; }); });
    rt.whole=Object.keys(set2);
  } else {
    var bar=document.createElement("div"); bar.className="study-progress"; bar.id="prog_"+def.scope;
    var h2=document.getElementById(def.h2); h2.parentNode.insertBefore(bar, h2.nextSibling);
    heads.forEach(function(hd,i){
      var b=document.createElement("button"); b.className="study-mark"; b.type="button";
      b.addEventListener("click",function(ev){ ev.preventDefault();
        var c=mark(rt); setMark(rt, c===i+1 ? i : i+1); renderMarks(rt);
      });
      hd.el.appendChild(b);
    });
    renderMarks(rt);
  }
  REG[def.scope]=rt;
}
function renderMarks(rt){
  var n=mark(rt);
  rt.heads.forEach(function(hd,i){
    hd.el.classList.toggle("studied", i<n);
    var b=hd.el.querySelector(".study-mark");
    if(i===n-1){ b.textContent="✓ studied up to here"; b.classList.add("here"); }
    else { b.textContent="mark studied to here"; b.classList.remove("here"); }
  });
  var p=document.getElementById("prog_"+rt.def.scope);
  if(p) p.innerHTML="📍 You've studied <b>"+n+" / "+rt.heads.length+"</b> "+rt.noun+
    ". This section's <b>Test</b> button will quiz you on "+(n?"just these.":"all of them — mark a stopping point to narrow it.");
}
// words to test for a section. forGlobal=true means only count it if explicitly marked.
function sectionWords(scope, forGlobal){
  var rt=REG[scope]; if(!rt) return [];
  if(rt.whole) return forGlobal ? [] : rt.whole;
  var n=mark(rt);
  var hs = (n>0) ? rt.heads.slice(0,n) : (forGlobal ? [] : rt.heads);
  var set={}; hs.forEach(function(hd){ hd.words.forEach(function(w){ set[w]=1; }); });
  return Object.keys(set);
}

// glossary §11 keeps its own letter-based marker (its tables are too big to tokenize)
var glossHeads=[], glossLetters=[];
function initGloss(){
  glossHeads = sectionEls("11-master-az-glossary-every-word").filter(function(e){
    return e.tagName==="H3" && /^[A-Z]$/.test(e.textContent.trim());
  });
  glossLetters = glossHeads.map(function(h){ return h.textContent.trim(); });
  if(!glossHeads.length) return;
  glossHeads.forEach(function(h,i){
    var b=document.createElement("button"); b.className="study-mark"; b.type="button";
    b.addEventListener("click",function(ev){ ev.preventDefault();
      var cur=studiedGloss(); set(LS_GLOSS, cur===glossLetters[i] ? (glossLetters[i-1]||"") : glossLetters[i]); renderGlossMarks();
    });
    h.appendChild(b);
  });
  renderGlossMarks();
}
function renderGlossMarks(){
  var L=studiedGloss(), idx=glossLetters.indexOf(L);
  glossHeads.forEach(function(h,i){
    h.classList.toggle("studied", L && i<=idx);
    var b=h.querySelector(".study-mark");
    if(i===idx){ b.textContent="✓ studied through "+L; b.classList.add("here"); }
    else { b.textContent="mark studied to here"; b.classList.remove("here"); }
  });
}
function initStudy(){ SECTIONS.forEach(setupSection); initGloss(); }

/* ================= LAUNCHERS ================= */
function wireLaunchers(){
  [].slice.call(document.querySelectorAll('.quiz-launch')).forEach(function(b){
    b.addEventListener('click',function(){ showSetup(b.getAttribute('data-scope')||""); });
  });
}
function boot(){ wireLaunchers(); initStudy(); }
if(document.readyState!=="loading") boot();
else document.addEventListener("DOMContentLoaded", boot);

})();
