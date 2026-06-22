#!/usr/bin/env python3
# Builds Section 7 (all 106 confusing pairs/groups) and inserts into the handbook.
# Meanings are taken faithfully from GRE-Lexicon-2024.txt (Common Confusing GRE Words).

items = [
 (1, [("acrid","sharp, bitterly pungent (acrid smell of burning hair)"),("acrimonious","stinging, caustic in tone (an acrimonious argument)")], "**acrid** = a *smell/taste*; **acrimonious** = a *dispute/manner*. Trick: acrimon**ious** people argue."),
 (2, [("affection","feeling of love"),("affectation","an artificial show, insincere pretense")], "**-ation** = a put-on. Mistake: writing 'affectation' for genuine fondness."),
 (3, [("allude","to make an indirect reference"),("elude","to escape, evade")], "**a**llude = **a**lludes to an idea; **e**lude = **e**scape. GRE pairs 'allude/allusion' with hints."),
 (4, [("amiable","lovable, agreeable — of *persons*"),("amicable","peaceable, harmonious — of *arrangements/settlements*"),("amenable","readily managed, willing to be led")], "amiable PERSON, amicable SETTLEMENT, amenable = persuadable."),
 (5, [("appraise","to estimate, judge (performance appraisal)"),("apprise","to inform (they apprised the police)")], "appr**ai**se = put a price; appr**i**se = give info."),
 (6, [("alternate","every other (visits on alternate days)"),("alternative","a choice between two or more options")], "alternate = takes turns; alternative = an option."),
 (7, [("attenuate","reduce, weaken (attenuated bodies)"),("extenuate","lessen the magnitude of guilt (nothing can extenuate your conduct)")], "extenuate almost always pairs with *circumstances/guilt*."),
 (8, [("baneful","ruinous, poisonous (the bane of his life)"),("baleful","deadly, destructive, sinister (baleful looks)")], "baleful = a *menacing look*; baneful = *causes ruin*."),
 (9, [("brusque","blunt, abrupt (brusque manner)"),("burlesque","an imitation that ridicules")], "brusque = curt; burlesque = parody."),
 (10,[("beneficial","useful (advice proved beneficial)"),("beneficent","kind (a beneficent act)")], "benefi**ci**al = does good *to you*; benefi**ce**nt = *kindly person/act*."),
 (11,[("bridal","of a wedding/bride"),("bridle","to control, check (bridle your passions)")], "bri**dle** = the horse's *bridle* restrains."),
 (12,[("broach","to initiate, open (broach the topic)"),("brooch","an ornament")], "broo**ch** = jewelry; broa**ch** = bring up."),
 (13,[("canker","any ulcerous sore, cancer"),("canter","slow gallop")], "cant**er** = a horse's gait."),
 (14,[("cannon","big gun"),("canon","law (canons of justice)")], "one-N canon = rule/body of works."),
 (15,[("capricious","whimsical, unpredictable"),("captious","fault-finding (captious mother-in-law)")], "capTious = picks faults; capRicious = on a whim."),
 (16,[("censor","to suppress, forbid, delete (film censors)"),("censure","rebuke, criticize adversely"),("cynosure","focal point of attraction")], "censor SUPPRESSES, censure SCOLDS, cynosure = center of attention."),
 (17,[("cessation","stopping (cessation of hostilities)"),("cession","yielding, ceding (territory ceded)")], "ce**ss**ation = ceases; ce**ssi**on = cedes."),
 (18,[("chaotic","in complete confusion"),("inchoate","rudimentary, undeveloped")], "inchoate = just-begun/formless; GRE loves it for early-stage ideas."),
 (19,[("climatic","relating to climate"),("climactic","pertaining to a climax")], "climaC-tic = the big moment."),
 (20,[("chord","string of a musical instrument"),("cord","a thin rope")], "chord has an H (harmony)."),
 (21,[("complacent","self-satisfied, smug"),("complaisant","pleasing, obliging")], "complaiSant = eager to pleaSe; complacent = smug."),
 (22,[("continual","going on with short breaks"),("continuous","without any break")], "continuOUS = One Unbroken Stream."),
 (23,[("corporal","bodily (corporal punishment)"),("corporeal","material, of this world (corporeal existence)")], "corporeal = physical vs spiritual."),
 (24,[("collate","make a careful comparison (collate editions)"),("collation","a light meal")], "collate = compare/order pages."),
 (25,[("comely","attractive, agreeable"),("comity","courtesy, civility")], "comity = of nations/manners (comity = courtesy)."),
 (26,[("condemn","to doom"),("contemn","to despise, to hold in contempt")], "contemn (rare) = scorn — note the second N."),
 (27,[("decant","pour off gently"),("descant","discuss fully, comment on")], "deScant = Speak at length."),
 (28,[("decry","disparage, disapprove of"),("descry","catch sight of, discover by observation")], "deScry = Spot/See; deCry = Criticize."),
 (29,[("definite","specific, exact"),("definitive","final, conclusive (a definitive offer)")], "definitive = the *last word*, authoritative."),
 (30,[("delude","deceive"),("delusion","false belief/hallucination"),("delusive","deceptive, raising false hopes"),("illusion","mistaken perception of reality (optical illusion)")], "delusion = a *belief*; illusion = a *perception*."),
 (31,[("dependent","relying on"),("dependant","one who depends on others (Br. noun)")], "-ANT noun = the person; -ENT adj = relying."),
 (32,[("deprecate","strongly disapprove"),("depreciate","belittle, reduce in value (shares depreciated)")], "depreCIate = drops in price; deprecate = disapprove."),
 (33,[("discomfited","defeated, frustrated"),("discomforted","uneasiness of body and mind")], "discomfit = THWART, not merely make uncomfortable."),
 (34,[("disinterested","impartial (disinterested as a judge)"),("uninterested","not interested")], "**The #1 GRE pair.** disinterested = *unbiased*, NOT bored."),
 (35,[("enormity","abnormality, monstrous outrageousness (enormity of the crime)"),("enormous","very huge")], "enormity = great *evil/wickedness*, not mere size."),
 (36,[("equable","steady, even-tempered (equable climate)"),("equitable","just, fair (equitable settlement)")], "equAble = even temper; equiTable = fair (equity)."),
 (37,[("errant","erring, straying (an errant husband)"),("arrant","thorough, unmitigated (an arrant rogue)")], "arrant = utter/downright (intensifier)."),
 (38,[("esoteric","known to a chosen few"),("exoteric","easily understood, for the general public")], "eXoteric = eXternal/open to all (rare)."),
 (39,[("excursion","a pleasure trip"),("incursion","a sudden invasion (the Hun incursion)")], "INcursion = motion IN/raid."),
 (40,[("exigent","urgent"),("exiguous","minute, small, trifling (an exiguous diet)")], "exiGuous = meaGre/scanty; exigent = pressing."),
 (41,[("expatiate","speak at length"),("expiate","make amends for (expiate a crime)")], "expiate = atone (pay for sin); expatiate = elaborate."),
 (42,[("economical","not wasteful, thrifty"),("economic","pertaining to the economy (economic growth)")], "economical = frugal; economic = of economics."),
 (43,[("expedient","advantageous (do what is expedient)"),("expeditious","acting quickly")], "expedient = convenient/self-serving; expeditious = speedy."),
 (44,[("emigrant","one who leaves a country"),("immigrant","one who enters a country")], "E-migrant Exits; IM-migrant comes IN."),
 (45,[("extract","take out (honey extracted)"),("extricate","pull out, free from entanglement")], "extricate = free from difficulty."),
 (46,[("extant","still existing (earliest extant manuscript)"),("extent","size, degree"),("extinct","no longer existing")], "extAnt = still Around; extinct = gone."),
 (47,[("facetious","humorous (a facetious remark)"),("factious","causing dissension, quarrelsome"),("factitious","unnatural, artificial (factitious demand)")], "facTITious = arTIFicial; facTIous = facTIONs/strife."),
 (48,[("flaunt","make a show of, display proudly (flaunt a new dress)"),("flout","defy, disregard (flout the rules)")], "**flaunt = SHOW off; flout = SCORN rules.** Top GRE confusion."),
 (49,[("forego","to precede in time/place (the foregoing pages)"),("forgo","to go without, abstain (forgo pleasures)")], "forgO = gO without."),
 (50,[("fractious","unruly (a fractious crowd)"),("factious","inclined to cause factions/dissension")], "fRactious = unRuly; factious = faction-prone."),
 (51,[("froward","disobedient, perverse, stubborn"),("frowzy","slovenly, disheveled, dirty (frowzy barracks)")], "froward = contrary; frowzy = grubby."),
 (52,[("fain","gladly"),("feign","pretend (feigned repentance)"),("feint","move to mislead an enemy")], "feiGn = pretend; feinT = a Trick move."),
 (53,[("farther","matter of distance"),("further","in addition to / extent")], "farther = physical distance (far)."),
 (54,[("forceful","full of force (forceful personality)"),("forcible","done by force (forcible entry)")], "forciBLE = aBLE to use force/by force."),
 (55,[("gage","article pledged as security"),("gauge","to measure (gauge a person's character)")], "gaUge = measUre."),
 (56,[("gentle","mild, polite"),("genteel","graceful, refined in taste")], "genTEEL = refined manners."),
 (57,[("hoard","to accumulate"),("horde","a gang (a horde of marauders)")], "hoarD = stockpile; horDE = a crowd."),
 (58,[("hypercritical","over-critical of small faults"),("hypocritical","not genuine, sham")], "hyPOcritical = a POser/phony."),
 (59,[("immanent","latent, inherent (immanent prejudices)"),("imminent","impending (imminent crisis)"),("eminent","prominent, lofty")], "imMAnent = inside/inherent; imMInent = about to happen; eminent = famous."),
 (60,[("imperial","pertaining to an empire"),("imperative","authoritative, obligatory"),("imperious","haughty, domineering (imperious attitude)")], "imperious = bossy/arrogant — GRE's favorite of the three."),
 (61,[("incredible","beyond belief"),("incredulous","unbelieving, skeptical")], "**incredible thing; incredulous person.** Common slip."),
 (62,[("inflammatory","tending to irritate/excite (inflammatory speech)"),("inflammable","catches fire easily")], "inflammable DOES burn (in- is intensive, not 'not')."),
 (63,[("ingenious","skillful, witty, clever"),("ingenuous","innocent, naive, frank")], "**ingenuous = naive/guileless;** ingenious = clever. Heavy GRE pair."),
 (64,[("irruption","a violent bursting IN (motion inward)"),("eruption","a violent bursting OUT (motion outward)")], "iRRuption = Rushing IN."),
 (65,[("judicial","pertaining to law/courts"),("judicious","wise, prudent (a judicious view)")], "judiCIOUS = wise; judiCIAL = of judges."),
 (66,[("luxuriant","growing profusely (of vegetation, hair)"),("luxurious","sumptuous, comfortable")], "luxuriAnt = Abundant growth."),
 (67,[("martial","warlike (martial arts)"),("marital","pertaining to marriage")], "marItal = of marrIage; martial = of Mars/war."),
 (68,[("mean","stingy, low"),("mien","personal bearing, manner")], "mien = look/demeanor."),
 (69,[("meet","to come together"),("mete","to allot (justice was meted out)")], "mete out = dole out."),
 (70,[("mendacity","lying (mendacious reports)"),("mendicity","begging")], "mendIcity = begging (mendicant); mendAcity = lies."),
 (71,[("militate","to work against, hinder (militated against his success)"),("mitigate","reduce severity, make milder")], "**militate AGAINST; mitigate = lessen.** Big GRE pair."),
 (72,[("mordant","biting, sarcastic"),("morbid","gloomy, unwholesome (morbid imagination)")], "morDant = a Dark, biting wit; morbid = grim."),
 (73,[("mystical","mysterious, incomprehensible"),("mythical","imagined, not real")], "mythical = of myth/fictional."),
 (74,[("momentary","lasting only a moment"),("momentous","of great importance")], "momentous = monumental, weighty."),
 (75,[("obdurate","stubborn"),("objurgate","to scold, severely rebuke")], "objurgate = berate (rare)."),
 (76,[("official","having authoritative standing"),("officious","interfering, meddlesome")], "**officious = a meddling busybody** — not 'official'."),
 (77,[("ordinance","a rule/decree (presidential ordinance)"),("ordnance","military weapons, cannon")], "ordnance (no I) = artillery."),
 (78,[("penurious","stingy, parsimonious"),("penury","extreme poverty")], "penury = destitution; penurious can mean *miserly* OR poor."),
 (79,[("perspicacity","clear insight, shrewdness (a perspicacious critic)"),("perspicuity","clarity of expression (clear, perspicuous style)")], "**perspicaCIOUS = sharp-SEEING (smart); perspicUOUS = clear writing.**"),
 (80,[("pertinacious","stubborn, persistent (pertinacious stand)"),("pertinent","suitable, to the point (pertinent remark)")], "pertinacious = tenacious; pertinent = relevant."),
 (81,[("perverse","stubborn, intractable"),("perversion","corruption, turning to wrong"),("perversity","stubborn maintenance of a wrong cause")], "perverse adj / perversion = the act / perversity = the trait."),
 (82,[("piquant","pleasantly tart, exciting (piquant gossip)"),("pique","irritation, resentment (took a pique against me)")], "piquant = zesty (good); pique = a fit of resentment."),
 (83,[("portent","an omen, forewarning"),("portend","to foretell, presage (this portends war)")], "porten**t** = noun (the sign); porten**d** = verb (to signal)."),
 (84,[("precipitate","hasty, rash (precipitate actions)"),("precipitous","steep, like a precipice"),("precipitation","rainfall")], "precipitate = rash/hasty; precipitous = a sheer drop."),
 (85,[("prescribe","lay down rules, order"),("proscribe","prohibit, forbid, denounce")], "**proscribe = PROhibit/ban; prescribe = recommend.** Near-opposites."),
 (86,[("presumptive","assumed to be true until disproved (heir presumptive)"),("presumptuous","arrogant, overconfident")], "presumptuous = takes too much for granted (rude)."),
 (87,[("propitiate","to appease (a propitiatory smile)"),("propitious","favorable, kindly (a propitious moment)")], "propitiATE = verb (appease); propitious = auspicious."),
 (88,[("provident","thrifty, showing foresight"),("providential","strikingly opportune, lucky")], "providential = like a godsend/lucky."),
 (89,[("reign","to rule"),("rein","curb, means of control")], "rein in = control (reins of a horse)."),
 (90,[("restless","uneasy, discontented"),("restive","stubborn, balky, refractory (the crowd grew restive)")], "**restive = restless AND resistant/balky**, not merely fidgety."),
 (91,[("septic","putrefactive, affected by bacteria"),("sceptic","a person who doubts")], "sceptic/skeptic = doubter."),
 (92,[("simulate","to pretend to be what one is not"),("dissimulate","to hide what one is feeling")], "**simulate = FAKE a feeling; dissimulate = CONCEAL a feeling.**"),
 (93,[("spacious","having a lot of space"),("specious","false though seemingly true (a specious argument)")], "**specious = deceptively plausible** — not 'spacious'. Frequent GRE trap."),
 (94,[("sensual","of bodily/sexual desires"),("sensuous","appealing to the senses (sensuous imagery)")], "sensuous = aesthetic; sensual = carnal."),
 (95,[("temperance","moderation, sobriety"),("temperament","one's physical/mental character")], "temperance = self-restraint."),
 (96,[("temporary","lasting a short time"),("temporal","worldly, as opposed to spiritual")], "temporal = secular/of time."),
 (97,[("tortuous","winding (long tortuous sentences)"),("torturous","painful")], "**tortuous = twisty; torturous = agonizing.** Note the extra 'r'."),
 (98,[("transcendent","superior, supreme"),("transcendental","vague, visionary, speculative")], "transcendental = abstract/metaphysical."),
 (99,[("turgid","swollen, inflated, pompous (turgid prose)"),("turbid","muddy, clouded (turbid waters)")], "turBid = muddy (water); turGid = bloated/pompous (prose)."),
 (100,[("unexceptionable","above reproach, altogether admirable"),("unexceptional","ordinary")], "**unexceptionABLE = beyond objection (good); unexceptional = mediocre.** Opposite tones!"),
 (101,[("urban","of the city"),("urbane","smooth, polite, polished (urbane manners)")], "urbanE = Elegant/suave."),
 (102,[("vain","conceited / futile"),("vein","a blood vessel; a mood (in a merry vein)")], "vein = a streak/mood."),
 (103,[("venial","trivial, easily pardonable (a venial sin)"),("venal","capable of being bribed (venal officialdom)")], "**venal = corruptible/bribable; venial = a minor, forgivable fault.**"),
 (104,[("veracity","truthfulness"),("voracity","greediness")], "Vor-acious = devouring; Ver-acity = truth (verity)."),
 (105,[("whet","to sharpen (whet the appetite)"),("wet","rainy, damp")], "whet = stimulate/sharpen."),
 (106,[("willing","disposed, having no reluctance"),("wilful","obstinate, perverse (wilful murder)")], "wilful = headstrong/deliberate."),
]

