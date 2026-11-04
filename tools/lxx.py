"""Look things up in the Septuagint (Greek Old Testament), for comparing with Matthew.

  python3 tools/lxx.py Exodus 3:19-20            # Greek + Brenton's English (+ dictionary forms)
  python3 tools/lxx.py ex 3:20                    # book names can be any unique start
  python3 tools/lxx.py -s "εκτεινας την χειρα"    # phrase search, accents optional; also searches Matthew
  python3 tools/lxx.py -l εκτεινω χειρ            # verses using all these dictionary forms (any ending)

Data: data/lxx/ (see tools/import_lxx.py). lxx_greek.tsv is Brenton's Greek
text (public domain); lxx_english.tsv is Brenton's 1851 English (public domain);
lxx_lemmas.tsv (gitignored, license unknown) has each word in dictionary form,
but it splits prefixes off verbs (ἐκτείνω shows as "ἐκ ... κτείνω"), so -l
also matches a lemma without its prefix.
"""
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LXX = os.path.join(ROOT, "data", "lxx")


def plain(text):
    """Lowercase, no accents or breathings, final sigma as σ: for matching."""
    text = unicodedata.normalize("NFD", text.lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    return text.replace("ς", "σ")


def load(name):
    path = os.path.join(LXX, name)
    if not os.path.exists(path):
        return {}
    rows = {}
    for line in open(path, encoding="utf-8"):
        ref, _, text = line.rstrip("\n").partition("\t")
        rows[ref] = text
    return rows


def matthew():
    rows = {}
    for line in open(os.path.join(ROOT, "data", "matthew_greek.txt"), encoding="utf-8"):
        ref, _, text = line.rstrip("\n").partition("\t")
        if ref.startswith("Matt "):
            rows[ref.replace("Matt ", "Matthew ")] = re.sub(r"[⸀⸁⸂⸃]", "", text).strip()
    return rows


def split_ref(ref):
    book, _, cv = ref.rpartition(" ")
    c, v = cv.split(":")
    n = re.match(r"\d+", v)
    # A few verses have letters (Esther's additions: 1:1a, 1:1b, ...).
    return book, int(c), int(n[0]) if n else 0, v


def show(args, greek, english, lemmas):
    *book_words, cv = args
    want = " ".join(book_words).lower()
    books = list(dict.fromkeys(split_ref(r)[0] for r in greek))
    match = [b for b in books if b.lower() == want] or [b for b in books if b.lower().startswith(want)]
    if not match:
        sys.exit(f"No book starting with {want!r}")
    if len(match) > 1:
        sys.exit(f"Which one? {', '.join(match)}")
    book = match[0]
    a, _, b = cv.partition("-")
    c1, v1 = map(int, a.split(":"))
    c2, v2 = map(int, b.split(":")) if ":" in b else (c1, int(b or v1))
    refs = sorted(
        {r for r in greek.keys() | english.keys() if split_ref(r)[0] == book and (c1, v1) <= split_ref(r)[1:3] <= (c2, v2)},
        key=lambda r: split_ref(r)[1:],
    )
    for ref in refs:
        print(f"\n{ref}")
        print(f"  {greek.get(ref, '(not in Brenton Greek)')}")
        print(f"  {english.get(ref, '(not in Brenton English)')}")
        if ref in lemmas:
            print(f"  [{lemmas[ref]}]")


def search(phrase, greek, english):
    needle = plain(phrase)
    pattern = re.compile(r"(?<!\w)" + re.escape(needle) + r"(?!\w)")
    for label, rows in (("Septuagint", greek), ("Matthew (SBLGNT)", matthew())):
        hits = [r for r, t in rows.items() if pattern.search(plain(re.sub(r"[^\w\s]", "", t)))]
        print(f"\n{label}: {len(hits)} verse(s)")
        for ref in hits:
            print(f"\n{ref}\n  {rows[ref]}")
            if ref in english:
                print(f"  {english[ref]}")


def lemma_search(words, greek, english, lemmas):
    wanted = [plain(w) for w in words]
    hits = []
    for ref, text in lemmas.items():
        forms = set(plain(text).split())
        # Prefixes are split off in this file: ἐκτείνω may appear as κτείνω.
        if all(w in forms or any(len(f) > 3 and w.endswith(f) for f in forms) for w in wanted):
            hits.append(ref)
    print(f"{len(hits)} verse(s)")
    for ref in hits:
        print(f"\n{ref}\n  {greek.get(ref, '(not in Brenton Greek: ' + lemmas[ref] + ')')}")
        if ref in english:
            print(f"  {english[ref]}")


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    greek, english, lemmas = load("lxx_greek.tsv"), load("lxx_english.tsv"), load("lxx_lemmas.tsv")
    if args[0] == "-s":
        search(" ".join(args[1:]), greek, english)
    elif args[0] == "-l":
        if not lemmas:
            sys.exit("data/lxx/lxx_lemmas.tsv is missing (it's gitignored; see tools/import_lxx.py)")
        lemma_search(args[1:], greek, english, lemmas)
    else:
        show(args, greek, english, lemmas)


if __name__ == "__main__":
    main()
