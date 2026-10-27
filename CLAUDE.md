# The Good News kata (according to) Matthew

Static Firebase Hosting site (`public/`, `cleanUrls: true`, so `public/sotm.html` is served at `/sotm`).

- `public/index.html` — the study calendar. Sermon on the Mount days link to `/sotm` as "Sermon Outline".
- `public/sotm.html` — Sermon on the Mount outline table (Matthew 5:1–7:27).

## Literary-design text (hosted locally)

BibleProject Classroom's literary-design units (Tim Mackie's translation with highlighting) were served from d3kfvpfexuy5fk.cloudfront.net, which is expected to go away. We keep our own copies and render them ourselves:

- `tools/fetch_visuals.py` — one-time downloader: reads every URL in `public/scripts/*text_visuals.json` and saves `public/visuals/<id>.json` (`reference`, `title`, `caption`, and `usx`; older units such as most of Ephesians have `html` instead). Re-run with `--force` to refresh while the site still exists. It also rebuilds `public/visuals/bundle-<book>.json` (all of a book's units in one file); run it after adding or editing any unit.
- `public/scripts/literary-design.js` — `LiteraryDesign.preload("matthew")` (fetches the bundle once), `LiteraryDesign.load(id)` (cached; waits for the bundle, falls back to the single file) and `LiteraryDesign.render(visual, "5:1–5:2")`. Renders USX to HTML and can slice a unit to a verse range (verse markers that go backwards, like the footnote-style 1–7 in Matthew 4:23–24, are ignored).
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
- Section introductions get a `.0` row so later numbers don't shift: 2.2.0 Introduction (6:1) sits above the three "in hiddenness" formulas (6:2–4, 5–6, 16–18).
- 2.3 Trust is A B A′ B′ + Golden Rule: (A) stuff 6:19–24 / (B) worry 6:25–34 / (A′) relationships 7:1–6 / (B′) your Father: ask, seek, knock 7:7–11 / 7:12. Each A opens with a "do not…" command plus three sayings; each B ends on "your Father in the skies" providing. Kept flat (not nesting B under A) so the parallel shows and Worry isn't buried.
- Alternate splits: the main rows follow Tim Mackie's divisions; the user's own alternative split goes right after them as `alt` rows (`<tr class="id kS alt" …>`, same number as the row it parallels, with "(alt)" at the start of the title so it shows even when numbers are hidden; italic, faded bar). Each set of children separately sums to the parent — alt rows are never added into totals. Currently: Beatitudes 1.1.1–1.1.3 are Tim's Social Status / Character / Conduct (5:3–5, 6–8, 9–12); alt rows are 5:3–6, 7–10, 11–12.
- One-liner conclusions get their own row a level up rather than being folded into the previous section — unless they clearly close the unit before them. (5:48 Teleios was its own row, then folded into 2.1.3.3 "Enemies (be complete)" because "your Father in the skies" in 5:45 and 5:48 ties them together.)

Row markup (the table is all on one line):

```html
<tr class="{color} {level}"><td style="padding-left:{indent}px"><span class="num">{n}</span> {title}</td><td class="ref">{a}–{b}</td><td class="vid">{video links}</td><td class="n">{words}</td><td class="n">{verses}</td><td class="barc"><span class="bar" style="width:{pct}%"></span></td></tr>
```

- Color: `x` grey (total, 0.0 Introduction, 2.0 Instruction), `id` Identity, `r` Righteousness, `p` Religious practice, `t` Trust, `c` Choice.
- Level: `kT` top total row, `kG` group header (no bar — empty `<td class="barc"></td>`), `kP` row that has sub-rows (full bar), `kS` leaf sub-row (thin faded bar).
- Indent by depth: 8, 26, 44, 62px (add 18px per further level).
- 📖 reading button: add `data-unit="<visual id>"` to the `<tr>` and put `<button class="read" type="button" aria-label="Read the text" title="Read the text">📖</button>` at the start of the `.ref` cell, right before the range (CSS reserves a slot so every range lines up). The row's verse range is the `.ref` cell text minus the icon. A row spanning several units lists them space-separated in order (`data-unit="matthew-5-3-12 matthew-5-13-16"`); each is cut to the range. Panels stay open, but opening one closes any open panel with overlapping verses (parent/child rows). Every numbered row has one. Panels roll down like a screen (sheet height and content slide together, 400ms, off under `prefers-reduced-motion`) and roll back up on close; the white box's left edge lines up with the row's title text (the title cell's padding). The Lord's Prayer has its own unit (`matthew-6-9-13`, which has no verse markers, so it is shown whole); only 2.2.2.2.2 uses it, and every other row covering 6:9–13 uses `matthew-6-5-15`.
- When adding buttons, compare row titles with Tim's wording in the unit and tell the user about mismatches (e.g. he renders δικαιοσύνη as "righteousness" in 5:6, 10 but "doing-what-is-right" in 5:20, 6:1, 6:33).
- Videos column (`td.vid`, right after the range; every row has the cell, often empty): BibleProject videos as `<a class="video" href="{url}" target="_blank" rel="noopener"><img src="images/videos/{slug}-sm.jpg" alt="Video: {title}" width="32" height="18"></a>` (the video's own thumbnail, rounded), series video first, then the visual commentary. Thumbnails are local copies from imagekit (the JSON `thumbnail` url with `tr:q-65,w-240` swapped): `{slug}-sm.jpg` at `tr:q-80,w-96` for the icon and `{slug}.jpg` at `tr:q-75,w-480` for the hover card; `{slug}` is the last part of the video url. Full res is the url with the `tr:…/` segment removed. `public/data/sotm_videos.json` holds all 24 (14 visual commentaries + 10-part series; site search finds no others) and the hover card (thumbnail, title, collection/part, length) looks them up by `href`, so the link url must match exactly. Clicking an icon plays the video in a pop-up `<dialog>` with `<mux-player>` (`@mux/mux-player@3.14.0` from jsdelivr, loaded on first play; accent `#00B3E5` like bibleproject.com); the JSON's `mux` field is the playback id, taken from the `contentUrl` (`stream.mux.com/<id>/high.mp4`) on each video page. Closing removes the player. Ctrl/cmd/shift-click, or a failed player load, opens the BibleProject page instead. On touch there's no card; one tap plays. Phones (`(hover: none) and (pointer: coarse)`) go straight to full screen: the player script is preloaded after page load so this can happen inside the tap's user activation. Full screen is the pop-up's `.screen` box (native `requestFullscreen`), and `player.mediaController.fullscreenElement` is set to that box so mux-player's own full-screen button knows the state (without it, the button says "enter" while full screen and can't exit); mux-player's `requestFullscreen` silently does nothing right after the element is created. iPhone, which has no element full screen, falls back to mux-player's (video `webkitEnterFullscreen`) — untested on a real iPhone. Leaving full screen closes the pop-up. Passages marked `guess` in the JSON weren't shown on the site. Each video sits on the row closest to its passage (e.g. series 8 Wealth and Worry 6:19–34 on 2.3.1 (A) stuff and 9 Wisdom in Relationships 7:1–12 on 2.3.3 (A′) relationships; 6:1–4 Generosity on 2.2.1).
- Single-verse ranges show one reference (`5:13`), not `5:13–5:13`. Use an en dash `–` in ranges.
- Collapsing (script at the bottom of `sotm.html`): sections 1.0, 2.1, 2.2, 2.3 and 3.0 start expanded; clicking a section header's title shows/hides all its rows at once (no partial states). `/sotm#2.3` collapses every other section and opens only 2.3; plain `/sotm` shows everything. Section membership comes from the row number prefix (alt rows included), so new rows need no extra markup.
- `firebase.json` caches `/visuals/**` for a day (`max-age=86400`).
- Narrow screens: below 900px the Greek words and Verses columns are hidden; below 700px the bars are hidden too (media queries in the `sotm.html` `<style>`).
- Display modes (`data-mode` on `.sotm-outline`, default `0` in the markup; the secret `n` key cycles them, `MODES` in the script):
  - 0 (default): no outline numbers, 📖 icons and videos shown, Verses column hidden (`nth-child(5)`; update it if columns move).
  - 1: everything (numbers, icons, videos, Greek words, Verses, bars).
  - 2 (leanest, for slides): titles, ranges and bars only — no numbers, icons, videos or count columns.
  The user expects to add more modes later: add a `[data-mode="N"]` CSS block and bump `MODES`.
