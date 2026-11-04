"""Study sheet for translating a passage of Matthew: every Greek word, what it
means, and how Tim Mackie translated the same word in 1:1-7:29.

  python3 tools/study.py 8:5-13          # one chapter
  python3 tools/study.py 8:28-9:1        # across chapters

For each verse: the SBLGNT text, then each word with its Strong's number,
the KJV gloss from the concordance, the lexicon's short definition, how often
Matthew uses the word, and up to three of Tim's verses that use it (his line
for that verse, so you can see his English). Words already in
docs/glossary.md are marked.

Reads the gitignored local reference files (data/matthew_concordance.json,
data/greek.json), so it only runs on a machine that has them. Output is for
the translator, never for the site.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")


def key(c, v):
    return c * 1000 + v


def parse_range(text):
    a, _, b = text.partition("-")
    c1, v1 = map(int, a.split(":"))
    if not b:
        return key(c1, v1), key(c1, v1)
    if ":" in b:
        c2, v2 = map(int, b.split(":"))
    else:
        c2, v2 = c1, int(b)
    return key(c1, v1), key(c2, v2)


def load_greek():
    verses = {}
    for line in open(os.path.join(DATA, "matthew_greek.txt"), encoding="utf-8"):
        ref, _, text = line.rstrip("\n").partition("\t")
        m = re.match(r"Matt (\d+):(\d+)$", ref)
        if m:
            verses[key(int(m[1]), int(m[2]))] = re.sub(r"[⸀⸁⸂⸃]", "", text).strip()
    return verses


def load_concordance():
    out = {}
    for entry in json.load(open(os.path.join(DATA, "matthew_concordance.json"), encoding="utf-8")):
        vid = entry["id"]
        out[key(int(vid[2:5]), int(vid[5:]))] = entry["verse"]
    return out


def load_lexicon():
    lex = {}
    for entry in json.load(open(os.path.join(DATA, "greek.json"), encoding="utf-8")):
        num = "g" + entry["strongs"][1:].lstrip("0")
        lex[num] = entry
    return lex


def tim_verses():
    """Tim's English for each verse of 1:1-7:29, from our local copies of his units."""
    out = {}
    for path in sorted(glob.glob(os.path.join(ROOT, "public", "visuals", "matthew-*.json"))):
        visual = json.load(open(path, encoding="utf-8"))
        usx = visual.get("usx")
        if not usx:
            continue
        chapter = int(re.search(r"(\d+):", visual["reference"])[1])
        text = re.sub(r"<verse number=\"([^\"]+)\"\s*/>", lambda m: "\x00" + m[1] + "\x00", usx)
        text = re.sub(r"<[^>]+>", " ", text)
        parts = text.split("\x00")
        current = None
        for i, part in enumerate(parts):
            if i % 2:
                n = part
                if ":" in n:
                    chapter, n = map(int, n.split(":"))
                elif n.isdigit():
                    n = int(n)
                else:
                    continue
                k = key(chapter, n)
                # Skip the genealogy's generation counters and 4:23-24's numbered list.
                if current and (k <= current or k > current + 3):
                    continue
                current = k
            elif current:
                out[current] = (out.get(current, "") + " " + re.sub(r"\s+", " ", part)).strip()
    return out


def glossary_words():
    path = os.path.join(ROOT, "docs", "glossary.md")
    if not os.path.exists(path):
        return set()
    return set(re.findall(r"^\| ([^|]+?) \|", open(path, encoding="utf-8").read(), re.M))


def main():
    first, last = parse_range(sys.argv[1])
    greek, conc, lex, tim = load_greek(), load_concordance(), load_lexicon(), tim_verses()
    known = glossary_words()
    uses = {}
    for k, words in conc.items():
        for w in words:
            uses.setdefault(w["number"].lower(), []).append(k)
    # The concordance follows the Textus Receptus, so a word's form can differ
    # slightly from the SBLGNT line above it. Very common words (the, and, he)
    # and words already shown earlier in the passage are skipped.
    seen = set()
    for k in sorted(v for v in greek if first <= v <= last):
        c, v = divmod(k, 1000)
        print(f"\n## {c}:{v}\n\n{greek[k]}\n")
        for w in sorted(conc.get(k, []), key=lambda w: w["i"]):
            num = w["number"].lower()
            refs = sorted(set(uses.get(num, [])))
            if num in seen or len(refs) > 150:
                continue
            seen.add(num)
            entry = lex.get(num, {})
            short = entry.get("data", {}).get("def", {}).get("short", "")
            earlier = [r for r in refs if r < 8000 and r in tim][:3]
            mark = " [glossary]" if any(w["word"].strip(",.;:·") in g for g in known) else ""
            print(f"- {w['word']} ({num}, {len(refs)}× in Matthew){mark}: KJV \"{w['text']}\"; {short[:90]}")
            for r in earlier:
                rc, rv = divmod(r, 1000)
                print(f"    Tim {rc}:{rv}: {tim[r][:150]}")


if __name__ == "__main__":
    main()
