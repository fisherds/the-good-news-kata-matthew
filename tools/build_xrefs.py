"""Build public/data/xrefs.json: the cross-references behind the ⓘ icons in our
translation units (<note style="x" xref="ID"> in translation/*/*.usx).

Each cross-reference shows evidence, not opinion: the Matthew verse (our English) and
the passage it links to (Brenton's English of the Septuagint, or Tim's English for
another verse of Matthew), with the matching
words in bold and only those Greek words shown, inline, checked against the
Greek (SBLGNT, Brenton's Septuagint). A short note at the bottom
says what the match shows. Texts come from the repo; only what's below is
hand-edited. Re-run after changing XREFS or a unit.

Usage: python3 tools/build_xrefs.py
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Each passage: ref; "match" is the English phrase that matches, the Greek words
# behind it (checked against the Greek text, then shown inline in brackets, since
# readers can't read the rest of the Greek) and, when the English hides the match,
# a literal rendering ("lit. ..."). "mark" is other English worth seeing.
XREFS = [
    {
        "id": "matthew-8-3-hand",
        "title": "Stretching out the hand",
        "matthew": {"ref": "8:3", "unit": "kata-matthew-8-1-4",
                    "match": [("stretching out the hand", "καὶ ἐκτείνας τὴν χεῖρα", None)]},
        "passages": [
            {"ref": "Exodus 3:20",
             "match": [("stretch out my hand", "Καὶ ἐκτείνας τὴν χεῖρα", "stretching out the hand")],
             "mark": ["with all my wonders"]},
        ],
        "note": "The same four Greek words. In Exodus the outstretched hand strikes Egypt with wonders; "
                "here it touches an outcast and makes him clean, the first of the wonders in Matthew 8–9.",
    },
    {
        "id": "matthew-8-2-master",
        "title": "“Master”",
        "matthew": {"ref": "8:2", "unit": "kata-matthew-8-1-4",
                    "match": [("Master", "Κύριε", None), ("want", "θέλῃς", None)]},
        "passages": [
            {"ref": "Matthew 7:21", "unit": "matthew-7-15-23",
             "match": [("Master, master!", "Κύριε κύριε", None), ("desire", "θέλημα", None)]},
        ],
        "note": "The Sermon ends by warning that saying “Master” is not enough; what counts is the Father's "
                "desire. The first person down the mountain says “Master” and leaves it to Jesus' desire: "
                "“if you want” (θέλω, the root of θέλημα).",
    },
    {
        "id": "matthew-8-8-worthy",
        "title": "“I am not worthy”",
        "matthew": {"ref": "8:8", "unit": "kata-matthew-8-5-13",
                    "match": [("I am not worthy", "οὐκ εἰμὶ ἱκανὸς", None)],
                    "mark": ["come in"]},
        "passages": [
            # A passage with "unit" is elsewhere in Matthew, in Tim's English.
            {"ref": "Matthew 3:11", "unit": "matthew-3-7-12",
             "match": [("I am not worthy", "οὐκ εἰμὶ ἱκανὸς", None)],
             "mark": ["the one coming after me"]},
        ],
        "note": "Only two people in Matthew say these words: John the Baptist, about the one coming after him, "
                "and a Gentile centurion, about Jesus coming under his roof.",
    },
    {
        "id": "matthew-8-6-thrown",
        "title": "Paralyzed, thrown down",
        "matthew": {"ref": "8:6", "unit": "kata-matthew-8-5-13",
                    "match": [("has been thrown down", "βέβληται", None), ("paralyzed", "παραλυτικός", None)]},
        "passages": [
            # "bsb": a verse of Matthew we haven't translated yet (Berean Standard Bible,
            # public domain). Switch to our unit when we get there.
            {"ref": "Matthew 9:2", "bsb": True,
             "match": [("paralytic", "παραλυτικὸν", None), ("lying", "βεβλημένον", "thrown down")],
             "mark": ["their faith"]},
            {"ref": "Matthew 9:6", "bsb": True,
             "match": [("authority", "ἐξουσίαν", None), ("go home", "ὕπαγε εἰς τὸν οἶκόν σου", None)]},
        ],
        "note": "The same two words for a man who can't move: paralyzed, and thrown down (the same perfect tense "
                "of βάλλω). Both stories also turn on authority (8:9) and trust (8:10), and end with "
                "“Go” (8:13).",
    },
    {
        "id": "matthew-8-8-healed",
        "title": "Healed from a distance",
        "matthew": {"ref": "8:8", "unit": "kata-matthew-8-5-13",
                    "match": [("will be healed", "ἰαθήσεται", None)]},
        "passages": [
            {"ref": "Matthew 15:28", "bsb": True,
             "match": [("was healed", "ἰάθη", None)],
             "mark": ["your faith is great", "from that very hour"]},
        ],
        "note": "Matthew's stories use this healing word (ἰάομαι) for only two people: a Gentile centurion's boy / servant "
                "and a Canaanite woman's daughter, both healed from a distance after Jesus praises a Gentile's "
                "trust. (It appears once more, in a quote of Isaiah, 13:15.)",
    },
]


def tsv(path):
    rows = {}
    for line in open(path, encoding="utf-8"):
        ref, _, text = line.rstrip("\n").partition("\t")
        rows[ref] = text
    return rows


def matthew_greek():
    rows = {}
    for line in open(os.path.join(ROOT, "data", "matthew_greek.txt"), encoding="utf-8"):
        ref, _, text = line.rstrip("\n").partition("\t")
        if ref.startswith("Matt "):
            rows[ref[5:]] = re.sub(r"[⸀⸁⸂⸃]", "", text).strip()
    return rows


def unit_verse(unit, ref):
    """Plain English of one verse of one of our units."""
    usx = json.load(open(os.path.join(ROOT, "public", "visuals", unit + ".json"), encoding="utf-8"))["usx"]
    usx = re.sub(r"<note\b.*?</note>", "", usx, flags=re.S)
    want = ref.split(":")[1]
    parts = re.split(r'<verse number="(?:\d+:)?(\d+)"\s*/>', usx)
    for n, text in zip(parts[1::2], parts[2::2]):
        if n == want:
            return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text)).replace(" ,", ",").replace(" .", ".").replace("“ ", "“").replace(" ”", "”").replace("‘ ", "‘").replace(" ’", "’").replace(" !", "!").strip()
    raise SystemExit(f"{unit} has no verse {ref}")


def emphasize(text, greek, match=(), mark=()):
    """HTML-escape the English, bolding each matching phrase with its Greek
    inline after it, and wrapping other phrases worth seeing in <mark>."""
    spans = []
    for en, gk, lit in match:
        if gk not in greek:
            raise SystemExit(f"{gk!r} not found in {greek!r}")
        extra = f" lit. {html.escape(lit)}" if lit else ""
        spans.append((en, f'<strong>{html.escape(en)}</strong> (<strong lang="grc">{html.escape(gk)}</strong>{extra})'))
    spans += [(phrase, f"<mark>{html.escape(phrase)}</mark>") for phrase in mark]
    found = []
    for phrase, rendered in spans:
        at = text.find(phrase)
        if at < 0:
            raise SystemExit(f"{phrase!r} not found in {text!r}")
        found.append((at, at + len(phrase), rendered))
    out, pos = [], 0
    for start, end, rendered in sorted(found):
        out += [html.escape(text[pos:start]), rendered]
        pos = end
    out.append(html.escape(text[pos:]))
    return "".join(out)


def main():
    lxx_gk = tsv(os.path.join(ROOT, "data", "lxx", "lxx_greek.tsv"))
    lxx_en = tsv(os.path.join(ROOT, "data", "lxx", "lxx_english.tsv"))
    mt_gk = matthew_greek()
    bsb = {c["chapter"]: {v["verse"]: v["text"] for v in c["verses"]}
           for c in json.load(open(os.path.join(ROOT, "data", "matthew_bsb.json"), encoding="utf-8"))}
    out = []
    for x in XREFS:
        m = x["matthew"]
        passages = [{
            "ref": html.escape("Matthew " + m["ref"]),
            "en": emphasize(unit_verse(m["unit"], m["ref"]), mt_gk[m["ref"]], m.get("match", ()), m.get("mark", ())),
            "sources": "kata Matthew · Greek: SBLGNT",
        }]
        for p in x["passages"]:
            if p.get("bsb"):
                ref = p["ref"].removeprefix("Matthew ")
                c, v = (int(n) for n in ref.split(":"))
                passages.append({
                    "ref": html.escape(p["ref"]),
                    "en": emphasize(bsb[c][v], mt_gk[ref], p.get("match", ()), p.get("mark", ())),
                    "sources": "Berean Standard Bible (public domain) · Greek: SBLGNT",
                })
                continue
            if "unit" in p:
                ref = p["ref"].removeprefix("Matthew ")
                passages.append({
                    "ref": html.escape(p["ref"]),
                    "en": emphasize(unit_verse(p["unit"], ref), mt_gk[ref], p.get("match", ()), p.get("mark", ())),
                    "sources": "Tim Mackie’s translation (BibleProject) · Greek: SBLGNT",
                })
                continue
            passages.append({
                "ref": html.escape(p["ref"] + " (LXX, the Greek translation of the Hebrew Bible)"),
                "en": emphasize(lxx_en[p["ref"]], lxx_gk[p["ref"]], p.get("match", ()), p.get("mark", ())),
                "sources": "Brenton’s English (1851) · Greek: Brenton’s Septuagint",
            })
        out.append({"id": x["id"], "title": x["title"], "passages": passages, "note": html.escape(x["note"])})
    path = os.path.join(ROOT, "public", "data", "xrefs.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"xrefs": out}, f, ensure_ascii=False, indent=1)
    print(f"wrote {len(out)} cross-reference(s) to public/data/xrefs.json")


if __name__ == "__main__":
    main()
