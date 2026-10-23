"""Draw how Luke's Sermon on the Plain (6:20-49) lines up with Matthew 5:1-7:29.

Writes public/images/sermon-plain-parallels.svg. To make the PNG, screenshot it
with headless Chrome (see the bottom of this file).

Usage: python3 tools/luke_parallels.py
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public", "images", "sermon-plain-parallels.svg")

CHAPTER_LENGTHS = {5: 48, 6: 34, 7: 29}

# Matthew outline sections (same colors as sotm.html).
SECTIONS = [
    ((5, 1), (5, 2), "Narration", "#9a95a8"),
    ((5, 3), (5, 16), "Identity", "#2f9e5b"),
    ((5, 17), (5, 48), "Righteousness", "#2f6fd6"),
    ((6, 1), (6, 18), "Religious practice", "#8a3fd1"),
    ((6, 19), (7, 12), "Trust", "#b93fc4"),
    ((7, 13), (7, 27), "Choice", "#d6337a"),
    ((7, 28), (7, 29), "Narration", "#9a95a8"),
]

# Luke 6 verse -> Matthew verses it parallels (standard synopsis parallels).
PARALLELS = {
    20: [(5, 2), (5, 3)],  # 20a "lifting his eyes ... he said" ~ 5:2; blessed are the poor
    21: [(5, 6), (5, 4)],  # hungry / weeping
    22: [(5, 11)],
    23: [(5, 12)],
    27: [(5, 44)],
    28: [(5, 44)],
    29: [(5, 39), (5, 40)],
    30: [(5, 42)],
    31: [(7, 12)],  # Golden Rule
    32: [(5, 46)],
    33: [(5, 47)],
    34: [(5, 42)],
    35: [(5, 44), (5, 45)],
    36: [(5, 48)],
    37: [(7, 1)],
    38: [(7, 2)],
    41: [(7, 3)],
    42: [(7, 4), (7, 5)],
    43: [(7, 17), (7, 18)],
    44: [(7, 16)],
    46: [(7, 21)],
    47: [(7, 24)],
    48: [(7, 24), (7, 25)],
    49: [(7, 26), (7, 27)],
}
# Luke verses with no parallel in Matthew 5-7.
ELSEWHERE = {24: "Mt 23:13–29", 25: "Mt 23:13–29", 26: "Mt 23:13–29",
             39: "Mt 15:14", 40: "Mt 10:24–25", 45: "Mt 12:34–35"}

LUKE_GROUPS = [
    (20, 23, "Blessings"), (24, 26, "Woes"), (27, 36, "Love your enemies"),
    (37, 42, "Judging"), (43, 45, "Trees and fruit"), (46, 49, "Two builders"),
]

# Layout
W = 1920
LEFT = 52
CELL = 15
STEP = 16
CH_GAP = 24
MATT_Y = 190
MATT_H = 30
LUKE_Y = 640
LUKE_H = 40


def section_of(ch, v):
    for start, end, name, color in SECTIONS:
        if start <= (ch, v) <= end:
            return name, color
    raise ValueError((ch, v))


def matt_x():
    xs, x = {}, LEFT
    for ch, n in CHAPTER_LENGTHS.items():
        for v in range(1, n + 1):
            xs[(ch, v)] = x
            x += STEP
        x += CH_GAP
    return xs, x - CH_GAP - (STEP - CELL)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


def main():
    mx, right = matt_x()
    span = right - LEFT
    luke_verses = list(range(20, 50))
    luke_step = (span + 4) / len(luke_verses)
    luke_w = luke_step - 4
    lx = {v: LEFT + i * luke_step for i, v in enumerate(luke_verses)}
    H = 860
    out = []
    add = out.append
    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        'font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, Helvetica, Arial, sans-serif">')
    add(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
    add('<text x="52" y="52" font-size="30" font-weight="700" fill="#1f1b2e">'
        "Luke's Sermon on the Plain → Matthew's Sermon on the Mount</text>")
    add('<text x="52" y="84" font-size="18" fill="#6b6580">'
        "Luke 6:20–49 linked to its parallels in Matthew 5:1–7:29. "
        "Not one lands in Matthew 6.</text>")

    # Matthew 6 band
    x6a, x6b = mx[(6, 1)] - 6, mx[(6, 34)] + CELL + 6
    add(f'<rect x="{x6a}" y="{MATT_Y - 52}" width="{x6b - x6a}" height="{LUKE_Y - MATT_Y + 52 - 14}" '
        'fill="#f4f1fa" rx="10"/>')

    # Chapter labels
    for ch, n in CHAPTER_LENGTHS.items():
        a, b = mx[(ch, 1)], mx[(ch, n)] + CELL
        add(f'<text x="{(a + b) / 2}" y="{MATT_Y - 62}" text-anchor="middle" font-size="18" '
            f'font-weight="700" fill="#1f1b2e">Matthew {ch}</text>')

    # Section labels with brackets
    for start, end, name, color in SECTIONS:
        a, b = mx[start], mx[end] + CELL
        add(f'<line x1="{a}" y1="{MATT_Y - 10}" x2="{b}" y2="{MATT_Y - 10}" stroke="{color}" stroke-width="3"/>')
        if b - a > 40:
            add(f'<text x="{(a + b) / 2}" y="{MATT_Y - 18}" text-anchor="middle" font-size="13" '
                f'font-weight="600" fill="{color}">{esc(name)}</text>')

    # Connection lines (drawn under the cells)
    targets = set()
    for lv, refs in PARALLELS.items():
        for ref in refs:
            targets.add(ref)
            _, color = section_of(*ref)
            x1 = mx[ref] + CELL / 2
            y1 = MATT_Y + MATT_H
            x2 = lx[lv] + luke_w / 2
            y2 = LUKE_Y
            dash = ' stroke-dasharray="6 5"' if ref == (5, 2) else ""
            add(f'<path d="M{x1:.1f},{y1} C{x1:.1f},{y1 + 180} {x2:.1f},{y2 - 180} {x2:.1f},{y2}" '
                f'fill="none" stroke="{color}" stroke-width="2.2" stroke-opacity="0.75"{dash}/>')

    # Matthew 6 caption, on a card above the lines so it stays readable
    cx, cy = (x6a + x6b) / 2, MATT_Y + 120
    add(f'<rect x="{cx - 190}" y="{cy - 34}" width="380" height="96" rx="10" fill="#ffffff" '
        'fill-opacity="0.92" stroke="#e2dfeb"/>')
    add(f'<text x="{cx}" y="{cy - 4}" text-anchor="middle" font-size="22" font-weight="700" '
        'fill="#8a3fd1">Matthew 6</text>')
    add(f'<text x="{cx}" y="{cy + 22}" text-anchor="middle" font-size="16" fill="#6b6580">'
        'giving · prayer · fasting · treasure · worry</text>')
    add(f'<text x="{cx}" y="{cy + 46}" text-anchor="middle" font-size="16" font-weight="600" '
        'fill="#1f1b2e">no parallels in Luke 6</text>')

    # Matthew cells
    for (ch, v), x in mx.items():
        _, color = section_of(ch, v)
        hit = (ch, v) in targets
        fill = color if hit else "#ffffff"
        stroke = color
        text = "#ffffff" if hit else color
        add(f'<rect x="{x}" y="{MATT_Y}" width="{CELL}" height="{MATT_H}" rx="3" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="1" stroke-opacity="{1 if hit else 0.45}"/>')
        add(f'<text x="{x + CELL / 2}" y="{MATT_Y + MATT_H / 2 + 3.5}" text-anchor="middle" '
            f'font-size="9" font-weight="{700 if hit else 400}" fill="{text}" '
            f'fill-opacity="{1 if hit else 0.8}">{v}</text>')

    # Luke cells
    add(f'<text x="{LEFT}" y="{LUKE_Y + LUKE_H + 92}" font-size="18" font-weight="700" fill="#1f1b2e">Luke 6</text>')
    for v in luke_verses:
        x = lx[v]
        if v in PARALLELS:
            add(f'<rect x="{x:.1f}" y="{LUKE_Y}" width="{luke_w:.1f}" height="{LUKE_H}" rx="5" fill="#1f1b2e"/>')
            add(f'<text x="{x + luke_w / 2:.1f}" y="{LUKE_Y + LUKE_H / 2 + 5}" text-anchor="middle" '
                f'font-size="15" font-weight="700" fill="#ffffff">6:{v}</text>')
        else:
            add(f'<rect x="{x:.1f}" y="{LUKE_Y}" width="{luke_w:.1f}" height="{LUKE_H}" rx="5" fill="#ffffff" '
                'stroke="#9a95a8" stroke-width="1.5" stroke-dasharray="4 3"/>')
            add(f'<text x="{x + luke_w / 2:.1f}" y="{LUKE_Y + LUKE_H / 2 + 5}" text-anchor="middle" '
                f'font-size="15" fill="#6b6580">6:{v}</text>')
            if not 24 <= v <= 26:  # the woes share one note, centered under the group
                add(f'<text x="{x + luke_w / 2:.1f}" y="{LUKE_Y + LUKE_H + 16}" text-anchor="middle" '
                    f'font-size="11" fill="#6b6580">{esc(ELSEWHERE[v])}</text>')
    wx = (lx[24] + lx[26] + luke_w) / 2
    add(f'<text x="{wx:.1f}" y="{LUKE_Y + LUKE_H + 16}" text-anchor="middle" font-size="11" '
        'fill="#6b6580">all → Mt 23:13–29</text>')
    for a, b, name in LUKE_GROUPS:
        x1, x2 = lx[a], lx[b] + luke_w
        add(f'<line x1="{x1:.1f}" y1="{LUKE_Y + LUKE_H + 30}" x2="{x2:.1f}" y2="{LUKE_Y + LUKE_H + 30}" '
            'stroke="#1f1b2e" stroke-width="2"/>')
        add(f'<text x="{(x1 + x2) / 2:.1f}" y="{LUKE_Y + LUKE_H + 50}" text-anchor="middle" font-size="15" '
            f'font-weight="600" fill="#1f1b2e">{esc(name)}</text>')

    # Footer
    n_links = sum(len(r) for r in PARALLELS.values())
    add(f'<text x="{LEFT}" y="{H - 28}" font-size="13" fill="#6b6580">'
        f"{len(PARALLELS)} of 30 Luke verses link to {len(targets)} Matthew verses ({n_links} links); "
        "filled Matthew boxes have a parallel. Dashed line: Luke 6:20a narration ~ Matthew 5:2. "
        "Parallels follow a standard gospel synopsis (e.g. Aland).</text>")
    add(f'<text x="{LEFT}" y="{H - 50}" font-size="13" fill="#6b6580">'
        "Luke pairs 4 blessings with 4 woes in one sermon; Matthew has 8 blessings (+1 bonus, 5:11–12) here "
        "and saves his 8 woes for chapter 23 (23:13–29).</text>")
    add("</svg>")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("wrote", OUT, f"{W}x{H}")


if __name__ == "__main__":
    main()

# PNG (2x):
#   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars \
#     --force-device-scale-factor=2 --window-size=1920,860 \
#     --screenshot=public/images/sermon-plain-parallels.png public/images/sermon-plain-parallels.svg
