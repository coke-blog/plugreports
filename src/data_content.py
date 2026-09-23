# Editorial content for plugreports.com
# BUSTS: entries marked confirmed=False are scaffolded from user-submitted source links
# and MUST be completed with verified details before publishing. Never invent bust facts.

BUSTS = [
 dict(slug="bust-river-grove-cocaine-339", tag="Alert", country="USA", title="DEA seizes 339.5 lbs of cocaine ($15.2M) and $700K cash in River Grove, Illinois", date="2026-09-18",
  confirmed=True, views=400, image="https://plugreports.com/media/drugs/bust-river-grove-cocaine.png",
  location="River Grove, Illinois (Chicago suburbs), USA", agency="DEA Chicago Field Division + ~10 partner agencies",
  sourceUrl="https://www.cbsnews.com/chicago/news/cocaine-cash-seized-river-grove-drug-bust-dea/",
  summary="DEA agents seized 339.5 pounds of cocaine with an estimated street value of $15.2 million plus roughly $700,000 in cash from a 'stash house' in River Grove after surveilling the crew for weeks. Two men — Burhan Ozerdinc, 33, and Ahmad Sanducka, 33 — are charged with possession with intent to distribute more than 900 grams and were ordered detained.",
  sentencing="Federal: possession with intent to distribute 5+ kg of cocaine carries a mandatory minimum of 10 years to life. Both men were ordered held pretrial.",
  drugsInvolved=["cocaine"]),
 dict(slug="bust-texas-cabbage-meth", title="2,000+ lbs of meth found packed inside cabbage shipment in South Texas", date="2026-09-12",
  location="Rio Grande Valley, South Texas, USA", agency="DEA / Homeland Security Task Force", confirmed=True,
  sourceUrl="https://vt.tiktok.com/ZSqQyGxJs/",
  summary="DEA agents peeling apart a commercial cabbage shipment in the Rio Grande Valley found more than 2,000 pounds of methamphetamine concealed inside the produce. The seizure is part of a Homeland Security Task Force investigation involving the DEA, HSI, FBI, CBP, Border Patrol and Texas DPS. Authorities have not publicly identified the exact location of the seizure.",
  drugsInvolved=["methamphetamine"],
  sentencing="Federal meth trafficking of 50 g or more carries a 10-year mandatory minimum up to life; multi-agency task force cases are prosecuted federally."),
 dict(slug="bust-spain-banana-cocaine-13t", title="13-ton cocaine haul disguised as banana shipment exposes international network", date="2026-07-20",
  location="Spain (investigation spans US, Dubai, Ireland)", agency="Bloomberg Politics / Spanish authorities", confirmed=True,
  sourceUrl="https://vt.tiktok.com/ZSqQyprWP/",
  summary="A 13-ton haul of cocaine disguised as a banana shipment has exposed alleged links between US financiers, luxury Dubai real estate and a crypto-trading Irish fintech, Bloomberg Politics reports. The case centers on cocaine concealed in fruit shipments entering Spain and a laundering network spanning three continents.",
  drugsInvolved=["cocaine"],
  sentencing="Spain: cocaine trafficking carries roughly 3–6 years, rising to 10+ years and beyond 20 for organized, large-quantity cases; EU coordination means additional member-state charges are likely."),
 dict(slug="bust-australia-sydney-cocaine-record", image="https://plugreports.com/media/drugs/4-fluorococaine.jpeg", title="Largest drug bust in Australian history: nearly $1B cocaine at rural Sydney property", date="2026-06-22",
  location="Rural property, western Sydney, NSW, Australia", agency="AFP-led joint operation (9News Sydney report)", confirmed=True,
  sourceUrl="https://vt.tiktok.com/ZSqQyqJMX/",
  summary="Authorities have executed the largest drug bust in Australian history, uncovering nearly a billion dollars' worth of cocaine at a rural property in western Sydney. Aerial footage shows dozens of shipping containers on the property being examined by investigators.",
  drugsInvolved=["cocaine"],
  sentencing="NSW: supplying a large commercial quantity of cocaine carries up to life imprisonment; Commonwealth importation charges can add further decades."),

 # --- Thin source-link stubs: noindex,follow + excluded from sitemap until verified ---
 dict(slug="bust-src-tiktok-1", title="Bust report (details pending verification)", date="2026-09-14",
  location="TBC", agency="TBC", confirmed=False, noindex=True,
  sourceUrl="https://vt.tiktok.com/ZSqQyGxJs/",
  summary="Source link submitted by editor (TikTok video). Details — location, agency, substances, quantities, arrest/sentencing — pending caption verification.",
  drugsInvolved=[], sentencing="Pending — confirm from source before publishing."),
 dict(slug="bust-src-tiktok-2", title="Bust report (details pending verification)", date="2026-09-14",
  location="TBC", agency="TBC", confirmed=False, noindex=True,
  sourceUrl="https://vt.tiktok.com/ZSqQyprWP/",
  summary="Source link submitted by editor (TikTok video). Details pending caption verification.",
  drugsInvolved=[], sentencing="Pending — confirm from source before publishing."),
 dict(slug="bust-src-tiktok-3", title="Bust report (details pending verification)", date="2026-09-14",
  location="TBC", agency="TBC", confirmed=False, noindex=True,
  sourceUrl="https://vt.tiktok.com/ZSqQyqJMX/",
  summary="Source link submitted by editor (TikTok video). Details pending caption verification.",
  drugsInvolved=[], sentencing="Pending — confirm from source before publishing."),
]

NEWS = [
dict(slug="hayden-panettiere-fentanyl-toxicology", country="USA", title="Hayden Panettiere died from fentanyl and prescription-drug mix, coroner rules", date="2026-09-23", tag="Alert",
  views=850,
  image="/assets/img/news-hayden-panettiere.png",
  summary="A South Carolina coroner has ruled that actor Hayden Panettiere died from the toxic effects of fentanyl, its manufacturing byproduct 4-ANPP, Xanax (alprazolam), a muscle relaxer and an antipsychotic. The 36-year-old 'Heroes' and 'Nashville' star was found unresponsive in a Greenville apartment on August 16. Her death was ruled an accident — and police say their investigation is not over.",
  markdown="""## The coroner's ruling, in plain terms
On September 22 the Greenville County Coroner's Office released the toxicology findings. The cause of death: the combined toxic effects of five substances — **fentanyl**, **4-ANPP** (a chemical used in fentanyl manufacturing; its presence almost always means illicitly made fentanyl, not a hospital prescription), **alprazolam** (the benzodiazepine sold as Xanax), **methocarbamol** (a prescription muscle relaxer) and **quetiapine** (the sedating antipsychotic sold as Seroquel). The manner of death was ruled an accident, and the coroner has administratively closed its case.

## What investigators found at the apartment
A 911 call at 1:51 PM on August 16 brought first responders to the Judson Mill Lofts on Easley Bridge Road in Greenville, where Panettiere was temporarily staying. According to the coroner's report, she was found face-down on a sofa bed, her skin deep purple. Her boyfriend, Brian Hickerson, administered two doses of Narcan before paramedics arrived; she did not respond. EMS crews continued resuscitation for more than 40 minutes before she was pronounced dead at 2:32 PM.

Investigators found **blue pressed pills and a cut straw** — both later testing positive for fentanyl — in a makeup bag, and a white powdery substance in a sunglasses case inside her suitcase. The autopsy found no signs of trauma. She had planned to spend her 36th birthday in Greenville five days later, then travel to Ukraine to visit her daughter.

## Why this combination stops breathing
Four of the five substances in her system slow the central nervous system: fentanyl (an opioid), alprazolam (a benzodiazepine), methocarbamol (a muscle relaxer) and quetiapine (a sedating antipsychotic). Stacked together they do not add up — they multiply. Each one deepens the respiratory depression of the others until breathing simply stops. This exact pattern — an opioid plus a benzo plus other sedating prescriptions — sits behind most fatal overdoses we track.

## The tolerance trap: she had just left rehab
Weeks before her death, Panettiere was released from a drug rehabilitation facility in Malibu, California, according to the coroner's report obtained by the AP. After any period of abstinence, tolerance collapses — a dose that was survivable in the spring can be fatal in the fall. It is the single deadliest window in opioid recovery, and it is why every quitting guide on this site repeats the same warning: after even a week clean, treat any dose like your first time, never use alone, and keep naloxone close.

## The counterfeit-pill theory
TMZ reports that law-enforcement sources believe Panettiere took a fentanyl-laced oxycodone pill supplied by a long-time dealer in Los Angeles, and that the DEA is working to trace the fatal pill back along that supply chain — a pattern that echoes the Mac Miller case, where dealers were later convicted. Greenville Police say their own investigation remains active even though the coroner's office has closed its file.

## What this changes for anyone reading
- Never mix opioids with benzodiazepines, sleepers, muscle relaxers or antipsychotics — that stack is what kills.
- A pill bought anywhere but a pharmacy can contain fentanyl, whatever it looks like. Test it before it touches you.
- After detox or rehab your tolerance is gone — the riskiest day of recovery is the first slip.
- Naloxone reverses fentanyl, but multiple doses are often needed and it only buys time. Call emergency services first, then give naloxone, then stay with the person.

If you or someone you know is struggling with opioids or prescription sedatives, the hotlines page lists free, confidential help in your region.""",
  sources=["Greenville County Coroner", "AP", "BBC", "The Guardian"], drugsInvolved=["fentanyl","alprazolam","methocarbamol","quetiapine"],
  related=["topics:fentanyl-numbers","topics:spot-pressed-pills","mix:opioids-benzodiazepines","quit:fentanyl"]),
dict(slug="sterling-nitrous-driving-case", country="United Kingdom", image="https://plugreports.com/media/drugs/sterling-nitrous-driving-case.webp", title="Raheem Sterling pleads guilty to driving on nitrous oxide before £270k Lamborghini crash", date="2026-09-17", tag="Alert",
  views=900,
  summary="The former England star admitted dangerous driving, possessing six 670g nitrous canisters and refusing a blood test after witnesses saw him inhaling from balloons at the wheel on the M3. Sentencing is set for November 25 - and it has put nitrous oxide, balloons and driving firmly in the spotlight.",
  body=["Raheem Sterling has pleaded guilty to dangerous driving and drug offences after crashing his £270,000 Lamborghini on the M3 in Hampshire, in a case that has thrown the growing nitrous oxide problem in professional football into harsh daylight.",
        "Basingstoke Magistrates' Court heard on September 15 that multiple motorists had called 999 between 1:10 AM and the crash at around 9 AM on May 28, 2026, reporting a black Lamborghini being driven erratically. One witness told the court she saw a large white balloon at the driver's mouth and 'had genuine concerns the driver might kill someone.' Three separate police forces received calls.",
        "Police bodycam footage shown in court captured the former Manchester City, Liverpool and Chelsea forward handling nitrous oxide canisters in the passenger seat and concealing deflated blue and yellow balloons between his legs. Officers found six 670-gram canisters - the large 'Galaxy Gas' style cylinders - inside the car. Sterling failed roadside coordination tests, swaying as he tried to perform them, and refused to provide a blood sample. At the custody desk, he told staff he 'had a problem with nitrous oxide.'",
        "Sterling, 31, who won 82 England caps, pleaded guilty to dangerous driving, possession of nitrous oxide with intent to wrongfully inhale it, and failing to provide a specimen. Nitrous oxide has been a Class C controlled drug in the UK since November 2023 - possession carries up to two years in prison. Judge Kirsty Allman imposed an interim driving ban and ordered an all-options pre-sentence report; Sterling returns to court on November 25, with prosecutors citing a 12-month starting point for the most serious offences, potentially suspended. The case could yet be escalated to Crown Court.",
        "The case matters beyond football. Nitrous is the 'party drug that looks harmless' - a 30-second high from a balloon, sold as whipped cream chargers or flavored catering canisters. The reality: heavy use chemically destroys vitamin B12, causing progressive nerve damage that has left regular users, including teenagers, temporarily unable to walk. And Sterling's case highlights the danger that rarely gets discussed: driving on nitrous. A driver mid-balloon is disoriented, oxygen-deprived and detached - a witness in this case believed she was watching someone about to kill another road user.",
        "Sterling's representatives have pointed to extensive mitigation, including voluntary steps to address his difficulties, and sources close to the player have previously spoken about the toll of the abrupt end of his top-level career. He has been without a club since leaving Feyenoord in the summer."],
  sources=["The Telegraph","BBC Sport","The Athletic","Sky News","Yahoo Sports/AFP"],
  drugsInvolved=["nitrous-oxide","whippets","nangs-galaxy-gas"],
  related=["topics:nitrous-nerve-damage","topics:inhalants-youth","nitrous-oxide","topics:talk-to-your-kid"]),

 dict(slug="nitazenes-spreading-eu", title="Nitazenes now detected in 12 European monitoring systems", date="2026-09-10", tag="Trend",
  summary="EMCDDA early-warning reports show the nitazene family (etonitazene, metonitazene, isotodesnitazene) spreading from the Baltics across Western Europe, mostly hidden in counterfeit oxycodone and 'heroin'.",
  body=["Nitazenes were developed by CIBA in the 1950s and abandoned as medicines — they are 10–25x fentanyl's potency and have no approved human use.",
        "Drug-checking services in several EU cities report nitazenes in pills sold as oxycodone 80 mg. Naloxone reverses them, but multiple doses are often needed.",
        "See our full nitazene explainer and the etonitazene / isotodesnitazene profiles."],
  sources=["EMCDDA EU Early Warning System","NIDA"], drugsInvolved=["etonitazene","isotodesnitazene"]),
 dict(slug="xylazine-beyond-us", title="Xylazine ('Tranq') confirmed in drug supply outside North America", date="2026-09-02", tag="Adulterant",
  summary="First confirmed lab detections of xylazine-adulterated fentanyl in the UK and EU supply. Wound-care and naloxone-limit guidance is being updated by harm-reduction services.",
  body=["Xylazine is a veterinary tranquilizer — not an opioid — so naloxone does not reverse it, though you should still give naloxone for suspected fentanyl co-exposure.",
        "Its hallmark is necrotic skin wounds far from injection sites. Wounds need medical care even when small.",
        "Read: our Xylazine (Tranq) guide and topic page."],
  sources=["NIDA","UK Home Office ACMD"], drugsInvolved=["xylazine","fentanyl"]),
 dict(slug="high-dose-ecstasy-warning", country="Europe", image="https://plugreports.com/media/drugs/xtc-pills.jpeg", title="High-dose ecstasy pills (250–330 mg) circulating again this festival season", date="2026-08-25", tag="Alert",
  summary="Pill-testing services across Europe are flagging pressed pills at 2–3x a typical adult dose. PMA/PMMA copycat pills — slow to kick in, deadly — remain in circulation.",
  body=["A common adult dose is 80–120 mg. Pills above 200 mg significantly raise the risk of severe overheating and serotonin toxicity.",
        "If a pill takes 2+ hours to work, do NOT assume it's weak — it may be PMA/PMMA. Never redose on a slow pill.",
        "See: How to spot pressed pills — real vs fake."],
  sources=["PillReports","EMCDDA","The Loop UK"], drugsInvolved=["mdma"]),
 dict(slug="counterfeit-xanax-update", country="United States", image="https://plugreports.com/media/drugs/counterfeit-xanax-update.jpeg", title="Counterfeit 'Xanax bars' increasingly contain flubromazolam or fentanyl", date="2026-08-18", tag="Alert",
  summary="Forensic testing in the US and UK shows counterfeit alprazolam bars frequently contain the ultra-potent RC benzo flubromazolam — active at 0.25 mg — and intermittent fentanyl.",
  body=["Flubromazolam causes multi-day blackouts and dangerous withdrawal after short exposure.",
        "If you take pressed bars: never mix with opioids or alcohol, and tell someone what you took.",
        "Profiles: alprazolam, flubromazolam, clonazolam."],
  sources=["DEA","WEDINOS UK","NIDA"], drugsInvolved=["alprazolam","flubromazolam","fentanyl"]),
]

