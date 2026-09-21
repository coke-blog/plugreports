# Content Gap Analysis — plugreports.com

*Compiled from the site's source data (`data_drugs.py`, `data_batch100.py`, `data_greymarket.py`, `data_content.py`, `data_categories.py`) and cross-checked against 2024–2026 trend sources: DEA National Drug Threat Assessment, CDC MMWR, FDA/HHS 7-OH actions, EMCDDA/EUDA European Drug Report & Early Warning System, CFSRE NPS Discovery, JAMA Health Forum, Washington/Baltimore HIDTA, Aegis Sciences alerts, UNODC World Drug Report.*

---

## (A) Coverage Inventory Summary

**430 drug profiles** across 18 categories (plus `BRAND_MAP` covering ~340 grey-market brands and a `PENDING` queue of ~47 assigned-but-unprofiled grey-market compounds).

| Category | Profiles | Notes |
|---|---|---|
| Stimulants | 66 | Deep cathinone/pyrovalerone RC coverage |
| Opioids | 50 | Strong fentanyl-analogue + nitazene coverage (etonitazene, metonitazene, protonitazene, isotonitazene, isotodesnitazene) |
| Cannabinoids | 38 | Excellent semi-synthetic hemp-cannabinoid coverage (Delta-8/10, HHC, THC-O, THC-P, HHCP…) |
| Psychedelics | 37 | Strong tryptamine/lysergamide coverage |
| Sedatives & Hypnotics | 27 | Z-drugs, barbiturates, OTC sleep aids covered |
| Benzodiazepines | 23 | Rx + RC benzos — but **bromazolam missing** (see B) |
| Steroids & Anabolics | 23 | |
| Performance & Grey-Market Pharma | 22 | |
| Hazardous Substances | 19 | KCN, BTMPS-class warnings (BTMPS itself missing) |
| Peptides & Research Chemicals | 19 | BPC-157, TB-500, Melanotan II covered; **retatrutide missing** |
| Beauty Industry & Med Spa | 18 | |
| Hair Loss & Hormones | 17 | |
| GHB / GBL (depressants) | 15 | GHB, GBL, 1,4-BDO all covered |
| Empathogens | 15 | MDMA family well covered |
| Dissociatives | 12 | Ketamine analogues covered — **PCP itself missing** |
| Weight Loss & Metabolic | 12 | Semaglutide covered; **tirzepatide missing** |
| Tobacco & Nicotine | 11 | Cigarettes, vapes, snus, pouches, hookah covered |
| Sexual Health & ED | 4 | + 3 compound pages with huge brand tables |

**Editorial content** (`data_content.py`):
- **26 topic guides**: xylazine, cocaine cuts, fentanyl numbers, pressed-pill spotting, bust-reading, krokodil myth, nitazenes, sentencing, talking to kids, hotline directory, quit hub, cocaine/MDMA nasal sprays, gas-station drugs, inhalants, beauty-injection dangers, nitrous nerve damage, roxy-vs-oxy-vs-percocet, MDMA overdose, pregabalin FAQ, vyvanse FAQ, EU drug checking, Thailand cannabis, India drug law, Gulf travel laws, nasal-spray trend.
- **8 quit timelines**: heroin, fentanyl, cocaine, meth, MDMA, alprazolam, ketamine, GHB. (**No alcohol, nicotine, kratom, benzo-generic, cannabis, gabapentinoid timelines.**)
- **5 news items, 4 busts.**
- **Hotlines: 9 regions** (USA, Canada, Europe, Australia, Africa, Europe-more, New Zealand, Asia-selected [India/Thailand only], Latin America-selected [Brazil only]).
- **Pharmacies: 6 verification entries** (NABP, PharmacyChecker, NAPRA, GPhC, EU Common Logo, HealthWarehouse) — all US/CA/UK/EU-focused.
- **Rehabs: 6 entries** (Hazelden, Priory, NA, AA, Turning Point, SMART) — US/UK/worldwide only.
- **Sentencing: 9 regions** (Gulf states, US, Canada, UK, EU, Australia, Africa, Asia, Latin America).

