"""One-time import of the Septuagint (LXX) into data/lxx/, one verse per line:
"Exodus 3:20<TAB>text".

  python3 tools/import_lxx.py BRENTON_USFM_DIR BOLLS_DIR

- BRENTON_USFM_DIR: ebible.org's grcbrent_usfm.zip, unzipped (Brenton's Greek
  Septuagint, public domain). The real Greek text, with accents and endings.
  -> data/lxx/lxx_greek.tsv
- BOLLS_DIR: a folder holding bolls.life's LXXEraw.json (Brenton's 1851 English,
  public domain) and LXXraw.json (the LXX with every word in dictionary form,
  e.g. "ἐκτείνω ὁ χείρ"; source license unknown, so it stays gitignored).
  -> data/lxx/lxx_english.tsv, data/lxx/lxx_lemmas.tsv

Versification follows each source; they mostly agree but not everywhere
(Psalms, Jeremiah, Esther, Daniel especially).
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "lxx")

USFM_BOOKS = {
    "GEN": "Genesis", "EXO": "Exodus", "LEV": "Leviticus", "NUM": "Numbers", "DEU": "Deuteronomy",
    "JOS": "Joshua", "JDG": "Judges", "RUT": "Ruth", "1SA": "1 Samuel", "2SA": "2 Samuel",
    "1KI": "1 Kings", "2KI": "2 Kings", "1CH": "1 Chronicles", "2CH": "2 Chronicles",
    "EZR": "Ezra", "NEH": "Nehemiah", "EST": "Esther", "ESG": "Esther", "JOB": "Job",
    "PSA": "Psalms", "PRO": "Proverbs", "ECC": "Ecclesiastes", "SNG": "Song of Songs",
    "ISA": "Isaiah", "JER": "Jeremiah", "LAM": "Lamentations", "EZK": "Ezekiel",
    "DAN": "Daniel", "DAG": "Daniel", "HOS": "Hosea", "JOL": "Joel", "AMO": "Amos",
    "OBA": "Obadiah", "JON": "Jonah", "MIC": "Micah", "NAM": "Nahum", "HAB": "Habakkuk",
    "ZEP": "Zephaniah", "HAG": "Haggai", "ZEC": "Zechariah", "MAL": "Malachi",
    "TOB": "Tobit", "JDT": "Judith", "WIS": "Wisdom", "SIR": "Sirach", "BAR": "Baruch",
    "LJE": "Epistle of Jeremiah", "SUS": "Susanna", "BEL": "Bel and the Dragon",
    "1MA": "1 Maccabees", "2MA": "2 Maccabees", "3MA": "3 Maccabees", "4MA": "4 Maccabees",
    "1ES": "1 Esdras", "MAN": "Prayer of Manasseh",
}

BOLLS_BOOKS = {
    1: "Genesis", 2: "Exodus", 3: "Leviticus", 4: "Numbers", 5: "Deuteronomy", 6: "Joshua",
    7: "Judges", 8: "Ruth", 9: "1 Samuel", 10: "2 Samuel", 11: "1 Kings", 12: "2 Kings",
    13: "1 Chronicles", 14: "2 Chronicles", 15: "Ezra", 16: "Nehemiah", 17: "Esther", 18: "Job",
    19: "Psalms", 20: "Proverbs", 21: "Ecclesiastes", 22: "Song of Songs", 23: "Isaiah",
    24: "Jeremiah", 25: "Lamentations", 26: "Ezekiel", 27: "Daniel", 28: "Hosea", 29: "Joel",
    30: "Amos", 31: "Obadiah", 32: "Jonah", 33: "Micah", 34: "Nahum", 35: "Habakkuk",
    36: "Zephaniah", 37: "Haggai", 38: "Zechariah", 39: "Malachi", 67: "1 Esdras", 68: "Tobit",
    69: "Judith", 70: "Wisdom", 71: "Sirach", 72: "Epistle of Jeremiah", 73: "Baruch",
    74: "1 Maccabees", 75: "2 Maccabees", 76: "3 Maccabees", 78: "Susanna",
    79: "Bel and the Dragon", 80: "4 Maccabees", 83: "Prayer of Manasseh", 85: "Psalms of Solomon",
    86: "Odes", 88: "Azariah",
}


def write(name, rows):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        for ref, text in rows:
            f.write(f"{ref}\t{text}\n")
    print(f"wrote {len(rows)} verses to data/lxx/{name}")


def brenton_greek(folder):
    rows = []
    for path in sorted(glob.glob(os.path.join(folder, "*.usfm"))):
        book = chapter = None
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if line.startswith("\\id "):
                book = USFM_BOOKS[line.split()[1]]
            elif line.startswith("\\c "):
                chapter = line.split()[1]
            elif line.startswith("\\v "):
                _, verse, text = line.split(" ", 2)
                text = re.sub(r"\\\w+\*?", "", text)
                rows.append((f"{book} {chapter}:{verse}", re.sub(r"\s+", " ", text).strip()))
            elif rows and line and not line.startswith("\\"):
                ref, text = rows[-1]
                rows[-1] = (ref, text + " " + line)
    return rows


def bolls(path):
    rows = []
    for v in json.load(open(path, encoding="utf-8")):
        text = re.sub(r"<[^>]+>", "", v["text"])
        rows.append((f"{BOLLS_BOOKS[v['book']]} {v['chapter']}:{v['verse']}", re.sub(r"\s+", " ", text).strip()))
    return rows


def main():
    usfm_dir, bolls_dir = sys.argv[1:3]
    write("lxx_greek.tsv", brenton_greek(usfm_dir))
    write("lxx_english.tsv", bolls(os.path.join(bolls_dir, "LXXEraw.json")))
    write("lxx_lemmas.tsv", bolls(os.path.join(bolls_dir, "LXXraw.json")))


if __name__ == "__main__":
    main()