HOTLINES = {
 "USA": [("911","Emergency — overdose, always call","Fire/EMS can carry naloxone; Good Samaritan laws protect callers in most states.", "911"),
  ("1-800-662-4357","SAMHSA National Helpline","Free, 24/7, confidential treatment referrals (English/Spanish).","18006624357"),
  ("988","Suicide & Crisis Lifeline","Call or text 988 — crisis support 24/7.","988"),
  ("1-800-222-1222","Poison Control","24/7 poison and overdose triage by toxicology nurses.","18002221222"),
  ("1-800-484-3731","Never Use Alone","Call while using — an operator stays on the line and calls help if you become unresponsive.","18004843731"),
  ("Text HOME to 741741","Crisis Text Line","Free 24/7 text crisis support.","")],
 "Canada": [("911","Emergency","Immediate danger to life — always call first.","911"),
  ("9-8-8","Suicide Crisis Helpline","Call or text 9-8-8, 24/7.","988"),
  ("1-866-531-2600","ConnexOntario","Substance use and problem-gambling helpline, 24/7, free.","18665312600"),
  ("1-800-668-6868","Kids Help Phone","Youth support, call or text 686868.","18006686868")],
 "Europe": [("112","EU Emergency Number","Works in all EU member states, free, 24/7.","112"),
  ("0300 123 6600","FRANK (UK)","Drugs information & advice, 24/7, confidential.","03001236600"),
  ("0 800 23 13 13","Drogues Info Service (France)","Free, anonymous drug information line.","0800231313"),
  ("0180 5 31 30 31","Sucht- und Drogenhotline (Germany)","Federal addiction & drug hotline.","01805313031"),
  ("088 505 1220","Jellinek Advieslijn (Netherlands)","Addiction care advice line.","0885051220")],
 "Australia": [("000","Emergency","Ambulance, police, fire.","000"),
  ("1800 250 015","National Alcohol & Other Drug Hotline","Free 24/7 counselling and referral.","1800250015"),
  ("13 11 14","Lifeline","24/7 crisis support and suicide prevention.","131114"),
  ("1800 888 236","DirectLine (Victoria)","Free 24/7 AOD counselling & referral.","1800888236")],
 "Africa": [("SADAG 0800 456 789","South African Depression & Anxiety Group","Mental health helpline with substance-use support.","0800456789"),
  ("SANCA 011 262 5986","South African National Council on Alcoholism","Treatment referral network across SA provinces.","0112625986"),
  ("1192","NACADA Helpline (Kenya)","Government drug-control helpline, toll-free.","1192"),
  ("Nearest hospital emergency","Across the continent","Where dedicated lines are unavailable, hospital casualty departments and clinics are the fastest route to help.","")],
 "Europe (more)": [
  ("08595","RUS-telefonen (Norway)","National drug counselling helpline, free and anonymous.","08595"),
  ("020-44 00 20","CAN Helpline (Sweden)","Council on Alcohol and Other Drugs — advice and referrals.","020440020"),
  ("900 16 15 15","Drogas y Alcohol (Spain)","Government drug information line, free and confidential.","900161515"),
  ("112","EU Emergency","All EU member states.","112")],
 "New Zealand": [
  ("111","Emergency","Ambulance, police, fire.","111"),
  ("0800 787 797","Alcohol Drug Helpline","Free, 24/7 counselling and referral.","0800787797"),
  ("0800 543 354","Lifeline NZ","24/7 crisis support and suicide prevention.","0800543354")],
 "Asia (selected)": [
  ("112","India Emergency","Single national emergency number.","112"),
  ("91529 87821","iCall (India)","TISS psychosocial helpline — substance use, crisis, mental health (call/WhatsApp).","9152987821"),
  ("1669","Thailand Ambulance","Free emergency medical transport.","1669"),
  ("1323","Thailand Mental Health Hotline","Dept. of Mental Health crisis line.","1323")],
 "Latin America (selected)": [
  ("188","CVV (Brazil)","Centro de Valorização da Vida — 24/7 crisis support by phone/chat.","188"),
  ("192","SAMU (Brazil)","Emergency ambulance, free.","192"),
  ("CAPS AD","Free public addiction treatment (Brazil)","Centros de Atenção Psicossocial — free government addiction clinics in every city.","")],
}

PHARMACIES = [
 dict(slug="nabp-safe-pharmacy", name="NABP Safe Pharmacy (verification program)", region="USA/online",
  desc="The National Association of Boards of Pharmacy verifies legitimate online pharmacies. Check any site against their .pharmacy registry before buying medication online — most 'online pharmacies' are counterfeit pill mills.",
  phone="(847) 391-4400", website="https://safe.pharmacy", verified=True),
 dict(slug="pharmacychecker", name="PharmacyChecker Verification", region="USA/Canada/online",
  desc="Independent verification of licensed mail-order pharmacies, with price comparison limited to accredited sellers. Use it to avoid counterfeit ED pills and fake 'Canadian' pharmacies.",
  phone="", website="https://www.pharmacychecker.com", verified=True),
 dict(slug="napra", name="NAPRA — Canadian Pharmacy Regulators", region="Canada",
  desc="The National Association of Pharmacy Regulatory Authorities compiles each provincial pharmacy regulator's register. Verify any Canadian online pharmacy against its provincial college before buying.",
  phone="", website="https://napra.ca", verified=True),
 dict(slug="gphc-register", name="GPhC Register (UK)", region="UK",
  desc="The General Pharmaceutical Council's public register lets you confirm any UK pharmacy (online or physical) is licensed — and check the pharmacist-in-charge. The UK requires online pharmacies to display their GPhC registration.",
  phone="+44 20 3713 8000", website="https://www.pharmacyregulation.org/registers", verified=True),
 dict(slug="eu-common-logo", name="EU Common Logo (European online pharmacies)", region="EU/EEA",
  desc="EU law requires legal online pharmacies to display the common safety logo (falsified-medicines directive). Verify it via your national medicines regulator's register — no logo, no legal online pharmacy.",
  phone="", website="https://health.ec.europa.eu/medicinal-products/falsified-medicines_en", verified=True),
 dict(slug="healthwarehouse", name="HealthWarehouse.com", region="USA",
  desc="NABP-accredited US online pharmacy (VIPPS). A reference example of what a verified online pharmacy looks like: requires prescriptions, licensed pharmacists, US address.",
  phone="(513) 8DEPO-7", website="https://www.healthwarehouse.com", verified=True),
]

REHABS = [
 dict(slug="hazelden-betty-ford", name="Hazelden Betty Ford Foundation", region="USA (multi-state)",
  desc="One of the largest nonprofit addiction treatment organizations in the US: residential, outpatient, detox, and virtual care. Sliding-scale and insurance accepted.",
  phone="1-866-831-5700", website="https://www.hazeldenbettyford.org", verified=True),
 dict(slug="priory-group", name="Priory Group", region="UK & Europe",
  desc="Major UK mental-health and addiction provider: residential rehab, day programs, NHS-funded pathways.",
  phone="0800 840 3218", website="https://www.priorygroup.com", verified=True),
 dict(slug="narcotics-anonymous", name="Narcotics Anonymous", region="Worldwide (free)",
  desc="Free, peer-led 12-step fellowship with meetings in 140+ countries. No cost, no insurance, no referral needed — welcome with any drug history.",
  phone="", website="https://www.na.org", verified=True),
 dict(slug="aa-worldwide", name="Alcoholics Anonymous — Worldwide", region="Worldwide (free)",
  desc="The original 12-step fellowship with meetings in 180+ countries and dozens of languages — including most of the countries sending you traffic. Free, anonymous, no referral needed.",
  phone="", website="https://www.aa.org", verified=True),
 dict(slug="turning-point", name="Turning Point", region="UK & Australia",
  desc="One of the largest addiction treatment and social-care charities in the UK, also operating in Australia: residential rehab, community programmes, and the national 'Frank' drug information service on behalf of government.",
  phone="020 7481 7600", website="https://www.turning-point.co.uk", verified=True),
 dict(slug="smart-recovery", name="SMART Recovery", region="Worldwide (free)",
  desc="Evidence-based, self-empowering alternative to 12-step: CBT and motivational tools. Free meetings online and in-person across our focus regions.",
  phone="", website="https://www.smartrecovery.org", verified=True),
]

SENTENCING = [
 dict(region="Middle East (Gulf states)", flag="ME",
  summary="The Gulf operates the world's harshest drug regimes — several states apply the death penalty for trafficking, and two have EXPANDED capital punishment in the last 10 months (Kuwait December 2025, Oman September 2026). Saudi Arabia is executing drug offenders at a record pace. Even trace amounts of drugs in your body can count as 'possession' in Kuwait. Travelers have been jailed for residue, prescription medicines, and poppy seeds.",
  table=[["Country","Possession / personal use","Trafficking","Documented cases"],
   ["Saudi Arabia","Prison terms + fines; Sharia courts","DEATH PENALTY (Narcotics & Psychotropic Substances Act)","Record 2025: 239 executions by Aug 4 — 15 people executed in one weekend (13 for hashish smuggling, 1 for cocaine); UN expert urged halt to execution of 26 Egyptians for drug offences, 2 executed May 24-25, 2025; on pace to beat 2024's 338 (highest on record)"],
   ["UAE","3 months – 2 yrs or fines AED 20k–200k (escalating with repeats); treatment instead of jail if help sought before arrest (Art. 89); tourists: fines AED 5k–100k + entry bans (Cabinet Res. 43/2024)","Life imprisonment; death penalty for gang-linked trafficking or repeat promotion (Federal Decree-Law 30/2021)","Deportation ordered for most foreign convictions (Art. 75); first-time personal use can be replaced with rehab; prescription rules strictly enforced at airports"],
   ["Qatar","~2–15 years prison + heavy fines + deportation (personal amounts)","DEATH PENALTY or life imprisonment + very heavy fines (Law No. 9 of 1987)","Zero-tolerance state; foreign embassies report very limited ability to intervene in drug cases; personal-use amounts still bring years in prison, not death"],
   ["Kuwait","5 years prison + 5,000 KWD fine — INCLUDING trace amounts in the body; penalties DOUBLE near schools, mosques, gyms (new law, Dec 2025)","DEATH or life imprisonment + 500,000 KWD+ fine (Dec 2025 amendments — toughest in decades)","Courts issued roughly ONE death sentence per month in drug cases in 2024; 2 Iranian nationals executed for drugs in 2025; ~30 on death row, 40% drug cases; government vows to clear backlog within 6 months; exemption if help sought before investigation"],
   ["Bahrain","Long prison terms + fines","DEATH PENALTY available (Law 15/2007); executions resumed 2017 after 7-year pause; King ratifies; firing squad","Jan 2020: Court of Cassation upheld death sentences of two Bahraini men for trafficking — 100+ human rights groups appealed to the UN; drug death sentences rising on death row"],
   ["Oman","Prison + fines","DEATH PENALTY for aggravated smuggling — NEW LAW (Sept 2026): repeat offences and quantity-based cases; life imprisonment in specified cases","September 2026 anti-narcotics law introduced capital punishment for aggravated trafficking for the first time in the sultanate's modern framework"]]),
 dict(region="United States", flag="US",
  summary="Two systems apply: federal and state. Federal simple possession (first offence) carries up to 1 year; trafficking scales to life. Most possession cases are prosecuted under state law, where penalties vary enormously.",
  table=[["Offence (federal)","Typical range"],
   ["Simple possession, 1st offence","Up to 1 year + fine"],
   ["Simple possession, 2nd+","15 days–2 years"],
   ["Trafficking (e.g., fentanyl >400g)","10 years–life (mandatory minimums)"],
   ["Good Samaritan laws","47 states protect overdose callers from possession charges"]]),
 dict(region="Canada", flag="CA",
  summary="Controlled Drugs and Substances Act. Simple possession (summary conviction): fines and diversion for first offences; indictable up to 3 years for repeat or hard drugs. Trafficking 1 year–life.",
  table=[["Offence","Typical range"],
   ["Possession (summary)","Discharge to 6 months / fines"],
   ["Possession (indictable)","Up to 3 years"],
   ["Trafficking","1 year–life"],
   ["Note","Supervised consumption sites operate legally in BC, ON, QC and AB"]]),
 dict(region="United Kingdom", flag="UK",
  summary="Misuse of Drugs Act 1971: Class A (heroin, cocaine, MDMA) possession up to 7 years; Class B (amphetamine, ketamine, cannabis) 5 years; Class C (benzos without Rx, GHB) 2 years. Supply sentences roughly triple possession.",
  table=[["Class","Possession","Supply"],
   ["A (heroin, coke, MDMA, LSD)","7 yrs","Life"],
   ["B (speed, ketamine, cannabis)","5 yrs","14 yrs"],
   ["C (benzos w/o Rx, GHB)","2 yrs","14 yrs"]]),
 dict(region="European Union", flag="EU",
  summary="No single EU drug law — each member state differs widely. Notable: Portugal decriminalized possession of small (10-day supply) amounts in 2001 (administrative offences only); most states treat supply far more harshly than possession.",
  table=[["Country","Possession (small amount)"],
   ["Portugal","Administrative fine / dissuasion panel — not criminal"],
   ["Germany (cannabis)","Legal within personal-use limits"],
   ["France","1 year + fine (use is also an offence)"],
   ["Netherlands","Cannabis tolerated in coffeeshops; hard drugs prosecuted"]]),
 dict(region="Australia", flag="AU",
  summary="State-based law. Simple possession commonly up to 2 years (varies by state and drug); several states offer diversion (caution / education) for first offences. Importation is federal and severe — up to life.",
  table=[["Offence","Typical range"],
   ["Possession (state)","Fines to 2 yrs imprisonment"],
   ["Cultivation/manufacture","2–25 yrs"],
   ["Importation (federal)","Up to life imprisonment"]]),
 dict(region="Africa (selected)", flag="AF",
  summary="Varies widely. South Africa: Drugs and Drug Trafficking Act — possession of dependence-producing drugs carries fines and/or up to 15 years for dangerous drugs; personal cannabis use was decriminalized by the Constitutional Court in 2018. Kenya and Nigeria maintain strict criminal regimes with long trafficking sentences.",
  table=[["Country","Possession"],
   ["South Africa","Fines / up to 15 yrs (dangerous drugs)"],
   ["Kenya","Fines + up to 10 yrs"],
   ["Nigeria","10 yrs+ (NDLEA Act)"]]),
 dict(slug="asia-selected", region="Asia (selected)", flag="AS",
  summary="Asia mixes the world's harshest regimes (Singapore, China, Malaysia, Indonesia — all execution states) with fast-changing laws elsewhere. India's NDPS Act is the subcontinent's framework; Thailand's cannabis status has swung legal-to-illegal within three years. Travelers: many common prescription medicines (codeine, ADHD meds, benzos, even some cold remedies) are controlled or banned at borders.",
  table=[["Country","Possession (personal)","Trafficking","Documented cases"],
   ["India","Small quantity (per-drug thresholds): 6 months – 1 yr + fine; below threshold can mean counselling. Commercial quantity: 10–20 yrs + heavy fines (NDPS Act 1985)","20 yrs – life; death possible for repeat large trafficking","High-profile 2020-21 cases (Rhea Chakraborty, Aryan Khan) ended in bail, not conviction — but months in jail before bail; 2024 NDPS amendments streamline prosecutions"],
   ["Singapore","Long prison + caning (drug consumption is itself an offence)","DEATH PENALTY above set thresholds (e.g., >15 g diamorphine) — presumption laws apply","2023 discretion reforms let some couriers get life + caning instead; executions: 11 in 2022, 5 in 2023, 9 in 2024 — mostly drug cases"],
   ["Thailand","Post-2025: cannabis flower re-criminalized for recreational use; meth/heroin (Category I): prison terms","Category I trafficking: life – death (Narcotics Act)","Cannabis legalized 2022, re-criminalized 2025 — a warning on how fast laws flip; meth ('yaba') trafficking carries life/death"],
   ["Malaysia / Indonesia","Long mandatory prison","DEATH PENALTY (Dadah Act 39B; Indonesian narcotics law)","Both execute foreign nationals for trafficking; quantity thresholds low"]]),
 dict(slug="latin-america-selected", region="Latin America (selected)", flag="LA",
  summary="Latin America distinguishes users from traffickers in law more than anywhere — but enforcement is unequal and cartel violence shapes the reality. Personal use is decriminalized (no prison) in Mexico, Brazil, Argentina, Colombia and others, yet thousands sit in pre-trial detention on trafficking charges.",
  table=[["Country","Possession (personal)","Trafficking","Documented cases"],
   ["Brazil","Personal use: NOT a crime (2006 law) — warning/treatment; no fixed quantity, judged case-by-case","5–15 yrs prison","Racial and class disparities: favela residents convicted as traffickers for quantities wealthier users walk on"],
   ["Mexico","Under allowed-table quantities: no criminal sanction (max: 5 g heroin? — per-drug table, e.g., 5 g opium, 0.5 g cocaine, 5 g cannabis)","Federal prison; organized-crime federal prosecutions","Personal-use table since 2009; enforcement at borders still harsh"],
   ["Colombia","Personal dose: legal possession of a 'minimum dose' (20 g cannabis, 1 g cocaine base...)","8–30 yrs (drug trafficking is an 'exceptional' crime)","Constitutional Court personal-dose rulings; ELN/cartel enforcement zones remain violent"]]),
]

