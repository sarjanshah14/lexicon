/* Original GRE-style Text Completion & Sentence Equivalence bank.
   Every item is written from our own lexicon; answer keys and per-option
   explanations are authored here (not scraped), so each can be trusted.
   Schema:
     TC : {type:"TC", stem, blanks:[{opts:[...], ans:idx, expl:{word:reason}}], words:[...]}
          (stem uses (i)___ , (ii)___ for the blank slots, or a single ___)
     SE : {type:"SE", stem, opts:[6], ans:[i,j], expl:{word:reason}, pairNote, words:[...]}
*/
window.TCSE = [
/* ---------------- Sentence Equivalence (pick the TWO that make equivalent sentences) -------------- */
{
  type:"SE",
  stem:"Though the committee expected a heated debate, the chairman's ______ manner kept the discussion remarkably calm.",
  opts:["placid","truculent","equable","verbose","sardonic","irascible"],
  ans:[0,2],
  pairNote:"Both 'placid' and 'equable' mean even-tempered and calm — they produce equivalent sentences.",
  expl:{
    "placid":"CORRECT — calm, untroubled; fits a manner that keeps things calm.",
    "equable":"CORRECT — even-tempered, free from extremes; the partner synonym to 'placid'.",
    "truculent":"Wrong meaning — aggressively defiant; that would inflame the debate, not calm it.",
    "verbose":"Wrong meaning — wordy. It describes speech quantity, not temperament, and has no partner here.",
    "sardonic":"Wrong meaning — mockingly scornful; not 'calm', and unpaired.",
    "irascible":"Wrong meaning — easily angered; the opposite of what keeps a discussion calm."
  },
  words:["placid","equable","truculent","verbose","sardonic","irascible"]
},
{
  type:"SE",
  stem:"Far from being the original thinker his admirers claimed, the columnist was utterly ______, recycling other writers' ideas as his own.",
  opts:["derivative","seminal","unoriginal","trenchant","prescient","jejune"],
  ans:[0,2],
  pairNote:"'derivative' and 'unoriginal' both mean copied/not original — the clue is 'recycling other writers' ideas'.",
  expl:{
    "derivative":"CORRECT — imitative, drawn from another source; matches 'recycling others' ideas'.",
    "unoriginal":"CORRECT — not new; the direct partner to 'derivative'.",
    "seminal":"Opposite — highly original and influential; contradicts the clue.",
    "trenchant":"Wrong meaning — sharply incisive; says nothing about originality.",
    "prescient":"Wrong meaning — foreseeing the future; irrelevant and unpaired.",
    "jejune":"Tempting but wrong — it means naive/insipid, not 'copied'; it has no synonym partner among the options."
  },
  words:["derivative","seminal","trenchant","prescient","jejune"]
},
{
  type:"SE",
  stem:"The senator's ______ remarks, intended to soothe the angry crowd, only deepened their suspicion that he was hiding something.",
  opts:["emollient","conciliatory","inflammatory","candid","mendacious","laconic"],
  ans:[0,1],
  pairNote:"'emollient' and 'conciliatory' both mean soothing/intended to appease.",
  expl:{
    "emollient":"CORRECT — softening, soothing; matches 'intended to soothe'.",
    "conciliatory":"CORRECT — meant to placate; the partner synonym.",
    "inflammatory":"Opposite — meant to enrage; contradicts 'soothe'.",
    "candid":"Wrong meaning — frank/honest; and the sentence implies he is NOT being open.",
    "mendacious":"Tempting — lying; fits the 'hiding something' hint, but it is not a synonym of 'soothing' and has no partner.",
    "laconic":"Wrong meaning — terse, using few words; unrelated to soothing."
  },
  words:["emollient","conciliatory","inflammatory","candid","mendacious","laconic"]
},
{
  type:"SE",
  stem:"Reviewers praised the memoir for its ______, noting that the author concealed none of her own failings.",
  opts:["candor","reticence","frankness","prolixity","equivocation","acerbity"],
  ans:[0,2],
  pairNote:"'candor' and 'frankness' both mean openness/honesty — the clue is 'concealed none of her failings'.",
  expl:{
    "candor":"CORRECT — forthright honesty; matches concealing nothing.",
    "frankness":"CORRECT — plain-spoken openness; the partner to 'candor'.",
    "reticence":"Opposite — reserve, a reluctance to speak; she did the reverse.",
    "prolixity":"Wrong meaning — tedious wordiness; about length, not honesty.",
    "equivocation":"Opposite in spirit — deliberate ambiguity to mislead; she hid nothing.",
    "acerbity":"Wrong meaning — sharpness/bitterness of tone; unrelated and unpaired."
  },
  words:["candor","reticence","prolixity","equivocation","acerbity"]
},
{
  type:"SE",
  stem:"Once a ______ student who shrank from every question, she became, after years of debate club, strikingly self-assured.",
  opts:["diffident","timorous","brazen","fastidious","indolent","perspicacious"],
  ans:[0,1],
  pairNote:"'diffident' and 'timorous' both mean shy/timid — contrasted with the later 'self-assured'.",
  expl:{
    "diffident":"CORRECT — lacking self-confidence; fits 'shrank from every question'.",
    "timorous":"CORRECT — fearful, timid; the partner synonym.",
    "brazen":"Opposite — bold to the point of shamelessness.",
    "fastidious":"Wrong meaning — fussy about detail; not about shyness.",
    "indolent":"Wrong meaning — lazy; the sentence is about timidity, not effort.",
    "perspicacious":"Wrong meaning — mentally sharp; unrelated and unpaired."
  },
  words:["diffident","timorous","brazen","fastidious","indolent","perspicacious"]
},
{
  type:"SE",
  stem:"The critic dismissed the novel's prose as hopelessly ______, padded with clauses that added nothing to its meaning.",
  opts:["prolix","verbose","terse","sublime","laconic","trenchant"],
  ans:[0,1],
  pairNote:"'prolix' and 'verbose' both mean wordy — the clue is 'padded with clauses that added nothing'.",
  expl:{
    "prolix":"CORRECT — tediously long-winded; matches the padding.",
    "verbose":"CORRECT — using more words than needed; partner to 'prolix'.",
    "terse":"Opposite — brief and to the point.",
    "sublime":"Wrong meaning — of awe-inspiring excellence; a value judgment of the wrong kind.",
    "laconic":"Opposite — sparing with words.",
    "trenchant":"Wrong meaning — incisive, forceful; the opposite of 'padded'."
  },
  words:["prolix","verbose","terse","sublime","laconic","trenchant"]
},
{
  type:"SE",
  stem:"His fortune, vast as it was, could not survive a decade of such ______ spending.",
  opts:["profligate","prodigal","frugal","abstemious","meticulous","capricious"],
  ans:[0,1],
  pairNote:"'profligate' and 'prodigal' both mean recklessly wasteful with money.",
  expl:{
    "profligate":"CORRECT — wildly extravagant and wasteful; fits draining a fortune.",
    "prodigal":"CORRECT — lavishly wasteful; the partner synonym.",
    "frugal":"Opposite — economical, thrifty.",
    "abstemious":"Opposite — sparing, restrained (esp. in consumption).",
    "meticulous":"Wrong meaning — extremely careful about detail; not about waste.",
    "capricious":"Wrong meaning — impulsive/changeable; tempting but it doesn't mean 'wasteful' and has no partner."
  },
  words:["profligate","prodigal","frugal","abstemious","meticulous","capricious"]
},
{
  type:"SE",
  stem:"The treaty proved ______: within months both sides had resumed the very hostilities it was meant to end.",
  opts:["ephemeral","evanescent","durable","binding","onerous","equivocal"],
  ans:[0,1],
  pairNote:"'ephemeral' and 'evanescent' both mean short-lived — the treaty lasted only months.",
  expl:{
    "ephemeral":"CORRECT — lasting a very short time; matches 'within months'.",
    "evanescent":"CORRECT — quickly fading; the partner synonym.",
    "durable":"Opposite — long-lasting.",
    "binding":"Wrong meaning — legally obligating; doesn't capture 'short-lived'.",
    "onerous":"Wrong meaning — burdensome; unrelated to duration.",
    "equivocal":"Wrong meaning — ambiguous; unrelated and unpaired."
  },
  words:["ephemeral","evanescent","durable","onerous","equivocal"]
},
{
  type:"SE",
  stem:"Even under withering cross-examination the witness remained ______, never once losing her composure.",
  opts:["unflappable","imperturbable","flustered","loquacious","querulous","vindictive"],
  ans:[0,1],
  pairNote:"'unflappable' and 'imperturbable' both mean impossible to upset — the clue is 'never losing her composure'.",
  expl:{
    "unflappable":"CORRECT — not easily disconcerted; matches keeping composure.",
    "imperturbable":"CORRECT — calm under pressure; the partner synonym.",
    "flustered":"Opposite — agitated, confused.",
    "loquacious":"Wrong meaning — very talkative; says nothing about composure.",
    "querulous":"Wrong meaning — complaining, peevish; not 'calm'.",
    "vindictive":"Wrong meaning — vengeful; unrelated and unpaired."
  },
  words:["unflappable","imperturbable","loquacious","querulous","vindictive"]
},
{
  type:"SE",
  stem:"The professor's ______ asides, delivered with a straight face, left students unsure whether to laugh or take notes.",
  opts:["droll","wry","earnest","caustic","insipid","bombastic"],
  ans:[0,1],
  pairNote:"'droll' and 'wry' both describe dry, understated humor.",
  expl:{
    "droll":"CORRECT — amusing in an odd, dry way; fits the deadpan delivery.",
    "wry":"CORRECT — drily humorous; the partner synonym.",
    "earnest":"Opposite in tone — sincere and serious, leaving no doubt to laugh.",
    "caustic":"Tempting — biting/sarcastic, but it stresses cruelty, not the gentle 'unsure whether to laugh'; no partner.",
    "insipid":"Opposite — dull, flavorless; such asides wouldn't provoke laughter.",
    "bombastic":"Wrong meaning — pompous and inflated; not understated humor."
  },
  words:["droll","wry","earnest","caustic","insipid","bombastic"]
},
{
  type:"SE",
  stem:"Reformers hoped the new measures would ______ the slum's worst conditions, but the funding fell far short.",
  opts:["ameliorate","alleviate","aggravate","exacerbate","obfuscate","sanction"],
  ans:[0,1],
  pairNote:"'ameliorate' and 'alleviate' both mean to make a bad situation better.",
  expl:{
    "ameliorate":"CORRECT — to improve or make better; fits 'improve the worst conditions'.",
    "alleviate":"CORRECT — to ease or lessen; the partner synonym.",
    "aggravate":"Opposite — to make worse.",
    "exacerbate":"Opposite — to worsen; a classic trap synonym of 'aggravate', not of the answer.",
    "obfuscate":"Wrong meaning — to obscure or confuse; not about improving conditions.",
    "sanction":"Wrong meaning (and ambiguous) — to approve or to penalize; neither fits."
  },
  words:["ameliorate","alleviate","aggravate","exacerbate","obfuscate","sanction"]
},
{
  type:"SE",
  stem:"What the brochure called a charming village was in truth a ______ cluster of huts, poorer than anything the tourists had imagined.",
  opts:["squalid","wretched","opulent","quaint","salubrious","pristine"],
  ans:[0,1],
  pairNote:"'squalid' and 'wretched' both mean miserably poor and degraded.",
  expl:{
    "squalid":"CORRECT — dirty and wretched from poverty; matches 'poorer than imagined'.",
    "wretched":"CORRECT — miserable, in deplorable condition; the partner synonym.",
    "opulent":"Opposite — luxurious, wealthy.",
    "quaint":"Wrong meaning — attractively old-fashioned; matches the brochure, not the truth.",
    "salubrious":"Opposite — healthful, pleasant.",
    "pristine":"Opposite — spotless, unspoiled."
  },
  words:["squalid","wretched","opulent","quaint","salubrious","pristine"]
},

/* ---------------- Single-blank Text Completion -------------- */
{
  type:"TC",
  stem:"Although she is celebrated for her wit in print, in person she is surprisingly ______, rarely volunteering more than a few words.",
  blanks:[{
    opts:["taciturn","garrulous","eloquent","pretentious","convivial"],
    ans:0,
    expl:{
      "taciturn":"CORRECT — habitually reserved in speech; 'rarely volunteering more than a few words' demands a word for sparing speech, and 'Although' signals a contrast with her witty writing.",
      "garrulous":"Opposite — excessively talkative; contradicts 'rarely volunteering' words.",
      "eloquent":"Wrong direction — fluent and persuasive; that would match, not contrast with, her celebrated wit.",
      "pretentious":"Wrong meaning — putting on airs; the sentence is about quantity of speech, not affectation.",
      "convivial":"Wrong meaning — sociable and merry; the opposite of someone who barely speaks."
    }
  }],
  words:["taciturn","garrulous","eloquent","pretentious","convivial"]
},
{
  type:"TC",
  stem:"The defense attorney's argument was ______: it sounded airtight in the courtroom, yet collapsed the moment one examined its premises.",
  blanks:[{
    opts:["specious","cogent","irrefutable","laconic","tactful"],
    ans:0,
    expl:{
      "specious":"CORRECT — superficially convincing but actually false; exactly 'sounded airtight … yet collapsed' under scrutiny.",
      "cogent":"Opposite — genuinely compelling and logical; it would not collapse.",
      "irrefutable":"Opposite — impossible to disprove; contradicts 'collapsed … on examination'.",
      "laconic":"Wrong meaning — terse; describes length, not soundness.",
      "tactful":"Wrong meaning — diplomatic; irrelevant to whether the argument holds up."
    }
  }],
  words:["specious","cogent","irrefutable","laconic","tactful"]
},
{
  type:"TC",
  stem:"Far from being the tyrant his rivals portrayed, the king was known for his ______, pardoning even those who had plotted against him.",
  blanks:[{
    opts:["clemency","severity","caprice","avarice","duplicity"],
    ans:0,
    expl:{
      "clemency":"CORRECT — mercy, leniency; 'pardoning even … plotters' is the definition in action, and 'Far from … tyrant' signals a positive trait.",
      "severity":"Opposite — harshness; contradicts pardoning enemies.",
      "caprice":"Wrong meaning — impulsive whim; doesn't explain consistent pardoning.",
      "avarice":"Wrong meaning — greed; unrelated to mercy.",
      "duplicity":"Wrong meaning — deceitfulness; the king's act is open generosity, not trickery."
    }
  }],
  words:["clemency","severity","caprice","avarice","duplicity"]
},
{
  type:"TC",
  stem:"The grant was meant to support promising research, yet the committee's ______ standards meant that only a handful of the hundreds of applicants ever qualified.",
  blanks:[{
    opts:["stringent","lax","arbitrary","munificent","nebulous"],
    ans:0,
    expl:{
      "stringent":"CORRECT — strict, demanding; explains why 'only a handful … qualified'.",
      "lax":"Opposite — lenient; lax standards would let many through.",
      "arbitrary":"Tempting but unsupported — 'arbitrary' implies randomness; nothing says the rejections were random, only that few passed a high bar.",
      "munificent":"Wrong meaning — extremely generous; describes giving, not selectivity.",
      "nebulous":"Wrong meaning — vague; vagueness wouldn't by itself disqualify nearly everyone."
    }
  }],
  words:["stringent","lax","arbitrary","munificent","nebulous"]
},
{
  type:"TC",
  stem:"New evidence did nothing to shake the historian's ______ conviction; he clung to his original thesis as stubbornly as ever.",
  blanks:[{
    opts:["obdurate","tentative","wavering","cursory","ingenuous"],
    ans:0,
    expl:{
      "obdurate":"CORRECT — stubbornly unyielding; matches 'clung … as stubbornly as ever'.",
      "tentative":"Opposite — hesitant, provisional; he was anything but.",
      "wavering":"Opposite — unsteady, undecided; contradicts clinging stubbornly.",
      "cursory":"Wrong meaning — hasty and superficial; describes effort, not stubbornness.",
      "ingenuous":"Wrong meaning — innocently frank; unrelated to obstinacy."
    }
  }],
  words:["obdurate","tentative","wavering","cursory","ingenuous"]
},
{
  type:"TC",
  stem:"The audience grew restless as the speaker, ignoring every signal to wrap up, continued his ______ account of each committee meeting from the past decade.",
  blanks:[{
    opts:["interminable","succinct","riveting","cryptic","impromptu"],
    ans:0,
    expl:{
      "interminable":"CORRECT — endless, tediously long; explains the restless audience and 'each meeting from the past decade'.",
      "succinct":"Opposite — brief and clear; would not make an audience restless.",
      "riveting":"Opposite in effect — gripping; a riveting account wouldn't bore them.",
      "cryptic":"Wrong meaning — mysterious, obscure; the problem is length, not obscurity.",
      "impromptu":"Wrong meaning — unrehearsed; a detailed decade-long account is the opposite of off-the-cuff."
    }
  }],
  words:["interminable","succinct","riveting","cryptic","impromptu"]
},
{
  type:"TC",
  stem:"Critics found the prize-winning installation utterly ______, unable to discern any meaning beneath its deliberately baffling surface.",
  blanks:[{
    opts:["abstruse","lucid","banal","derivative","garish"],
    ans:0,
    expl:{
      "abstruse":"CORRECT — hard to understand, recondite; matches 'unable to discern any meaning' and 'deliberately baffling'.",
      "lucid":"Opposite — clear and easy to grasp.",
      "banal":"Wrong meaning — dull and obvious; the opposite of baffling.",
      "derivative":"Wrong meaning — imitative; says nothing about being hard to understand.",
      "garish":"Wrong meaning — tastelessly showy; about appearance, not intelligibility."
    }
  }],
  words:["abstruse","lucid","banal","derivative","garish"]
},
{
  type:"TC",
  stem:"Where his predecessor had courted the press at every turn, the new director was almost ______, granting not a single interview in his first year.",
  blanks:[{
    opts:["reclusive","gregarious","ostentatious","affable","candid"],
    ans:0,
    expl:{
      "reclusive":"CORRECT — shunning others; 'not a single interview' and the contrast with a press-courting predecessor point to withdrawal.",
      "gregarious":"Opposite — sociable; contradicts avoiding all interviews.",
      "ostentatious":"Opposite in spirit — showy; the director shrinks from publicity.",
      "affable":"Wrong direction — friendly and approachable; doesn't fit avoiding the press.",
      "candid":"Wrong meaning — frank; about honesty when speaking, not about refusing to speak."
    }
  }],
  words:["reclusive","gregarious","ostentatious","affable","candid"]
},

/* ---------------- Double-blank Text Completion -------------- */
{
  type:"TC",
  stem:"The biography is admirably balanced: it neither (i)______ its subject as a flawless hero nor (ii)______ him as a mere villain, but presents a believably complex man.",
  blanks:[
    {
      opts:["lionizes","censures","caricatures"],
      ans:0,
      expl:{
        "lionizes":"CORRECT — treats as a celebrity/hero; pairs with 'flawless hero' and is rejected by 'neither … nor'.",
        "censures":"Wrong — to condemn; that belongs with the villain side, not the 'flawless hero' side.",
        "caricatures":"Wrong for blank (i) — to exaggerate into a distortion; it doesn't specifically mean glorify."
      }
    },
    {
      opts:["exonerates","vilifies","extols"],
      ans:1,
      expl:{
        "vilifies":"CORRECT — to defame as wicked; pairs with 'mere villain'.",
        "exonerates":"Wrong — to clear of blame; the opposite of casting as a villain.",
        "extols":"Wrong — to praise highly; that belongs on the hero side, not the villain side."
      }
    }
  ],
  words:["lionizes","censures","caricatures","exonerates","vilifies","extols"]
},
{
  type:"TC",
  stem:"Initially (i)______ about the merger, shareholders grew (ii)______ once the projected savings were revealed, voting overwhelmingly in favor.",
  blanks:[
    {
      opts:["skeptical","euphoric","indifferent"],
      ans:0,
      expl:{
        "skeptical":"CORRECT — doubtful; the word 'Initially … grew [positive]' requires an earlier negative stance that the savings reverse.",
        "euphoric":"Wrong — intensely happy; leaves no room to 'grow' more favorable and contradicts the turnaround.",
        "indifferent":"Wrong — uninterested; but indifference doesn't get overturned by evidence the way doubt does, and it weakens the contrast."
      }
    },
    {
      opts:["enthusiastic","despondent","wary"],
      ans:0,
      expl:{
        "enthusiastic":"CORRECT — eager and positive; explains 'voting overwhelmingly in favor'.",
        "despondent":"Opposite — dejected; contradicts the favorable vote.",
        "wary":"Wrong — still cautious; doesn't match an overwhelming yes vote."
      }
    }
  ],
  words:["skeptical","euphoric","indifferent","enthusiastic","despondent","wary"]
},
{
  type:"TC",
  stem:"The essay's argument is (i)______, advancing through tightly linked steps, yet its prose is so (ii)______ that few readers will have the patience to follow it to the end.",
  blanks:[
    {
      opts:["rigorous","specious","desultory"],
      ans:0,
      expl:{
        "rigorous":"CORRECT — exact and thorough; 'tightly linked steps' signals sound, careful reasoning.",
        "specious":"Wrong — superficially plausible but false; contradicts genuinely 'tightly linked steps'.",
        "desultory":"Wrong — aimless, disconnected; the opposite of tightly linked."
      }
    },
    {
      opts:["turgid","limpid","terse"],
      ans:0,
      expl:{
        "turgid":"CORRECT — pompously dense and hard to read; explains why readers lack patience to follow.",
        "limpid":"Opposite — clear and lucid; that would invite readers, not deter them.",
        "terse":"Opposite tendency — concise; terse prose is easy to get through, not patience-testing."
      }
    }
  ],
  words:["rigorous","specious","desultory","turgid","limpid","terse"]
},
{
  type:"TC",
  stem:"For all his reputation as a ______ negotiator, in the final round he made concession after concession, surrendering points no one had even pressed him to give up.",
  blanks:[{
    opts:["tenacious","mercurial","pliant","verbose","genial"],
    ans:0,
    expl:{
      "tenacious":"CORRECT — stubbornly persistent; the sentence sets up an ironic contrast ('For all his reputation as … , in fact he caved'), so the blank needs the trait he failed to live up to — toughness.",
      "mercurial":"Wrong — volatile, changeable; that would predict, not contradict, sudden concessions, so there's no irony.",
      "pliant":"Wrong — yielding; this matches his actual behavior, but 'For all his reputation as a pliant negotiator' would make caving expected, not surprising.",
      "verbose":"Wrong meaning — wordy; irrelevant to making concessions.",
      "genial":"Wrong meaning — cheerfully friendly; doesn't set up the contrast with surrendering points."
    }
  }],
  words:["tenacious","mercurial","pliant","verbose","genial"]
}
];
