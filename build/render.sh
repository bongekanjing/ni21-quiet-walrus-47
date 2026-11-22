#!/usr/bin/env bash
# Render build/poster.html to entry.png at a fixed 1024x1024, and prove the
# screenshot really is that size before overwriting the committed image.
set -euo pipefail

CHROME=${CHROME:-/root/.cache/ms-playwright/chromium-1255/chrome-linux64/chrome}
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(dirname "$HERE")"
RAW="${TMPDIR:-/tmp}/ni21_raw.png"

python3 "$HERE/poster.py"

"$CHROME" \
  --headless=new --no-sandbox --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 \
  --window-size=1024,1024 \
  --virtual-time-budget=6000 \
  --screenshot="$RAW" "file://$HERE/poster.html"

python3 - "$RAW" "$ROOT/entry.png" <<'PY'
import sys
from PIL import Image

raw, out = sys.argv[1], sys.argv[2]
im = Image.open(raw).convert("RGB")
if im.size != (1024, 1024):
    sys.exit("screenshot is %dx%d, expected 1024x1024" % im.size)

# The page must not have spilled: a full-bleed background is one colour, so any
# row of the outer 3px frame that differs from the corner pixel means overflow.
corner = im.getpixel((2, 2))
px = im.load()
bad = 0
for y in range(1024):
    for x in (0, 1, 1022, 1023):
        if px[x, y] != corner:
            bad += 1
if bad:
    sys.exit("%d pixels of the outer frame are not the page background" % bad)

im.save(out, "PNG", optimize=True)
print("entry.png %d bytes %dx%d" % (len(open(out, "rb").read()), im.size[0], im.size[1]))
PY
