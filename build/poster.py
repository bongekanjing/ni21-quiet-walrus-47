#!/usr/bin/env python3
"""Generate the front page for Saturday 21 November 2026.

The page is drawn for one viewing size that matters: a 1024 square seen at
about 300 pixels across. So the sheet carries one lead and eight briefs, each
headline big enough to read as a thumbnail, and everything else of the day in
the ticker.

BRIEFS is the only place stories live. The generator counts them for the
masthead, refuses to write a page whose parts disagree, and refuses a headline
or gloss too long for the column it has to fit - so a build that would spill
fails loudly instead of shipping a broken page.
"""

import html
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
DAY = "SATURDAY 21 NOVEMBER 2026"

LEAD = {
    "kicker": "CLIMATE \u00b7 ANTALYA",
    "headline": "COP31 blows past its deadline",
    "dek": "A third draft is on the table, objections are due by 03:00 GMT, and the "
           "plenary that could approve it is set for 06:00 GMT on Sunday.",
    "body": "Negotiators sat through Saturday after a draft drew fire for never naming "
            "fossil fuels. President Murat Kurum says the new package answers that and "
            "the quarrel over adaptation\u00a0finance. Australia leads the talks, Turkey "
            "hosts them, and the hall has yet to say yes.",
}

# beat -> (headline, one short line of gloss)
BRIEFS = [
    ("EUROPE", "Kyiv sets terms for talks",
     "Zelensky wants a written agenda before the next round"),
    ("MIDDLE EAST", "Iran: Russia backs doctrine",
     "Araghchi says both oppose any change; inspectors barred"),
    ("SOUTH ASIA", "Tainted liquor kills 13",
     "300+ hospitalised in Manipur since 18 November"),
    ("NORTH AMERICA", "No treaty on killer robots",
     "Geneva talks end with a two-year study, not a mandate"),
    ("EAST ASIA", "Snow cuts off a village",
     "Fallen trees isolate 1,400 people in Fukushima"),
    ("LATIN AMERICA", "One plan for El Ni\u00f1o urged",
     "World Bank flags La Plata floods, Dry Corridor drought"),
    ("MARKETS", "Bitcoin stuck below $60k",
     "Seventh straight weekly fall as the AI rout spreads"),
    ("SPORT", "Rahul rewrites the record",
     "First Indian opener with a ton in each SENA country"),
]

CREDIT = "Reporting: Reuters, AP, Kyodo, The Hindu, Yonhap"

UNIQUE_BEATS = {"EUROPE", "MIDDLE EAST", "SOUTH ASIA", "NORTH AMERICA",
                "EAST ASIA", "LATIN AMERICA", "MARKETS", "SPORT"}


def check():
    """Refuse to build a page whose parts contradict each other."""
    beats = [b[0] for b in BRIEFS]
    if len(set(beats)) != len(beats):
        sys.exit("a beat appears twice")
    if set(beats) != UNIQUE_BEATS:
        sys.exit("beats drifted: %s" % sorted(set(beats) ^ UNIQUE_BEATS))
    for beat, headline, gloss in BRIEFS:
        if not headline.strip() or not gloss.strip():
            sys.exit("empty brief in %s" % beat)
        if len(headline) > 28:
            sys.exit("headline too long for the column in %s: %r" % (beat, headline))
        if len(gloss) > 62:
            sys.exit("gloss too long for one line in %s: %d chars" % (beat, len(gloss)))
    if len(BRIEFS) % 2:
        sys.exit("briefs must fill whole rows of the two-column grid")


def glyph(beat):
    """One flat mark per beat, drawn in a single 24x24 box, one stroke weight."""
    paths = {
        "EUROPE": '<circle cx="12" cy="12" r="8.5"/><path d="M12 3.5v17M3.5 12h17"/>',
        "MIDDLE EAST": '<circle cx="12" cy="12" r="8.5"/><path d="M12 3.5a8.5 8.5 0 0 0 0 17"/>',
        "EAST ASIA": '<path d="M12 3v18M3.5 11.5L12 3l8.5 8.5"/>',
        "SOUTH ASIA": '<path d="M12 3.5l8.5 15.5h-17z"/><path d="M8 14h8"/>',
        "NORTH AMERICA": '<rect x="3.5" y="6" width="17" height="12" rx="2"/><path d="M7.5 12h9"/>',
        "LATIN AMERICA": '<path d="M3.5 15c3-7.5 6 3 8.5-2.5s5.5 3.5 8.5-3.5"/>',
        "MARKETS": '<path d="M3.5 19l6-8 4 4 6.5-9.5"/><path d="M15 5.5h5V11"/>',
        "SPORT": '<circle cx="12" cy="12" r="8.5"/><path d="M12 3.5v17M6 7.5l12 9"/>',
    }
    return ('<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="#e9b95c" '
            'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">%s</svg>'
            % paths[beat])


def build():
    check()
    cards = "\n".join(
        """      <article class="brief">
        <div class="tag">{glyph}<span>{beat}</span></div>
        <h3>{headline}</h3>
        <p>{gloss}</p>
      </article>""".format(
            glyph=glyph(beat),
            beat=html.escape(beat),
            headline=html.escape(headline),
            gloss=html.escape(gloss),
        )
        for beat, headline, gloss in BRIEFS
    )
    tick = '<span class="credit">%s</span>' % html.escape(CREDIT)

    page = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>The World in One Page \u2014 21 November 2026</title>
<style>{css}</style></head>
<body>
<div class="page">
  <header class="masthead">
    <div class="top-rule"></div>
    <h1>THE WORLD IN ONE PAGE</h1>
    <div class="dateline">{day}</div>
    <div class="strap">{n} stories \u00b7 {b} beats \u00b7 one Saturday, everywhere</div>
    <div class="bot-rule"></div>
  </header>

  <section class="lead">
    <div class="lead-text">
      <div class="kicker">{kicker}</div>
      <h2>{headline}</h2>
      <p class="dek">{dek}</p>
      <p class="body">{body}</p>
    </div>
    <figure class="lead-art">
      <svg viewBox="0 0 160 160" fill="none" stroke="#f3efe2" stroke-width="3.4">
        <circle cx="80" cy="80" r="66"/>
        <path d="M14 80h132M80 14c22 21 22 111 0 132M80 14c-22 21-22 111 0 132"/>
        <path d="M28 46c26 16 78 16 104 0M28 114c26-16 78-16 104 0"/>
      </svg>
      <figcaption>The hall in Antalya</figcaption>
    </figure>
  </section>

  <section class="grid">
{cards}
  </section>

  <footer class="ticker"><span class="label">21 NOVEMBER 2026</span> {tick}</footer>
</div>
</body></html>
""".format(
        css=(HERE / "poster.css").read_text(),
        day=DAY,
        n=len(BRIEFS) + 1,
        b=len(BRIEFS) + 1,
        kicker=html.escape(LEAD["kicker"]),
        headline=html.escape(LEAD["headline"]),
        dek=html.escape(LEAD["dek"]),
        body=html.escape(LEAD["body"]),
        cards=cards,
        tick=tick,
    )

    out = HERE / "poster.html"
    out.write_text(page)
    print("wrote %s (%d bytes, %d stories, %d beats)"
          % (out, len(page), len(BRIEFS) + 1, len(BRIEFS) + 1))


if __name__ == "__main__":
    build()
