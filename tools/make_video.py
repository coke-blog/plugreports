#!/usr/bin/env python3
"""plugreports explainer-video generator: drug profile -> branded 9:16 MP4 for TikTok/Shorts.
Usage: python3 tools/make_video.py <slug> [<slug> ...]   (outputs to /mnt/agents/output/videos/)
Requires: PIL, gTTS, moviepy, ffmpeg. Slides: hook -> appearance -> effects -> risks -> overdose+response -> CTA."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from data_drugs import DRUGS

W, H = 1080, 1920
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
OUT = "/mnt/agents/output/videos"
os.makedirs(OUT, exist_ok=True)

HOOKS = {
 "fentanyl": ("2 milligrams of fentanyl can kill you.", "That's a few grains of salt. And it's in pills everywhere."),
 "nitrous-oxide": ("The party drug leaving teens unable to walk.", "Whippets and Galaxy Gas destroy vitamin B12 — and your nerves."),
}
HOOK_AUDIO = {
 "fentanyl": "Two milligrams of fentanyl can kill you. That's a few grains of salt. And it's hiding in pills everywhere.",
 "nitrous-oxide": "The party drug that's leaving teenagers unable to walk. Whippits and Galaxy Gas destroy vitamin B twelve, and your nerves along with it.",
}

def esc(s): return s

def slide_base(draw):
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new("RGB", (W, H), (12, 17, 33))  # dark slate
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 220], fill=(185, 28, 28))
    f = ImageFont.truetype(FB, 40)
    d.text((60, 80), "plugreports", font=f, fill=(255, 255, 255))
    f2 = ImageFont.truetype(FB, 26)
    d.text((60, 135), "harm reduction saves lives", font=f2, fill=(252, 165, 165))
    return img, d

def txt(d, xy, s, size, color=(255,255,255), maxw=960):
    from PIL import ImageFont
    f = ImageFont.truetype(FB, size)
    words = s.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if d.textlength(t, font=f) <= maxw: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    y=xy[1]
    for ln in lines:
        d.text((xy[0], y), ln, font=f, fill=color); y += int(size*1.4)
    return y

def build_slides(drug):
    from PIL import ImageDraw
    name = drug["name"].split("(")[0].strip()
    s = []
    hook = HOOKS.get(drug["slug"], (drug["risks"][0], name))
    img, d = slide_base(None); y = txt(d, (60, 300), hook[0], 74, (255,255,255)); txt(d, (60, y+30), hook[1], 44, (252, 165, 165)); s.append((img, HOOK_AUDIO.get(drug["slug"], f"{hook[0]} {hook[1]}")))
    img, d = slide_base(None); y = txt(d, (60, 300), name.upper(), 58, (245, 158, 11)); y = txt(d, (60, y+40), "WHAT IT LOOKS LIKE", 44); txt(d, (60, y+30), drug["appearance"], 40, (203, 213, 225)); s.append((img, f"What is {name}? {drug['appearance']}"))
    img, d = slide_base(None); y = txt(d, (60, 300), "WHAT IT DOES", 56, (245, 158, 11))
    for e in drug["effects"][:3]: y = txt(d, (60, y+40), "• " + e, 40) + 6
    s.append((img, "What it does. " + ". ".join(drug["effects"][:3])))
    img, d = slide_base(None); y = txt(d, (60, 300), "THE RISKS", 56, (220, 38, 38))
    for r in drug["risks"][:4]: y = txt(d, (60, y+40), "• " + r, 34) + 4
    s.append((img, "The risks. " + ". ".join(drug["risks"][:3])))
    img, d = slide_base(None); y = txt(d, (60, 300), "OVERDOSE SIGNS", 56, (220, 38, 38))
    for o in drug["overdoseSigns"][:3]: y = txt(d, (60, y+40), "• " + o, 36) + 4
    y = txt(d, (60, y+60), "CALL EMERGENCY SERVICES. GIVE NALOXONE FOR OPIOOD-LIKE SIGNS. STAY.", 38, (245, 158, 11))
    s.append((img, "Overdose signs. " + ". ".join(drug["overdoseSigns"][:3]) + ". If this happens: call emergency services, give naloxone for opioid-like signs, and stay with the person."))
    img, d = slide_base(None); y = txt(d, (60, 420), "Free, sourced drug info", 62); y = txt(d, (60, y+50), f"plugreports.com/drugs/{drug['slug']}", 48, (245, 158, 11)); txt(d, (60, y+40), "Know the drug. Know the risk. Know the way out.", 36, (203, 213, 225))
    s.append((img, f"Full profile free at plugreports dot com slash drugs slash {drug['slug']}. Know the drug, know the risk, know the way out."))
    return s

def make(slug):
    from gtts import gTTS
    from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
    drug = next(d for d in DRUGS if d["slug"] == slug)
    slides = build_slides(drug)
    clips = []
    tmp = []
    for i, (img, narration) in enumerate(slides):
        ip = f"/tmp/sl_{slug}_{i}.png"; ap = f"/tmp/sl_{slug}_{i}.mp3"
        img.save(ip)
        gTTS(narration, lang="en", tld="com").save(ap)
        tmp += [ip, ap]
        a = AudioFileClip(ap)
        clips.append(ImageClip(ip, duration=a.duration + 0.4).with_audio(a))
    out = os.path.join(OUT, f"{slug}.mp4")
    concatenate_videoclips(clips, method="compose").write_videofile(out, fps=24, codec="libx264", audio_codec="aac", preset="medium", threads=4)
    for f in tmp: os.remove(f)
    print(out, round(os.path.getsize(out)/1048576, 1), "MB")

if __name__ == "__main__":
    for slug in sys.argv[1:]:
        make(slug)
