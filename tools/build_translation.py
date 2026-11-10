"""Build our own literary-design units from translation/<book>/*.usx.

Our translation (continuing Tim Mackie's style past Matthew 7) is written by
hand as USX files, one per unit, e.g. translation/matthew/kata-matthew-8-1-4.usx
(same markup as BibleProject's units: <group>, <verse>, <char mark-color ...>).
This script wraps each one as public/visuals/<id>.json, the same shape as the
BibleProject copies, so LiteraryDesign can render them, then rebuilds the
bundles (ours are bundle-kata.json, since ids start with "kata-").

  python3 tools/build_translation.py          build every .usx file
  python3 tools/build_translation.py --seed   first write any missing unit in
                                              UNITS as plain Greek (SBLGNT),
                                              one line per verse

Edit the .usx files, never the generated JSON. Units whose text is still
Greek get the SBLGNT credit; a unit becomes "ours" once it has
status="translated" on its <usx> element.
"""
import glob
import json
import os
import re
import sys
import xml.dom.minidom

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch_visuals import OUT_DIR, ROOT, write_bundles  # noqa: E402

SRC_DIR = os.path.join(ROOT, "translation")
GREEK = os.path.join(ROOT, "data", "matthew_greek.txt")

# Units for /ninemiraclestories (Matthew 8-9): (chapter, first verse, last verse).
UNITS = {
    "matthew": [
        (8, 1, 4), (8, 5, 13), (8, 14, 17), (8, 18, 22),
        (8, 23, 27), (8, 28, 34), (9, 1, 8), (9, 9, 13), (9, 14, 17),
        (9, 18, 26), (9, 27, 31), (9, 32, 34), (9, 35, 38),
    ],
}

GREEK_CREDIT = (
    "Greek text: SBL Greek New Testament, © 2010 Society of Biblical Literature "
    "and Logos Bible Software (CC BY 4.0). Translation and literary design in progress."
)
OUR_CREDIT = (
    "Note: this is not a BibleProject translation. It is a very literal translation of the "
    "SBL Greek New Testament, © 2010 Society of Biblical Literature and Logos Bible Software "
    "(CC BY 4.0), with added highlights and structure. Beta: it may still change."
)
# Adapted copies of Tim's units (translation/adapted/adapted-<his id>.usx, his
# original USX beside it in translation/adapted/original/<his id>.usx so the two
# can be diffed; reasons in translation/adapted/NOTES.md). His caption, then this.
ADAPTED_NOTE = (
    ", adapted. The ⓘ notes and any wording changes are additions, not from "
    "BibleProject; they are our opinions, not BibleProject's statements."
)


def greek_verses():
    verses = {}
    for line in open(GREEK, encoding="utf-8"):
        ref, _, text = line.rstrip("\n").partition("\t")
        m = re.match(r"Matt (\d+):(\d+)$", ref)
        if m:
            verses[(int(m[1]), int(m[2]))] = re.sub(r"[⸀⸁⸂⸃]", "", text).strip()
    return verses


def seed():
    verses = greek_verses()
    for book, units in UNITS.items():
        os.makedirs(os.path.join(SRC_DIR, book), exist_ok=True)
        for chapter, a, b in units:
            path = os.path.join(SRC_DIR, book, f"kata-{book}-{chapter}-{a}-{b}.usx")
            if os.path.exists(path):
                continue
            lines = "\n".join(
                f'      <group>\n        <verse number="{v}" /> {verses[(chapter, v)]}\n      </group>'
                for v in range(a, b + 1)
            )
            with open(path, "w", encoding="utf-8") as f:
                f.write(f'<usx version="2.6">\n  <para>\n    <group type="primary">\n{lines}\n    </group>\n  </para>\n</usx>\n')
            print("seeded", os.path.relpath(path, ROOT))


def build_adapted(path, uid):
    tim = uid.removeprefix("adapted-")
    if not os.path.exists(os.path.join(SRC_DIR, "adapted", "original", tim + ".usx")):
        sys.exit(f"{uid}: keep Tim's original USX in translation/adapted/original/{tim}.usx")
    original = json.load(open(os.path.join(OUT_DIR, tim + ".json"), encoding="utf-8"))
    usx = open(path, encoding="utf-8").read()
    xml.dom.minidom.parseString(usx)  # fails loudly on bad XML
    visual = {
        "id": uid,
        "reference": original["reference"],
        "title": original["title"],
        "caption": original["caption"].rstrip().rstrip(".") + ADAPTED_NOTE,
        "usx": usx,
    }
    with open(os.path.join(OUT_DIR, f"{uid}.json"), "w", encoding="utf-8") as f:
        json.dump(visual, f, ensure_ascii=False, indent=1)
    print("built", uid, "(adapted)")


def build():
    for path in sorted(glob.glob(os.path.join(SRC_DIR, "*", "*.usx"))):
        uid = os.path.basename(path)[:-4]
        if uid.startswith("adapted-"):
            build_adapted(path, uid)
            continue
        m = re.match(r"kata-([a-z0-9]+)-(\d+)-(\d+)-(?:(\d+)-)?(\d+)$", uid)
        if not m:
            sys.exit(f"bad unit file name: {uid}")
        book, c1, v1, c2, v2 = m[1], m[2], m[3], m[4], m[5]
        span = f"{c1}:{v1}-{c2}:{v2}" if c2 else f"{c1}:{v1}-{v2}"
        reference = f"{book.capitalize()} {span}"
        usx = open(path, encoding="utf-8").read()
        root = xml.dom.minidom.parseString(usx).documentElement  # fails loudly on bad XML
        translated = root.getAttribute("status") == "translated"
        visual = {
            "id": uid,
            "reference": reference,
            "title": f"Translation and Literary Design of {reference}",
            "caption": f"<bp-cite>{reference}</bp-cite>. {OUR_CREDIT if translated else GREEK_CREDIT}",
            "usx": usx,
        }
        with open(os.path.join(OUT_DIR, f"{uid}.json"), "w", encoding="utf-8") as f:
            json.dump(visual, f, ensure_ascii=False, indent=1)
        print("built", uid, "(translated)" if translated else "(Greek)")
    write_bundles()


if __name__ == "__main__":
    if "--seed" in sys.argv:
        seed()
    build()
