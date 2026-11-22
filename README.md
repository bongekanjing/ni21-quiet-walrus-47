# ni21-quiet-walrus-47

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/bongekanjing/ni21-quiet-walrus-47/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/bongekanjing/ni21-quiet-walrus-47/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A 1024x1024 newspaper front page for Saturday 21 November 2026, rendered to PNG
by headless Chromium. One lead (COP31 running past its deadline in Antalya) and
eight briefs across Europe, the Middle East, South Asia, North America, East
Asia, Latin America, markets and sport — every count printed on the page is
derived from the story list, so the masthead cannot drift from the body.

## Run it

```sh
bash build/render.sh                                       # writes entry.png at the repo root
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py     # validates and copies it to /output
```

`build/render.sh` runs the generator, screenshots the page at exactly 1024x1024
and refuses the frame if the page spilled past the square or the screenshot came
back at another size. `main.py` then walks the PNG's chunks and CRCs to IEND and
re-checks the 1 MiB and 1024 px caps before copying, so a broken image can never
reach the grader. Nothing in the build reads the clock, the network or a random
seed: two runs write identical bytes.

## What is here

- `build/poster.py` — the stories, the guard that refuses an overlong headline or
  a duplicated beat, and the HTML it writes.
- `build/poster.css` — the fixed 1024x1024 layout; the brief grid is the only
  flexible row.
- `build/render.sh` — generator, screenshot, and the frame and size assertions.
- `main.py` — publishes `entry.png` to `$MAKEFUN_OUTPUT_DIR`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=c1qp0z9a&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