**Data-quality flags found while inventorying** (fix in source, not this file): two profiles have misspelled category keys (`empatogens`, `stimulands`) that will orphan them from category hubs; a few alias lists contain adjacent-string-concatenation bugs (e.g., `aliases=["Dillies", "8s" "dilsudid"]`).

---

## (B) Missing Substances

Priorities: **P0** = major active harm trend and/or very high search demand; **P1** = significant trend or search gap; **P2** = worth adding for completeness.

| # | Substance | Why it matters (source) | Priority | Suggested category |
|---|---|---|---|---|
| 1 | **Bromazolam** | The most-detected novel benzodiazepine in North America since 2023 (DEA NDTA; CFSRE NPS Discovery; Aegis alerts). Floods counterfeit "Xanax bars" — the site's own news item flags flubromazolam in fake bars but there is no profile for the #1 fake-bar ingredient. Multi-day blackouts, lethal withdrawal. | P0 | Benzodiazepines |
| 2 | **Medetomidine** | The successor to xylazine as dominant fentanyl adulterant: detected in 18+ states by 2024, dominant in Philadelphia/Pittsburgh/Chicago supplies (CDC MMWR June 2025); ~37% of opioid samples by Oct 2025 vs 4% in May 2024. Causes ICU-grade withdrawal (severe hypertension/tachycardia, dexmedetomidine-refractory-to-standard-care). DEA field alerts 2026 (Indiana). Site covers xylazine but not this. | P0 | Sedatives (adulterant cross-tag with Opioids) |
| 3 | **7-Hydroxymitragynine (7-OH) + MGM-15/MGM-16/pseudoindoxyl** | FDA recommended Schedule I for concentrated 7-OH (29 July 2025); DEA issued Notices of Intent for temporary scheduling of 7-OH + 3 synthetic derivatives (1 July 2026); Florida/Tennessee emergency bans; FDA seizures Dec 2025. Massive search volume ("is 7-OH legal", "7-OH withdrawal"). Kratom is profiled but the concentrated 7-OH products are a distinct, far more opioid-like phenomenon. | P0 | Opioids |
| 4 | **PCP (Phencyclidine)** | Classic dissociative with very high baseline search volume ("PCP effects", "wet/sherm"); 3-MeO-PCP and other analogues are profiled but the parent compound is missing. Still regularly seized (DEA). | P0 | Dissociatives |
| 5 | **Crack Cocaine** | Distinct route/harm profile from powder cocaine (smoking, compulsion loop, crack lung, pipe-sharing infections) and a huge standalone query cluster ("crack vs coke"). Only powder cocaine is profiled. | P0 | Stimulants |
| 6 | **Tirzepatide (Mounjaro/Zepbound)** | The most counterfeited GLP-1 after semaglutide; FDA counterfeit alerts; Eli Lilly ITC litigation against grey-market vendors; site profiles semaglutide/liraglutide/cagrilintide/survodutide/mazdutide but not the #2 molecule in the class. | P1 | Weight Loss |
| 7 | **Retatrutide ("reta", "GLP-3")** | The most-searched grey-market peptide of 2025–26: unapproved triple agonist, sold by "research" vendors; Peptide Sciences shutdown (Mar 2026) after 37 retatrutide samples failed third-party testing; FDA raids (Amino Asylum). Grey-market demand + zero legal supply = exactly this site's remit. | P1 | Weight Loss / Peptides |
| 8 | **Phenazolam (Clobromazolam)** | Rising designer benzo overtaking bromazolam in detections (Aegis Sciences, Q3 2025: top designer benzo in Tennessee + 4 states); mis-sold as Xanax/bromazolam; ultra-potent, seizure-risk withdrawal. | P1 | Benzodiazepines |
| 9 | **N-Pyrrolidino etonitazene (Etonitazepyne / NPE)** | Most prominent pyrrolidino-nitazene; EU Early Warning notification; multiple US/UK death series; distinct from the 5 nitazenes already profiled. Also consider **N-desethyl isotonitazene** (EUDA notification Dec 2023, linked to EU death clusters). | P1 | Opioids |
| 10 | **Para-fluorofentanyl** | Among the top fentanyl analogues in NFLIS reports 2023–2025; routinely co-detected with xylazine/BTMPS; gaps between "fentanyl" and niche analogues in the current set. | P1 | Opioids |
| 11 | **BTMPS (Tinuvin 770)** | New industrial plastic stabilizer adulterating fentanyl since mid-2024; 600+ CFSRE-positive samples, 11+ states (JAMA Health Forum 2025; HIDTA bulletin); calcium-channel blocker, no naloxone response, "bug spray" smell tell — and now a precursor for tetramethyl-fentanyl variants (CFSRE 2025). Fits the Hazardous Substances remit. | P1 | Hazardous Substances |
| 12 | **O-DSMT (O-desmethyltramadol)** | The most-used RC opioid after the nitazene crackdowns; active tramadol metabolite sold as powder/pellets; steady harm-reduction-community demand; bridges the tramadol profile and the RC opioid set. | P1 | Opioids |
| 13 | **Bupropion (Wellbutrin)** | Very high search volume: "bupropion and alcohol", seizure threshold, insufflation abuse (documented prison/ER phenomenon), "poor man's cocaine". The site has no antidepressant profiles despite heavy mixing-query demand. | P1 | Sedatives / new "Mental-Health Meds" grouping |
| 14 | **SSRIs / SNRIs as a class profile** (sertraline, escitalopram, fluoxetine, venlafaxine, duloxetine) | Among the most-searched drug questions on earth: "can you drink on…", "MDMA on SSRIs", serotonin syndrome, discontinuation ("brain zaps"). Site covers MAOIs, 5-HTP and St John's Wort but not the mainstream class people actually mix with everything. | P1 | New grouping: Mental-Health Meds (or Sedatives) |
| 15 | **Nalmefene (Opvee)** | FDA-approved 2023 long-acting opioid antagonist now carried by some first responders; users/families search "nalmefene vs naloxone". Natural companion to the existing naloxone profile. | P2 | Opioids (reversal agents) |
| 16 | **Methocarbamol / Tizanidine** | Common muscle-relaxant searches + sedation/mixing questions; carisoprodol, cyclobenzaprine and baclofen are already profiled — completes the set. | P2 | Sedatives |
| 17 | **Amitriptyline & tricyclics** | High mixing/OD-severity search volume; tricyclic overdose is a leading tox-fatality class. | P2 | Sedatives / Mental-Health Meds |
| 18 | **Clonidine / Lofexidine** | Withdrawal-adjunct searches ("clonidine for opioid withdrawal"); also emerging misuse + hypotension risk; relevant to the medetomidine-withdrawal story (same α2 class). | P2 | Sedatives |
| 19 | **Butane / lighter-fluid huffing** | The inhalant set covers duster, petrol, glue, freon, nitrous — butane is the classic "sudden sniffing death" agent with its own query cluster. | P2 | Hazardous / inhalants |
| 20 | **Flunitrazolam / Fluclotizolam** | Active novel-benzo market entries after etizolam bans; completes the RC-benzo shelf alongside bromazolam/phenazolam. | P2 | Benzodiazepines |
| 21 | **THCjd / THCh / HHC-O** | Next-wave hemp cannabinoids already on US vape-shop shelves; the site owns this content lane (38 cannabinoid profiles) and these are the conspicuous remaining gaps. | P2 | Cannabinoids |
| 22 | **Dipyanone** | Cyclohexylmethyl opioid detected in EU post-nitazene-scheduling substitution (EUDA EWS); "what replaces nitazenes" watchlist item. | P2 | Opioids |
| 23 | **5-MAPB / 6-MAPB** | Common MDMA-substitute empathogens in EU pill/powder testing; site covers 5-APB/6-APB but not the methylated analogues. | P2 | Empathogens |
| 24 | **Mitragynine (standalone) & kratom extracts/shots** | The kratom profile covers the leaf; concentrated shots (OPMS-style) and pure mitragynine behave differently and drive the poison-center call surge (DEA St Louis bulletin, 2026). | P2 | Opioids |