SETTINGS = dict(site="plugreports.com", tagline="Know the drug. Know the risk. Know the way out.",
 reddit="https://www.reddit.com/u/plugreports/s/WV01nxBLan", quora="https://plugreports.quora.com/", email="contact@plugreports.com",
 gsc="fpjrQ73pPwkCAm_jYft5fKHfCgei5Eu3zr6KTmTmNtc", bing="", clarity="yiltr1g8h1", ga="",
 crisisNote="If you or someone nearby may be overdosing: call emergency services now, give naloxone if available, stay with the person.")

QUIT_SPECS = {
 "heroin": dict(name="Heroin", cat="Opioid", danger="Medical detox strongly advised — opioid withdrawal is rarely deadly on its own; complications (dehydration, relapse into lowered tolerance) are the killers.",
  days=[("Hour 6–12","First withdrawal","Anxiety, muscle aches, sweating, runny nose — like a severe flu starting."),
        ("Day 1–3","Peak","Nausea, vomiting, diarrhea, insomnia, cramps. Peak and highest relapse-risk window."),
        ("Day 4–7","Turning corner","Physical symptoms ease; exhaustion and low mood dominate. Sleep slowly returns."),
        ("Week 2–4","PAWS begins","Anhedonia (nothing feels good), cravings, anxiety. Most relapses happen here — support matters most now."),
        ("Month 2–6","PAWS fades","Energy and mood normalize gradually. Exercise and routine genuinely accelerate this.")],
  tips=["Naloxone on hand — relapse after detox is the #1 overdose killer because tolerance drops",
        "Buprenorphine/methadone and meds like clonidine make detox far safer — see a clinic",
        "Never Use Alone line if you do use: 1-800-484-3731"]),
 "fentanyl": dict(name="Fentanyl", cat="Opioid", danger="Same opioid withdrawal profile as heroin, often starting sooner and dragging longer due to fentanyl's fat storage. Buprenorphine induction needs special timing — see a clinician.",
  days=[("Hour 4–8","Early withdrawal","Fentanyl stores in body fat — symptoms can start fast and drag out."),
        ("Day 1–4","Brutal peak","Longer peak than heroin — days 2 and 3 are typically the worst."),
        ("Day 5–10","Slow ease","Symptoms fade slowly; insomnia and restless legs linger."),
        ("Weeks 2–8","Extended PAWS","Stored metabolites make post-acute symptoms longer than heroin for many people."),
        ("Month 3+","Recovery","Most report feeling substantially normal by month 3–6 with support.")],
  tips=["Do not attempt fentanyl detox alone — the relapse-overdose window is deadly",
        "Methadone/buprenorphine maintenance is medicine, not failure",
        "Keep naloxone everywhere you might be"]),
 "cocaine": dict(name="Cocaine", cat="Stimulant", danger="Withdrawal is psychological more than physical — the crash is depression and craving, and suicide risk is real. Support matters.",
  days=[("Hour 1–72","The crash","Exhaustion, depression, increased appetite, intense craving. Sleep a lot — your brain is repairing."),
        ("Week 1","Anhedonia","Nothing feels rewarding. This is dopamine depletion, not a permanent state."),
        ("Weeks 2–4","Craving waves","Cravings come in waves, usually triggered by people, places, paraphernalia. Each wave passes in ~15 minutes."),
        ("Month 1–3","Steady recovery","Sleep, mood and motivation normalize. Vivid drug dreams are common and normal."),
        ("Month 3+","New baseline","Most cognitive and mood effects resolve. Cardiovascular risk starts dropping immediately after quitting.")],
  tips=["The crash is temporary — week 1 is not how you'll feel forever",
        "Delete numbers, change routes, avoid using friends for the first 90 days",
        "If depression feels dangerous, call/text 988 (US)"]),
 "meth": dict(name="Methamphetamine", cat="Stimulant", danger="Longest and deepest crash of the stimulants — expect 1–3 weeks of heavy sleep and low mood, then months of gradual dopamine recovery.",
  days=[("Days 1–3","The wall","12–20 hour sleeps, ravenous hunger, flat mood. Normal repair, not failure."),
        ("Week 1–2","Low mood","Anhedonia, irritability, intense craving. Suicide risk peaks here — don't isolate."),
        ("Weeks 3–6","Fog lifting","Thinking clears; 'meth dreams' and sudden cravings are common and pass."),
        ("Months 2–6","Dopamine rebuild","Motivation and pleasure return slowly. Exercise is one of the few proven accelerants."),
        ("Month 6+","Largely recovered","Most cognitive testing returns to normal ranges within 6–12 months.")],
  tips=["Eat and sleep on schedule — the brain needs raw materials to rebuild",
        "Cravings pass in waves; have a 15-minute plan (shower, walk, call someone)",
        "NA/MA meetings and contingency-management programs have the best evidence"]),
 "mdma": dict(name="MDMA", cat="Empathogen", danger="No dangerous physical withdrawal — but expect a real serotonin comedown. The main risks are depression in week 1 and the temptation to redose to escape it.",
  days=[("Day 1–3","Comedown","Low mood, fatigue, appetite loss. Serotonin stores are depleted; they rebuild."),
        ("Week 1","Emotional flatness","Some feel tearful or anxious. Sleep, sunlight and exercise help more than anything."),
        ("Week 2–4","Back to baseline","Mood normalizes. If it doesn't — or low mood predates use — talk to a professional."),
        ("Ongoing","Frequency rule","The brain needs roughly 1–3 months between rolls to recover serotonin function — more frequent use is where real damage happens.")],
  tips=["Never use MDMA to escape the MDMA comedown — that's the spiral",
        "Persistent low mood after use is a sign to stop and get support",
        "Test pills — PMA/PMMA masquerading as MDMA kills"]),
 "alprazolam": dict(name="Alprazolam (Xanax)", cat="Benzodiazepine", danger="NEVER quit cold turkey after regular use — benzodiazepine withdrawal can cause fatal seizures. Taper under medical supervision (diazepam-switch / Ashton-style).",
  days=[("During taper","Slow reduction","A proper taper reduces dose ~5–10% every 1–2 weeks so symptoms stay manageable."),
        ("Post-taper wk 1","Rebound","Anxiety and insomnia return hard — the brain recalibrating, not a need for the drug."),
        ("Weeks 2–6","Acute withdrawal","Sensory hypersensitivity, muscle pain, waves of panic. Peaks around week 2–3."),
        ("Months 2–12","Protracted (some)","A minority get months of windows-and-waves. It resolves — peer support groups help enormously.")],
  tips=["Seizure risk is exactly why you taper — never stop abruptly",
        "Tell a prescriber honestly; they help with this every day",
        "Avoid alcohol completely during withdrawal"]),
 "ketamine": dict(name="Ketamine", cat="Dissociative", danger="Physical withdrawal is mild; the real recovery targets are the bladder and the mind. Heavy users often need months for bladder symptoms to improve.",
  days=[("Day 1–7","Cravings + low mood","Irritability, restlessness, low mood. Urinary frequency may temporarily worsen before improving."),
        ("Weeks 2–4","Bladder recovery","Pelvic pain and frequency ease when use stops. Hydrate; see a urologist if blood appears."),
        ("Months 1–3","Mood rebuild","Motivation returns. K-cravings are strongly situational — change routines."),
        ("Month 3+","Mostly recovered","Bladder symptoms largely resolve in most former heavy users who stay stopped.")],
  tips=["K cramps and blood in urine = stop now and see a doctor",
        "Improving urinary symptoms are your proof the body repairs",
        "Ketamine is used clinically for depression — self-medicating is not the same thing"]),
 "ghb": dict(name="GHB/GBL", cat="Depressant", danger="Daily GHB/GBL use creates the most dangerous withdrawal of any recreational drug — abrupt cessation can be fatal (seizures, delirium, rhabdomyolysis). Medical detox is NOT optional for daily users.",
  days=[("Hour 4–8","First signs","Tremor, anxiety, insomnia — GHB clears fast, so daily users dose around the clock."),
        ("Day 1–3","Acute withdrawal","Severe anxiety, hallucinations, fast heart rate. A MEDICAL EMERGENCY — hospital detox with benzodiazepines is standard."),
        ("Weeks 2–4","Rebound","Insomnia, low mood, persistent tremor slowly fade."),
        ("Month 1–3","Stabilize","Sleep architecture and mood normalize.")],
  tips=["Daily user? Do not attempt sudden withdrawal outside hospital",
        "GHB withdrawal kills — treat it like alcohol withdrawal (mechanistically it is)",
        "Every hour of recovered sleep is measurable progress"]),
}

# Block types: p, h2, h3, ul, ol, quote, callout(color,title,text), stats[(n,label)],
# table(headers+rows), figure(html, caption), timeline, checklist, related[slugs], links[urls]
TOPICS = [
 dict(slug="what-is-xylazine", title="What is Xylazine (Tranq) and why it's terrifying first responders", date="2026-09-11", read="6 min",
  desc="The veterinary sedative being cut into fentanyl — the wounds, the blackouts, and why naloxone doesn't fix it.",
  blocks=[
   ("p","Xylazine is a veterinary anesthetic approved for horses and cattle. It is <b>not an opioid, not a human medicine, and has no approved antidote</b> for human overdose. Since roughly 2020 it has spread through the US fentanyl supply; by 2023 the DEA found it in about a quarter of tested fentanyl powder, and detections have since been confirmed in Canada, the UK and continental Europe."),
   ("h2","Why it's different from every other adulterant"),
   ("ul",["It <b>slows breathing like an opioid but isn't one</b> — naloxone will NOT reverse it (give naloxone anyway if fentanyl is possible; xylazine is almost always mixed with it).",
          "It causes <b>necrotic skin wounds</b> — 'tranq lesions' — black scabs that can appear anywhere on the body, not just injection sites, and can lead to amputation.",
          "It causes <b>hours-long blackouts</b> during which people are robbed, assaulted, or stop breathing."]),
   ("callout",("red","If someone is unresponsive","Call emergency services immediately. Give naloxone if you have it (for the fentanyl). Xylazine has no field antidote — hospital supportive care (airway, breathing support) is the only treatment.")),
   ("h2","Why first responders are alarmed"),
   ("p","Overdoses involving xylazine respond slower and less predictably. Blood pressure drops hard. Wounds need wound-care teams most paramedics don't carry. And users in withdrawal face <b>both</b> opioid withdrawal and xylazine withdrawal at once — a combination clinics are still learning to treat."),
   ("stats",[("~25%","of US fentanyl powder contained xylazine (DEA, 2023)"),("0","approved human antidotes"),("hrs","typical blackout length after a tranq-heavy dose")]),
   ("h2","If you or someone you know is using tranq-dope"),
   ("checklist",["Never use alone — call Never Use Alone (US): 1-800-484-3731","Carry naloxone — it reverses the fentanyl half of the mix","Treat every small wound seriously: clean, cover, and get medical care early — tranq wounds do not heal on their own","Tell wound-care and outreach workers you use tranq — they now specialize in this"]),
   ("related",["xylazine","fentanyl","nitazenes-new-opioids"])]),

 dict(slug="cocaine-purity-and-cuts", image="https://plugreports.com/media/drugs/cocaine-purity-and-cuts.jpeg", title="What is cocaine actually cut with? Purity explained", date="2026-09-09", read="7 min",
  desc="From levamisole to phenacetin to fentanyl: what drug-checking shows is really in cocaine, and why 'pure' can be more dangerous, not less. External deep-dive: 247avlplug.com/understanding-cocaine-purity/.",
  blocks=[
   ("p","Retail cocaine purity has climbed in Europe (EMCDDA reports averages near 60–70% in several countries) while US seizures vary widely. But purity is not safety — the most dangerous things in cocaine are often the <b>cuts and adulterants</b>, and occasionally fentanyl itself."),
   ("h2","The usual suspects found by drug checking"),
   ("table",[["Adulterant","Why it's there","The risk"],
     ["Levamisole (vet wormer)","Bulks powder, mimics stimulant feel","Immune suppression; severe skin necrosis"],
     ["Phenacetin / paracetamol / caffeine","Cheap bulk, numbing effect","Kidney damage (phenacetin); liver stress"],
     ["Boric acid / benzocaine","Mimics shine & numbing","Seizures at high dose; methemoglobinemia"],
     ["Mannitol, lactose, glucose","Inert bulk","Low risk by themselves"],
     ["Fentanyl (rare, deadly)","Cross-contamination at packaging","Opioid overdose in a non-tolerant user"]]),
   ("h2","Why 'stronger' cocaine sends more people to hospital"),
   ("p","When purity jumps from 30% to 70% without the user knowing, the same 'two lines' is more than double the dose. Drug-checking services report that <b>most cocaine hospitalizations track unexpected potency, not new drugs</b>."),
   ("callout",("amber","Harm reduction if you use","Start with a quarter of your usual amount when the source changes. Never mix with alcohol (forms cocaethylene — extra cardiotoxic) or opioids. If someone collapses with slow breathing after cocaine: give naloxone — it may be fentanyl contamination.")),
   ("quote","Cocaine-related deaths in England & Wales hit record levels in recent ONS releases — most involve cocaine plus opioids or alcohol together, not cocaine alone.","ONS / EMCDDA trend reporting"),
   ("related",["cocaine","4-fluorococaine","fentanyl"])]),

 dict(slug="fentanyl-numbers", image="https://plugreports.com/media/drugs/fentanyl.webp", title="Fentanyl: the numbers nobody tells you", date="2026-09-07", read="6 min",
  desc="2 milligrams. 5 minutes. One naloxone spray may not be enough. The arithmetic of the deadliest drug supply in history.",
  blocks=[
   ("stats",[("2 mg","potentially fatal dose — a few grains of salt"),("~75,000","US overdose deaths involving fentanyl per year (CDC)"),("10–25x","nitazene potency vs fentanyl — the next wave"),("3–5 min","for fentanyl to reach the brain when smoked")]),
   ("p","Fentanyl is a legitimate medicine — 50–100x morphine's potency, used for surgical pain and end-of-life care. Illegally manufactured fentanyl is the same molecule made in clandestine labs, pressed into fake pills that mimic oxycodone, Xanax, Adderall — even candy-colored tablets."),
   ("h2","The arithmetic that kills"),
   ("ul",["A lethal dose is <b>2 mg</b>; a $20 bag can hold hundreds of lethal doses — street mixes are eyeballed, not scaled.",
          "Pills are pressed, not dosed: <b>one pill in a batch can be 10x another</b>.",
          "Fentanyl builds dependence fast: <b>3–5 days of daily use creates physical dependence</b>."]),
   ("h2","The reversal arithmetic that saves"),
   ("p","Naloxone displaces fentanyl from opioid receptors. Because fentanyl binds hard, <b>one spray may reverse for only 30–90 minutes while fentanyl outlasts it</b> — the person can re-overdose. Protocol: give naloxone, call 911, and STAY — even after they wake up."),
   ("table",[["Sign","What to do"],
     ["Unresponsive, pinpoint pupils, slow/gurgling breathing","Call 911 (Good Samaritan laws protect you in most places)"],
     ["Naloxone given, person wakes","STAY. Second overdose possible as naloxone wears off"],
     ["No naloxone available","Rescue breathing / chest compressions until help arrives"]]),
   ("callout",("red","Free naloxone","US: naloxone is over-the-counter nationwide (Narcan, ~$45; many states and syringe programs give it free). Nextdistro.org and harm-reduction programs mail it free. Canada: pharmacies. UK: via drug services.")),
   ("related",["fentanyl","nitazenes-new-opioids","what-actually-happens-when-you-quit"])]),

 dict(slug="spot-pressed-pills", title="How to spot pressed pills: real vs fake", date="2026-09-04", read="8 min",
  desc="Counterfeit oxycodone, Xanax and Adderall kill thousands. The tells, the tests, and why appearance alone can never guarantee safety.",
  blocks=[
   ("p","Pill presses are cheap and imprints are copyable — <b>the DEA states most counterfeit pills tested contain fentanyl or meth</b>. You cannot identify a fake reliably by eye. What you CAN do is stack the odds: know the tells, use test strips, and never use alone."),
   ("h2","Visual tells (weak, but worth knowing)"),
   ("checklist",["Imprint uneven, smudged or off-center — pharma imprints are laser-crisp","Color 'too' uniform or slightly off-shade; coating looks painted on","Pill crumbles or chips easily; real tablets are dense","Source: social-media DM, 'a friend of a friend', or '$5 blues' — classic counterfeit channels","Price too good: real 30 mg oxycodone diverts at $15–40"]),
   ("h2","What lab testing actually finds"),
   ("table",[["Pill sold as","Typical lab finding"],
     ["'Oxycodone 30' (blue, M30)","Fentanyl + filler — sometimes ONLY fentanyl"],
     ["'Xanax bar'","Alprazolam — or etizolam, flubromazolam, sometimes fentanyl"],
     ["'Adderall 30' (orange)","Methamphetamine or caffeine/dextro blends"],
     ["'Percocet'","Fentanyl; rarely any oxycodone"]]),
   ("h2","The real safety layers"),
   ("ul",["<b>Fentanyl test strips</b> (~$1): dissolve a tiny sample — two lines = fentanyl absent, one line = present.",
          "<b>Reagent kits</b> (Marquis/Mecke): distinguish MDMA from PMA, opiates, etc.",
          "<b>Never use alone</b> + naloxone within reach — the last line, and the one that has saved hundreds of thousands of lives.",
          "<b>Drug checking</b> where legal: The Loop (UK), DIMS (NL), Energy Control (ES), CheckIt! (AT)."]),
   ("callout",("red","If someone took a pill and is now unresponsive","Naloxone NOW (repeat doses if needed), 911, rescue breathing. Tell responders exactly what was taken — they treat, not arrest.")),
   ("related",["fentanyl","alprazolam","counterfeit-xanax-update"])]),

 dict(slug="drug-busts-this-week", title="Drug busts this week: how to read enforcement news", date="2026-09-01", read="5 min",
  desc="Seizures are data about the supply, not just police wins. What a bust headline actually tells you — and what it doesn't.",
  blocks=[
   ("p","Every week agencies publish seizure figures: pills, kilograms, precursor chemicals. Read them like a supply-chain analyst — they tell you <b>what's flowing, where, and in what form</b>."),
   ("h2","How to read a bust headline"),
   ("ul",["<b>Pill counts (e.g. '500,000 pills')</b> → industrial pill-press networks; that volume means a regional hub, not a street dealer.",
          "<b>Kilograms at ports</b> → the wholesale tier; price ripples reach streets months later.",
          "<b>Precursor seizures (NPP, ANPP, 4-AP)</b> → a fentanyl lab is being starved; expect temporary local potency spikes.",
          "<b>One region repeatedly</b> → an active trafficking corridor; local harm-reduction services usually post alerts."]),
   ("h2","Why this matters for safety"),
   ("p","After major seizures, markets destabilize: <b>strength varies batch to batch for weeks</b>. The period after a big bust is consistently a high-risk window for unexpected potency."),
   ("callout",("amber","Practical takeaway","When big seizures make local news: treat your usual dose as unknown, test if you can, never use alone, keep naloxone close.")),
   ("p","We track notable seizures in our Busts section — each entry lists agency, location, substances and the applicable sentencing exposure."),
   ("related",["busts","fentanyl-numbers"])]),
]

