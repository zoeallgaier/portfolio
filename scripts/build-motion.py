#!/usr/bin/env python3
"""
build-motion.py — cuts the home-card video covers (including the Motion Reel
card) from the clips already published under _projects/.

Usage:
    python3 scripts/build-motion.py            # everything
    python3 scripts/build-motion.py reel       # just the Motion Reel card
    python3 scripts/build-motion.py cards      # just the card covers
    python3 scripts/build-motion.py posters    # posters for clips without one
    python3 scripts/build-motion.py masters    # web cuts of the big masters in _source/, plus home-card cuts

Needs ffmpeg on PATH (brew install ffmpeg).

Everything is driven by the lists below: REEL is the short cut on the Motion
Reel card (motion.html itself shows every clip separately), CARDS are the
loops that replace still covers on the home page. Edit a start time or a
duration and re-run.

Layouts
  full   a 16:9 clip, filling the frame
  fit    a square or near-square clip, centred over a blurred copy of itself
  pair   two clips side by side (vertical social cuts, a sponsor slide beside
         its welcome graphic), over a blurred copy of the first
"""
import json, pathlib, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
P = ROOT / "_projects"
OUT = P / "Motion"

# (layout, [(clip, start s)], duration s)
REEL = [
    ("full", [("Freelance/Victig-outro.mp4", 0.4)], 3.0),   # green wipe 0.5–1.5 s, logo settled by 2.75 s
    ("full", [("PSB26/PSB26-afteropen.mp4", 5.0)], 6.6),     # Utah is growing, the 3.6M → 5.6M line
    ("full", [("Any Hour Services/along-for-the-ride-intro-2021.mp4", 2.4)], 7.5),  # red wipe, title words, the truck
]

# name -> (layout, [(clip, start s)], duration s)
# e.g. "evergreen-card": ("fit", [("UVU/studentstories.mp4", 0.0)], 13.4)
CARDS = {}

# Posters for clips that had none: clip -> time of a frame that reads on its own.
POSTERS = {
    "Freelance/ShiftShapers intro v9.mp4": 8.2,
    "Freelance/Victig-outro.mp4": 3.5,
    "UVU/nextlevel.mp4": 3.0,
    "Freelance/Intro-blank.mp4": 2.0,
}

# Masters too big to publish (in _source/ or gitignored under _projects/),
# relative to the repo root -> web cut in _projects/<folder>/.
MASTERS = {
    "_source/Motion/2024-BirthdayVideo-12fps_v3.mp4": "Motion/uvu-birthday-2024",
    "_source/Freelance/strangerthingsFINAL.mp4": "Motion/strangerthings-title",
    "_projects/Any Hour Services/Along for the Ride Intro 2021.mp4": "Any Hour Services/along-for-the-ride-intro-2021",
}
CARD_CUTS = {
    "_projects/Any Hour Services/Along for the Ride Intro 2021.mp4": "Any Hour Services/along-for-the-ride-intro-2021-card",
    "_projects/PSB26/PSB26-PSBlogo.mp4": "PSB26/PSB26-PSBlogo-card",
}
POSTER_AT = {"Motion/uvu-birthday-2024": 10.5, "Motion/strangerthings-title": 33.8,
             "Any Hour Services/along-for-the-ride-intro-2021": 1.1}

FPS = 30
XFADE = 0.3     # crossfade between reel cuts, s
GAP = 24        # px between the two halves of a pair, at 1080p


def run(args):
    subprocess.run(args, check=True)


def dims(clip):
    j = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height", "-of", "json", str(P / clip)],
        capture_output=True, text=True, check=True).stdout)
    s = j["streams"][0]
    return s["width"], s["height"]


def even(x):
    return int(round(x / 2)) * 2


def segment(layout, clips, dur, W, H, out):
    """Render one segment to a high-quality intermediate at W×H, FPS."""
    args = ["ffmpeg", "-v", "error", "-y"]
    for clip, start in clips:
        args += ["-ss", f"{start:.3f}", "-t", f"{dur:.3f}", "-i", str(P / clip)]
    norm = f"fps={FPS},format=yuv420p,setsar=1"
    # Blurred backdrop from the first clip: shrink, blur, scale back up, dim.
    bg = (f"[0:v]scale=480:{even(480 * H / W)}:force_original_aspect_ratio=increase,"
          f"crop=480:{even(480 * H / W)},boxblur=14:2,scale={W}:{H},"
          f"eq=brightness=-0.12:saturation=1.05[bg]")
    if layout == "full":
        fc = f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},{norm}[v]"
    elif layout == "fit":
        fc = (f"[0:v]split[a][b];{bg.replace('[0:v]', '[a]')};"
              f"[b]scale=-2:{H}[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2:eof_action=repeat,{norm}[v]")
    elif layout == "pair":
        (w0, h0), (w1, h1) = dims(clips[0][0]), dims(clips[1][0])
        a, b = even(w0 * H / h0), even(w1 * H / h1)
        gap = even(GAP * H / 1080)
        x0 = (W - (a + gap + b)) // 2
        fc = (f"[0:v]split[a][l];{bg.replace('[0:v]', '[a]')};"
              f"[l]scale={a}:{H}[L];[1:v]scale={b}:{H}[R];"
              f"[bg][L]overlay={x0}:0:eof_action=repeat[t];"
              f"[t][R]overlay={x0 + a + gap}:0:eof_action=repeat,{norm}[v]")
    else:
        raise ValueError(layout)
    args += ["-filter_complex", fc, "-map", "[v]", "-an", "-t", f"{dur:.3f}",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", str(out)]
    run(args)


def encode(src, out, W, crf):
    run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf", f"scale={W}:-2:flags=lanczos",
         "-an", "-c:v", "libx264", "-preset", "slow", "-crf", str(crf), "-profile:v", "high",
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)])