**Deliberately NOT gaps** (checked — already covered): tianeptine, kratom, phenibut (+F-phenibut, FAA), xylazine, nitrous (+ Galaxy Gas, whippets), alcohol, caffeine, nicotine/vapes/pouches, Delta-8/HHC/THC-P/edibles, semaglutide, BPC-157, melanotan, SARMs, poppers, GHB/GBL/1,4-BDO, DMT/ayahuasca/5-MeO-DMT/changa, ibogaine, mescaline, 2C-B + 2C-x + DOx + NBOMe, 4-AcO-DMT and major tryptamines, khat, salvia, kanna, DXM, loperamide, diphenhydramine, doxylamine, gabapentin, pregabalin, carfentanil, U-47700, brorphine, AH-7921, krokodil, captagon, yaba, tusi ("pink cocaine"), propylhexedrine, memantine.

---

## (C) Missing Guide / Topic Areas (prioritized)

### P0 — highest impact, strongest query demand
1. **Fentanyl test strips: complete how-to** — step-by-step (dissolve, dilute ratios for meth/MDMA vs opioids, cookie-sheet residue method for pills), false-negative causes, xylazine strips, benzo strips, where to get them free, legality by state/country (still paraphernalia in some US states). `spot-pressed-pills` mentions strips in one bullet; a dedicated page is the single most-searched harm-reduction how-to.
2. **Naloxone: complete access & use guide** — nasal vs IM vs auto-injector, nalmefene comparison, dose-repetition protocol for nitazenes, "they woke up ≠ it's over" re-sedation, free sources (NEXT Distro, pharmacies, community programs) per country. Currently scattered across topic pages.
3. **Mixing & combination danger hub + per-combo pages** — benzos + opioids; alcohol + benzos; alcohol + GHB (the date-rape/OD classic); opioids + gabapentinoids (~1/3 of opioid ODs); cocaine + alcohol (cocaethylene); speedball (heroin + cocaine); stimulants + PDE5 inhibitors. Each is a standalone high-volume query ("can you mix Xanax and alcohol").
4. **Serotonin syndrome & MAOI interaction guide** — MDMA/SSRIs, DXM/SSRIs, tramadol/SSRIs, ayahuasca + MAOIs + tyramine, stimulants + MAOIs; symptom ladder vs "bad trip". Partially inside MDMA guides; deserves a canonical page that every empathogen/psychedelic profile links to.

