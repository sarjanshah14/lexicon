/* GRE Lexicon practice engine.
   Pick-range-per-test: every launch opens a setup screen where you choose the pool
   (all / high-frequency / by letter / by root / by cluster) and the question formats.
   Vocab MCQs are generated live from window.QUIZ (faithful to the glossary); TC/SE come
   from the authored window.TCSE bank. Nothing is stored — score lives in the session only. */
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
function uniqBy(a,key){ var seen={},out=[]; a.forEach(function(x){var k=key(x); if(!seen[k]){seen[k]=1;out.push(x);}}); return out; }
var LAB = ["A","B","C","D","E","F"];

/* ---------- state ---------- */
var sel = { roots:{}, clusters:{}, letters:{}, hf:false, fmts:{} };
var DEFAULT_FMTS = ["def","rev","syn","ant"];
var run = null; // active quiz

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

/* ================= SETUP SCREEN ================= */
var LETTERS = (function(){ var s={}; WORDS.forEach(function(w){ s[w.w[0].toUpperCase()]=1; }); return Object.keys(s).sort(); })();
var FORMATS = [
  ["def","Definition","word → meaning"],
  ["rev","Reverse","meaning → word"],
  ["syn","Synonyms","pick a synonym"],
  ["ant","Antonyms","pick an antonym"],
  ["root","Roots","root → meaning"],
  ["tc","Text Completion","fill the blank(s)"],
  ["se","Sentence Equiv.","pick the matching pair"]
];

function showSetup(scope){
  titleEl.textContent = "Set up your test";
  // pre-scope from a section button
  sel.fmts = {}; DEFAULT_FMTS.forEach(function(f){ sel.fmts[f]=true; });
  if(scope==="roots"){ sel.fmts={root:true,def:true,syn:true}; }
  if(scope==="clusters"){ sel.fmts={se:true,def:true,ant:true}; }
  if(scope==="tcse"){ sel.fmts={tc:true,se:true}; }

  var h = '<div class="qz-set">';

  // --- pool: source ---
  h += '<h4>1 · What should I test you on?</h4>';
  h += '<p class="qz-sub">Tick only what you have studied. Leave roots / clusters / letters blank to draw from the whole list.</p>';

  h += '<div class="qz-chips" id="qzScopeQuick">'+
       chip("hf","★ High-frequency only",false,"scope")+
       '</div>';

  h += '<h4 style="margin-top:14px">Roots ('+Q.roots.length+')</h4>';
  h += '<div class="qz-chips" id="qzRoots">'+
       Q.roots.map(function(r,i){ return chip("r"+i, r.root, false, "root"); }).join("")+'</div>';

  if(Q.clusters.length){
    h += '<h4>Semantic clusters ('+Q.clusters.length+')</h4>';
    h += '<div class="qz-chips" id="qzClusters">'+
       Q.clusters.map(function(c,i){ return chip("c"+i, c.name, false, "cluster"); }).join("")+'</div>';
  }

  h += '<h4>By first letter</h4>';
  h += '<div class="qz-chips" id="qzLetters">'+
       LETTERS.map(function(L){ return chip("L"+L, L, false, "letter"); }).join("")+'</div>';

  // --- formats ---
  h += '<h4>2 · Question types</h4>';
  h += '<div class="qz-chips" id="qzFmts">'+
       FORMATS.map(function(f){ return '<span class="qz-chip fmt'+(sel.fmts[f[0]]?" on":"")+'" data-fmt="'+f[0]+'" title="'+f[2]+'">'+f[1]+'</span>'; }).join("")+'</div>';

  // --- count ---
  h += '<h4>3 · How many questions?</h4>';
  h += '<div class="qz-count" id="qzCount">'+
       [10,15,20,30].map(function(n,i){ return '<span class="qz-chip cnt'+(i===0?" on":"")+'" data-n="'+n+'">'+n+'</span>'; }).join("")+'</div>';

  h += '<div class="qz-pool" id="qzPool"></div>';
  h += '<div class="qz-err" id="qzErr"></div>';
  h += '<button class="qz-start" id="qzStart">Start test</button>';
  h += '</div>';
  body.innerHTML = h;

  // reset selection model
  sel.roots={}; sel.clusters={}; sel.letters={}; sel.hf=false;
  sel.count = 10;

  // pre-check format chips already in sel.fmts handled above; sync chip 'on' states
  body.querySelectorAll('#qzFmts .qz-chip').forEach(function(c){
    c.classList.toggle('on', !!sel.fmts[c.getAttribute('data-fmt')]);
  });

  // wire chips
  bindToggle('#qzScopeQuick',function(el){ sel.hf = el.classList.toggle('on'); refreshPool(); });
  bindToggle('#qzRoots',function(el,i){ toggleKey(sel.roots,i,el); refreshPool(); });
  bindToggle('#qzClusters',function(el,i){ toggleKey(sel.clusters,i,el); refreshPool(); });
  bindToggle('#qzLetters',function(el,i){ toggleKey(sel.letters,i,el); refreshPool(); });
  body.querySelectorAll('#qzFmts .qz-chip').forEach(function(c){
    c.addEventListener('click',function(){ var f=c.getAttribute('data-fmt'); sel.fmts[f]=!sel.fmts[f]; c.classList.toggle('on'); refreshPool(); });
  });
  body.querySelectorAll('#qzCount .qz-chip').forEach(function(c){
    c.addEventListener('click',function(){
      body.querySelectorAll('#qzCount .qz-chip').forEach(function(x){x.classList.remove('on');});
      c.classList.add('on'); sel.count=parseInt(c.getAttribute('data-n'),10); refreshPool();
    });
  });

  // pre-scope checks
  if(scope==="roots") selectAll('#qzRoots', sel.roots);
  if(scope==="clusters" && Q.clusters.length) selectAll('#qzClusters', sel.clusters);
  if(scope==="hf"){ var hfc=body.querySelector('#qzScopeQuick .qz-chip'); if(hfc){ hfc.classList.add('on'); sel.hf=true; } }

  body.querySelector('#qzStart').addEventListener('click', start);
  refreshPool();
  open();
}

