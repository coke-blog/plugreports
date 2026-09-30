# Video library — short visual ID clips ("what does X look like") served from
# KV media (media:videos/<slug>.mp4). Keep clips under ~3 MB (480p, 4-6 s).
# poster = still image shown before play. drug = related profile slug.

VIDEOS = [
 dict(slug="cocaine-powder", title="What does cocaine powder look like?",
      drug="cocaine", duration="0:05",
      video="https://plugreports.com/media/videos/cocaine-powder.mp4",
      poster="https://plugreports.com/media/drugs/cocaine.jpeg",
      desc="Close-up: typical street cocaine — off-white, clumpy crystalline powder with a slight shine. Pure-looking white rocks or powder say nothing about purity: cuts are invisible."),
 dict(slug="heroin-powder", title="What does heroin look like?",
      drug="heroin", duration="0:05",
      video="https://plugreports.com/media/videos/heroin-powder.mp4",
      poster="https://plugreports.com/media/drugs/heroin.jpeg",
      desc="Close-up: typical street heroin — tan to brown powder (or dark 'tar' in the western US). Color tells you nothing about strength: fentanyl is invisible in any of it."),
 dict(slug="mdma-crystals", title="What do MDMA crystals look like?",
      drug="mdma", duration="0:05",
      video="https://plugreports.com/media/videos/mdma-crystals.mp4",
      poster="https://plugreports.com/media/drugs/mdma.jpeg",
      desc="Close-up: typical MDMA — translucent amber-to-brown crystal shards ('molly' powder is the same crystals crushed). Color varies batch to batch and proves nothing."),
]