TOPICS += [
 dict(slug="krokodil-fact-vs-myth", title="Krokodil: the drug that rots flesh — fact vs myth", date="2026-08-29", read="6 min",
  desc="Desomorphine is real. The zombie-apocalypse version mostly wasn't. What krokodil actually is, and where the flesh-rotting really comes from.",
  blocks=[
   ("p","Krokodil is desomorphine — a semi-synthetic opioid 8–10x morphine's potency, used medically in Soviet-era Russia. The 'flesh-rotting zombie drug' of 2010s headlines was <b>not the molecule</b> — it was the chemistry: users synthesize it from codeine tablets using gasoline, hydrochloric acid and red phosphorus, then <b>inject without purification</b>."),
   ("h2","The facts"),
   ("ul",["Desomorphine itself is a short-acting opioid — the damage attributed to 'krokodil' comes from <b>residual acids and solvents burning skin and veins</b>.",
          "Confirmed cases cluster where codeine is OTC and heroin is scarce — Russia, Ukraine, Kazakhstan. Isolated cases elsewhere were often misattributed.",
          "Repeated 'spreading to the US/EU' panics were debunked — codeine is prescription-controlled in the West, removing the raw material.",
          "Yes, real users lost limbs — from gangrene and infections of the injection site, worsened by immune collapse."]),
   ("h2","Why the myth matters"),
   ("p","Panic coverage did real harm: it made users hide wounds until amputation was the only option, and it taught the public that drug injury is punishment rather than a medical emergency. The correct response to any injection wound — any drug, any country — is <b>early wound care</b>. Tranq (xylazine) wounds today are a real, spreading phenomenon; krokodil mostly wasn't."),
   ("callout",("green","If you have a wound from injecting","Clean with soap and water, cover with a clean dressing, seek a clinic EARLY. No clinic will report you to police for a wound. Hidden wounds become amputations.")),
   ("related",["xylazine","heroin"])]),

 dict(slug="nitazenes-new-opioids", title="Nitazenes: the new opioids stronger than fentanyl", date="2026-08-26", read="6 min",
  desc="Abandoned 1950s medicines, resurrected by the drug trade. Etonitazene, isotodesnitazene and what their spread changes about overdose response.",
  blocks=[
   ("p","The nitazenes are a family of benzimidazole opioids synthesized at CIBA in the 1950s and <b>never approved for human use</b> — animal studies showed them too dangerous for medicine. The drug trade disagreed: they are cheap to synthesize, easy to ship, and 10–25x fentanyl's potency."),
   ("h2","Which ones are showing up"),
   ("table",[["Compound","Relative potency","Where it's appearing"],
     ["Etonitazene","10–25x fentanyl","Counterfeit pills; US Schedule I (2023); EU alerts"],
     ["Isotodesnitazene ('ISO')","≈ fentanyl","Heroin/fentanyl adulterant; US midwest + Baltic→EU spread"],
     ["Metonitazene","≈ fentanyl","US east coast; injected 'dope' supplies"],
     ["Protonitazene","≈ 3x fentanyl","Increasing US forensic identifications"]]),
   ("h2","What changes for overdose response"),
   ("ul",["<b>Naloxone still works</b> — nitazenes are opioids — but <b>higher or repeated doses are often required</b>.",
          "They last long: re-sedation after naloxone wears off is common. <b>Stay; repeat doses every 2–3 min if they re-sedate.</b>",
          "Standard urine screens often MISS nitazenes — hospitals may not detect them. Tell responders what the local supply rumor mill says."]),
   ("callout",("red","If you use any opioid in 2026","Assume fentanyl, assume nitazenes, assume tranq. Carry 2+ naloxone doses, never use alone, and treat 'they woke up' as the START of the emergency, not the end.")),
   ("related",["etonitazene","isotodesnitazene","fentanyl-numbers","xylazine"])]),

 dict(slug="sentencing-explained", title="Drug sentencing explained: what possession actually costs you", date="2026-08-22", read="9 min",
  desc="Schedule classes, mandatory minimums, Good Samaritan laws and the one phone call that changes everything. Region-by-region tables.",
  blocks=[
   ("p","Nothing on this page is legal advice — penalties change constantly and facts matter enormously. What follows is the map of how sentencing <b>systems</b> work in our five focus regions, so the stakes are understood before anyone stands in front of a judge."),
   ("h2","How the US system works (short version)"),
   ("ul",["<b>Federal vs state</b>: most possession cases are state; trafficking can be either. Federal simple possession (1st offence): up to 1 year. Trafficking fentanyl >400 g: <b>10 years to life, mandatory minimum</b>.",
          "<b>Drug weight drives everything</b>: a baggie + a scale can convert possession into 'possession with intent'.",
          "<b>Good Samaritan laws</b>: 47 US states + DC protect overdose-callers from possession charges. <b>They only work if someone calls.</b>",
          "<b>Drug courts & diversion</b>: many jurisdictions route first offences to treatment instead of jail — a fast lawyer request changes outcomes."]),
   ("h2","The five regions at a glance"),
   ("p","Full tables live on our Sentencing page — summary: UK Class A possession (heroin/coke/MDMA) up to <b>7 years</b>; Canada up to <b>3 years</b> indictable; the EU varies wildly (Portugal: no prison for personal amounts); Australia state-based, typically <b>up to 2 years</b>; Africa ranges from reform-minded (South Africa decriminalized personal cannabis) to severe."),
   ("h2","What to actually do if arrested"),
   ("checklist",["Say only: 'I want a lawyer and I'm exercising my right to remain silent.'","Do not consent to searches verbally — say 'I do not consent' calmly","Never discuss where anything came from — that sentence converts charges","Ask about diversion/drug court — they exist precisely for this"]),
   ("callout",("amber","The one thing that outweighs all of it","A living person beats a clean record. If someone is overdosing: CALL. Good Samaritan laws exist so fear of jail never wins over a life.")),
   ("related",["sentencing","hotlines"])]),

 dict(slug="talk-to-your-kid", title="How to talk to your kid about drugs without losing them", date="2026-08-19", read="7 min",
  desc="The evidence is clear: fear lectures fail, honest conversations work. A practical script for every age.",
  blocks=[
   ("p","Decades of prevention research converge on one finding: <b>'just say no' programs don't work; connected, honest conversations do.</b> Kids who can talk to their parents about drugs use less, and use more safely when they do experiment. The goal isn't a promise — it's a channel."),
   ("h2","The core rules"),
   ("ul",["<b>Ask before you tell.</b> 'What have you heard about vapes/pills at school?' turns a lecture into a conversation.",
          "<b>Trade honesty for honesty.</b> You don't have to confess details — but don't lie. 'I tried things; here's what I wish I'd known' lands harder than any threat.",
          "<b>Teach the fentanyl reality, not the 1980s version.</b> The conversation that matters most now: <b>never take a pill that wasn't prescribed to them</b> — counterfeit Adderall/Xanax/oxycodone is where kids die.",
          "<b>Separate the person from the drug.</b> 'I'm not mad at you — I'm worried about the pill' keeps the channel open after a confession."]),
   ("h2","Age-by-age script"),
   ("table",[["Age","What to say"],
     ["8–12","Medicine rules: only from parents/doctor, never a friend's pill; some people sell pills that look real but aren't"],
     ["13–15","Vapes, edibles and the counterfeit-pill warning; extract the 3 AM promise"],
     ["16–18","Fentanyl specifics, naloxone at school, Good Samaritan laws, and the standing deal: 'call me at 3 AM and I'll come — no punishment that night, ever'"],
     ["18+","Treat as adults: harm reduction, testing, what an overdose looks like"]]),
   ("callout",("green","The 3 AM rule","One promise unlocks everything: 'If you or a friend is in trouble, call me first. No punishment that night — we talk tomorrow.' Fear of punishment is exactly why kids die in parking lots instead of calling.")),
   ("related",["hotlines","fentanyl-numbers"])]),

 dict(slug="hotline-directory", title="Hotline directory: help anywhere", date="2026-08-15", read="4 min",
  desc="Every verified helpline across the USA, Canada, Europe, Australia and Africa — overdose, crisis, treatment referral, in one place.",
  blocks=[
   ("p","These are the numbers that answer at 3 AM. Save this page. Full cards with tap-to-call buttons are on our Hotlines page — this is the quick-reference directory."),
   ("h2","USA"),
   ("ul",["<b>911</b> — emergency (say 'unresponsive, not breathing'; naloxone given if available)",
          "<b>SAMHSA 1-800-662-4357</b> — treatment referral, 24/7, free",
          "<b>988</b> — suicide & crisis (call/text/chat)",
          "<b>Poison Control 1-800-222-1222</b>",
          "<b>Never Use Alone 1-800-484-3731</b>",
          "<b>Crisis Text Line: text HOME to 741741</b>"]),
   ("h2","Canada"),
   ("ul",["<b>911</b> · <b>9-8-8</b> crisis (call/text) · <b>ConnexOntario 1-866-531-2600</b> · <b>Kids Help Phone 1-800-668-6868</b>"]),
   ("h2","Europe"),
   ("ul",["<b>112</b> EU emergency · <b>UK FRANK 0300 123 6600</b> · <b>FR 0 800 23 13 13</b> · <b>DE 0180 5 31 30 31</b> · <b>NL Jellinek 088 505 1220</b>"]),
   ("h2","Australia"),
   ("ul",["<b>000</b> emergency · <b>National AOD Hotline 1800 250 015</b> · <b>Lifeline 13 11 14</b> · <b>DirectLine 1800 888 236</b>"]),
   ("h2","Africa"),
   ("ul",["<b>South Africa: SADAG 0800 456 789</b> · <b>SANCA 011 262 5986</b> · <b>Kenya NACADA 1192</b> · elsewhere: nearest hospital emergency department"]),
   ("callout",("red","Overdose right now?","Call your local emergency number FIRST. Then naloxone if you have it. Then rescue breathing. Order matters.")),
   ("related",["hotlines","talk-to-your-kid"])]),

 dict(slug="what-actually-happens-when-you-quit", title="What actually happens to your body when you quit — day by day", date="2026-08-12", read="5 min",
  desc="Every substance has its own withdrawal clock. The honest, day-by-day timelines — what hurts, what's normal, and when it ends.",
  blocks=[
   ("p","Fear of withdrawal keeps people using more than almost anything else. The antidote is <b>a concrete timeline</b>: knowing that day 3 is the peak, or that the crash ends, is itself harm reduction. We publish full day-by-day pages per substance — this is the hub."),
   ("h2","The pattern across all substances"),
   ("ul",["<b>Hour 0–72</b>: acute phase. Opioids peak at 48–72 h; stimulants 'crash' at 24–72 h; alcohol and benzos are the dangerous ones (seizures) — both need medical detox.",
          "<b>Weeks 2–4</b>: most physical symptoms resolve. Mood is the battleground now.",
          "<b>Months 2–6</b>: PAWS (post-acute withdrawal) — waves of low mood, craving, poor sleep. They pass. Nearly everyone who stays stopped feels substantially normal by month 3–6.",
          "<b>The exception rule</b>: benzo and GHB/GBL withdrawal can kill — never cold-turkey daily use."]),
   ("h2","Pick your substance"),
   ("table",[["Substance","Peak misery","Feel-better point"],
     ["Heroin/fentanyl","Day 2–4","~1 week physical; months of PAWS"],
     ["Cocaine","Day 1–3 (crash)","Weeks for mood"],
     ["Meth","Week 1–2","1–3 months"],
     ["MDMA","Day 1–3 (comedown)","1–2 weeks"],
     ["Xanax/benzos","Week 2–3 of a taper","Months; must be tapered"],
     ["GHB/GBL (daily)","Day 1–3 — MEDICAL EMERGENCY","Weeks, hospital-supervised"],
     ["Ketamine","Days 1–7 mild","Weeks; bladder heals for months"]]),
   ("callout",("amber","The relapse rule that saves lives","Tolerance drops fast. After even a week clean, your old dose can kill you. If you slip, treat it like your first time — and never use alone.")),
  ],
  links=["quit/heroin","quit/fentanyl","quit/cocaine","quit/meth","quit/mdma","quit/alprazolam","quit/ketamine","quit/ghb"]),
]