function chip(id,label,on,kind){
  return '<span class="qz-chip'+(on?" on":"")+'" data-id="'+id+'" data-kind="'+kind+'">'+esc(label)+'</span>';
}
function bindToggle(selStr,fn){
  var box=body.querySelector(selStr); if(!box) return;
  [].slice.call(box.querySelectorAll('.qz-chip')).forEach(function(el,i){
    el.addEventListener('click',function(){ fn(el,i); });
  });
}
function toggleKey(obj,i,el){ if(obj[i]){delete obj[i];el.classList.remove('on');} else {obj[i]=1;el.classList.add('on');} }
function selectAll(selStr,obj){
  var box=body.querySelector(selStr); if(!box) return;
  [].slice.call(box.querySelectorAll('.qz-chip')).forEach(function(el,i){ obj[i]=1; el.classList.add('on'); });
  refreshPool();
}

/* build the active word pool from current selections */
function buildPool(){
  var set={};
  Object.keys(sel.roots).forEach(function(i){ (Q.roots[i].words||[]).forEach(function(w){ if(BYWORD[w]) set[w]=1; }); });
  Object.keys(sel.clusters).forEach(function(i){ (Q.clusters[i].words||[]).forEach(function(w){ if(BYWORD[w]) set[w]=1; }); });
  var letters = Object.keys(sel.letters).map(function(k){ return k.replace('L',''); });
  if(letters.length){
    WORDS.forEach(function(w){ if(letters.indexOf(w.w[0].toUpperCase())>=0) set[w.w.toLowerCase()]=1; });
  }
  var keys = Object.keys(set);
  var pool;
  if(keys.length){ pool = keys.map(function(k){ return BYWORD[k]; }); }
  else { pool = WORDS.slice(); }            // nothing picked -> whole list
  if(sel.hf) pool = pool.filter(function(w){ return w.hf; });
  return pool;
}
function refreshPool(){
  var pool=buildPool();
  var fmts=Object.keys(sel.fmts).filter(function(f){return sel.fmts[f];});
  var poolNames={}; pool.forEach(function(w){poolNames[w.w.toLowerCase()]=1;});
  var tcN = BANK.filter(function(b){return b.type==="TC" && bankInPool(b,poolNames,pool);}).length;
  var seN = BANK.filter(function(b){return b.type==="SE" && bankInPool(b,poolNames,pool);}).length;
  var el=body.querySelector('#qzPool');
  var bits=['<b>'+pool.length+'</b> words in pool'];
  if(sel.fmts.tc) bits.push(tcN+' TC');
  if(sel.fmts.se) bits.push(seN+' SE');
  el.innerHTML = 'Pool: '+bits.join(' · ')+' · formats: <b>'+(fmts.length||0)+'</b>';
  var err=body.querySelector('#qzErr'); var start=body.querySelector('#qzStart');
  var ok = fmts.length>0 && pool.length>=4;
  start.disabled=!ok;
  err.textContent = !fmts.length ? 'Pick at least one question type.' : (pool.length<4 ? 'Pick a larger pool (need 4+ words).' : '');
}
function bankInPool(b,poolNames,pool){
  if(pool.length===WORDS.length) return true;          // whole-list pool: everything qualifies
  return (b.words||[]).some(function(w){ return poolNames[w.toLowerCase()]; });
}