lines = []
lines.append("---\n")
lines.append("## 7. Common Confusing Words\n")
lines.append("> All **106** confusable pairs/groups from the source, transformed into study material. Format per item: each word with its **faithful meaning**, then a bolded **GRE distinction / memory trick** (and the common mistake it prevents). These are prime **Text Completion** material — the GRE plants the look-alike as a distractor and rewards the precise meaning.\n")
for num, pairs, trick in items:
    head = " vs ".join(f"**{w}**" for w, _ in pairs)
    lines.append(f"**{num}. {head}**  ")
    for w, m in pairs:
        lines.append(f"&nbsp;&nbsp;• *{w}* — {m}  ")
    lines.append(f"&nbsp;&nbsp;↳ {trick}\n")

section = "\n".join(lines) + "\n<!-- SECTION-BREAK -->\n"

path = "GRE-Lexicon-Master-Handbook.md"
doc = open(path, encoding="utf-8").read()
assert doc.count("<!-- SECTION-BREAK -->") == 1, "marker count != 1"
doc = doc.replace("<!-- SECTION-BREAK -->\n", section).replace("<!-- SECTION-BREAK -->", section) if False else doc
doc = doc.replace("<!-- SECTION-BREAK -->", section, 1)
open(path, "w", encoding="utf-8").write(doc)
print("Inserted Section 7 with", len(items), "items.")
