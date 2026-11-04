"""Build public/data/xrefs.json: the cross-references behind the ⓘ icons in our
translation units (<note style="x" xref="ID"> in translation/*/*.usx).

Each cross-reference shows evidence, not opinion: the Matthew verse (our English) and
the passage it links to (Brenton's English of the Septuagint), with the matching
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
            return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text)).replace(" ,", ",").replace(" .", ".").strip()
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
    out = []
    for x in XREFS:
        m = x["matthew"]
        passages = [{
            "ref": html.escape("Matthew " + m["ref"]),
            "en": emphasize(unit_verse(m["unit"], m["ref"]), mt_gk[m["ref"]], m.get("match", ()), m.get("mark", ())),
            "sources": "kata Matthew · Greek: SBLGNT",
        }]
        for p in x["passages"]:
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