/* ================= QUESTION GENERATION ================= */
function withMeaning(pool){ return pool.filter(function(w){return w.m;}); }

function makeDef(pool){
  var src=withMeaning(pool); if(src.length<4) return null;
  var w=src[rnd(src.length)];
  var distract=sample(WORDS.filter(function(x){
    return x.w!==w.w && x.m && x.m!==w.m && (w.s||[]).indexOf(x.w)<0;
  }),3);
  var opts=shuffle([w].concat(distract)).map(function(x){
    return { text:cap(x.m), correct:x.w===w.w,
             why: x.w===w.w ? "This is the meaning of <b>"+esc(w.w)+"</b>." :
                  "This is the meaning of <b>"+esc(x.w)+"</b>, not "+esc(w.w)+"." };
  });
  return { type:"Definition", stem:"Which is the best meaning of <b>"+esc(w.w)+"</b>?", opts:opts, multi:false };
}
function makeRev(pool){
  var src=withMeaning(pool); if(src.length<4) return null;
  var w=src[rnd(src.length)];
  var distract=sample(WORDS.filter(function(x){ return x.w!==w.w && x.m && x.m!==w.m; }),3);
  var opts=shuffle([w].concat(distract)).map(function(x){
    return { text:cap(x.w), correct:x.w===w.w,
             why: x.w===w.w ? "<b>"+esc(w.w)+"</b> — "+esc(w.m)+"." :
                  "<b>"+esc(x.w)+"</b> means "+esc(x.m)+"." };
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
    return { text:cap(o.t), correct:o.c,
             why:o.c ? "<b>"+esc(ans)+"</b> is a listed synonym of "+esc(w.w)+" ("+esc(w.m)+")." :
                       "Not a synonym of "+esc(w.w)+"." };
  });
  return { type:"Synonym", stem:"Which word is closest in meaning to <b>"+esc(w.w)+"</b>?", opts:opts, multi:false,
           note:"<b>"+esc(w.w)+"</b> means "+esc(w.m)+"." };
}
function makeAnt(pool){
  var src=pool.filter(function(w){ return w.a && w.a.length; }); if(src.length<1) return null;
  var w=src[rnd(src.length)];
  var ans=w.a[rnd(w.a.length)];
  var bad={}; (w.a||[]).forEach(function(x){bad[x.toLowerCase()]=1;}); (w.s||[]).forEach(function(x){bad[x.toLowerCase()]=1;}); bad[w.w.toLowerCase()]=1;
  var distract=sample(WORDS.filter(function(x){ return !bad[x.w.toLowerCase()]; }),3).map(function(x){return x.w;});
  if(distract.length<3) return null;
  var opts=shuffle([{t:ans,c:true}].concat(distract.map(function(d){return {t:d,c:false};}))).map(function(o){
    return { text:cap(o.t), correct:o.c,
             why:o.c ? "<b>"+esc(ans)+"</b> is a listed antonym of "+esc(w.w)+" ("+esc(w.m)+")." :
                       "Not an antonym of "+esc(w.w)+"." };
  });
  return { type:"Antonym", stem:"Which word is most nearly <i>opposite</i> to <b>"+esc(w.w)+"</b>?", opts:opts, multi:false,
           note:"<b>"+esc(w.w)+"</b> means "+esc(w.m)+"." };
}
function makeRoot(){
  if(Q.roots.length<4) return null;
  var r=Q.roots[rnd(Q.roots.length)];
  var distract=sample(Q.roots.filter(function(x){return x.root!==r.root;}),3);
  var opts=shuffle([r].concat(distract)).map(function(x){
    return { text:cap(x.mean), correct:x.root===r.root,
             why:x.root===r.root ? "The root <b>"+esc(r.root)+"</b> means “"+esc(r.mean)+"” (e.g. "+esc((r.words||[]).slice(0,3).join(", "))+")." :
                  "“"+esc(x.mean)+"” is the meaning of the root <b>"+esc(x.root)+"</b>." };
  });
  return { type:"Root", stem:"What does the root <b>"+esc(r.root)+"</b> mean?", opts:opts, multi:false };
}

