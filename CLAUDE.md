# The Good News kata (according to) Matthew

Static Firebase Hosting site (`public/`, `cleanUrls: true`, so `public/sotm.html` is served at `/sotm`).

- `public/index.html` — the study calendar. Each day lists its Google Slides links (labelled "… Slides") and the site reader for that section: "Old Testament Connections reader" (`/otconnections`) on the 1:1–4:16 days, "Sermon on the Mount reader" (`/sotm`) on the Sermon days.
- `public/sotm.html` — Sermon on the Mount outline table (Matthew 5:1–7:27). A complete page (doctype, charset, viewport, title); it used to be a paste-in fragment, which put browsers in quirks mode and, with no viewport tag, made phones lay it out 980px wide so the narrow-screen media queries never fired. To keep the old compact rows in standards mode the table has `line-height:normal` and `.vid` has `line-height:0`.

## Literary-design text (hosted locally)

BibleProject Classroom's literary-design units (Tim Mackie's translation with highlighting) were served from d3kfvpfexuy5fk.cloudfront.net, which is expected to go away. We keep our own copies and render them ourselves:

- `tools/fetch_visuals.py` — one-time downloader: reads every URL in `public/scripts/*text_visuals.json` and saves `public/visuals/<id>.json` (`reference`, `title`, `caption`, and `usx`; older units such as most of Ephesians have `html` instead). Re-run with `--force` to refresh while the site still exists. It also rebuilds `public/visuals/bundle-<book>.json` (all of a book's units in one file); run it after adding or editing any unit.
- `public/scripts/literary-design.js` — `LiteraryDesign.preload("matthew")` (fetches the bundle once), `LiteraryDesign.load(id)` (cached; waits for the bundle, falls back to the single file) and `LiteraryDesign.render(visual, "5:1–5:2")`. Renders USX to HTML and can slice a unit to a verse range (verse markers that go backwards, like the footnote-style 1–7 in Matthew 4:23–24, are ignored).
- `public/styles/literary-design.css` — highlight colors and group layout copied from bp-web-components v0.27.2 (`mark.css`, `literary-design.css`).
- Backup source: the user's old checkout of BibleProject's classroom-content repo at `/Users/davidfisher/Documents/BibleProject/github/classroom-content` has all 294 units as YAML in `public/data/visuals/literary-design-units/`.
- Not yet done: `/reader` still iframes the cloudfront URLs. Ephesians (a side project for a friend) is low priority; its `html` format has no renderer.

## Master plan

Two ways into the same text. **Text and highlighting are shared** (the USX unit files, rendered by `LiteraryDesign`); **outlines are not** — each reader and section page keeps its own outline data, and duplication there is fine. Videos are mostly an sotm thing; BibleProject has few outside the Sermon on the Mount. Section colors should carry a meaning through the whole book where possible (some colors will be reused). Sections overlap where Tim's units do (4:17 is in both `/otconnections` and `/announcingkingdom`).

- **Readers** (whole-book, unit after unit):
  - `/reader` — only what BibleProject has published (they have more, not yet published).
  - `/extendedreader` (planned) — all of Matthew: BibleProject's published units first, then our own continuation in the same style.
- **Section pages** (one per part of Matthew, like `/sotm`: outline table, 📖 text panels, videos):
  - `/matthew` — colorful overview page linking to the sections below.
  - `/otconnections` — 1:1–4:17.
  - `/announcingkingdom` — 4:17–4:25.
  - `/otconnections` (first draft) is described below; the thinking behind it is in `docs/old-testament-connections-notes.md`.

`/matthew` (`public/matthew.html`) is the top of the hierarchy: kept simple, the BibleProject mountain image (`images/mountain.jpg`, local copy of imagekit `the-mountain/mountain_16.9.jpg`) above an sotm-style list of the sections, each row linking to its page (rows without a page yet are muted, marked "coming"). Story sections green, teaching blocks blue; counts are Textus Receptus, bars scale to the longest section (Sermon on the Mount, 2043). Add a section's link when its page exists.

### The 60,000-foot view: waterfalls up the mountain

How the user sees Matthew's shape (a possible future infographic on `/matthew`, in the style of the mountain image):

- The story is a climb. **The five teaching blocks are waterfalls** we travel *up*; the narrative between them are **pools**, each at a higher energy level than the last, like a symphony getting louder and more climactic.
- Base pool: Connection to the OT (1:1–4:17) and 4:17–25 sit at the same level. **Waterfall 1:** Sermon on the Mount (5–7).
- Pool 2: the nine miracle stories (8–9). Almost no pushback yet — only "it is by Beelzebul, the prince of demons, that he drives out demons", and Jesus answers it kindly. **Waterfall 2:** sending the Twelve (10).
- Pool 3: responses to Jesus (11–12), a reset that starts with John the Baptist's question (John was also in the story just before the Sermon). Different people react differently; the Beelzebul charge comes back and Jesus answers less kindly — the stakes are higher. **Waterfall 3:** the kingdom parables (13).
- Pool 4: John the Baptist returns at the same pivot and is killed (14); the miracles get bigger (feeding the 5000, walking on water, feeding the 4000) than the nine of 8–9. And so on up.
- Recurring markers to watch as pools rise: John the Baptist at each pivot, the Beelzebul charge, the scale of the miracles, the level of opposition.
  - `/sotm` — Matthew 5–7, first of the five teaching blocks (done).
  - `/ninemiraclestories` — Matthew 8–9.
  - `/sendingthetwelve` — Matthew 10, second teaching block.
  - `/responses` — Matthew 11–12, people's different reactions to Jesus.
  - `/kingdomparables` — Matthew 13, third teaching block.
  - More sections to come, in the same pattern.

## Extended translation (planned `public/extendedreader.html`)

Goal: continue Tim Mackie's style of translation and literary design past Matthew 7:29, a little at a time, with everything stored in this repo. The page shows Tim's units for chapters 1–7. Our own practice translations of 1–7 are only for comparing with his, never shown to users. **Style guide: `docs/translation-style.md`** (findings from comparing his 1–7 with the Greek and four translations; keep findings there, not here). Side-by-side working file: `data/compare/matthew-1-7.md` (gitignored). Reference files in `data/`:

- `matthew_greek.txt` — SBLGNT (1,068 verses; `Matt 1:1<TAB>text`; strip the ⸀ ⸂ ⸃ variant markers). The base text. CC BY 4.0, needs attribution.
- `matthew_tr.json` — Textus Receptus (Elzevir 1624) from bolls.life (`TR`), same format as the English files, lowercase without accents. Public domain. **Greek word counts on every page come from this** (sotm's TSV matches it).
- `matthew_byzantine.csv` — Robinson–Pierpont Byzantine text (`chapter,verse,text`, without accents), from github.com/byztxt/byzantine-majority-text. Public domain. Reference only.
- `matthew_concordance.json` — KJV/Textus Receptus interlinear by verse id (`40001001`) with Strong's numbers; `greek.json` — Strong's lexicon (5,523 entries). Source and license unknown, so both are gitignored (local reference only).
- `matthew_{niv,esv,nasb95,net}.json` — English translations from bolls.life (`[{chapter, verses:[{pk, verse, text}]}]`; NIV and NET text has `<b>` tags). Downloaded with `getting_bible_text.py` (codes NIV2011, ESV, NASB = 1995, NET = 2007). **Copyrighted and gitignored — never commit or publish them; the repo is public.**

## Connection to the Old Testament (`public/otconnections.html`)

Matthew 1:1–4:17, built from the `/sotm` pattern (same row markup, levels, indents, 📖 panels, collapsing, `n` modes; CSS prefix `.ot-outline`). Differences:

- Five parts with sotm's palette in order: `g` Genealogy green `#2f9e5b`, `b` Birth and Magi blue `#2f6fd6`, `j` John the Baptist orange `#d9822b`, `w` Wilderness purple `#8a3fd1`, `c` Capernaum pink `#d6337a`; `x` grey total. All five parts have the same 6px left line (`top` class on the two that have no sub-rows). Sections that collapse: 2.0, 3.0, 4.0. No more sub-rows wanted (Herod's three quotes stay on one row; no genealogy split).
- Row titles are the user's familiar names (John the Baptist, Herod, Jesus is baptized), not Tim's (Ioannes the immerser, Herodes, immersed) — that's intended. "Test 1: Bread / Test 2: Temple / Test 3: Kingdoms" follow Tim's group titles.
- Bars scale to 277 (1.0 The Genealogy, the longest barred row). Word counts are Textus Receptus.
- The third column is **OT quotes**, not videos: `<button class="quote {kind}" type="button" data-quote="{id}" aria-label="Quote {id}: {title}">{id}</button>` in `td.ot`, kind `fill` (filled-full formula, solid), `prophet` (names the prophet, no filled-full; outlined) or `jesus` (J1–J3, dark). Clicking opens a pop-up with Tim's text of the Matthew verses (`unit` + `matthew` range), the Greek formula, the OT passages (BSB) with focus verses highlighted, and a note. Data: `public/data/otconnections_quotes.json`, generated by `tools/fetch_ot_quotes.py` — edit the `QUOTES` list there and re-run, don't hand-edit the JSON.
- The genealogy's verse markers also count the 41 generations. `literary-design.js` skips those when cutting to a range (`isCounter`: right against a name or ending in a comma; plus any marker jumping more than 3 verses ahead, e.g. "Iekhonia ²⁸" after verse 11) and shows a unit whole when the range covers all of it.
- Pages load `scripts/literary-design.js?v=N`; Firebase caches it for an hour, so **bump `v` in every page that loads it whenever the script changes** (stale copies once cut the genealogy off at 1:7).

## Sermon on the Mount outline (`public/sotm.html`)

Word counts come from `data/sotm_greek_word_counts.tsv` (Greek words per verse, 109 verses, 2000 words total).

- Text is the **Textus Receptus** (Elzevir 1624, `data/matthew_tr.json`; longer readings in e.g. 5:27, 6:5, 6:6, 6:10, 6:16, 6:18), but **without the 6:13 doxology** — 6:13 is 12 words. All 109 verses match TR exactly; Robinson–Pierpont differs in 7 (5:23, 5:27, 5:39, 5:45, 6:13, 6:18, 7:20).
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

- Color: `x` grey (total, 0.0 Introduction, 2.0 Instruction), `id` Identity green `#2f9e5b`, `r` Righteousness blue `#2f6fd6`, `p` Religious practice orange `#d9822b`, `t` Trust purple `#8a3fd1`, `c` Choice pink `#d6337a`. Neighboring sections need clearly different hues (Practice and Trust were once two purples). Leaf rows (`kS`) have the same solid, full-color left border as other rows (no dots, no fading). The diagrams in `images/` still use the old palette; they now live in Google Slides, so leave them alone.
- Level: `kT` top total row, `kG` group header (no bar — empty `<td class="barc"></td>`), `kP` row that has sub-rows (full bar), `kS` leaf sub-row (thin faded bar).
- Indent by depth: 8, 26, 44, 62px (add 18px per further level).
- 📖 reading button: add `data-unit="<visual id>"` to the `<tr>` and put `<button class="read" type="button" aria-label="Read the text" title="Read the text">📖</button>` at the start of the `.ref` cell, right before the range (CSS reserves a slot so every range lines up). The row's verse range is the `.ref` cell text minus the icon. A row spanning several units lists them space-separated in order (`data-unit="matthew-5-3-12 matthew-5-13-16"`); each is cut to the range. Panels stay open, but opening one closes any open panel with overlapping verses (parent/child rows). Every numbered row has one. Panels roll down like a screen (sheet height and content slide together, 400ms, off under `prefers-reduced-motion`) and roll back up on close; the white box's left edge lines up with the row's title text (the title cell's padding). The Lord's Prayer has its own unit (`matthew-6-9-13`, which has no verse markers, so it is shown whole); only 2.2.2.2.2 uses it, and every other row covering 6:9–13 uses `matthew-6-5-15`.
- When adding buttons, compare row titles with Tim's wording in the unit and tell the user about mismatches (e.g. he renders δικαιοσύνη as "righteousness" in 5:6, 10 but "doing-what-is-right" in 5:20, 6:1, 6:33).
- Videos column (`td.vid`, right after the range; every row has the cell, often empty): BibleProject videos as `<a class="video" href="{url}" target="_blank" rel="noopener"><img src="images/videos/{slug}-sm.jpg" alt="Video: {title}" width="32" height="18"></a>` (the video's own thumbnail, rounded), series video first, then the visual commentary, then insights. Thumbnails are local copies from imagekit (the JSON `thumbnail` url with `tr:q-65,w-240` swapped): `{slug}-sm.jpg` at `tr:q-80,w-96` for the icon and `{slug}.jpg` at `tr:q-75,w-480` for the hover card; `{slug}` is the last part of the video url. Full res is the url with the `tr:…/` segment removed. `public/data/sotm_videos.json` holds 35: the 14 visual commentaries, the 10-part series (site search finds no others) and the 11 Sermon on the Mount videos from the 32-video Insights collection (`kind: "insight"`; card titles like "Teleios / Whole", from the collection page — the video pages' `<title>`s are SEO titles) and the hover card (thumbnail, title, collection/part, length) looks them up by `href`, so the link url must match exactly. Clicking an icon plays the video in a pop-up `<dialog>` with `<mux-player>` (`@mux/mux-player@3.14.0` from jsdelivr, loaded on first play; accent `#00B3E5` like bibleproject.com); the JSON's `mux` field is the playback id, taken from the `contentUrl` (`stream.mux.com/<id>/high.mp4`) on each video page. Closing removes the player. Ctrl/cmd/shift-click, or a failed player load, opens the BibleProject page instead. On touch there's no card; one tap plays. Phones (`(hover: none) and (pointer: coarse)`) go straight to full screen: the player script is preloaded after page load so this can happen inside the tap's user activation. Full screen is the pop-up's `.screen` box (native `requestFullscreen`), and `player.mediaController.fullscreenElement` is set to that box so mux-player's own full-screen button knows the state (without it, the button says "enter" while full screen and can't exit); mux-player's `requestFullscreen` silently does nothing right after the element is created. iPhone, which has no element full screen, falls back to mux-player's (video `webkitEnterFullscreen`) — untested on a real iPhone. Leaving full screen closes the pop-up. Android turns to landscape in full screen, except videos with `"portrait": true` in the JSON (Murder and Contempt, Adultery and Lust, Eye and Hand Mutilation, and the insights Do Not Worry, Purpose of Fasting, Creative Nonviolence — BibleProject uploaded these as 1080×1920; check a new video's `stream.mux.com/<id>.m3u8` RESOLUTION), which stay upright. On desktop the same flag gives the pop-up a `.portrait` class: a 9:16 screen sized to the window height (`width: min((100vh - 170px) * 9/16, 100vw - 32px)`). Passages marked `guess` in the JSON weren't shown on the site. Each video sits on the row closest to its passage (e.g. series 8 Wealth and Worry 6:19–34 on 2.3.1 (A) stuff and 9 Wisdom in Relationships 7:1–12 on 2.3.3 (A′) relationships; 6:1–4 Generosity on 2.2.1). The user's placements: Torah / Instruction on 2.0 Instruction, series 3 Jesus Fulfills the Law on the 2.1 Greater Righteousness header (2.1.1 keeps only the Righteousness and Jesus' Bible commentary), Dikaiosune / Righteousness on 1.1 Beatitudes, Basileia / Kingdom on 2.2.2.2.2 The Lord's Prayer, Gehenna on 2.1.2.1 Murder, anger, contempt.
- Single-verse ranges show one reference (`5:13`), not `5:13–5:13`. Use an en dash `–` in ranges.
- Collapsing (script at the bottom of `sotm.html`): sections 1.0, 2.1, 2.2, 2.3 and 3.0 start expanded; clicking a section header's title shows/hides all its rows at once (no partial states). `/sotm#2.3` collapses every other section and opens only 2.3; plain `/sotm` shows everything. Section membership comes from the row number prefix (alt rows included), so new rows need no extra markup.
- `firebase.json` caches `/visuals/**` for a day (`max-age=86400`).
- Narrow screens: below 900px the Greek words and Verses columns are hidden; below 700px the bars are hidden too (media queries in the `sotm.html` `<style>`).
- Display modes (`data-mode` on `.sotm-outline`, default `0` in the markup; the secret `n` key cycles them, `MODES` in the script):
  - 0 (default): no outline numbers, 📖 icons and videos shown, Verses column hidden (`nth-child(5)`; update it if columns move).
  - 1: everything (numbers, icons, videos, Greek words, Verses, bars).
  - 2 (leanest, for slides): titles, ranges and bars only — no numbers, icons, videos or count columns.
  The user expects to add more modes later: add a `[data-mode="N"]` CSS block and bump `MODES`.
