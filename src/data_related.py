# Curated internal-link values for existing content.
# Format: {content_type: {slug: {"related": [...], "drugsInvolved": [...]}}}
# Entries in `related`: drug slug (→ /drugs/x/) or type:slug (topics:x, news:x, busts:x, quit:x) or section page (hotlines, sentencing…)
# Merged into all datasets at build/seed time — these ARE the examples to copy in the admin.

RELATED_OVERRIDES = {
 "drugs": {
  "fentanyl":        {"related": ["xylazine", "medetomidine", "heroin", "etonitazene", "topics:fentanyl-numbers", "topics:spot-pressed-pills"]},
  "heroin":          {"related": ["fentanyl", "xylazine", "quit:heroin", "topics:what-actually-happens-when-you-quit"]},
  "cocaine":         {"related": ["crack", "4-fluorococaine", "topics:cocaine-purity-and-cuts", "busts:bust-australia-sydney-cocaine-record"]},
  "methamphetamine": {"related": ["speed", "mdpv", "quit:meth", "busts:bust-texas-cabbage-meth"]},
  "mdma":            {"related": ["molly", "xtc-pills", "topics:spot-pressed-pills", "news:high-dose-ecstasy-warning"]},
  "xylazine":        {"related": ["fentanyl", "medetomidine", "topics:what-is-xylazine", "topics:krokodil-fact-vs-myth"]},
  "alprazolam":      {"related": ["etizolam", "bromazolam", "flubromazolam", "topics:spot-pressed-pills", "news:counterfeit-xanax-update", "quit:alprazolam"]},
  "ketamine":        {"related": ["2f-dck", "quit:ketamine"]},
  "adderall":        {"related": ["adderall-xr", "ritalin", "topics:spot-pressed-pills"]},
  "oxycodone":       {"related": ["oxycontin", "fentanyl", "topics:spot-pressed-pills"]},
  "suboxone":        {"related": ["subutex", "methadone", "quit:heroin"]},
  "etonitazene":     {"related": ["isotodesnitazene", "fentanyl", "topics:nitazenes-new-opioids"]},
  "isotodesnitazene":{"related": ["etonitazene", "fentanyl", "topics:nitazenes-new-opioids"]},
  "ghb":             {"related": ["gbl", "quit:ghb"]},
  "flubromazolam":   {"related": ["alprazolam", "clonazolam", "bromazolam", "news:counterfeit-xanax-update"]},
  "kratom":          {"related": ["tianeptine", "7-hydroxymitragynine", "heroin", "quit:heroin"]},
  "3-meo-pcp":       {"related": ["pcp", "ketamine", "2f-dck", "topics:talk-to-your-kid"]},
  "weed":            {"related": ["4f-adb", "5f-adbica", "nm2201", "topics:talk-to-your-kid"]},
 },
 "busts": {
  "bust-texas-cabbage-meth":          {"related": ["speed", "topics:drug-busts-this-week", "news:high-dose-ecstasy-warning"]},
  "bust-spain-banana-cocaine-13t":    {"related": ["topics:cocaine-purity-and-cuts", "busts:bust-australia-sydney-cocaine-record", "topics:drug-busts-this-week"]},
  "bust-australia-sydney-cocaine-record": {"related": ["topics:cocaine-purity-and-cuts", "busts:bust-spain-banana-cocaine-13t", "sentencing"]},
 },
 "news": {
  "nitazenes-spreading-eu":   {"related": ["topics:nitazenes-new-opioids", "fentanyl"]},
  "xylazine-beyond-us":       {"related": ["topics:what-is-xylazine", "topics:krokodil-fact-vs-myth"]},
  "high-dose-ecstasy-warning":{"related": ["topics:spot-pressed-pills", "molly", "mdma"]},
  "counterfeit-xanax-update": {"related": ["topics:spot-pressed-pills", "etizolam", "flubromazolam"]},
 },
 "topics": {
  "what-is-xylazine":      {"drugsInvolved": ["xylazine", "fentanyl"], "related": ["topics:krokodil-fact-vs-myth", "topics:nitazenes-new-opioids", "fentanyl"]},
  "cocaine-purity-and-cuts": {"drugsInvolved": ["cocaine"], "related": ["topics:drug-busts-this-week", "busts:bust-spain-banana-cocaine-13t"]},
  "fentanyl-numbers":      {"drugsInvolved": ["fentanyl"], "related": ["topics:nitazenes-new-opioids", "topics:what-is-xylazine", "etonitazene"]},
  "spot-pressed-pills":    {"drugsInvolved": ["fentanyl", "alprazolam", "adderall"], "related": ["news:counterfeit-xanax-update", "news:high-dose-ecstasy-warning", "topics:fentanyl-numbers"]},
  "drug-busts-this-week":  {"related": ["busts:bust-texas-cabbage-meth", "busts:bust-australia-sydney-cocaine-record", "topics:cocaine-purity-and-cuts"]},
  "krokodil-fact-vs-myth": {"related": ["topics:what-is-xylazine", "heroin"]},
  "nitazenes-new-opioids": {"drugsInvolved": ["etonitazene", "isotodesnitazene"], "related": ["fentanyl", "topics:fentanyl-numbers", "news:nitazenes-spreading-eu"]},
  "sentencing-explained":  {"related": ["sentencing", "topics:talk-to-your-kid", "hotlines"]},
  "talk-to-your-kid":      {"drugsInvolved": ["fentanyl"], "related": ["topics:fentanyl-numbers", "hotlines", "topics:spot-pressed-pills"]},
  "hotline-directory":     {"related": ["hotlines", "rehabs", "topics:talk-to-your-kid"]},
  "what-actually-happens-when-you-quit": {"related": ["quit:heroin", "quit:cocaine", "quit:alprazolam", "quit:ghb"]},
 },
 "quit": {
  "heroin":    {"related": ["topics:what-actually-happens-when-you-quit", "hotlines", "rehabs"]},
  "fentanyl":  {"related": ["topics:what-actually-happens-when-you-quit", "hotlines", "rehabs"]},
  "cocaine":   {"related": ["topics:what-actually-happens-when-you-quit", "hotlines", "rehabs"]},
  "meth":      {"related": ["topics:what-actually-happens-when-you-quit", "hotlines", "rehabs"]},
  "mdma":      {"related": ["topics:what-actually-happens-when-you-quit", "hotlines", "rehabs"]},
  "alprazolam":{"related": ["topics:what-actually-happens-when-you-quit", "hotlines", "rehabs"]},
  "ketamine":  {"related": ["topics:what-actually-happens-when-you-quit", "hotlines", "rehabs"]},
  "ghb":       {"related": ["topics:what-actually-happens-when-you-quit", "hotlines", "rehabs"]},
 },
}