def poster(src, t, out, W):
    # Homebrew's ffmpeg has no WebP encoder, so grab a PNG and let Pillow
    # write the WebP (as scripts/optimize-images.py does for stills).
    from PIL import Image
    png = out.with_suffix(".png")
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(src), "-frames:v", "1",
         "-vf", f"scale='min({W},iw)':-2:flags=lanczos", str(png)])   # never upscale
    Image.open(png).convert("RGB").save(out, "WEBP", quality=82, method=6)
    png.unlink()


def build_reel(tmp):
    W, H = 1280, 720
    parts, durs = [], []
    for i, (layout, clips, dur) in enumerate(REEL):
        out = tmp / f"reel-{i:02d}.mp4"
        segment(layout, clips, dur, W, H, out)
        parts.append(out)
        durs.append(dur)

    # Chain the cuts with short crossfades; it loops on the card, so no fade to black.
    args = ["ffmpeg", "-v", "error", "-y"]
    for p in parts:
        args += ["-i", str(p)]
    chain, prev, t = [], "[0:v]", durs[0]
    for i in range(1, len(parts)):
        t -= XFADE
        chain.append(f"{prev}[{i}:v]xfade=transition=fade:duration={XFADE}:offset={t:.3f}[x{i}]")
        prev = f"[x{i}]"
        t += durs[i]
    total = t
    chain.append(f"{prev}null[v]")
    master = tmp / "reel-master.mp4"
    run(args + ["-filter_complex", ";".join(chain), "-map", "[v]", "-an",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", str(master)])

    encode(master, OUT / "motion-card.mp4", W, 28)
    # The cut opens on the Victig outro's wipe before the logo resolves, so
    # the poster is the finished logo on charcoal instead.
    poster(master, 2.0, OUT / "motion-card-poster.webp", W)
    print(f"reel card: {total:.1f}s")


def build_cards(tmp):
    W, H = 1280, 720
    for name, (layout, clips, dur) in CARDS.items():
        raw = tmp / f"{name}.mp4"
        segment(layout, clips, dur, W, H, raw)
        encode(raw, OUT / f"{name}.mp4", W, 28)
        poster(raw, 0.0, OUT / f"{name}-poster.webp", W)
        print(f"card: {name} {dur:.1f}s")


def web_cut(src, out, W):
    run(["ffmpeg", "-v", "error", "-y", "-i", str(src),
         "-vf", f"scale={W}:-2:flags=lanczos,fps='min({FPS},source_fps)'",
         "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "28", "-profile:v", "high",
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)])


def build_masters():
    # crf 28: at 26 the Stranger Things title came out 7.6MB and the 2021
    # opener 4.6MB; 28 is ~30% lighter with no visible change on either.
    for src, name in MASTERS.items():
        out = P / f"{name}.mp4"
        web_cut(ROOT / src, out, 1920)
        poster(out, POSTER_AT.get(name, 1.0), P / f"{name}-poster.webp", 1280)
        print(f"master: {out.relative_to(P)}")
    # 720p cuts for the home cards, which are a quarter of the window at most.
    # Each shares its full clip's poster.
    for src, name in CARD_CUTS.items():
        out = P / f"{name}.mp4"
        web_cut(ROOT / src, out, 1280)
        print(f"card cut: {out.relative_to(P)}")


def build_posters():
    for clip, t in POSTERS.items():
        src = P / clip
        out = src.with_name(src.stem.replace(" ", "-") + "-poster.webp")
        poster(src, t, out, 1280)
        print(f"poster: {out.relative_to(P)}")


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    OUT.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as d:
        tmp = pathlib.Path(d)
        if what in ("all", "reel"):
            build_reel(tmp)
        if what in ("all", "cards"):
            build_cards(tmp)
        if what in ("all", "posters"):
            build_posters()
        if what in ("all", "masters"):
            build_masters()