function makeBank(b){
  if(b.type==="SE"){
    var opts=b.opts.map(function(w,i){
      return { text:cap(w), correct:b.ans.indexOf(i)>=0, why:b.expl[w]||"" };
    });
    return { type:"Sentence Equivalence", stem:esc(b.stem), opts:opts, multi:true,
             note:b.pairNote||"", hint:"Select the TWO words that give the sentence the same meaning." };
  }
  // TC: flatten to one blank at a time (each blank scored as its own question card)
  return null; // handled specially below
}

/* build the question queue from selections */
function buildQueue(pool,fmts,count){
  var poolNames={}; pool.forEach(function(w){poolNames[w.w.toLowerCase()]=1;});
  var gens=[];
  if(fmts.def) gens.push(function(){return makeDef(pool);});
  if(fmts.rev) gens.push(function(){return makeRev(pool);});
  if(fmts.syn) gens.push(function(){return makeSyn(pool);});
  if(fmts.ant) gens.push(function(){return makeAnt(pool);});
  if(fmts.root) gens.push(makeRoot);

  // bank items eligible for this pool
  var bankItems=[];
  if(fmts.se) BANK.filter(function(b){return b.type==="SE" && bankInPool(b,poolNames,pool);}).forEach(function(b){ bankItems.push({se:b}); });
  if(fmts.tc) BANK.filter(function(b){return b.type==="TC" && bankInPool(b,poolNames,pool);}).forEach(function(b){
    b.blanks.forEach(function(bl,bi){ bankItems.push({tc:b,bi:bi}); });
  });
  bankItems=shuffle(bankItems);

  var queue=[], guard=0;
  // interleave: aim ~ one third bank items if available
  var bankQuota = Math.min(bankItems.length, Math.round(count* (gens.length? 0.4 : 1)));
  for(var i=0;i<bankQuota;i++){ var bq=tcseCard(bankItems[i]); if(bq) queue.push(bq); }
  while(queue.length<count && gens.length && guard++<count*40){
    var q=gens[rnd(gens.length)]();
    if(q && !dup(queue,q)) queue.push(q);
  }
  // if only bank formats chosen, fill from remaining bank
  var bi2=bankQuota;
  while(queue.length<count && bi2<bankItems.length){ var c=tcseCard(bankItems[bi2++]); if(c) queue.push(c); }
  return shuffle(queue).slice(0,count);
}
function dup(queue,q){ return queue.some(function(x){return x.stem===q.stem;}); }

