"""Build public/data/otconnections_quotes.json: the ten Old Testament quotations
in Matthew 1:1-4:17 (seven "through the prophet" quotes plus Jesus' three
"it has been written" answers in the wilderness), each with the Old Testament
passages it draws on in the Berean Standard Bible (public domain), fetched
from bolls.life.

The quotes themselves (which OT passages, which verses to highlight, the short
notes) are edited here; re-run after changing them.

Usage: python3 tools/fetch_ot_quotes.py
"""
import json
import os
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public", "data", "otconnections_quotes.json")

# bolls.life book numbers.
BOOKS = {"Deuteronomy": 5, "Judges": 7, "2 Samuel": 10, "Psalm": 19, "Isaiah": 23,
         "Jeremiah": 24, "Hosea": 28, "Micah": 33}

# kind: "fill" = the "so that it would be filled-full (πληρόω)" formula;
# "prophet" = names the prophet but without "filled-full"; "jesus" = Jesus' "it has been written".
# Each passage: (book, chapter, first verse, last verse, verses to highlight).
QUOTES = [
    {"id": "1", "kind": "fill", "title": "Immanuel", "matthew": "1:22–1:23", "unit": "matthew-1-18-25",
     "formula": "ἵνα πληρωθῇ τὸ ῥηθὲν ὑπὸ κυρίου διὰ τοῦ προφήτου",
     "passages": [("Isaiah", 7, 10, 17, [14, 16]), ("Isaiah", 8, 8, 8, [8])],
     "note": "The sign to Ahaz was a timeline: before the boy knows good from evil, the land of the two kings "
             "he dreads will be deserted. Trust God, not Assyria. Jesus fills full the name: God with us."},
    {"id": "2", "kind": "prophet", "title": "Bethlehem", "matthew": "2:5–2:6", "unit": "matthew-2-1-12",
     "formula": "οὕτως γὰρ γέγραπται διὰ τοῦ προφήτου",
     "passages": [("Micah", 5, 2, 5, [2, 4]), ("2 Samuel", 5, 1, 3, [2])],
     "note": "Not \"filled-full\": the chief priests and scribes quote it to Herodes. A fusion of Micah's ruler "
             "from Bethlehem with 2 Samuel's \"you will shepherd my people Israel\". Jesus is the new King David."},
    {"id": "3", "kind": "fill", "title": "Egypt", "matthew": "2:15", "unit": "matthew-2-13-23",
     "formula": "ἵνα πληρωθῇ τὸ ῥηθὲν ὑπὸ κυρίου διὰ τοῦ προφήτου",
     "passages": [("Hosea", 11, 1, 5, [1])],
     "note": "Hosea looks back, not ahead: a lament. Israel was called out of Egypt and kept running back to the "
             "Baals, to Egypt, to Assyria. Jesus is the son who is called out and stays out."},
    {"id": "4", "kind": "fill", "title": "Rachel", "matthew": "2:17–2:18", "unit": "matthew-2-13-23",
     "formula": "τότε ἐπληρώθη τὸ ῥηθὲν διὰ Ἰερεμίου τοῦ προφήτου",
     "passages": [("Jeremiah", 31, 15, 17, [15, 17])],
     "note": "Rama is where the exiles were gathered for Babylon. Mothers grieving under a cruel ruler keeps "
             "happening, but Jeremiah's next lines are hope: your children will return. Jesus fills full that hope."},
    {"id": "5", "kind": "fill", "title": "Nazareth", "matthew": "2:23", "unit": "matthew-2-13-23",
     "formula": "ὅπως πληρωθῇ τὸ ῥηθὲν διὰ τῶν προφητῶν",
     "passages": [("Isaiah", 11, 1, 1, [1]), ("Judges", 13, 5, 5, [5]), ("Psalm", 22, 6, 6, [6]),
                  ("Isaiah", 53, 3, 3, [3])],
     "note": "\"The prophets\", plural: no single verse says it. Ναζωραῖος echoes netzer (the branch, Isaiah 11:1), "
             "nazir (set apart from birth, Judges 13:5), and despised little Nazareth (Psalm 22:6, Isaiah 53:3)."},
    {"id": "6", "kind": "prophet", "title": "A voice in the wilderness", "matthew": "3:3", "unit": "matthew-3-1-6",
     "formula": "οὗτος γάρ ἐστιν ὁ ῥηθεὶς διὰ Ἠσαΐου τοῦ προφήτου",
     "passages": [("Isaiah", 40, 3, 5, [3])],
     "note": "Not \"filled-full\": John the immerser is the voice that prepares the way of the Lord."},
    {"id": "J1", "kind": "jesus", "title": "Test 1: Bread", "matthew": "4:4", "unit": "matthew-4-1-11",
     "formula": "γέγραπται",
     "passages": [("Deuteronomy", 8, 2, 3, [3])],
     "note": "Israel's forty years of testing in the wilderness, Jesus' forty days."},
    {"id": "J2", "kind": "jesus", "title": "Test 2: Temple", "matthew": "4:7", "unit": "matthew-4-1-11",
     "formula": "πάλιν γέγραπται",
     "passages": [("Deuteronomy", 6, 16, 16, [16])],
     "note": "Massah, where Israel tested God by demanding proof that he was with them."},
    {"id": "J3", "kind": "jesus", "title": "Test 3: Kingdoms", "matthew": "4:10", "unit": "matthew-4-1-11",
     "formula": "γέγραπται γάρ",
     "passages": [("Deuteronomy", 6, 13, 15, [13])],
     "note": "Bow down to the Lord your God and serve him only."},
    {"id": "7", "kind": "fill", "title": "Zebulun and Naphtali", "matthew": "4:14–4:16", "unit": "matthew-4-12-17",
     "formula": "ἵνα πληρωθῇ τὸ ῥηθὲν διὰ Ἠσαΐου τοῦ προφήτου",
     "passages": [("Isaiah", 9, 1, 7, [1, 2])],
     "note": "Jesus moves from Nazareth (Zebulun) to Capernaum (Naphtali), the land first humbled by Assyria. "
             "The light rises there first, and Isaiah goes on: a child is born to us, a son is given."},
]


def fetch_chapter(book, chapter, cache={}):
    key = (book, chapter)
    if key not in cache:
        url = f"https://bolls.life/get-text/BSB/{BOOKS[book]}/{chapter}/"
        with urllib.request.urlopen(url) as response:
            cache[key] = {v["verse"]: v["text"].strip() for v in json.loads(response.read())}
    return cache[key]


def main():
    out = []
    for quote in QUOTES:
        passages = []
        for book, chapter, first, last, focus in quote["passages"]:
            verses = fetch_chapter(book, chapter)
            ref = f"{book} {chapter}:{first}" + (f"–{last}" if last != first else "")
            passages.append({"ref": ref, "focus": focus,
                             "verses": [{"v": v, "text": verses[v]} for v in range(first, last + 1)]})
        out.append({**quote, "passages": passages})
    data = {"translation": "Berean Standard Bible (BSB), public domain", "quotes": out}
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"Wrote {len(out)} quotes to {OUT}")


if __name__ == "__main__":
    main()