### P1
5. **Overdose first aid by drug class (hub)** — opioid / stimulant / GHB / benzo / psychedelic-crisis / inhalant: signs → actions → what to tell paramedics. Individual content exists (MDMA overdose, cocaine spray) but there's no canonical hub.
6. **Withdrawal & quit-timeline expansion** — the QUIT framework has 8 substances; missing the two most dangerous (alcohol — delirium tremens, seizure window; benzos beyond alprazolam — Ashton taper, RC-benzo specifics for clonazolam/bromazolam) plus the highest-search ones: nicotine/vaping, kratom & 7-OH, tianeptine, phenibut, gabapentin/pregabalin, cannabis, caffeine, suboxone/methadone tapering, antidepressant discontinuation.
7. **Pregnancy, breastfeeding & drugs** — per-class guidance: opioids/withdrawal-informed birth (NOWS), alcohol/FASD, cannabis evidence, stimulants, benzos; "I used before I knew I was pregnant" — huge, underserved, stigma-heavy query cluster.
8. **Festival & nightlife safety hub** — heat/hydration math, PMA redosing rule, drug checking on-site, buddy systems, drug-facilitated assault (spiking) response.
9. **Chemsex harm reduction (LGBTQ+)** — GHB/mephedrone/crystal meth "PnP" context, slamming (injecting) safety, GHB dosing-clock rules, HIV/PrEP interactions, community-specific services. High-harm niche with almost no mainstream coverage.
10. **Fake pill identification library** — per-product pages: M30 "blues", Xanax bars, Adderall 30s, Percocet, with photo comparisons + lab findings + strip protocol. Systematizes `spot-pressed-pills` into a searchable mini-directory.
11. **Drug-induced psychosis, HPPD & "bad trip" first aid** — stimulant psychosis recognition, cannabis-induced psychosis, psychedelic crisis support (talk-down techniques), when to hospitalize.
12. **Counterfeit GLP-1 pens** — how to spot fake Ozempic/Mounjaro pens (FDA counterfeit alerts), compounded-semaglutide risks, dosing-error hospitalizations. Sits naturally beside the semaglutide profile and weight-loss category.
13. **Drug checking directory beyond Europe** — `europe-drug-checking` exists; add US/Canada/Australia/NZ (DanceSafe, mail-in GC/MS services, CanTEST, KnowYourStuffNZ), plus reagent-kit color charts.