TOPICS += [
 dict(slug="cocaine-nasal-spray", tag="Important", title="Cocaine Nasal Spray: what it actually is, and why it's more dangerous than lines", date="2026-09-16", read="7 min",
  image="https://plugreports.com/media/drugs/cocaine-nasal-spray.jpg",
  desc="The TikTok trend of 'coke nasal spray' — what pharmacists say is in it, why spraying hits harder and faster than snorting, and why the overdose math changes completely.",
  blocks=[
   ("p","If you've seen <b>cocaine nasal spray</b> on TikTok or in group chats, you're watching a genuine pharmaceutical product collide with recreational use — and the result is a <b>faster, more compulsive, and easier-to-overdose</b> version of an already dangerous drug. This guide breaks down what's actually in these sprays, why they behave differently in your body than lines, and the specific harms most users never hear about."),
   ("callout",("amber","First, a key distinction","There are <b>two different things</b> being called 'cocaine nasal spray' online. One is a legitimate pharmaceutical (Cocaine HCl solution, 4–10%, used in ENT surgery as a local anesthetic and vasoconstrictor). The other is <b>street cocaine dissolved in saline and put in a spray bottle</b> — homemade, unmeasured, and far more common on social media. This guide covers both, because the harms overlap but the dosing danger is far worse with the homemade version.")),
   ("h2","What is pharmaceutical cocaine nasal spray?"),
   ("p","Medical cocaine solution is a real, FDA-scheduled pharmaceutical (Chemistry, Manufacturing and Controls documented since the 1800s). It's a <b>clear solution of cocaine hydrochloride in sterile water</b>, typically 4% or 10% concentration, used by ear-nose-throat surgeons to numb the nasal cavity and control bleeding during procedures. It works because cocaine is both a <b>local anesthetic</b> (blocks sodium channels, numbing tissue on contact) and a <b>vasoconstrictor</b> (shrinks blood vessels, reducing bleeding)."),
   ("table",[["Component","Function"],
     ["Cocaine HCl (4–10%)","Anesthetic + vasoconstrictor"],
     ["Sterile water/saline","Solvent"],
     ["No preservatives","Single-use vials — cocaine solutions degrade and grow bacteria if stored"],
     ["No additives, no cuts","Pharmaceutical purity — the opposite of the street version"]]),
   ("callout",("red","Why you can't buy it legally","Cocaine is Schedule II in the US and controlled everywhere. Medical cocaine solution is restricted to hospital settings, dispensed in single-use vials with documentation. There is no legal retail version. Anything sold online as 'cocaine spray' is either diverted medical product (rare, traceable) or — vastly more common — <b>street cocaine in a repurposed bottle.</b>")),
   ("h2","The street version: what TikTok is actually showing"),
   ("p","The viral 'cocaine nasal spray' is almost always <b>powder cocaine dissolved in saline and put into a repurposed nasal spray bottle or neti pot</b>. The appeal is simple: no paraphernalia, no lines, no nose-drip, and a discreet format that looks like an innocent decongestant bottle. The problem is equally simple: <b>the dose is completely unknown and the delivery is far more efficient.</b>"),
   ("ul",["<b>Unknown concentration:</b> street cocaine purity already varies (50–90%+). Dissolving it in a spray bottle means each spray could deliver anywhere from near-nothing to a dangerous hit.",
          "<b>No sterile technique:</b> tap water, non-sterile saline, and reused bottles introduce bacteria directly into the nasal mucosa — the infection pathway behind most 'coke nose' complications.",
          "<b>The bottle lies:</b> a standard nasal spray bottle delivers ~100 mL per spray. Street versions vary wildly. Users assume 'one spray = one line' — it doesn't work that way.",
          "<b>Cuts carry through:</b> levamisole, boric acid, benzocaine — whatever the cocaine was cut with dissolves into the spray and enters your bloodstream."]),
   ("h2","Why spraying hits harder than snorting (the pharmacology)"),
   ("p","Snorting cocaine is actually an <b>inefficient</b> delivery method: powder sits on the nasal mucosa and absorbs slowly, with much of it swallowed or drip-loss. A fine spray <b>atomizes the solution into a mist</b> that coats a far larger surface area of the nasal cavity and absorbs faster. The result:"),
   ("table",[["Route","Onset","Peak","Bioavailability"],
     ["Snorted (lines)","3–5 min","15–30 min","~30–60%"],
     ["Nasal spray (medical or street)","1–3 min","10–20 min","~60–80%"],
     ["Smoked (crack)","5–10 sec","~1 min","~70–90%"]]),
   ("callout",("red","The compulsion trap","Faster onset means a harder, shorter rush — which the brain reads as 'more rewarding.' Users redose sooner and more frequently with sprays than with lines. The compulsion loop tightens. This is the same reason crack is more addictive than powder: it's not the molecule, it's the delivery speed. Nasal spray sits uncomfortably close to smoked cocaine in onset profile — but users treat it like snorting and overdose accordingly.")),
   ("h2","The specific harms of cocaine nasal spray"),
   ("stats",[("4–10%","medical cocaine concentration — never dispensed for recreation"),("60–80%","bioavailability via spray vs 30–60% snorted"),("1–3 min","onset — twice as fast as lines"),("0","sterile, measured street versions in existence")]),
   ("h3","1. Cardiovascular events — the leading killer"),
   ("p","Cocaine is a triple threat to the heart: it <b>constricts coronary arteries</b> (starving the heart muscle of oxygen), <b>raises blood pressure and heart rate</b> dramatically, and <b>promotes clotting</b>. Nasal spray delivers a faster, sharper spike than lines, pushing the cardiovascular system harder in a shorter window. Heart attacks and strokes occur even in young, healthy users — the faster the delivery, the sharper the spike, the higher the risk."),
   ("h3","2. Nasal and sinus destruction"),
   ("p","Cocaine is a vasoconstrictor — it cuts blood flow to the nasal tissue it touches. Repeated use causes: <b>septum perforation</b> (a hole in the cartilage between your nostrils), <b>saddle-nose deformity</b> (collapse of the nasal bridge), chronic sinusitis, and loss of smell. The spray format makes this <b>worse</b>: it coats the entire nasal cavity evenly, including areas lines never reach. Medical cocaine is used once, under supervision, and still carries warnings about mucosal damage. Daily spraying is a fast track to surgical reconstruction."),
   ("h3","3. The cuts and their own toxicities"),
   ("table",[["Common cocaine cut","Toxicity"],
     ["Levamisole (vet wormer)","Immune suppression, skin necrosis, agranulocytosis"],
     ["Boric acid","Seizures, multi-organ damage at high doses"],
     ["Benzocaine/lidocaine","Methemoglobinemia — blood stops carrying oxygen"],
     ["Fentanyl (rare, fatal)","Opioid overdose in a cocaine user with no tolerance — naloxone saves lives"]]),
   ("h3","4. The stimulant overdose pattern"),
   ("p","Cocaine overdose doesn't look like opioid overdose (no pinpoint pupils, no slow breathing). It looks like a <b>body in overdrive</b>:"),
   ("ul",["<b>Chest pain</b> — pressure, squeezing, radiating to arm or jaw (heart attack)",
          "<b>Racing, irregular heartbeat</b> — arrhythmia",
          "<b>Severe agitation, paranoia, hallucinations</b>",
          "<b>Overheating</b> — hot, sweaty skin, temperature climbing",
          "<b>Seizures</b>",
          "<b>Stroke symptoms</b> — facial droop, slurred speech, one-sided weakness"]),
   ("callout",("red","Cocaine overdose: what to do","1. <b>Call emergency services</b> — say 'chest pain' or 'seizure' or 'unresponsive.' Good Samaritan laws protect you. 2. <b>Cool the person</b> — strip outer layers, cool damp cloth. 3. <b>If they seize</b> — protect the head, nothing in the mouth, time the seizure. 4. <b>If unresponsive with slow breathing after possible fentanyl exposure</b> — give <b>naloxone</b> (it won't hurt if it's not opioids, and it saves lives if it is). 5. <b>Stay</b> — reassure, monitor, tell responders exactly what was taken.")),
   ("h2","How the high ends: the crash"),
   ("p","Cocaine burns through dopamine stores. When it clears (30–60 min after a spray hit), the crash is proportionate to the rush: <b>exhaustion, depression, irritability, intense craving</b>. Because sprays produce a sharper peak, the crash is sharper too — and the brain screams for another spray. This is the addiction mechanism working exactly as designed. There is no safe frequency; dependence can form within weeks of daily use."),
   ("h2","If you're going to use anyway (harm reduction)"),
   ("checklist",["<b>Never mix with Viagra/Cialis/Levitra</b> — cocaine + PDE5 inhibitors is the classic cardiac killer combo","<b>Never mix with alcohol</b> — forms cocaethylene, a metabolite more cardiotoxic than cocaine alone","Wait at least 20 minutes before considering more — the spray onset fools people into redosing too soon","Snort slowly OR use the lowest-concentration spray you can verify — but know there's no truly safe version","Have naloxone anyway (fentanyl contamination happens)","Tell someone what you're doing — the isolation kills more than the chemistry"]),
   ("related",["cocaine","mdma","topics:cocaine-purity-and-cuts","topics:spot-pressed-pills"])]),

 dict(slug="mdma-nasal-spray", tag="Important", title="MDMA Nasal Spray: the 'safer' myth, what's actually in it, and the serotonin danger nobody mentions", date="2026-09-16", read="7 min",
  image="https://plugreports.com/media/drugs/mdma-nasal-spray.jpg",
  desc="The TikTok trend of spraying MDMA instead of dropping pills — why it's not safer, what cuts ride along, and the serotonin syndrome risk that makes this route uniquely dangerous.",
  blocks=[
   ("p","MDMA nasal spray is being marketed on TikTok as a <b>'cleaner, safer, more precise'</b> way to take ecstasy. The logic sounds appealing: no pill press uncertainty, no waiting an hour, 'just a measured spray.' The reality is almost the opposite: <b>the dose is unknown, the cuts are dissolved in with it, the onset is dangerously fast for a serotonin-heavy drug, and the redose pattern it encourages is the exact mechanism behind MDMA's rare but real deaths.</b>"),
   ("callout",("amber","The core myth","Spraying MDMA doesn't make it safer — it makes it <b>faster</b>. And with MDMA, faster is not better. The drug's dangers scale with how hard and how fast it floods serotonin. A spray that hits in 5–10 minutes produces a sharper, more overwhelming come-up, a more brutal comedown, and a far stronger urge to redose. 'Measured' is also a lie when the source is a street powder dissolved in a kitchen bottle.")),
   ("h2","What is MDMA nasal spray, actually?"),
   ("p","There is <b>no pharmaceutical MDMA nasal spray</b> (unlike cocaine, which has a legitimate medical version). What exists online is entirely homemade: <b>MDMA powder or crushed pills dissolved in saline</b> and put into a spray bottle. Some sellers pre-make it; more commonly users DIY it from their own supply. The concentration is anyone's guess — street MDMA is already 30–90% pure, and dissolving it in an unmeasured volume of liquid removes even the rough visual gauge users rely on."),
   ("table",[["Claim from TikTok","Reality"],
     ["'It's measured — one spray, one dose'","Spray bottles deliver wildly variable volumes (50–150 mL per squeeze). No street bottle is calibrated. Your 'one spray' could be a quarter-dose or a double."],
     ["'No pill presses — pure MDMA'","You're dissolving the same powder that was in the pills — including every cut. The spray doesn't purify anything."],
     ["'Safer for your nose than snorting'","Spraying a caustic, acidic MDMA solution onto the full nasal mucosa is harder on tissue than a line that sits in one spot."],
     ["'Hits faster — more fun'","Faster onset = sharper serotonin spike = higher core temperature = higher neurotoxicity risk. The 'fun' is the danger."]]),
   ("h2","Why the nasal route changes MDMA's risk profile"),
   ("p","MDMA's harms are dose- and rate-dependent. The drug dumps serotonin, norepinephrine, and dopamine; the serotonin surge is what creates the euphoria and empathy — and it's also what drives <b>hyperthermia</b> (overheating), the primary killer in MDMA deaths. When you spray instead of swallow:"),
   ("ul",["<b>Onset collapses from 45–60 min (oral) to 5–15 min (nasal)</b> — the body has no time to ramp up temperature regulation",
          "<b>The peak is sharper</b> — a wall of serotonin instead of a wave, which is more neurotoxic",
          "<b>The comedown hits sooner and harder</b> — the brain's serotonin is depleted faster, the crash is deeper, and the craving to redose is stronger",
          "<b>You lose the body's natural brake:</b> swallowing means the drug passes through the stomach and liver first (first-pass metabolism slightly blunts the peak). Nasal spray bypasses that buffer entirely."]),
   ("callout",("red","The redose trap","MDMA's most dangerous pattern is <b>redosing because 'it's wearing off.'</b> When the first spray fades at 60–90 minutes, users spray again — but the drug is still in their system, still dumping serotonin, still raising temperature. Stacked doses are how the rare, fatal cases happen: serotonin syndrome, hyperthermia >40°C (104°F), and multi-organ failure. The rule that saves lives — <b>never redose on a comedown</b> — is precisely the rule nasal spray makes hardest to follow.")),
   ("h2","What's it cut with? (and why dissolving doesn't help)"),
   ("p","Spraying doesn't remove adulterants — it <b>delivers them straight into your bloodstream</b> alongside the MDMA. Current drug-checking data on 'MDMA' powder shows:"),
   ("table",[["What testing finds","Why it matters more in a spray"],
     ["Caffeine, sugar, inert filler","Variable strength per spray — the 'measured dose' is fiction"],
     ["Bath-salt cathinones (4-CMC, 3-CMC)","Longer, more compulsive stimulation — masks MDMA wearing off, drives redosing"],
     ["PMA / PMMA (the killer impersonators)","Slow onset — users spray more thinking it's weak, then overdose. PMA has killed hundreds of people who thought they took MDMA"],
     ["Ketamine, speed (amphetamine)","Unpredictable stacking of dissociation or extra stimulant load on the heart"]]),
   ("callout",("amber","Why PMA/PMMA is the nightmare scenario","PMA looks like weak MDMA for 2+ hours — users take (or spray) more, thinking it's bunk. Then it hits: extreme overheating, seizures, and a body temperature that spirals past 42°C (108°F). PMA kills by cooking people from the inside. It has been found in pills and powders sold as MDMA across Europe, Australia, and North America. <b>If a spray or pill takes 2 hours to work, it is NOT more MDMA — it may be PMA. Never redose a slow one.</b>")),
   ("h2","Serotonin syndrome: the overdose that looks like a 'bad trip'"),
   ("p","MDMA overdose is rarely a quiet collapse like opioids. It's a body and mind in catastrophic overdrive — and the most dangerous form is <b>serotonin syndrome</b>, which can look like a panic attack or a bad trip until it's too late:"),
   ("ul",["<b>Agitation, confusion, hallucinations</b> — beyond normal MDMA weirdness",
          "<b>Rapid heart rate, high blood pressure</b>",
          "<b>High fever</b> — >38.5°C (101°F) and climbing is the red flag",
          "<b>Muscle rigidity, jerky movements</b> — legs that won't stay still, jaw clenching beyond the normal gurn",
          "<b>Sweating, diarrhea</b>",
          "<b>Seizures</b> in severe cases"]),
   ("callout",("red","MDMA overdose: what to do","1. <b>Call emergency services immediately.</b> Say 'possible drug overdose, high fever, confusion.' Good Samaritan laws protect you. 2. <b>Active cooling is everything</b> — strip layers, fan them, cool damp cloths on neck/groin/armpits. MDMA kills by heat. 3. <b>No more fluids than they can comfortably drink</b> — MDMA can also cause dangerous water intoxication (hyponatremia); sips, not gulps. 4. If they're unconscious but breathing, recovery position. 5. <b>Tell responders it was MDMA</b> — they can treat serotonin syndrome and hyperthermia, but only if they know. Time matters: cooling in the first 30 minutes changes outcomes.")),
   ("h2","The comedown: why spray users crash hardest"),
   ("p","MDMA depletes serotonin. Oral users crash at hour 4–6; nasal users, because the peak came faster, crash at hour 2–4 — and the brain reads the sudden emptiness as an emergency. The Tuesday blues become the 'same-night despair.' Repeated rapid-cycle use (the spray pattern) accelerates the long-term damage: <b>memory problems, depression, anxiety</b> that can persist for months. The brain needs 1–3 months between rolls to rebuild serotonin function — spraying weekly is how people burn out at 22."),
   ("h2","If you're going to use anyway (harm reduction)"),
   ("checklist",["<b>Reagent test the powder FIRST</b> (Marquis/Mecke) — a spray made from PMA is a loaded gun","Never redose on a comedown — wait a full 90 minutes minimum, and honestly, don't at all","Dose low: a true 75–100 mg oral is the safety ceiling for most people; sprays make it impossible to know","Cool down proactively — rest in shade, sip electrolyte water (not more than ~500 mL/hour)","Never mix with antidepressants (SSRI/SNRI/MAOI) — serotonin syndrome risk multiplies","Never mix with alcohol — dehydration + overheating + impaired judgment","Have a sober friend who knows what you took — and have naloxone anyway (contamination happens)","If a spray/pill takes 2 hours to work, assume it's PMA — do NOT take more"]),
   ("related",["mdma","xtc-pills","topics:spot-pressed-pills","news:high-dose-ecstasy-warning","quit:mdma"])]),
]

