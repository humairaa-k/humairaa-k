#!/usr/bin/env python3
"""Generate name.svg — a self-typing, monochrome name banner.

Same technique as the original portrait: GitHub strips <script> from
READMEs, so the typewriter effect is done with SMIL — a clipPath rect
that widens over time, plus a small cursor block riding its edge.

    python3 scripts/make_name_banner.py

Produces name.svg at the repo root.
"""
import os

TEXT = "Humaira Khaliq  </>"   # name + coder-vibe mark; edit freely
# Coder-vibe alternatives to swap in for the mark above, if you'd rather:
#   <>   {}   ⌘   ✦   ⚡   ~/

FG_LIGHT = "#6e7681"
FG_DARK = "#c9d1d9"
FONT_SIZE = 22
CHAR_W = FONT_SIZE * 0.6          # monospace advance width
LINE_H = FONT_SIZE + 10
PAD = 14
CHAR_DELAY = 0.09                 # seconds per character
FAMILY = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"


def build_svg(text):
    width = int(len(text) * CHAR_W + PAD * 2)
    height = LINE_H + PAD * 2
    y = PAD + LINE_H / 2

    total_w = len(text) * CHAR_W
    safe = (text.replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;"))

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
         f'height="{height}" viewBox="0 0 {width} {height}" '
         f'font-family="{FAMILY}">',
         f'<style>.a{{fill:{FG_LIGHT}}}'
         f'@media(prefers-color-scheme:dark){{.a{{fill:{FG_DARK}}}}}</style>']

    dur = f"{len(text) * CHAR_DELAY:.2f}s"

    p.append(f'<clipPath id="c0"><rect x="{PAD}" y="{PAD}" '
              f'height="{LINE_H}" width="0">'
              f'<animate attributeName="width" from="0" to="{total_w:.1f}" '
              f'begin="0s" dur="{dur}" fill="freeze"/>'
              f'</rect></clipPath>')
    p.append(f'<g clip-path="url(#c0)"><text xml:space="preserve" '
              f'x="{PAD}" y="{y + FONT_SIZE * 0.35:.1f}" class="a" '
              f'font-size="{FONT_SIZE}">{safe}</text></g>')

    # blinking-block cursor riding the wipe edge, then blinking in place
    end = f"{len(text) * CHAR_DELAY:.2f}s"
    p.append(f'<rect y="{PAD + 2}" width="{FONT_SIZE * 0.55:.1f}" '
              f'height="{FONT_SIZE}" class="a">'
              f'<animate attributeName="x" from="{PAD}" '
              f'to="{PAD + total_w:.1f}" begin="0s" dur="{dur}" '
              f'fill="freeze"/>'
              f'<animate attributeName="opacity" values="1;0;1" '
              f'dur="1s" begin="{end}" repeatCount="indefinite"/>'
              f'</rect>')

    p.append("</svg>")
    return "".join(p)


def main():
    out_dir = os.environ.get("OUT_DIR", ".")
    with open(os.path.join(out_dir, "name.svg"), "w") as f:
        f.write(build_svg(TEXT))
    print("wrote name.svg")


if __name__ == "__main__":
    main()
