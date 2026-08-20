#!/usr/bin/env python3
"""Generate name.svg — an ASCII block-letter banner, self-drawing row by row.

Same visual language as the original portrait (ascii.svg): monospace grey
ink, transparent background, and a row-by-row reveal done in SMIL, since
GitHub strips <script> from READMEs. Instead of a photo, the "art" is your
name rendered as block letters via pyfiglet.

    pip install pyfiglet
    python3 scripts/make_name_banner.py

Produces name.svg at the repo root.
"""
import os
import pyfiglet

NAME = "HUMAIRA KHALIQ"
FONT = "small"          # pyfiglet font; try "standard" or "straight" too
TAG = "</>"              # small coder-vibe mark under the name

FG_LIGHT = "#6e7681"
FG_DARK = "#c9d1d9"
CHAR_W = 7.74             # monospace advance width, JetBrains-Mono-ish
FONT_SIZE = 12.9
LINE_H = 15
PAD = 14
ROW_DELAY = 0.09          # seconds per row, same cadence as the portrait
FAMILY = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"


def to_lines():
    art = pyfiglet.figlet_format(NAME, font=FONT)
    lines = art.rstrip("\n").split("\n")
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    lines.append("")
    lines.append(TAG.center(max(len(l) for l in lines)))
    return lines


def build_svg(lines):
    cols = max(len(l) for l in lines) if lines else 0
    width = int(cols * CHAR_W + PAD * 2)
    height = len(lines) * LINE_H + PAD * 2

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
         f'height="{height}" viewBox="0 0 {width} {height}" '
         f'font-family="{FAMILY}">',
         f'<style>.a{{fill:{FG_LIGHT}}}'
         f'@media(prefers-color-scheme:dark){{.a{{fill:{FG_DARK}}}}}</style>']

    for i, line in enumerate(lines):
        y = PAD + i * LINE_H
        begin = f"{i * ROW_DELAY:.2f}s"
        end = f"{(i + 1) * ROW_DELAY:.2f}s"
        w = max(len(line), 1) * CHAR_W
        safe = (line.replace("&", "&amp;").replace("<", "&lt;")
                    .replace(">", "&gt;"))
        if not safe.strip():
            continue

        p.append(f'<clipPath id="c{i}"><rect x="{PAD}" y="{y}" '
                  f'height="{LINE_H}" width="0">'
                  f'<animate attributeName="width" from="0" to="{w:.1f}" '
                  f'begin="{begin}" dur="{ROW_DELAY}s" fill="freeze"/>'
                  f'</rect></clipPath>')
        p.append(f'<g clip-path="url(#c{i})"><text xml:space="preserve" '
                  f'x="{PAD}" y="{y + 11.2:.1f}" class="a" '
                  f'font-size="{FONT_SIZE}">{safe}</text></g>')
        p.append(f'<rect y="{y + 1}" width="6" height="12" class="a" '
                  f'opacity="0">'
                  f'<animate attributeName="x" from="{PAD}" to="{PAD + w:.1f}" '
                  f'begin="{begin}" dur="{ROW_DELAY}s" fill="freeze"/>'
                  f'<set attributeName="opacity" to="0.8" begin="{begin}"/>'
                  f'<set attributeName="opacity" to="0" begin="{end}"/></rect>')

    p.append("</svg>")
    return "".join(p)


def main():
    out_dir = os.environ.get("OUT_DIR", ".")
    lines = to_lines()
    svg = build_svg(lines)
    with open(os.path.join(out_dir, "name.svg"), "w") as f:
        f.write(svg)
    print("wrote name.svg")


if __name__ == "__main__":
    main()