TOPICS += [
 dict(slug="gas-station-drugs", title="Gas Station Drugs: the 'legal highs' sold next to the energy drinks", date="2026-09-17", read="8 min",
  image="",
  desc="Tianeptine, kratom, phenibut, Delta-8 — the unregulated 'dietary supplements' at gas stations and vape shops that carry opioid-level addiction and real death tolls.",
  markdown="""## The new dealer is a gas station

No ID checks beyond the register. No prescription. No dealer. The fastest-growing addiction market in America sits between the energy drinks and the lottery tickets: **tianeptine, kratom, phenibut, Delta-8 and kava** — sold as 'dietary supplements', 'mood enhancers' and 'hemp products'.

The word 'legal' does the marketing. None of these products passed a safety review. Several are actively warned against by the FDA. And at least one behaves like heroin.

## The lineup: what's actually on the shelf

| Product | Sold as | What it really is | The catch |
|---|---|---|---|
| **Tianeptine** (ZaZa, Neptune's Fix) | 'Dietary supplement' | An opioid — gas station heroin | Full opioid addiction + withdrawal; FDA links it to coma and death |
| **Kratom** | 'Botanical supplement' | Plant opioid (mitragynine) | Dependence, seizures, liver damage; contaminated batches |
| **Phenibut** | 'Nootropic' | GABA drug — Russian prescription anxiolytic | Dependence in 2–3 weeks; withdrawal can include psychosis and seizures |
| **Delta-8 / HHC / THC-O** | 'Hemp-derived' | Psychoactive cannabinoids | Solvent residues, unknown potency; THC-O is federally Schedule I |
| **Kava** | 'Relaxation tea' | Liver-toxic sedative | Banned or restricted in several countries for liver injury |

::: danger The tianeptine warning
The FDA has specifically warned about tianeptine (sold as ZaZa, Tiana, Neptune's Fix) after reports of **addiction, overdoses, and death** — including a 2024 New Jersey cluster where Neptune's Fix was contaminated with synthetic cannabinoids. It produces opioid-type withdrawal: cold sweats, muscle cramps, insomnia, diarrhea. If someone who uses it heavily stops suddenly, they can become violently ill — like heroin withdrawal, next to a highway.
:::

## Why 'legal' is the whole scam

1. **The supplement loophole.** Anything sold as a 'supplement' skips FDA approval. The burden is on the FDA to prove harm AFTER people get hurt.
2. **The hemp loophole.** The 2018 Farm Act legalized hemp, and chemists responded by converting CBD into Delta-8, HHC and THC-O — psychoactive drugs that never existed in nature.
3. **State patchwork.** Tianeptine is banned in a dozen states and legal next door. The same bottle is 'heroin' in Alabama and 'supplement' in Mississippi.
4. **No testing.** No batch purity checks, no dosing standards, no childproofing. Gas station shelves are the least regulated pharmacy on earth.

## The overdose picture (it's opioid-shaped)

- **Tianeptine & kratom overdoses look like opioid overdoses**: pinpoint pupils, slow breathing, unresponsiveness. **Give naloxone** — it works on opioid receptors.
- **Phenibut overdose**: extreme sedation, slow breathing — dangerous with alcohol. Naloxone does NOT reverse it; call emergency services.
- **Kratom seizures** happen even without overdose-level doses.

::: amber What parents should actually do
- Know the brand names: ZaZa, Tiana, Neptune's Fix, OPMS, Vivazen — these aren't vitamins.
- The gas station/vape shop habit shift (going daily, money disappearing) is the red flag — not a specific product.
- If someone is dependent on tianeptine or kratom: stopping cold turkey causes real withdrawal. A doctor can taper safely, and it's nothing to be ashamed of — it's an opioid dependence, acquired at a convenience store.
:::

## If someone is overdosing right now

1. Call emergency services — say 'possible opioid overdose'
2. Give **naloxone** if you have it (it works on tianeptine and kratom)
3. Stay — they can re-sedate
4. Tell responders exactly what was taken — the bottle helps

Full profiles with effects, risks and street prices for each product are linked below. Know the shelf before someone you love shops it.""",
  drugsInvolved=["tianeptine","kratom","phenibut","delta-8-thc","kava-kava"],
  related=["topics:inhalants-youth","tianeptine","kratom","pharmacies","topics:talk-to-your-kid"]),

 dict(slug="inhalants-youth", title="Inhalants: the cheap, legal drugs quietly damaging young brains", date="2026-09-17", read="7 min",
  image="",
  desc="Whippets, Galaxy Gas, air duster, glue — the substances most likely to be a young person's first 'drug experience', and the ones most likely to kill them on the first try.",
  markdown="""## The first drug most kids try

Before weed, before pills, before anything illegal — there are **inhalants**. Whipped cream chargers in the kitchen drawer. Keyboard duster under the desk. Glue in the craft box. They cost pocket money, require no ID, no dealer, and no paraphernalia anyone would recognize.

That accessibility is exactly the danger. Inhalant use peaks at **age 14–15** — younger than any other drug class.

## The three families

| Type | Examples | What it does | Signature harm |
|---|---|---|---|
| **Nitrous** | Whippets, Galaxy Gas, balloons | 30–60s euphoria | Destroys vitamin B12 → nerve damage, 'drop foot' |
| **Aerosols/dusters** | Air duster, Freon, deodorant | 10–30s dissociation | **Sudden Sniffing Death** — heart stops on first use |
| **Solvents/glue** | Model glue, thinners, petrol | 10–15 min euphoria | Permanent brain damage, oral cancer pathway |

::: danger Sudden Sniffing Death
Duster gases (difluoroethane) and butane sensitize the heart to adrenaline. A user who gets startled, chased, or even just stands up fast can trigger **instant fatal cardiac arrhythmia**. It has killed first-time users with a single can. There is no warning, no gradual overdose, and naloxone does nothing — it's a heart-stopping event, and CPR rarely saves it.
:::

## The nitrous wave nobody is watching

Galaxy Gas — flavored, pastel, 640-gram canisters — has turned whippets from a niche rave relic into a **teen social media trend**. The harm is quiet and progressive:

- Nitrous **chemically inactivates vitamin B12**, which your nerves need to work
- Heavy users develop numb feet and hands, then **wobbly walking, then an inability to walk at all** ('drop foot')
- Catch it early, quit, and B12 injections can reverse it. Keep using, and nerve damage can be **permanent**
- Teens are presenting to neurology clinics unable to walk — and doctors initially search for MS or tumors before asking about whippets

::: amber What parents should look for
- Small silver canisters (not CO2 cartridges — **8g nitrous chargers**), balloons lying around, or large catering canisters in a teenager's room
- The 'cracker' dispenser tools sold online
- B12-deficiency symptoms in a healthy teen: tingling hands, leg weakness, unsteady walking — take it seriously and ask the question
:::

## Solvents: the permanent price

Chronic glue/petrol sniffing dissolves the brain's white matter (myelin). The result is a dementia-like syndrome — tremor, unsteady gait, slurred speech — **in teenagers**, sometimes irreversible. The tell-tale 'huffer's rash' (red rash around the mouth and nose) is an obvious sign.

## If someone collapses while inhaling

1. **Call emergency services immediately** — say 'collapsed, possible inhalant'
2. Remove them from the gas source; fresh air
3. If not breathing: start CPR and continue until help arrives
4. **Do not** give anything by mouth; if they vomit, roll them on their side
5. A victim of sudden sniffing death can sometimes be revived with **immediate, continuous CPR and a defibrillator** — minutes matter

The gas station and kitchen drawer are the real supply chain. Every product in this family has a full harm-reduction profile below.""",
  drugsInvolved=["nitrous-oxide","whippets","nangs-galaxy-gas","air-duster","glue-sniffing","gasoline-huffing"],
  related=["nitrous-oxide","nangs-galaxy-gas","air-duster","topics:gas-station-drugs","topics:talk-to-your-kid"]),

 dict(slug="beauty-injection-dangers", title="Black-Market Filler & Botox: how a beauty appointment can blind you", date="2026-09-17", read="8 min",
  tag="Important",
  image="",
  desc="Vascular occlusion, blindness, pumping-party deaths — the unregulated cosmetic injection industry and the red flags that separate a licensed clinic from a kitchen-table injector.",
  markdown="""## The prettiest drug problem in the world

An estimated **73% of FDA adverse-event reports for dermal fillers** come from unlicensed or non-medical settings — hotel rooms, homes, 'Botox parties'. A syringe of hyaluronic acid is a medical device. In the wrong hands it becomes a weapon: **it can block an artery, kill skin, or take someone's eyesight in under an hour.**

And the market is getting younger. Lip filler at 17, 'baby Botox' at 22, jawline filler bought with birthday money — normalized by TikTok, supplied by gray-market websites that sell injector kits to anyone with a card.

## The five procedures doing the damage

| Procedure | Sold as | The specific danger |
|---|---|---|
| **Lip/cheek filler** | 15-min lunchtime tweak | Vascular occlusion → skin death; **blindness** if filler reaches the eye artery |
| **Nose (non-surgical rhino)** | Cheaper alternative to surgery | Highest blindness risk zone — dangerous even with licensed injectors |
| **Black-market silicone shots** | 'Pumping parties', butt shots | Industrial silicone → embolism deaths, cement-like tissue, unremovable |
| **Counterfeit Botox** | Party injections, 'budget units' | Overdosed toxin → drooping face, swallowing/breathing difficulty |
| **Tanning injections (Melanotan)** | 'Tan jabs' online | Mole darkening, new nevi, melanoma-monitoring nightmare |

::: danger Blindness from filler is real and documented
Filler injected into a facial artery can travel backwards into the **ophthalmic artery** and cut off blood to the retina. There are 300+ documented cases of vision loss from dermal filler, most from the nose, forehead, and glabella (between the brows). It can happen to excellent injectors. The difference between a bad outcome and a catastrophe is **one thing: hyaluronidase on hand and someone trained to use it** — which unlicensed injectors never have.
:::

## The red flags — how to spot an unlicensed injector

1. **No medical prescriber** — legitimate filler requires a licensed prescriber on site (or supervising)
2. **Price too good** — a $150 'full lip kit' clinic is buying counterfeit stock
3. **No hyaluronidase in the room** — ask. Watch the face change
4. **Venue is a home, hotel, or 'party'** — sterility, emergency equipment, and accountability don't exist there
5. **They can't name the product batch** — legit clinics show you the sealed box and batch number before opening it
6. **Selling DIY kits online** — a syringe is not a toy; the 'do it at home' marketing targets under-25s specifically

## The pumping-party horror

Black-market **industrial silicone** injected into hips and buttocks at 'pumping parties' has a body count. Unlike dissolvable HA filler, silicone migrates through tissue into lungs and kidneys, causes granulomas that harden like cement, and **cannot be fully removed** — victims undergo years of reconstructive surgery. Multiple unlicensed injectors have been prosecuted for manslaughter and murder after silicone embolism deaths.

::: amber If you or a friend had filler — the warning signs
- Blanching (white/pale) or lacy-purple skin near the injection site — possible occlusion. This is a **minutes-to-hours emergency**
- Severe pain during or after injection — not normal
- Any vision change — partial loss, curtain across vision, blurring — go to an ER immediately and say 'dermal filler vascular occlusion'
- Hours matter: occlusions treated fast with hyaluronidase save tissue; treated late cost faces and eyes
:::

## The honest bottom line

Licensed medical aesthetics is a real, generally safe industry. The danger zone is everything around it: the gray market, the parties, the DIY kits, the 18-year-olds injecting themselves from YouTube tutorials. Check the register (in the US: state medical board license lookup; UK: Save Face; AUS: AHPRA), verify the product, and walk away from any kitchen table.

Every substance and procedure in this space has a full profile below — share them with anyone considering their first tweak.""",
  drugsInvolved=["botox","dermal-fillers","silicone-injections","hyaluronidase","melanotan-2-beauty","lipolysis-injections"],
  related=["dermal-fillers","botox","silicone-injections","pharmacies","topics:talk-to-your-kid"]),

 dict(slug="nitrous-nerve-damage", title="Whippets & Galaxy Gas: the 'harmless' party drug leaving teens unable to walk", date="2026-09-17", read="6 min",
  tag="Important",
  image="",
  desc="Vitamin B12 destruction, drop foot, wheelchairs — the quiet neurological epidemic behind the flavored-canister trend, and why 'legal' has never meant safe.",
  markdown="""## It looks like candy. It paralyzes like a disease.

Flavored canisters in pastel colors. 'Whipped cream chargers' that are never near a kitchen. A 30-second giggle that costs the user a vitamin their nerves need to survive.

**Nitrous oxide — whippets, Galaxy Gas, hippy crack — is in the middle of a youth wave.** And a growing number of its heavy young users are showing up at neurology clinics unable to walk.

## The mechanism: how laughing gas cripples nerves

1. Every inhale inactivates **vitamin B12** — the gas oxidizes the cobalt core, permanently disabling the molecule
2. Your nerves need B12 to build and repair **myelin** — the insulation around nerve fibers
3. Without it, the longest nerves fail first: **feet, legs, hands**
4. The result is **myeloneuropathy**: numbness, burning, pins-and-needles, then weakness

::: danger The progressive pattern
**Weeks of heavy use:** tingling feet and fingertips, wobbly balance.
**Months:** legs give way on stairs, 'drop foot' (toes drag), falls.
**Untreated:** wheelchair. Some damage is reversible with B12 injections and total abstinence — but recovery takes months, and **heavy, prolonged use can leave permanent deficits**. Users in their late teens and twenties have needed walking aids for a year or more.
:::

## Why nobody diagnoses it

A 19-year-old with leg weakness gets scanned for MS, tumors, and Guillain-Barré before anyone asks about party drugs. The tell-tale sign doctors eventually find: **B12 levels can test normal** — the vitamin is present but chemically switched off. Only the neurological picture and an honest history reveal it.

## The Galaxy Gas multiplier

- Large catering canisters (500–640g) cost a fraction of per-charger prices — **heavy daily use became affordable**
- Dessert flavors and pastel branding are aimed squarely at the under-25 market
- Sessions involve dozens of balloons in a row — the dose pattern that destroys B12 fastest
- 'Oxygen deprivation' blackouts mid-session compound the neurological hit

## The other harms on the list

- **Sudden death** — 100% nitrous displaces oxygen; users who pass out with a mask or balloon still attached can suffocate
- **Frostbite** — direct gas contact freezes lips, tongue, and throat tissue
- **B12-deficiency anemia** — exhaustion, breathlessness, pale skin
- **Psychological dependence** — the 60-second escape is highly re-doseable; daily use creeps up fast

## What actual protection looks like

- **Total abstinence** is the only guaranteed protection
- If use is happening anyway: B12 supplementation helps but does NOT make heavy use safe — the gas destroys B12 faster than any pill can replace it
- Any tingling, numbness, or leg weakness after use = **stop immediately and see a doctor, saying exactly what you've used** — early treatment with B12 injections reverses most cases
- Parents: silver chargers, cracked-open canisters, and balloons in a teen's space are worth a calm conversation, not a search-and-destroy

Legal. Cheap. Flavored. Paralyzing. The full picture — including whippets, Galaxy Gas, and poppers — is in the profiles below.""",
  drugsInvolved=["nitrous-oxide","whippets","nangs-galaxy-gas"],
  related=["nitrous-oxide","nangs-galaxy-gas","topics:inhalants-youth","topics:talk-to-your-kid","hotlines"]),
]

