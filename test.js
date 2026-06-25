/* Standalone practice page for the GRE lexicon.
   Draws from the whole 775-word lexicon; pick a test type + length and go.
   Vocab questions are generated live from the glossary (always faithful); TC/SE
   come from the authored bank. Score is per-session only — nothing is stored. */
(function(){
"use strict";
var Q = window.QUIZ || {words:[],roots:[]};
var BANK = window.TCSE || [];
var WORDS = Q.words;

function rnd(n){ return Math.floor(Math.random()*n); }
function shuffle(a){ a=a.slice(); for(var i=a.length-1;i>0;i--){var j=rnd(i+1);var t=a[i];a[i]=a[j];a[j]=t;} return a; }
function sample(a,n){ return shuffle(a).slice(0,n); }
function cap(s){ return s.charAt(0).toUpperCase()+s.slice(1); }
function esc(s){ return (s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;"); }
var LAB=["A","B","C","D","E","F"];
var app=document.getElementById("tApp");

var MODES=[
  {id:"mixed",  name:"Mixed test",            desc:"Anything from the lexicon — definitions, synonyms, antonyms, roots, and Text Completion / Sentence Equivalence, all blended.", fmts:{def:1,rev:1,syn:1,ant:1,root:1,tc:1,se:1}, full:true},
  {id:"def",    name:"Definitions",           desc:"Match a word to its meaning, and a meaning to its word.", fmts:{def:1,rev:1}},
  {id:"synant", name:"Synonyms & Antonyms",   desc:"Pick the closest synonym or the truest opposite.", fmts:{syn:1,ant:1}},
  {id:"roots",  name:"Roots",                 desc:"What does each root mean? Build the family from the root.", fmts:{root:1}},
  {id:"tcse",   name:"Text Completion & SE",  desc:"Fill the blank, and pick the matching pair — with full explanations.", fmts:{tc:1,se:1}, fullBank:true},
];
var state={mode:MODES[0], count:15};

/* ================= start screen ================= */
function startScreen(){
  var h='<div class="t-hero"><div class="t-kicker">Practice</div>'+
        '<h1>Test yourself</h1><p>Every question is drawn from the full 775-word lexicon. '+
        'Pick a type and a length — you\'ll get one question at a time with the answer explained.</p></div>';
  h+='<div class="t-label">Choose a test</div><div class="mode-grid">';
  MODES.forEach(function(m){
    h+='<button class="mode'+(m.full?' full':'')+(state.mode.id===m.id?' sel':'')+'" data-m="'+m.id+'">'+
       '<h3>'+esc(m.name)+'</h3><p>'+esc(m.desc)+'</p></button>';
  });
  h+='</div>';
  h+='<div class="t-label">How many questions?</div><div class="t-counts">'+
     [10,15,20,25,30].map(function(n){ return '<button class="t-chip'+(state.count===n?' on':'')+'" data-n="'+n+'">'+n+'</button>'; }).join("")+'</div>';
  h+='<button class="t-start" id="tStart">Start test</button>';
  app.innerHTML=h;
  app.querySelectorAll('.mode').forEach(function(b){
    b.addEventListener('click',function(){ state.mode=MODES.filter(function(m){return m.id===b.getAttribute('data-m');})[0]; startScreen(); });
  });
  app.querySelectorAll('.t-chip').forEach(function(b){
    b.addEventListener('click',function(){ state.count=parseInt(b.getAttribute('data-n'),10); startScreen(); });
  });
  document.getElementById('tStart').addEventListener('click', start);
  window.scrollTo(0,0);
}

/* ================= generators ================= */
function withMeaning(pool){ return pool.filter(function(w){return w.m;}); }
function makeDef(pool){
  var src=withMeaning(pool); if(src.length<4) return null;
  var w=src[rnd(src.length)];
  var d=sample(WORDS.filter(function(x){return x.w!==w.w && x.m && x.m!==w.m && (w.s||[]).indexOf(x.w)<0;}),3);
  if(d.length<3) return null;
  var opts=shuffle([w].concat(d)).map(function(x){ return {text:cap(x.m),correct:x.w===w.w,
    why:x.w===w.w?"This is the meaning of <b>"+esc(w.w)+"</b>.":"This is the meaning of <b>"+esc(x.w)+"</b>, not "+esc(w.w)+"."}; });
  return {type:"Definition", stem:"Which is the best meaning of <b>"+esc(w.w)+"</b>?", opts:opts, multi:false};
}
function makeRev(pool){
  var src=withMeaning(pool); if(src.length<4) return null;
  var w=src[rnd(src.length)];
  var d=sample(WORDS.filter(function(x){return x.w!==w.w && x.m && x.m!==w.m;}),3);
  if(d.length<3) return null;
  var opts=shuffle([w].concat(d)).map(function(x){ return {text:cap(x.w),correct:x.w===w.w,
    why:x.w===w.w?"<b>"+esc(w.w)+"</b> — "+esc(w.m)+".":"<b>"+esc(x.w)+"</b> means "+esc(x.m)+"."}; });
  return {type:"Reverse", stem:"Which word means: <i>"+esc(w.m)+"</i>?", opts:opts, multi:false};
}
function makeSyn(pool){
  var src=pool.filter(function(w){return w.s && w.s.length;}); if(src.length<1) return null;
  var w=src[rnd(src.length)], ans=w.s[rnd(w.s.length)], bad={};
  (w.s||[]).forEach(function(x){bad[x.toLowerCase()]=1;}); bad[w.w.toLowerCase()]=1;
  var d=sample(WORDS.filter(function(x){return !bad[x.w.toLowerCase()];}),3).map(function(x){return x.w;});
  if(d.length<3) return null;
  var opts=shuffle([{t:ans,c:true}].concat(d.map(function(x){return {t:x,c:false};}))).map(function(o){
    return {text:cap(o.t),correct:o.c,why:o.c?"<b>"+esc(ans)+"</b> is a listed synonym of "+esc(w.w)+" ("+esc(w.m)+").":"Not a synonym of "+esc(w.w)+"."}; });
  return {type:"Synonym", stem:"Which word is closest in meaning to <b>"+esc(w.w)+"</b>?", opts:opts, multi:false, note:"<b>"+esc(w.w)+"</b> means "+esc(w.m)+"."};
}
function makeAnt(pool){
  var src=pool.filter(function(w){return w.a && w.a.length;}); if(src.length<1) return null;
  var w=src[rnd(src.length)], ans=w.a[rnd(w.a.length)], bad={};
  (w.a||[]).forEach(function(x){bad[x.toLowerCase()]=1;}); (w.s||[]).forEach(function(x){bad[x.toLowerCase()]=1;}); bad[w.w.toLowerCase()]=1;
  var d=sample(WORDS.filter(function(x){return !bad[x.w.toLowerCase()];}),3).map(function(x){return x.w;});
  if(d.length<3) return null;
  var opts=shuffle([{t:ans,c:true}].concat(d.map(function(x){return {t:x,c:false};}))).map(function(o){
    return {text:cap(o.t),correct:o.c,why:o.c?"<b>"+esc(ans)+"</b> is a listed antonym of "+esc(w.w)+" ("+esc(w.m)+").":"Not an antonym of "+esc(w.w)+"."}; });
  return {type:"Antonym", stem:"Which word is most nearly <i>opposite</i> to <b>"+esc(w.w)+"</b>?", opts:opts, multi:false, note:"<b>"+esc(w.w)+"</b> means "+esc(w.m)+"."};
}
function makeRoot(){
  if(Q.roots.length<4) return null;
  var r=Q.roots[rnd(Q.roots.length)];
  var d=sample(Q.roots.filter(function(x){return x.root!==r.root;}),3);
  var opts=shuffle([r].concat(d)).map(function(x){ return {text:cap(x.mean),correct:x.root===r.root,
    why:x.root===r.root?("The root <b>"+esc(r.root)+"</b> means “"+esc(r.mean)+"” (e.g. "+esc((r.words||[]).slice(0,3).join(", "))+")."):("“"+esc(x.mean)+"” is the meaning of the root <b>"+esc(x.root)+"</b>.")}; });
  return {type:"Root", stem:"What does the root <b>"+esc(r.root)+"</b> mean?", opts:opts, multi:false};
}
function tcseCard(it){
  if(it.se){ var b=it.se;
    var opts=b.opts.map(function(w,i){return {text:cap(w),correct:b.ans.indexOf(i)>=0,why:b.expl[w]||""};});
    return {type:"Sentence Equivalence", stem:esc(b.stem), opts:opts, multi:true, note:b.pairNote||"", hint:"Select the TWO words that give the sentence the same meaning."};
  }
  var t=it.tc, bl=t.blanks[it.bi];
  var stem=t.blanks.length>1
    ? esc(t.stem).replace(/\((i+)\)_{2,}/g,function(_,r){return '<span class="bk">('+r+') ____</span>';})
    : esc(t.stem).replace(/_{2,}/g,'<span class="bk">____</span>');
  var label=t.blanks.length>1?("Blank "+(it.bi===0?"(i)":it.bi===1?"(ii)":"(iii)")+" — choose the best word:"):null;
  var opts=bl.opts.map(function(w,i){return {text:cap(w),correct:i===bl.ans,why:bl.expl[w]||""};});
  return {type:"Text Completion"+(t.blanks.length>1?" · double blank":""), stem:stem, opts:shuffle(opts), multi:false, hint:label};
}
function buildQueue(fmts,count,fullBank){
  var pool=WORDS, gens=[];
  if(fmts.def) gens.push(function(){return makeDef(pool);});
  if(fmts.rev) gens.push(function(){return makeRev(pool);});
  if(fmts.syn) gens.push(function(){return makeSyn(pool);});
  if(fmts.ant) gens.push(function(){return makeAnt(pool);});
  if(fmts.root) gens.push(makeRoot);
  var bankItems=[];
  if(fmts.se) BANK.filter(function(b){return b.type==="SE";}).forEach(function(b){bankItems.push({se:b});});
  if(fmts.tc) BANK.filter(function(b){return b.type==="TC";}).forEach(function(b){ b.blanks.forEach(function(bl,bi){bankItems.push({tc:b,bi:bi});}); });
  bankItems=shuffle(bankItems);
  var queue=[], guard=0;
  var quota = gens.length ? Math.min(bankItems.length, Math.round(count*0.35)) : bankItems.length;
  for(var i=0;i<quota;i++){ var c=tcseCard(bankItems[i]); if(c) queue.push(c); }
  while(queue.length<count && gens.length && guard++<count*40){
    var q=gens[rnd(gens.length)](); if(q && !queue.some(function(x){return x.stem===q.stem;})) queue.push(q);
  }
  var bi=quota; while(queue.length<count && bi<bankItems.length){ var cc=tcseCard(bankItems[bi++]); if(cc) queue.push(cc); }
  return shuffle(queue).slice(0,count);
}

/* ================= run ================= */
var run=null;
function start(){
  var queue=buildQueue(state.mode.fmts, state.count, state.mode.fullBank);
  if(queue.length<3){ alert("Couldn't build that test — try another type."); return; }
  run={queue:queue,i:0,score:0,streak:0,correct:0,missed:[]};
  renderQ();
}
function renderQ(){
  var q=run.queue[run.i]; q._picked=q.multi?[]:null; q._answered=false;
  var h='<div class="q-bar"><span class="score">Score <b>'+run.score+'</b></span>'+
        '<span>Q '+(run.i+1)+' / '+run.queue.length+'</span>'+
        '<span class="streak">'+(run.streak>1?(run.streak+' streak'):'')+'</span></div>';
  h+='<div class="q-prog"><i style="width:'+(run.i/run.queue.length*100)+'%"></i></div>';
  h+='<div class="q-type">'+esc(q.type)+'</div><div class="q-stem">'+q.stem+'</div>';
  if(q.hint) h+='<div class="q-hint">'+esc(q.hint)+'</div>';
  if(q.note) h+='<div class="q-hint">Tip: '+q.note+'</div>';
  h+='<div class="q-opts">'+q.opts.map(function(o,i){ return '<button class="q-opt" data-i="'+i+'"><span class="lab">'+LAB[i]+'</span>'+esc(o.text)+'</button>'; }).join("")+'</div>';
  h+='<div class="q-expl" id="qExpl"></div>';
  h+='<div class="q-actions">'+(q.multi?'<button class="q-btn" id="qCheck" disabled>Check answer</button>':'')+
     '<button class="q-btn ghost" id="qNext" style="display:none">'+(run.i+1<run.queue.length?'Next →':'See results')+'</button></div>';
  app.innerHTML=h;
  app.querySelectorAll('.q-opt').forEach(function(el){
    el.addEventListener('click',function(){
      if(q._answered) return; var i=+el.getAttribute('data-i');
      if(q.multi){ var p=q._picked.indexOf(i);
        if(p>=0){q._picked.splice(p,1);el.classList.remove('sel');}
        else{ if(q._picked.length>=2) return; q._picked.push(i); el.classList.add('sel'); }
        document.getElementById('qCheck').disabled=q._picked.length!==2;
      } else grade(q,[i]);
    });
  });
  if(q.multi) document.getElementById('qCheck').addEventListener('click',function(){grade(q,q._picked.slice());});
  document.getElementById('qNext').addEventListener('click', next);
  window.scrollTo(0,0);
}
function grade(q,picked){
  q._answered=true;
  var correct=[]; q.opts.forEach(function(o,i){if(o.correct)correct.push(i);});
  var right=picked.length===correct.length && picked.every(function(i){return q.opts[i].correct;});
  app.querySelectorAll('.q-opt').forEach(function(el,i){ el.disabled=true;
    if(q.opts[i].correct) el.classList.add('correct');
    else if(picked.indexOf(i)>=0) el.classList.add('wrong'); else el.classList.add('muted'); });
  var pts=0;
  if(right){ run.streak++; run.correct++; pts=10+(run.streak>1?(run.streak-1)*2:0); run.score+=pts; }
  else { run.streak=0; run.missed.push(q); }
  var ex=document.getElementById('qExpl');
  ex.innerHTML='<div class="verdict '+(right?'ok':'no')+'">'+(right?'✓ Correct  +'+pts+' pts':'✗ Not quite')+'</div>'+
    (q.note?'<div class="note">'+q.note+'</div>':'')+
    '<div class="lines">'+q.opts.map(function(o,i){ return '<div class="ln '+(o.correct?'r':'x')+'"><span class="w">'+LAB[i]+'. '+esc(o.text)+'</span> — '+(o.why||'')+'</div>'; }).join("")+'</div>';
  ex.classList.add('show');
  if(document.getElementById('qCheck')) document.getElementById('qCheck').style.display='none';
  document.getElementById('qNext').style.display='';
}
function next(){ run.i++; if(run.i>=run.queue.length){ results(); return; } renderQ(); }
function results(){
  var total=run.queue.length, pct=Math.round(run.correct/total*100);
  var msg=pct>=90?"Outstanding — these are locked in.":pct>=75?"Strong. Review the few you missed.":pct>=50?"Getting there — re-drill the misses below.":"Keep at it — study and test again.";
  var h='<div class="res"><div class="pct">You scored</div><div class="big">'+run.score+'</div>'+
        '<div class="pct">'+run.correct+' / '+total+' correct · '+pct+'%</div><div class="msg">'+msg+'</div></div>';
  if(run.missed.length){
    h+='<div class="review"><h3>Review — '+run.missed.length+' to revisit</h3>'+
       run.missed.map(function(q){ var ans=q.opts.filter(function(o){return o.correct;}).map(function(o){return o.text;}).join(" + ");
         var s=q.stem.replace(/<[^>]+>/g,''); return '<div class="item">'+esc(s.length>90?s.slice(0,90)+'…':s)+'<br>Answer: <b>'+esc(ans)+'</b></div>'; }).join("")+'</div>';
  }
  h+='<div class="q-actions" style="margin-top:22px"><button class="q-btn" id="qAgain">New test</button></div>';
  app.innerHTML=h;
  document.getElementById('qAgain').addEventListener('click', startScreen);
  window.scrollTo(0,0);
}

if(!WORDS.length){ app.innerHTML='<p>Could not load the lexicon data.</p>'; }
else startScreen();
})();