function tcseCard(it){
  if(it.se){
    var b=it.se;
    var opts=b.opts.map(function(w,i){ return { text:cap(w), correct:b.ans.indexOf(i)>=0, why:b.expl[w]||"" }; });
    return { type:"Sentence Equivalence", stem:esc(b.stem), opts:opts, multi:true,
             note:b.pairNote||"", hint:"Select the TWO words that give the sentence the same meaning." };
  }
  if(it.tc){
    var t=it.tc, bl=t.blanks[it.bi];
    var stem=t.blanks.length>1
      ? esc(t.stem).replace(/\((i+)\)_{2,}/g,function(_,r){ return '<span class="bk">('+r+') ____</span>'; })
      : esc(t.stem).replace(/_{2,}/g,'<span class="bk">____</span>');
    var label = t.blanks.length>1 ? "Blank "+(it.bi===0?"(i)":it.bi===1?"(ii)":"(iii)")+" — choose the best word:" : null;
    var opts=bl.opts.map(function(w,i){ return { text:cap(w), correct:i===bl.ans, why:bl.expl[w]||"" }; });
    return { type:"Text Completion"+(t.blanks.length>1?" · double blank":""), stem:stem, opts:shuffleKeepWhy(opts), multi:false, hint:label };
  }
  return null;
}
function shuffleKeepWhy(opts){ return shuffle(opts); }

/* ================= RUN A TEST ================= */
function start(){
  var pool=buildPool();
  var fmts=sel.fmts;
  var queue=buildQueue(pool, fmts, sel.count);
  if(!queue.length){ body.querySelector('#qzErr').textContent="Couldn't build questions for that selection — widen the pool or pick more types."; return; }
  run = { queue:queue, i:0, score:0, streak:0, best:0, correct:0, missed:[] };
  titleEl.textContent = "Test in progress";
  renderQ();
}

function renderQ(){
  var q=run.queue[run.i];
  q._picked = q.multi ? [] : null;
  q._answered=false;
  var h='';
  h+='<div class="qz-bar">'+
     '<span class="qz-score">Score <b>'+run.score+'</b></span>'+
     '<span>Q '+(run.i+1)+' / '+run.queue.length+'</span>'+
     '<span class="qz-streak">'+(run.streak>1?('🔥 '+run.streak+' streak'):'')+'</span>'+
     '</div>';
  h+='<div class="qz-prog"><i style="width:'+(run.i/run.queue.length*100)+'%"></i></div>';
  h+='<div class="qz-type">'+esc(q.type)+'</div>';
  h+='<div class="qz-stem">'+q.stem+'</div>';
  if(q.hint) h+='<div class="qz-hint">'+esc(q.hint)+'</div>';
  if(q.note) h+='<div class="qz-hint">Tip: '+q.note+'</div>';
  h+='<div class="qz-opts" id="qzOpts">'+
     q.opts.map(function(o,i){ return '<button class="qz-opt" data-i="'+i+'"><span class="lab">'+LAB[i]+'</span>'+esc(o.text)+'</button>'; }).join("")+
     '</div>';
  h+='<div class="qz-expl" id="qzExpl"></div>';
  h+='<div class="qz-actions">'+
     (q.multi?'<button class="qz-btn" id="qzCheck" disabled>Check answer</button>':'')+
     '<button class="qz-btn ghost" id="qzNext" style="display:none">'+(run.i+1<run.queue.length?'Next →':'See results')+'</button>'+
     '</div>';
  body.innerHTML=h;

  var optEls=[].slice.call(body.querySelectorAll('.qz-opt'));
  optEls.forEach(function(el){
    el.addEventListener('click',function(){
      if(q._answered) return;
      var i=+el.getAttribute('data-i');
      if(q.multi){
        var pos=q._picked.indexOf(i);
        if(pos>=0){ q._picked.splice(pos,1); el.classList.remove('sel'); }
        else { if(q._picked.length>=2) return; q._picked.push(i); el.classList.add('sel'); }
        body.querySelector('#qzCheck').disabled = q._picked.length!==2;
      } else {
        grade(q,[i]);
      }
    });
  });
  if(q.multi){ body.querySelector('#qzCheck').addEventListener('click',function(){ grade(q,q._picked.slice()); }); }
  body.querySelector('#qzNext').addEventListener('click', next);
}