TOPICS += [
 dict(slug="roxy-vs-oxycodone-vs-percocet", image="https://plugreports.com/media/drugs/oxycodone-apap.png", title="Roxicodone vs Oxycodone vs Percocet: what's actually the difference?", date="2026-09-17", read="5 min",
  desc="Roxicodone, OxyContin, Percocet, Roxicet — the oxycodone brand soup explained: which contain the same drug, which add paracetamol, and why the difference can be dangerous.",
  markdown="""## The short answer

**Roxicodone, OxyContin and Percocet all contain the same core drug: oxycodone.** The differences are the release mechanism and the extra ingredients — and one of those extras is the one that quietly destroys livers.

| Brand | Contains | Release | What it means |
|---|---|---|---|
| **Roxicodone** | Oxycodone only | Immediate (IR) | Fast onset, ~4–6 h relief; small blue 30 mg 'blues' are the most-counterfeited pill in the US |
| **Oxycodone** (generic) | Oxycodone only | IR or ER depending on tablet | Same molecule as Roxicodone |
| **OxyContin** | Oxycodone only | Extended (ER, 12 h) | Long-acting pain relief; crushing it defeats the mechanism and is how most overdoses happen |
| **Percocet / Roxicet / Endocet** | Oxycodone + **paracetamol (APAP)** | Immediate | Same opioid high + a hidden liver toxin — the dangerous one |
| **Tylox** | Oxycodone + APAP | Immediate | Older Percocet equivalent |

## Why the APAP combination matters

Percocet-type products add paracetamol (acetaminophen) to the oxycodone. The paracetamol adds **zero** pain relief or high at recreational doses — it exists to deter abuse, because exceeding 4 g/day damages the liver.

That deterrence becomes a trap: someone taking several 'Percocet 325' tablets on top of other paracetamol-containing products (cold remedies, Tylenol) can blow past the safe limit **while chasing only the oxycodone**. Liver failure from APAP is the silent killer in this family — the opioid is what you feel, the paracetamol is what kills you days later.

::: danger The counterfeit's cruel twist
The DEA's testing has found most counterfeit 'Roxicodone 30s' (blue, 'M30' imprint) contain fentanyl, not oxycodone. A user who thinks they know their dose takes what is actually an unknown fentanyl dose. Naloxone reverses it — but only if someone calls 911. Never use alone: 1-800-484-3731 (US).
:::

## Is Roxicodone stronger than Percocet?

No — at equal oxycodone doses, the opioid effect is identical. What differs:

- **Roxicodone hits faster** (no waiting, no APAP), which is why it's preferred on the street and diverted harder
- **Percocet feels 'milder'** only because users typically take lower oxycodone doses per tablet (5–10 mg vs 30 mg)

## Quick safety facts

- All are **Schedule II** — same legal class, same felony exposure
- All cause the **same dependence and withdrawal** — oxycodone is oxycodone
- Mixing any of them with **alcohol or benzodiazepines multiplies the respiratory-depression risk**
- Overdose signs are identical: pinpoint pupils, slow breathing, blue lips — **naloxone works on all of them**

Full profiles with street prices and overdose protocols for each product are linked below.""",
  drugsInvolved=["oxycodone","oxycontin","oxycodone-apap","hydrocodone"],
  related=["oxycodone","oxycontin","oxycodone-apap","topics:spot-pressed-pills","pharmacies"]),

 dict(slug="mdma-overdose", image="https://plugreports.com/media/drugs/xtc-pills.jpeg", title="Can you overdose on MDMA? The signs, the 'lethal dose' myth, and what to do", date="2026-09-17", read="6 min",
  desc="People overdose on MDMA every festival season — usually not from one giant dose but from heat, water imbalance, and stacked doses. The actual danger signs and the response protocol.",
  markdown="""## Yes — and it usually doesn't look like an opioid overdose

MDMA deaths are rare relative to use, but they follow a predictable pattern every summer: overheating, water imbalance, and stacked doses. Unlike fentanyl, MDMA rarely just 'stops your breathing' — it **cooks you from the inside** and floods your brain with serotonin.

## The real danger signs

| Sign | What's happening |
|---|---|
| **Body temperature climbing past 40°C / 104°F** | The core killer — serotonin-driven hyperthermia |
| **Confusion, agitation, weird behavior** | Serotonin toxicity — beyond normal MDMA euphoria |
| **Rigid muscles, jaw clenching that won't stop, shivering** | Classic serotonin syndrome signs |
| **Vomiting + headache** | Possible hyponatremia (water intoxication) |
| **Collapse, seizures** | Late stage — emergency |

::: danger The water trap
MDMA makes you hot, thirsty, and water-retaining (it triggers ADH). Drink *too much* water — several liters — and your blood sodium crashes. The result, hyponatremia, kills festival-goers who did everything 'right' except the water math. **Sip electrolyte drinks, don't chug water. Roughly 500 mL per hour max, more if dancing hard in heat — and eat something salty.**
:::

## The 'lethal dose' myth

There is no reliable single lethal dose number — it varies wildly by person, temperature, activity, and what's actually in the pill. What the data shows:

- **Deaths cluster at high doses (200 mg+ in a session), hot environments, and redosing**
- The risk compounds: dose 1 + heat + dose 2 at 2 AM is the classic fatal pattern
- Pills sold as MDMA sometimes contain **PMA/PMMA** — slower to hit, deadly when redosed. A pill that takes 2+ hours to work is a red flag, not a weak pill

## What to do in an MDMA emergency

1. **Call emergency services** — say 'possible drug overdose, high fever, confused.' Good Samaritan protections apply in most places
2. **Cool them actively**: shade, strip layers, fan, cool damp cloths on neck/groin/armpits. Heat is what kills
3. **Sips of electrolyte drink only** — not gulps of water
4. If seizing: protect the head, nothing in the mouth, time it
5. **Tell responders it was MDMA** — they can treat serotonin syndrome and hyperthermia, but only if they know

## The prevention rules that actually work

- Test your drugs (reagent kits distinguish MDMA from PMA for ~$20)
- One dose, then hands off: **never redose on a comedown**
- Rest and cool down between dances; the danger is heat + duration, not just the pill
- Tell your friends what you took and when — the person who can call for help at 3 AM is your real safety equipment

The comedown, redose mechanics, and full harm-reduction profile are linked below.""",
  drugsInvolved=["mdma","xtc-pills","molly"],
  related=["mdma","xtc-pills","topics:mdma-nasal-spray","quit:mdma","news:high-dose-ecstasy-warning"]),

 dict(slug="pregabalin-safety-faq", image="https://plugreports.com/media/drugs/pregabalin.jpg", title="Pregabalin (Lyrica) safety: overdose, controlled status, and the questions everyone asks", date="2026-09-17", read="5 min",
  desc="Is Lyrica a narcotic? Can you overdose on pregabalin? Is it a controlled substance? The straight answers to the most-searched pregabalin safety questions.",
  markdown="""## Is pregabalin (Lyrica) a narcotic?

**No — but it's a controlled drug with opioid-like dangers.** Pregabalin is a gabapentinoid (a calcium-channel modulator), not an opioid. But it produces calm, euphoria at high doses, and physical dependence — and mixing it with opioids **multiplies respiratory depression**. About a third of opioid overdoses now involve a gabapentinoid. UK regulators moved it to Class C in 2019; the US made it Schedule V; prescription-only essentially everywhere.

## Is pregabalin a controlled substance?

| Country | Status |
|---|---|
| USA | Schedule V (since 2019) |
| UK | Class C under the Misuse of Drugs Act 1971 |
| EU | Prescription-only; abuse monitoring in place |
| Australia | Schedule 4 |

## Can you overdose on pregabalin?

**Yes — alone it's rarely fatal, but with opioids or benzos it's a genuine killer.**

- **Pregabalin alone at high doses**: extreme sedation, dizziness, slurred speech, confusion. Deaths from pregabalin alone are rare because it doesn't strongly suppress breathing on its own
- **Pregabalin + opioids (methadone, oxycodone, heroin, tianeptine)**: the combination causes the breathing suppression that kills. This is the documented, rising death pattern — pregabalin is detectable in a large share of gabapentinoid-involved overdoses
- **Pregabalin + benzos or alcohol**: additive sedation; falls, aspiration, and respiratory depression

::: danger Signs someone took too much
Extreme drowsiness, unsteady walking, slurred speech, confusion. If they've also taken opioids and breathing slows or they become unresponsive — **call emergency services and give naloxone** (it won't reverse pregabalin, but it reverses the opioid half of the combination, which is usually what's stopping the breathing).
:::

## What happens if you take too much pregabalin regularly?

- **Dependence within weeks** of daily high-dose use; withdrawal causes insomnia, anxiety, nausea, sweating, and in heavy users seizures
- Tolerance climbs fast — recreational doses escalate from 300 mg into gram territory
- It's massively diverted: prison economies run on it, and 'legal high' sellers market it as a benzo alternative

## Pregabalin overdose treatment — what hospitals do

There's no specific antidote. Treatment is supportive: airway and breathing support, IV fluids, monitoring. If opioids are involved, **naloxone is given**. Doctors will also check kidney function — pregabalin is cleared renally, and kidney impairment makes accumulation worse.

## The practical rules

- Never mix with opioids, benzos, or alcohol
- If prescribed it, take it exactly as prescribed — dependence creeps at supratherapeutic doses
- If dependent and wanting to stop: taper with a doctor. Stopping abruptly after heavy use can cause seizures
- If someone is unresponsive and may have mixed it with opioids: naloxone + 911, always

Full profile with street prices and dependence data linked below.""",
  drugsInvolved=["pregabalin"],
  related=["pregabalin","gabapentin" if False else "zopiclone","topics:gas-station-drugs","topics:what-actually-happens-when-you-quit","pharmacies"]),

 dict(slug="vyvanse-safety-faq", image="https://plugreports.com/media/drugs/vyvanse.png", title="Vyvanse (lisdexamfetamine) safety: overdose signs, abuse questions, and what it does to your liver", date="2026-09-17", read="5 min",
  desc="Can you overdose on Vyvanse? Is lisdexamfetamine the same as Adderall? Can you smoke or snort it? The searched questions, answered straight.",
  markdown="""## What is lisdexamfetamine, exactly?

**Vyvanse is a prodrug of dextroamphetamine.** The capsule contains lisdexamfetamine, which does nothing until your body converts it into dextroamphetamine — the same active stimulant as Dexedrine and half of Adderall. That's why it lasts 10–12 hours and why it feels 'smoother': the conversion rate-limits the peak.

## Can you overdose on Vyvanse?

**Yes.** An amphetamine overdose is a cardiac and neurological event, not a quiet shutdown:

| Sign | Why |
|---|---|
| Racing, irregular heartbeat, chest pain | Cardiovascular strain — the main killer |
| Extreme agitation, paranoia, hallucinations | Stimulant psychosis |
| Overheating, sweating | Amphetamines raise body temperature |
| Tremors, seizures | CNS toxicity at high doses |
| Dangerously high blood pressure | Stroke risk |

Single massive doses (far above prescription) are the acute overdose pattern; chronic abuse causes the same damage more slowly. If someone has chest pain or a racing irregular heart after taking it: **emergency services now** — say 'possible stimulant overdose.'

::: amber Can you smoke or snort Vyvanse?
Snorting or injecting lisdexamfetamine is mostly pointless — it must go through the liver to become active, so insufflation doesn't speed it up much and burns for little gain. That prodrug design is precisely why it was marketed as abuse-deterrent. But 'harder to abuse' is not 'safe': people still take huge oral doses, binge it, and develop dependence. The deterrent bends the route, not the risk.
:::

## Is Vyvanse the same as Adderall?

No — related but different:

- **Adderall** = mixed amphetamine salts (dextro- + levoamphetamine), starts working in ~30 min, lasts 4–6 h (IR)
- **Vyvanse** = lisdexamfetamine only, converts to pure dextroamphetamine, ~1–2 h to full effect, lasts 10–12 h
- Same class, same Schedule II, same cardiovascular and dependence risks — different duration and slightly different feel

## Does Vyvanse damage your liver?

**The liver damage risk is low at prescribed doses** — the drug is converted in red blood cells, not primarily metabolized by liver enzymes. The real liver conversation is different:

- Vyvanse can mildly raise liver enzymes at high doses; clinically significant liver injury is rare
- It's **not the liver you should worry about — it's the heart**: BP elevation, heart rate, and in people with structural heart defects, real danger
- Combining with alcohol stresses both the heart and judgment; the combo also masks drunkenness

## Dependence and the crash

Daily use builds tolerance and dependence like any amphetamine. The Vyvanse crash: 1–2 days of exhaustion, low mood, and intense craving after heavy use. Withdrawal itself is miserable but rarely dangerous — the danger is the relapse dose, taken at old tolerance after a break. If you've stopped for a week, your tolerance dropped; an old dose can be a new overdose.

Full profile and the day-by-day stimulant quitting timeline are linked below.""",
  drugsInvolved=["vyvanse","adderall","dexedrine"],
  related=["vyvanse","adderall","adderall-xr","dexedrine","quit:meth","topics:talk-to-your-kid"]),
]

TOPICS += [
 dict(slug="europe-drug-checking", title="Drug checking in Europe: where to test your drugs before you take them", date="2026-09-18", read="6 min",
  desc="The Netherlands, Austria, Switzerland, Spain and the UK run world-leading drug-checking services — free, anonymous, no questions asked. How each works and how to use them.",
  markdown="""## The harm-reduction superpower hiding in Europe

While most of the world debates whether drug checking 'encourages use', Europe has quietly built the world's most advanced testing infrastructure — and the results are undeniable: festivals with checking services have measurably fewer hospitalizations, and early-warning networks catch dangerous batches (like PMA masquerading as MDMA) before they kill dozens.

If you're in Europe, **testing is free, anonymous, and legal** in most countries. Here's where:

| Country | Service | How it works |
|---|---|---|
| **Netherlands** | DIMS (Jellinek / GGZ) | The world's oldest programme (since 1992). Drop samples at ~30 locations nationwide; results within days; national trend monitoring |
| **Austria** | CheckIt! | Lab analysis of pills/powders; free, anonymous; strong festival presence |
| **Switzerland** | DIZ / SAJE | Canton-based testing in Zurich, Bern and others — free and anonymous |
| **Spain** | Energy Control | Private lab testing (small fee) + festival services; publishes market data |
| **UK** | The Loop | Nonprofit, festival + city-centre pop-ups (Bristol, Manchester); free results in ~10 min with a 15-min harm-reduction chat |
| **France** | PsychonautWiki-linked / CAARUD | Testing available via CAARUD centres in major cities |
| **Germany** | Drug checking varies by state (Berlin, NRW lead) | State-by-state; Berlin offers anonymous testing |

## What testing actually catches

- **PMA/PMMA sold as MDMA** — the slow-onset killers. Testing catches these reliably
- **Fentanyl in cocaine and benzos** — increasingly detected in EU supplies
- **Nitazenes in counterfeit oxycodone** — the new wave, 10–25× fentanyl strength
- **Wrong cathinones** — '4-MMC' that's actually 3-CMC, doses that are 2× the label

::: tip The 15-minute rule
The Loop's model is the gold standard: you hand over a sample, get lab-accurate results in about 10 minutes, then sit with a trained worker for a 15-minute harm-reduction conversation — no judgment, no police, no data kept. People who use checking services change their behavior: most say they'd take less, warn friends, or not take it at all.
:::

## Can't get to a service? The fallback layers

1. **Reagent kits** (Marquis, Mecke, Froehde — ~€20 online): distinguish MDMA from PMA, opioids from non-opioids. Not lab-grade, but a solid first filter
2. **Fentanyl test strips** (~€2 each): dissolve a crumb; one line = fentanyl present. Standard gear in North America, increasingly relevant in Europe
3. **Pill reports / warning networks**: national early-warning apps and forums aggregate batch alerts — check before a festival

## For travelers

European drug laws remain strict (see our sentencing pages), but **possession of a tiny testing sample is treated differently from possession for use in most of these countries** — the services exist precisely so the state knows what's in the supply. Never carry amounts beyond a test sample, and check local law if unsure.

Full profiles for the substances these services most often test — MDMA, ketamine, 2C-B, cathinones — are linked below.""",
  drugsInvolved=["mdma","ketamine","2c-b"],
  related=["topics:spot-pressed-pills","news:nitazenes-spreading-eu","mdma","xtc-pills","sentencing"]),

 dict(slug="thailand-cannabis-reversal", title="Thailand's cannabis reversal: what the 2025 re-criminalization means", date="2026-09-18", read="5 min",
  desc="Thailand went from jail for a joint to legal cannabis shops in 2022 — then flipped back in 2025. What the current law says, what tourists get wrong, and the penalties that haven't changed.",
  markdown="""## The fastest policy flip in cannabis history

**2022:** Thailand became the first Asian country to decriminalize cannabis — overnight, dispensaries opened on every corner of Bangkok and Chiang Mai, tourists lit up on Khao San Road, and the country became a global cannabis tourism destination.

**2025:** The government re-criminalized recreational cannabis, moving the plant back toward the narcotics list. Shops that built a business on the 2022 law faced closure; the 'Thailand weed vacation' era ended almost as quickly as it began.

## What the law says now

| Situation | Status |
|---|---|
| **Recreational use (smoking flower for fun)** | Moving back to ILLEGAL — re-criminalization framework passed 2025; enforcement resumed against public use and unlicensed sale |
| **Medical cannabis (prescription, registered products)** | Legal — the prescription pathway remains |
| **Possession of extracts/oils above 0.2% THC without authorization** | Illegal — concentrates never left the narcotics framework |
| **Import/export without license** | Illegal — treated as trafficking |
| **Methamphetamine (yaba), heroin — Category I drugs** | Never decriminalized: trafficking carries LIFE or DEATH |

::: danger What did NOT change
Everything about Category I narcotics. Thailand's harsh core regime — life imprisonment and the death penalty for trafficking yaba or heroin — was untouched by the cannabis experiment. Tourists caught with MDMA, cocaine, or 'party pills' face the same decades-long sentences they always have. The cannabis flip changed one thing; the rest of Thai drug law remains among Asia's toughest.
:::

## The tourist traps

1. **Assuming the dispensary era still applies.** Old blog posts and YouTube videos describe a legal landscape that no longer exists — check dates on anything you read
2. **Vape cartridges.** Cannabis vapes and e-cigarettes with liquid are treated more harshly than flower, and nicotine vaping is restricted
3. **Prescription medicines at the border.** Codeine, ADHD medication, benzos, and some antidepressants require a permit or doctor's letter — arriving without paperwork has landed travelers in detention
4. **Buying from strangers.** Undercover operations around tourist areas are routine; the seller walking free while the buyer is arrested is a documented pattern

## What happens if you're arrested

Thai drug process: detention, bail (possible but expensive for foreigners), long pre-trial periods, and sentencing under the Narcotics Act. Embassy help is limited — consular staff can visit and refer lawyers but cannot get you released. The one genuine protection is the same as everywhere: **don't put yourself in the system. Know the current law, which in Thailand now means assume cannabis is illegal again unless a doctor is involved.**

Our Thailand hotline and sentencing entries are linked below — and the cannabis profile covers what changed.""",
  drugsInvolved=["weed","thc-vapes"],
  related=["weed","thc-vapes","sentencing","hotlines","topics:europe-drug-checking"]),

 dict(slug="india-drug-law", title="Drug laws in India: the NDPS Act explained (what actually happens if you're caught)", date="2026-09-18", read="7 min",
  desc="India's Narcotic Drugs and Psychotropic Substances Act — the small vs commercial quantity system, why celebrity cases end in bail, and what an ordinary person should actually expect.",
  markdown="""## India's zero-tolerance law — with a quantity-based escape hatch

The **NDPS Act (1985)** is one of the world's strictest drug laws: no bail presumptions for trafficking, 10–20 year sentences for commercial quantities, and an entire chapter that applies whether you knew about the drugs or not (the law presumes guilt for certain offences — the accused must prove innocence).

But there's a crucial **three-tier quantity system** that decides everything:

| Tier | Definition | Typical outcome |
|---|---|---|
| **Small quantity** | Per-drug thresholds (e.g., 100 g cannabis, 1 g charas/hashish, 0.5 g cocaine, 250 mg MDMA) | 6 months – 1 year + fine; courts increasingly divert to counselling/de-addiction instead of jail |
| **Intermediate (more than small, less than commercial)** | Between the two thresholds | 10–20 years + fine of ₹1–2 lakh |
| **Commercial quantity** | e.g., 20 kg cannabis, 250 g charas, 100 g cocaine, 0.5 g* MDMA (*MDMA's commercial threshold is extremely low) | 10–20 years minimum, can extend to 30; repeat/large trafficking: death penalty possible |

## The celebrity paradox

The cases you read about — Rhea Chakraborty (2020, Sushant Singh Rajput case), Aryan Khan (2021, cruise ship raid) — both ended in **bail without conviction**, after weeks-to-months in custody. What those cases actually demonstrate:

- **Arrest and jail come first, bail comes later.** NDPS's Section 37 makes bail genuinely hard — courts must be satisfied the accused is not guilty (a trial-stage finding) before releasing
- **The process is the punishment.** Even when charges collapse, the months in custody, the media circus, and the legal bills are real
- **2024 amendments** streamlined some prosecutions and expanded treatment access — the system is slowly softening at the edges

::: danger The thresholds trap
India's commercial quantities are shockingly low — a few grams of MDMA or charis is 'commercial.' Someone carrying what a European would call a weekend supply can face a 10–20 year mandatory sentence. The law's harshness is not theoretical: over 90% of NDPS prisoners are undertrials, many for small quantities.
:::

## What actually happens if you're caught

1. **Arrest and seizure** — everything documented; even phone chats get examined
2. **Bail hearing** — Section 37: the court must find 'reasonable grounds' you're not guilty. First weeks are often spent in custody
3. **Charge sheet within 60–90 days** — delays beyond this can support bail
4. **Trial** — years-long; conviction rates for possession cases are lower than for trafficking
5. **If small quantity:** de-addiction treatment is increasingly ordered instead of prison

## For foreign travelers

- Prescription rules: some medicines legal in the West (strong painkillers, ADHD meds, certain cold remedies with codeine) are controlled — carry prescriptions and check the customs list
- Goa and Himachal are enforcement hotspots, not safe zones — tourist-season drives are routine
- The embassy can monitor but not rescue; undertrial periods are long

The subcontinent's quit timelines and the full sentencing table are linked below.""",
  drugsInvolved=["weed","mdma"],
  related=["sentencing","hotlines","weed","mdma","topics:what-actually-happens-when-you-quit"]),

 dict(slug="gulf-travel-drug-laws", title="Traveling to the Gulf? The drug laws that catch tourists and expats", date="2026-09-18", read="6 min",
  desc="UAE, Saudi Arabia, Qatar, Kuwait — prescription medicines that are routine at home can be controlled substances here. What to check before you fly, and what happens if you don't.",
  markdown="""## The highest-stakes packing decision you'll make

Gulf states run some of the world's strictest drug regimes — and they apply to **what's in your bloodstream, not just your bag**. Kuwait's December 2025 law explicitly criminalizes trace amounts in your body. The UAE has prosecuted travelers for poppy seeds on a bagel, codeine in a carry-on, and melatonin bought at an airport elsewhere.

None of this is exotic risk — it's routine travel confusion with extreme consequences.

## The medicines that get people arrested

| Medicine (legal at home) | Gulf status | The fix |
|---|---|---|
| **Codeine** (painkillers, some cough syrups) | Controlled/prescription-required in UAE, Qatar; restricted Saudi | Check the destination's controlled list; carry the prescription; some need prior approval |
| **ADHD meds (Adderall, Ritalin, Vyvanse)** | Controlled — UAE allows with prior approval; personal import rules vary by country | Apply for approval weeks before travel |
| **Benzodiazepines (Xanax, Valium, Ativan)** | Prescription-only; some require pre-approval | Doctor's letter + original packaging |
| **Pregabalin (Lyrica)** | Controlled in UAE and others | Prior approval |
| **Strong painkillers (oxycodone, tramadol)** | Tightly controlled; tramadol has caused multiple tourist arrests in UAE/Egypt | Avoid unless essential + full paperwork |
| **Melatonin** | Varies — some Gulf states restrict higher doses | Check current rules; keep pharmacy receipt |
| **Poppy seeds** | UAE: prosecuted (treated as opiate traces) | Do not carry food containing them |

## What happens if you're stopped

1. **Airport detention** — can last days while tests are processed. Blood and urine are tested; trace presence = possession in Kuwait; 'importation' is presumed if found at the border
2. **Bail** — possible for residents, rare and expensive for visitors
3. **Prosecution** — zero-tolerance frameworks; personal-use amounts still bring years in Qatar; trafficking thresholds trigger death-penalty-eligible charges in Saudi, Kuwait, and (newly) Oman
4. **Your embassy's limits** — visits, lawyer lists, and consular checks. They cannot intervene in the legal process

::: danger The specific trap nobody warns about
**Transit.** Changing planes in Dubai or Doha with controlled medication in your carry-on can constitute 'importation' even if you never leave the airport. If your itinerary transits the Gulf, check the transit country's rules for everything in your bag — not just your destination's.
:::

## The pre-flight checklist

1. **Search the destination's controlled-medicines list** — UAE (MOHAP), Qatar (MOPH), Saudi (SFDA) publish them; when in doubt, email the health authority
2. **Get a doctor's letter** — drug name (generic), dose, quantity, and that it's prescribed to you
3. **Keep everything in original packaging** with the pharmacy label
4. **Carry only what you need** — days-of-supply, not months
5. **Check transit countries separately**
6. **Never carry anything for anyone else** — Gulf law presumes possession; 'holding for a friend' has the same penalty

Our full Gulf sentencing section — with Saudi Arabia's 2025 execution record, Kuwait's new law, and Oman's September 2026 changes — is linked below. Read it before you fly, not at the airport.""",
  drugsInvolved=[],
  related=["sentencing","hotlines","pharmacies","topics:talk-to-your-kid"]),
]

