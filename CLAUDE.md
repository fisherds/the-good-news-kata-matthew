# The Good News kata (according to) Matthew

Static Firebase Hosting site (`public/`, `cleanUrls: true`, so `public/sotm.html` is served at `/sotm`).

- `public/index.html` — the study calendar. Sermon on the Mount days link to `/sotm` as "Sermon Outline".
- `public/sotm.html` — Sermon on the Mount outline table (Matthew 5:1–7:27).

## Literary-design text (hosted locally)

BibleProject Classroom's literary-design units (Tim Mackie's translation with highlighting) were served from d3kfvpfexuy5fk.cloudfront.net, which is expected to go away. We keep our own copies and render them ourselves:

- `tools/fetch_visuals.py` — one-time downloader: reads every URL in `public/scripts/*text_visuals.json` and saves `public/visuals/<id>.json` (`reference`, `title`, `caption`, and `usx`; older units such as most of Ephesians have `html` instead). Re-run with `--force` to refresh while the site still exists.
- `public/scripts/literary-design.js` — `LiteraryDesign.load(id)` and `LiteraryDesign.render(visual, "5:1–5:2")`. Renders USX to HTML and can slice a unit to a verse range (verse markers that go backwards, like the footnote-style 1–7 in Matthew 4:23–24, are ignored).
- `public/styles/literary-design.css` — highlight colors and group layout copied from bp-web-components v0.27.2 (`mark.css`, `literary-design.css`).
- Backup source: the user's old checkout of BibleProject's classroom-content repo at `/Users/davidfisher/Documents/BibleProject/github/classroom-content` has all 294 units as YAML in `public/data/visuals/literary-design-units/`.
- Not yet done: `/reader` still iframes the cloudfront URLs. Ephesians (a side project for a friend) is low priority; its `html` format has no renderer.

## Sermon on the Mount outline (`public/sotm.html`)

Word counts come from `data/sotm_greek_word_counts.tsv` (Greek words per verse, 109 verses, 2000 words total).

- Text is **Byzantine** (longer readings in e.g. 6:5, 6:6, 6:10, 6:16, 6:18), but **without the 6:13 doxology** — 6:13 is 12 words.
- A row's word count is the sum of its verses in the TSV; its verse count is the number of verses. Parent rows must equal the sum of their children.
- Bar width = row words ÷ 268 × 100 (268 = 2.1.2 Case studies: Murder, Adultery, Divorce — the longest barred row; group headers `kG` have no bar), one decimal place. If the longest barred row changes, rescale all bars.

Structural decisions:

- The six case studies (5:21–47) are split 3/3 (2.1.2 and 2.1.3): 5:33 opens with πάλιν ("Again") and repeats the full "to those of old" formula from 5:21.
- Alternate splits: the main rows follow Tim Mackie's divisions; the user's own alternative split goes right after them as `alt` rows (`<tr class="id kS alt" …>`, number shown as `alt 1.1.1`; italic, faded bar). Each set of children separately sums to the parent — alt rows are never added into totals. Currently: Beatitudes 1.1.1–1.1.3 are Tim's Social Status / Character / Conduct (5:3–5, 6–8, 9–12); alt rows are 5:3–6, 7–10, 11–12.
- One-liner conclusions get their own row a level up rather than being folded into the previous section — unless they clearly close the unit before them. (5:48 Teleios was its own row, then folded into 2.1.3.3 "Enemies (be complete)" because "your Father in the skies" in 5:45 and 5:48 ties them together.)

Row markup (the table is all on one line):

```html
<tr class="{color} {level}"><td style="padding-left:{indent}px"><span class="num">{n}</span> {title}</td><td class="ref">{a}–{b}</td><td class="n">{words}</td><td class="n">{verses}</td><td class="barc"><span class="bar" style="width:{pct}%"></span></td></tr>
```

- Color: `x` grey (total, 0.0 Introduction, 2.0 Torah), `id` Identity, `r` Righteousness, `p` Religious practice, `t` Trust, `c` Choice.
- Level: `kT` top total row, `kG` group header (no bar — empty `<td class="barc"></td>`), `kP` row that has sub-rows (full bar), `kS` leaf sub-row (thin faded bar).
- Indent by depth: 8, 26, 44, 62px (add 18px per further level).
- 📖 reading button: add `data-unit="<visual id>"` to the `<tr>` and put `<button class="read" type="button" aria-label="Read the text" title="Read the text">📖</button>` at the start of the `.ref` cell, right before the range (CSS reserves a slot so every range lines up). The row's verse range is the `.ref` cell text minus the icon. A row spanning several units lists them space-separated in order (`data-unit="matthew-5-3-12 matthew-5-13-16"`); each is cut to the range. Panels stay open, but opening one closes any open panel with overlapping verses (parent/child rows). Every numbered row has one. The Lord's Prayer has its own unit (`matthew-6-9-13`, which has no verse markers, so it is shown whole); only 2.2.2.2.2 uses it, and every other row covering 6:9–13 uses `matthew-6-5-15`.
- When adding buttons, compare row titles with Tim's wording in the unit and tell the user about mismatches (e.g. he renders δικαιοσύνη as "righteousness" in 5:6, 10 but "doing-what-is-right" in 5:20, 6:1, 6:33).
- Single-verse ranges show one reference (`5:13`), not `5:13–5:13`. Use an en dash `–` in ranges.