### P2
14. **Traveling with prescription medications** — general guide (controlled-med letters, original packaging, country rules) extending the Gulf-specific page; ADHD meds/benzos/codeine border rules by destination.
15. **Safe storage & disposal** — lockboxes vs curious teens, take-back programs, fentanyl-patch disposal, "flush list".
16. **How to talk to your doctor or pharmacist about drug use** — stigma scripts, what clinicians must keep confidential, getting honest interaction advice, taper requests.
17. **Cannabinoid hyperemesis syndrome (CHS)** — heavy daily-use teen/young-adult query cluster ("scromiting"), hot-shower tell, the only cure.
18. **Microdosing: evidence & safety** — LSD/psilocybin microdosing, interaction with SSRIs, chronic 5-HT2B cardiac questions, legal status; huge lifestyle query volume.
19. **Driving & drugs** — per-substance impairment windows + per-jurisdiction testing laws; the Sterling nitrous case shows traffic appetite.
20. **Darknet market safety & myths** — scam/fraud reality, fentanyl unpredictability doesn't improve online, law-enforcement exposure. Frame strictly as risk information (editorial care needed).
21. **Stigma-free language guide** — for families, media, clinicians ("person who uses drugs"); supports the brand's positioning and earns links from NGOs/journalism programs.
22. **Seniors & polypharmacy** — benzo/Z-drug deprescribing in 65+, fall risk, alcohol + medication cascade.
23. **Veteran-specific resources** — PTSD + substance use, VA pathways, benzo/opioid legacy prescribing.
24. **"Found drugs — what now" for parents/partners** — identification, testing, conversation scripts, naloxone in the home (extends `talk-to-your-kid`).

---

## (D) Directory Expansion Recommendations

### Hotlines — priority regions to add
The sentencing section already covers the Gulf and Asia/LatAm, but hotlines don't — a user reading "UAE: death penalty" finds no help number. Add:

1. **Middle East / Gulf (P0)** — UAE (treatment-instead-of-jail pathway under Art. 89 — the single most useful fact to surface), Saudi (hospital-based detox), Qatar; include embassy contacts and the caveat that help-seeking has legal dimensions there.
2. **Latin America beyond Brazil (P0)** — Mexico (Línea de la Vida 800 911 2000, 24/7 federal addiction line), Argentina (SEDRONAR 141), Colombia (192/106 crisis lines), Chile (SENDA 1412), Peru.
3. **Asia beyond India/Thailand (P0)** — Philippines (DOH/DDB; huge relevance given the drug war), Indonesia, Malaysia, Singapore (NCADA), Japan (English-language options), South Korea, Pakistan, Vietnam, China (hotline caveats).
4. **Europe gaps (P1)** — Portugal (SICAD life line — pairs with the decriminalization story), Ireland (HSE helpline), Italy, Poland, Denmark, Finland, Czechia; UK already has FRANK.
5. **Africa beyond SA/Kenya (P2)** — Nigeria (NDLEA), Ghana, Egypt, Morocco.
6. **Specialized lines (P1)** — Brave-app/overdose-response lines beyond US "Never Use Alone" (Canada's NORS 1-888-688-6677), LGBTQ+ specific lines, veterans' crisis line (US 988 press 1), youth-specific per region.

### Rehabs — what the directory needs
Current: 6 entries, 2 commercial providers + peer groups. To be "the one directory": add Canada (per-province funded options), Australia (state AOD services), Germany (Suchtberatung network), Spain, Netherlands, South Africa (SANCA clinics), India (with quality caveats), Thailand (a major treatment-tourism destination — high scam potential, needs vetting), Mexico (warn about unregulated "anexos"). **Verification methodology for a trustworthy rehab listing:**
- Licensing: current license with the national/state health regulator, verifiable in a public register; license number displayed on the listing.
- Accreditation: JCI / CARF / national equivalents where they exist.
- Medical staffing: named medical director; 24/7 medical cover for detox claims; published detox protocols.
- Red flags to publish as a "warning flags" list: guaranteed-cure claims, no named clinical staff, patient-broker/kickback model (body-brokering), pressure sales with same-day payment, no detox medical supervision offered for alcohol/benzo/GHB patients, "interventionists" paid per placement, unverifiable testimonials, no transparent pricing.
- Evidence of practice: MAT availability (buprenorphine/methadone) — rehabs that refuse MAT should be flagged, not silently listed.
- Re-verification cadence: annual license re-check + complaint/ sanction scan; user-report channel with a takedown SLA.

### Pharmacies — verification rubric
The current 6 entries teach users to verify (NABP/GPhC/EU logo) — extend into an actual rubric the site applies: (1) licensure check in the national register (license # displayed), (2) prescription required for Rx-only meds (any site selling benzos/opioids/GLP-1s without Rx = auto-fail), (3) physical jurisdiction + pharmacist contact, (4) domain-age and payment-method checks (crypto-only = fail), (5) LegitScript/NABP/EU common-logo status, (6) price-sanity floor, (7) product sourcing (named wholesalers). Publish the **warning-flags list** as its own page — it's evergreen SEO ("is [pharmacy] legit"). Add Australia (TGA), New Zealand (Medsafe), India, Singapore (HSA) register links.

---

## (E) Top-20 SEO Query Opportunities

The site has **no systematic detection-window coverage** and only **one comparison page** (`roxy-vs-oxycodone-vs-percocet`) and **one overdose page** (`mdma-overdose`). These three templates — "how long does X stay in your system", "X vs Y", "can you overdose on X", "can you mix X and Y" — are the highest-volume drug queries in existence and the profiles already contain 80% of the raw facts.

**Detection windows (template: urine/blood/saliva/hair + factors table):**
1. How long does weed (THC) stay in your system? *(highest-volume drug query globally)*
2. How long does cocaine stay in your system?
3. How long does fentanyl stay in your system?
4. How long does Xanax stay in your system?
5. How long does Adderall stay in your system?
6. How long does ketamine stay in your system?
7. How long does MDMA/molly stay in your system?
8. How long does alcohol stay in your system (breath/urine/EtG/hair)?

**Comparisons ("X vs Y" — profiles exist on both sides; just add comparison pages):**
9. Xanax vs Valium vs Ativan vs Klonopin (benzo comparison hub)
10. Adderall vs Vyvanse (both profiled incl. Vyvanse FAQ)
11. Oxycodone vs hydrocodone (extends the existing Roxicodone page)
12. Crack vs cocaine (requires the new crack profile — #5 above)
13. Delta-8 vs Delta-9 vs HHC vs THC-P (all profiled)
14. Kratom vs 7-OH (requires the new 7-OH profile — #3 above; 2025–26 news cycle makes this urgent)
15. GHB vs GBL vs 1,4-BDO (all profiled; dosing-conversion angle is genuinely life-saving)
16. Suboxone vs methadone (both profiled)

**"Can you overdose on X" / "can you mix X and Y" (extends the proven mdma-overdose template):**
17. Can you overdose on weed / shrooms / LSD / melatonin? (series)
18. Can you mix Xanax and alcohol? / shrooms and alcohol? / Adderall and weed? / MDMA on SSRIs? (series — feeds the missing mixing hub in C.3)

**Legality & withdrawal trackers (news-cycle-driven, high freshness value):**
19. Is kratom / 7-OH / Delta-8 / tianeptine legal in [state/country]? — state-by-state and country trackers; the 7-OH federal scheduling process (DEA NOI, July 2026) guarantees sustained query volume through 2026–27.
20. How long does [kratom / alcohol / phenibut / gabapentin / nicotine] withdrawal last? — ties directly to the quit-timeline expansion (C.6); each timeline page is itself the answer.

*Implementation note: items 1–8 are pure template scale-out over existing profile data and represent the fastest traffic win; items 12–14 require 3–5 of the new substance profiles in section B, which is why those profiles carry P0/P1 priority.*