TOPICS += [
 dict(slug="nasal-spray-drug-use", title="Nasal Spray Drug Use: the fastest-growing consumption method nobody teaches you about", date="2026-09-21", read="8 min",
  image="",
  desc="From Spravato and Numbrino to gray-market ketamine sprays and TikTok cocaine spray tutorials — why nasal sprays changed the risk math, and what every user and parent should know.",
  markdown="""## The spray format went mainstream — and the black market followed

Ten years ago, "nasal drug spray" meant one thing: decongestant. Then two pharmaceutical approvals changed everything:

| Year | Event |
|---|---|
| 2019 | **Spravato (esketamine)** — first nasal spray for depression, but locked in clinics under a strict REMS program |
| 2019 | **Numbrino (cocaine HCl 4%)** — FDA-approved cocaine spray for ENT surgery, administered only by clinicians |
| 2022–2025 | Gray-market **ketamine sprays** explode via telehealth and online sellers |
| 2024–2026 | TikTok tutorials teach DIY cocaine/MDMA/ketamine nasal sprays; "coke spray" and "K spray" become search terms |

The pattern is always the same: pharma legitimizes a format, the black market copies the format. Sprays are now being filled with cocaine, ketamine, MDMA, crushed pills, opioids — even research chemicals.

## Why sprays change the risk math

**1. Faster, stronger absorption.** Snorting powder is surprisingly inefficient — much of it drips down the throat or sits unabsorbed. An atomized spray coats the nasal mucosa evenly and absorbs faster and more completely. Translation: the same amount of drug hits harder and quicker than the line users are used to. People dose for the line they know and get the spray they don't.

**2. The dose-per-spray problem.** A standard spray bottle delivers roughly 0.1 mL per pump. But the concentration inside? Unknown in any gray-market bottle. "Two sprays" from two different sellers can differ by 5–10×. This is the single biggest overdose driver in this category — users can't know their dose, so they can't titrate.

**3. No paraphernalia, no friction.** A spray bottle looks like a decongestant. No mirror, no card, no rolled note, no smell trail. That discretion is exactly why dependence escalates faster — the ritual barriers that slow use are gone.

**4. Nasal damage scales.** Frequent spraying of anything but saline irritates and eventually erodes the septum — same mechanism as cocaine nose, but now applying to ketamine, MDMA and RC users who thought they were avoiding it.

## The legal landscape (it matters)

- **Numbrino** is real pharmaceutical cocaine — but it's a clinic supply for ENT procedures. There is no patient prescription for take-home cocaine spray. Any website "selling Numbrino" is selling diversion or counterfeit — both federal felonies, for seller AND buyer.
- **Spravato** is the only legal ketamine-family spray, and it physically cannot leave the clinic — patients are observed for 2 hours per session.
- **Compounded ketamine sprays** from telehealth clinics occupied a gray zone that regulators have been closing (state boards disciplined multiple companies in 2024–2025 after adverse events).
- Everything else in a spray bottle is an unregulated, unmeasured product.

## What's actually inside gray-market sprays

Testing of seized and voluntarily submitted sprays has found:

- **Correct drug, wrong dose** — the most common finding; concentrations varying 2–10× between bottles from the same seller
- **Wrong drug entirely** — ketamine sprays containing deschloroketamine or 2F-DCK; "coke spray" containing lidocaine + caffeine + levamisole
- **Contaminants** — residual solvents, heavy metals, bacterial growth in non-sterile home-brewed bottles
- **Surprise opioids** — fentanyl appearing in spray bottles is rare but documented; if someone collapses after any unknown spray, treat it as a possible opioid overdose and give naloxone

## If someone is using these anyway — the harm-reduction floor

1. **Never assume the dose.** Treat every new bottle as unknown strength; a test dose (one spray, wait 20+ minutes) isn't optional with this format
2. **Never share bottles.** Nasal membranes bleed; blood-borne infections transmit
3. **Saline rinse after use** — the single best thing you can do for your nose
4. **Watch the frequency.** The convenience trap is the mechanism: if sprays became daily, that's the dependence pattern — bladder damage (ketamine), septum damage (everything)
5. **Naloxone anyway.** Unknown bottle + collapse = give naloxone, call emergency services, stay
6. **Never drive.** Nasal onset feels "milder" than injection or lines; impairment is not milder

::: danger The overdose picture
Someone who sprays an unknown concentration and redoses because "nothing's happening yet" (nasal absorption is fast but not instant) is the classic fatal pattern in this category. The second dose lands while the first is still climbing. With opioids in the bottle, naloxone and 911; with stimulants, treat the racing heart and call anyway. The delay kills.
:::

## The bigger picture

Consumption methods evolve faster than drug education. We published guides on pressed pills and gas-station drugs because the market moved; nasal sprays are the same story one chapter later. Every profile below — Numbrino, ketamine sprays, cocaine spray, MDMA spray — exists because the format itself is now a risk category.

Know the format. The bottle is not a decongestant just because it looks like one.""",
  drugsInvolved=["ketamine-nasal-spray","numbrino","cocaine","esketamine"],
  related=["topics:cocaine-nasal-spray","topics:mdma-nasal-spray","numbrino","ketamine-nasal-spray","esketamine","topics:spot-pressed-pills"]),
]


TOPICS += [
 dict(slug="ketamine-nasal-spray", tag="Important", title="Ketamine Nasal Spray: the Spravato confusion, the dosing trap, and the bladder damage nobody warns you about", date="2026-09-23", read="8 min",
  image="/assets/img/topics-ketamine-nasal-spray.png",
  desc="Ketamine nasal sprays are everywhere now — some prescribed, most homemade from street powder. Why the dose is a guess, why the k-hole comes on fast, and what heavy use does to your bladder.",
  markdown="""## The two sprays people confuse — and why it matters

There are really two things called "ketamine nasal spray," and mixing them up is where the trouble starts.

The first is **Spravato (esketamine)** — a prescription spray for treatment-resistant depression, made by Janssen, taken in a clinic under observation because of its dissociation and blood-pressure effects. It is precisely dosed (28 mg or 84 mg per device), pharmacy-sealed, and legally dispensed.

The second is everything else: **street sprays made by dissolving ketamine powder — or crushed tablets — in water or saline** and pouring it into a nasal spray bottle. Sold on Telegram, passed around at festivals, sometimes marketed as "microdose sprays." The concentration is whatever the maker felt like that day. The myth is that spraying is cleaner and more controlled than snorting lines. The reality is almost the opposite: **with a homemade spray, the dose per pump is unknown, the powder may be cut, and the fast nasal onset means the k-hole arrives before you have time to reconsider.**

::: amber The core trap
A line of ketamine lets you see roughly how much powder you're taking. A spray bottle hides it completely. One bottle might deliver 5 mg per pump; the next, from the same seller, might deliver 30 mg. Users routinely redose because "the first spray did nothing" — and the second pump lands while the first is still climbing. That is exactly how an evening turns into a k-hole in a bathroom stall.
:::

## Why the dose is a guess

Street ketamine is already variable — purity ranges widely, and powders are commonly cut with MSG, caffeine, or other dissociatives. Dissolving an unknown amount of that powder in an unknown volume of water removes the last rough gauge users had: visual size. There is no way to eyeball concentration in a liquid.

- **No label, no math.** Sellers quote "mg per spray" that nobody has ever measured.
- **Pumps vary.** Cheap bottles deliver wildly different volumes per press.
- **Tolerance resets nothing.** A bottle strength that was manageable last month is not a promise about the next bottle.

If you are going to use it regardless, the only defensible move is to **test one pump first and wait at least 20 minutes** before any second — nasal ketamine onsets in 5–15 minutes and peaks later than users expect.

## The k-hole comes faster than you think

Nasal absorption bypasses nothing — ketamine sprayed up the nose hits the bloodstream quickly through the nasal mucosa. The dissociative effect that experienced users call a **k-hole** — full-body detachment, inability to move or speak coherently, time distortion — can arrive within minutes of a strong pump.

::: danger What a k-hole actually looks like from outside
Someone in a deep k-hole cannot protect themselves: they may be immobile, unable to call for help, vomiting while lying on their back. If someone near you is unresponsive but breathing after ketamine, put them in the **recovery position**, stay with them, and call emergency services if breathing is slow or they cannot be roused. Ketamine overdoses are rarely fatal alone — but **mixing with alcohol, GHB, opioids, or benzos changes that completely**, because every one of those adds respiratory depression on top.
:::

## The part nobody warns you about: your bladder

This is the section that matters most for regular users, and the one TikTok never mentions. **Ketamine destroys the bladder lining.** Heavy or frequent use causes **ketamine-induced cystitis**: urinary frequency, urgency, pain, blood in the urine, and — in advanced cases — a bladder so scarred and shrunken it holds a fraction of its normal volume. Some long-term users have needed **bladder removal surgery in their twenties**.

The damage is dose- and frequency-related, appears in some users within months of heavy use, and is only partially reversible. Early warning signs:

1. Needing to urinate far more often, in small amounts
2. Pain or burning when urinating
3. Blood in urine
4. Lower abdominal cramps between uses

If any of these show up, **stop completely and see a doctor — and tell them it is ketamine.** Continuing to use through bladder symptoms is how a treatable irritation becomes a surgical problem.

## Harm reduction checklist

If someone is going to use ketamine nasal spray despite all of the above:

1. **Know what "one spray" means for THIS bottle** — test a single pump and wait 20+ minutes before more
2. **Never mix with alcohol, GHB, opioids, or benzos** — this combination is the actual killer, not ketamine alone
3. **Don't use alone at high doses** — a k-hole leaves you unable to protect yourself
4. **Recovery position** for anyone unresponsive but breathing; emergency services if breathing is slow or shallow
5. **Track bladder symptoms** — frequency, pain, or blood means stop now, not later
6. **Never drive.** Nasal onset feels smoother than snorting; impairment is not smoother

## The bottom line

Spraying ketamine does not sanitize it. It removes the one rough dose-gauge users had, accelerates the onset, and — with heavy use — quietly wrecks the bladder while users are watching for other problems. If bladder symptoms have already started, or if use has become daily, our ketamine recovery guide below covers what quitting actually involves, including what to expect as the bladder heals.""",
  drugsInvolved=["ketamine"],
  related=["ketamine","topics:nasal-spray-drug-use","topics:cocaine-nasal-spray","topics:mdma-nasal-spray","quit:ketamine"]),
]
