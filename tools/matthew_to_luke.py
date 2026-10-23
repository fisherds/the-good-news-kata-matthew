"""Draw where each verse of Matthew 5:1-7:29 turns up anywhere in Luke.

Companion to luke_parallels.py (which only looks at Luke 6:20-49). Writes
public/images/matthew-to-luke.svg; render the PNG with headless Chrome
(see the bottom of this file).

Usage: python3 tools/matthew_to_luke.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from luke_parallels import CHAPTER_LENGTHS, LEFT, SECTIONS, esc, matt_x, section_of  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public", "images", "matthew-to-luke.svg")

LUKE_LENGTHS = [80, 52, 38, 44, 39, 49, 50, 56, 62, 42, 54, 59,
                35, 35, 32, 31, 37, 43, 48, 47, 38, 71, 56, 53]

# Matthew verse -> Luke (chapter, verse) parallels (standard synopsis parallels).
MATT_TO_LUKE = {
    (5, 2): [(6, 20)],
    (5, 3): [(6, 20)], (5, 4): [(6, 21)], (5, 6): [(6, 21)],
    (5, 11): [(6, 22)], (5, 12): [(6, 23)],
    (5, 13): [(14, 34), (14, 35)],
    (5, 15): [(8, 16), (11, 33)],
    (5, 18): [(16, 17)],
    (5, 25): [(12, 58)], (5, 26): [(12, 59)],
    (5, 32): [(16, 18)],
    (5, 39): [(6, 29)], (5, 40): [(6, 29)], (5, 42): [(6, 30), (6, 34)],
    (5, 44): [(6, 27), (6, 28), (6, 35)], (5, 45): [(6, 35)],
    (5, 46): [(6, 32)], (5, 47): [(6, 33)], (5, 48): [(6, 36)],
    (6, 9): [(11, 2)], (6, 10): [(11, 2)], (6, 11): [(11, 3)],
    (6, 12): [(11, 4)], (6, 13): [(11, 4)],
    (6, 19): [(12, 33)], (6, 20): [(12, 33)], (6, 21): [(12, 34)],
    (6, 22): [(11, 34)], (6, 23): [(11, 34), (11, 35)],
    (6, 24): [(16, 13)],
    (6, 25): [(12, 22), (12, 23)], (6, 26): [(12, 24)], (6, 27): [(12, 25)],
    (6, 28): [(12, 26), (12, 27)], (6, 29): [(12, 27)], (6, 30): [(12, 28)],
    (6, 31): [(12, 29)], (6, 32): [(12, 30)], (6, 33): [(12, 31)],
    (7, 1): [(6, 37)], (7, 2): [(6, 38)], (7, 3): [(6, 41)],
    (7, 4): [(6, 42)], (7, 5): [(6, 42)],
    (7, 7): [(11, 9)], (7, 8): [(11, 10)], (7, 9): [(11, 11)],
    (7, 10): [(11, 12)], (7, 11): [(11, 13)],
    (7, 12): [(6, 31)],
    (7, 13): [(13, 24)], (7, 14): [(13, 24)],
    (7, 16): [(6, 44)], (7, 17): [(6, 43)], (7, 18): [(6, 43)],
    (7, 19): [(3, 9)],  # John the Baptist's version of the saying
    (7, 20): [(6, 44)], (7, 21): [(6, 46)],
    (7, 22): [(13, 26)], (7, 23): [(13, 27)],
    (7, 24): [(6, 47), (6, 48)], (7, 25): [(6, 48)],
    (7, 26): [(6, 49)], (7, 27): [(6, 49)],
    (7, 28): [(7, 1), (4, 32)], (7, 29): [(4, 32)],
}

# Colors for the Luke chapters that receive lines.
LUKE_COLORS = {6: "#1f1b2e", 11: "#e07b00", 12: "#0a9396", 13: "#c0392b",
               14: "#5b8c00", 16: "#7b4ab8", 8: "#b08900", 3: "#6b7384",
               4: "#6b7384", 7: "#6b7384"}
LUKE_NOTES = {
    3: "John: axe at the root", 4: "taught with authority", 6: "Sermon on the Plain",
    7: "finished his sayings", 8: "lamp", 11: "Lord's Prayer · lamp · ask, seek, knock",
    12: "treasure · worry · settle on the way", 13: "narrow door · “depart from me”",
    14: "salt", 16: "law · divorce · two masters",
}

W, H = 1920, 900
MATT_Y, MATT_H = 190, 30
LUKE_Y, LUKE_H = 640, 44


def main():
    mx, right = matt_x()
    span = right - LEFT
    total = sum(LUKE_LENGTHS)
    gap = 3
    per_verse = (span - gap * (len(LUKE_LENGTHS) - 1)) / total
    ch_x, x = {}, LEFT
    for ch, n in enumerate(LUKE_LENGTHS, 1):
        ch_x[ch] = (x, n * per_verse)
        x += n * per_verse + gap

    def luke_x(ch, v):
        x0, _ = ch_x[ch]
        return x0 + (v - 0.5) * per_verse

    out = []
    add = out.append
    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        'font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, Helvetica, Arial, sans-serif">')
    add(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
    add(f'<text x="{LEFT}" y="52" font-size="30" font-weight="700" fill="#1f1b2e">'
        "Matthew's Sermon on the Mount → all of Luke</text>")
    add(f'<text x="{LEFT}" y="84" font-size="18" fill="#6b6580">'
        "Each verse of Matthew 5:1–7:29 linked to wherever Luke has the same teaching. "
        "Matthew 6 is there — scattered through Luke 11–12.</text>")

    for ch, n in CHAPTER_LENGTHS.items():
        a, b = mx[(ch, 1)], mx[(ch, n)] + 15
        add(f'<text x="{(a + b) / 2}" y="{MATT_Y - 62}" text-anchor="middle" font-size="18" '
            f'font-weight="700" fill="#1f1b2e">Matthew {ch}</text>')
    for start, end, name, color in SECTIONS:
        a, b = mx[start], mx[end] + 15
        add(f'<line x1="{a}" y1="{MATT_Y - 10}" x2="{b}" y2="{MATT_Y - 10}" stroke="{color}" stroke-width="3"/>')
        if b - a > 40:
            add(f'<text x="{(a + b) / 2}" y="{MATT_Y - 18}" text-anchor="middle" font-size="13" '
                f'font-weight="600" fill="{color}">{esc(name)}</text>')

    # Lines, colored by the Luke chapter they land in
    hits = {}
    for ref, targets in MATT_TO_LUKE.items():
        for lch, lv in targets:
            hits.setdefault(lch, set()).add(lv)
            x1, y1 = mx[ref] + 7.5, MATT_Y + MATT_H
            x2, y2 = luke_x(lch, lv), LUKE_Y
            color = LUKE_COLORS[lch]
            add(f'<path d="M{x1:.1f},{y1} C{x1:.1f},{y1 + 200} {x2:.1f},{y2 - 200} {x2:.1f},{y2}" '
                f'fill="none" stroke="{color}" stroke-width="2" stroke-opacity="0.7"/>')

    # Matthew cells: filled if Luke has it somewhere
    for (ch, v), x in mx.items():
        _, color = section_of(ch, v)
        hit = (ch, v) in MATT_TO_LUKE
        fill = color if hit else "#ffffff"
        add(f'<rect x="{x}" y="{MATT_Y}" width="15" height="{MATT_H}" rx="3" fill="{fill}" '
            f'stroke="{color}" stroke-width="1" stroke-opacity="{1 if hit else 0.45}"/>')
        add(f'<text x="{x + 7.5}" y="{MATT_Y + MATT_H / 2 + 3.5}" text-anchor="middle" font-size="9" '
            f'font-weight="{700 if hit else 400}" fill="{"#ffffff" if hit else color}">{v}</text>')

    # Luke strip
    for ch, (x0, w) in ch_x.items():
        color = LUKE_COLORS.get(ch)
        add(f'<rect x="{x0:.1f}" y="{LUKE_Y}" width="{w:.1f}" height="{LUKE_H}" rx="4" '
            f'fill="{color if color else "#f1eff6"}" fill-opacity="{0.16 if color else 1}" '
            f'stroke="{color or "#d9d5e3"}" stroke-width="{1.5 if color else 1}"/>')
        for v in sorted(hits.get(ch, ())):
            tx = luke_x(ch, v)
            add(f'<line x1="{tx:.1f}" y1="{LUKE_Y}" x2="{tx:.1f}" y2="{LUKE_Y + LUKE_H}" '
                f'stroke="{color}" stroke-width="2"/>')
        add(f'<text x="{x0 + w / 2:.1f}" y="{LUKE_Y + LUKE_H + 20}" text-anchor="middle" font-size="14" '
            f'font-weight="{700 if color else 400}" fill="{color or "#9a95a8"}">{ch}</text>')
    # Notes for chapters that receive lines, on rows chosen so neighbors don't collide
    note_rows = {3: 0, 4: 1, 6: 0, 7: 1, 8: 0, 11: 2, 12: 0, 13: 1, 14: 0, 16: 2}
    for ch in sorted(LUKE_NOTES):
        x0, w = ch_x[ch]
        y = LUKE_Y + LUKE_H + 44 + note_rows[ch] * 20
        add(f'<text x="{x0 + w / 2:.1f}" y="{y}" text-anchor="middle" font-size="12" '
            f'fill="{LUKE_COLORS[ch]}">{esc(LUKE_NOTES[ch])}</text>')
    add(f'<text x="{LEFT}" y="{LUKE_Y + LUKE_H + 112}" font-size="18" font-weight="700" fill="#1f1b2e">'
        "Luke 1–24 (each chapter drawn to its length)</text>")

    # Footer stats
    in6 = sum(1 for t in MATT_TO_LUKE.values() if any(c == 6 for c, _ in t))
    anywhere = len(MATT_TO_LUKE)
    nverses = sum(CHAPTER_LENGTHS.values())
    add(f'<text x="{LEFT}" y="{H - 28}" font-size="13" fill="#6b6580">'
        f"{anywhere} of {nverses} Matthew verses have a parallel in Luke: {in6} in Luke 6, "
        f"{anywhere - in6} only elsewhere; {nverses - anywhere} are Matthew only (empty boxes). "
        "Parallels follow a standard gospel synopsis (e.g. Aland).</text>")
    add("</svg>")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("wrote", OUT, f"{W}x{H}")


if __name__ == "__main__":
    main()

# PNG (2x):
#   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars \
#     --force-device-scale-factor=2 --window-size=1920,900 \
#     --screenshot=public/images/matthew-to-luke.png public/images/matthew-to-luke.svg
