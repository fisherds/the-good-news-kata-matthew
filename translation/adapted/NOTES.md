# Adapted Tim units: what changed and why

Each adapted unit is `adapted-<Tim's id>.usx`; his original USX is in `original/<Tim's id>.usx`, so
`diff original/<id>.usx adapted-<id>.usx` shows every change. Build with `python3 tools/build_translation.py`.

## adapted-matthew-5-31-32 (used on /sotm)

- 5:32 “except on the ground of sexual immorality”: bold (`<char style="bd">`, the words an ⓘ hangs on are
  always bold) and an ⓘ, `matthew-5-32-divorce` (in `tools/build_xrefs.py`). Reason: Jesus comes back to
  divorce in Matthew 19:3–12 and argues from Genesis 1:27 and 2:24 (LXX); the pop-up shows those texts and
  the setting of his words (who was listening, why it is wisdom and not a rule lifted out of context).
- Deuteronomy 10:20 LXX added to the same pop-up (2026-11-06): Jesus' verb for “cleave to his wife” (κολλάω) is Moses' verb for Israel holding fast to the LORD. SBLGNT has the plain κολληθήσεται, matching Deuteronomy; the Textus Receptus and Byzantine text have προσκολληθήσεται, matching Genesis 2:24.
- Deuteronomy 24:1 LXX added (the Pharisees' text, 19:7): “certificate of divorce” βιβλίον ἀποστασίου matches exactly (purple). “For any reason” (19:3) has no Greek match in Deut 24:1 (ἄσχημον πρᾶγμα), so it is only marked, and the note explains the Shammai / Hillel / Akiva debate (Mishnah Gittin 9:10).
