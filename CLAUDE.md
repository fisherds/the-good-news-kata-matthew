# The Good News kata (according to) Matthew

Static Firebase Hosting site (`public/`, `cleanUrls: true`, so `public/sotm.html` is served at `/sotm`).

- `public/index.html` — the study calendar. Sermon on the Mount days link to `/sotm` as "Sermon Outline".
- `public/sotm.html` — Sermon on the Mount outline table (Matthew 5:1–7:27).

## Sermon on the Mount outline (`public/sotm.html`)

Word counts come from `data/sotm_greek_word_counts.tsv` (Greek words per verse, 109 verses, 2000 words total).

- Text is **Byzantine** (longer readings in e.g. 6:5, 6:6, 6:10, 6:16, 6:18), but **without the 6:13 doxology** — 6:13 is 12 words.
- A row's word count is the sum of its verses in the TSV; its verse count is the number of verses. Parent rows must equal the sum of their children.
- Bar width = row words ÷ 283 × 100 (283 = 3.0 Choice, the longest barred row), one decimal place. If the longest barred row changes, rescale all bars.

Structural decisions:

- The six case studies (5:21–47) are split 3/3 (2.1.2 and 2.1.3): 5:33 opens with πάλιν ("Again") and repeats the full "to those of old" formula from 5:21.
- One-liner conclusions get their own row a level up rather than being folded into the previous section (e.g. 2.1.4 Teleios, 5:48).

Row markup (the table is all on one line):

```html
<tr class="{color} {level}"><td style="padding-left:{indent}px"><span class="num">{n}</span> {title}</td><td class="ref">{a}–{b}</td><td class="n">{words}</td><td class="n">{verses}</td><td class="barc"><span class="bar" style="width:{pct}%"></span></td></tr>
```

- Color: `x` grey (total, 0.0 Introduction, 2.0 Torah), `id` Identity, `r` Righteousness, `p` Religious practice, `t` Trust, `c` Choice.
- Level: `kT` top total row, `kG` group header (no bar — empty `<td class="barc"></td>`), `kP` row that has sub-rows (full bar), `kS` leaf sub-row (thin faded bar).
- Indent by depth: 8, 26, 44, 62px (add 18px per further level).
- Single-verse ranges show one reference (`5:13`), not `5:13–5:13`. Use an en dash `–` in ranges.