function grade(q,picked){
  q._answered=true;
  var correctIdx=[]; q.opts.forEach(function(o,i){ if(o.correct) correctIdx.push(i); });
  var right = picked.length===correctIdx.length && picked.every(function(i){return q.opts[i].correct;});

  var optEls=[].slice.call(body.querySelectorAll('.qz-opt'));
  optEls.forEach(function(el,i){
    el.disabled=true;
    if(q.opts[i].correct) el.classList.add('correct');
    else if(picked.indexOf(i)>=0) el.classList.add('wrong');
    else el.classList.add('muted');
  });

  // scoring
  if(right){
    run.streak++; run.correct++;
    var pts=10 + (run.streak>1?(run.streak-1)*2:0);
    run.score+=pts;
  } else {
    run.streak=0;
    run.missed.push(q);
  }

  // explanation panel: verdict + per-option why
  var ex=body.querySelector('#qzExpl');
  var lines = q.opts.map(function(o,i){
    return '<div class="ln '+(o.correct?'r':'x')+'"><span class="w">'+LAB[i]+'. '+esc(o.text)+'</span> — '+(o.why||'')+'</div>';
  }).join("");
  ex.innerHTML =
    '<div class="verdict '+(right?'ok':'no')+'">'+(right?'✓ Correct  +'+(10+(run.streak>1?(run.streak-1)*2:0))+' pts':'✗ Not quite')+'</div>'+
    (q.note?'<div class="note">'+q.note+'</div>':'')+
    '<div class="lines">'+lines+'</div>';
  ex.classList.add('show');

  if(body.querySelector('#qzCheck')) body.querySelector('#qzCheck').style.display='none';
  body.querySelector('#qzNext').style.display='';
}

function next(){
  run.i++;
  if(run.i>=run.queue.length){ results(); return; }
  renderQ();
}

function results(){
  titleEl.textContent="Results";
  var total=run.queue.length;
  var pct=Math.round(run.correct/total*100);
  var msg = pct>=90?"Outstanding — these are locked in.":
            pct>=75?"Strong. Review the few you missed and move on.":
            pct>=50?"Getting there — re-drill the misses below.":
            "Early days. Re-study this batch and test again.";
  var h='<div class="qz-res">'+
        '<div class="pct">You scored</div>'+
        '<div class="big">'+run.score+'</div>'+
        '<div class="pct">'+run.correct+' / '+total+' correct · '+pct+'%</div>'+
        '<div class="msg">'+msg+'</div>'+
        '</div>';
  if(run.missed.length){
    h+='<div class="qz-review"><h4>Review — '+run.missed.length+' to revisit</h4>'+
       run.missed.map(function(q){
         var ans=q.opts.filter(function(o){return o.correct;}).map(function(o){return o.text;}).join(" + ");
         var stem=q.stem.replace(/<[^>]+>/g,'');
         return '<div class="item">'+esc(stem.length>90?stem.slice(0,90)+'…':stem)+'<br>Answer: <b>'+esc(ans)+'</b></div>';
       }).join("")+'</div>';
  }
  h+='<div class="qz-actions"><button class="qz-btn" id="qzAgain">New test</button>'+
     '<button class="qz-btn ghost" id="qzDone">Done</button></div>';
  body.innerHTML=h;
  body.querySelector('#qzAgain').addEventListener('click',function(){ showSetup(); });
  body.querySelector('#qzDone').addEventListener('click', close);
}

/* ================= LAUNCHERS ================= */
function wireLaunchers(){
  [].slice.call(document.querySelectorAll('.quiz-launch')).forEach(function(b){
    b.addEventListener('click',function(){ showSetup(b.getAttribute('data-scope')||""); });
  });
}
if(document.readyState!=="loading") wireLaunchers();
else document.addEventListener("DOMContentLoaded", wireLaunchers);

})();
