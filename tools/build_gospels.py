"""Build public/data/ninemiraclestories_gospels.json: the "Other Gospels" pop-ups
on /ninemiraclestories. For each story, where it is in Mark, Luke (and John),
the accounts side by side in "beats" (the same moment on one row), and a short
discussion: how they are alike, how they differ (optional: only when it is
interesting to a general reader), what Matthew is doing.

English only, little Greek: Matthew in our translation (kata Matthew; the BSB
where a unit is still Greek only), Mark and Luke in the Berean Standard Bible
(public domain). Every piece of text is checked against its verse, so a beat
can quote part of a verse but never change it. "only" marks words worth seeing
that only this Gospel has. Edit STORIES and re-run.

Usage: python3 tools/build_gospels.py
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_xrefs import ROOT, comment, unit_verse  # noqa: E402

BOOKS = ["Matthew", "Mark", "Luke", "John"]

# A beat cell: a list of (ref, piece, only). piece None = the whole verse;
# only = phrases inside it to mark as found only in this Gospel.
# A story's optional "words": {book: {ref: [(english, greek, color)]}} shows a key
# word with its Greek in brackets, colored (checked against SBLGNT). Use it only for
# the one word the story turns on (the centurion: boy / slave / son). Its "key" lists
# the colors for the line under the texts.
STORIES = [
    {
        "id": "leper",
        "title": "You can make me clean",
        "matthew": {"ref": "8:1–4", "unit": "kata-matthew-8-1-4"},
        "accounts": {"Mark": "1:40–45", "Luke": "5:12–16"},
        "before": {"Matthew": "The Sermon on the Mount (5–7)",
                   "Mark": "Preaching through Galilee (1:35–39)",
                   "Luke": "Calling Simon, James and John (5:1–11)"},
        "beats": [
            {"label": "Setting",
             "Matthew": [("8:1", None, ["when he came down from the mountain", "many crowds followed him"])],
             "Luke": [("5:12", "While Jesus was in one of the towns,", [])]},
            {"label": "He comes",
             "Matthew": [("8:2", "And look, a skin-diseased man, approaching, was bowing down to him, saying,", ["bowing down"])],
             "Mark": [("1:40", "Then a leper came to Jesus, begging on his knees:", ["on his knees"])],
             "Luke": [("5:12", "a man came along who was covered with leprosy. When he saw Jesus, he fell facedown and begged Him,",
                       ["covered with leprosy", "fell facedown"])]},
            {"label": "“If you want”",
             "Matthew": [("8:2", "“Master, if you want, you are able to make me clean.”", [])],
             "Mark": [("1:40", "“If You are willing, You can make me clean.”", [])],
             "Luke": [("5:12", "“Lord, if You are willing, You can make me clean.”", [])]},
            {"label": "The touch",
             "Matthew": [("8:3", "And stretching out the hand, he touched him, saying, “I want. Be clean.”", [])],
             "Mark": [("1:41", None, ["Moved with compassion"])],
             "Luke": [("5:13", "Jesus reached out His hand and touched the man. “I am willing,” He said. “Be clean!”", [])]},
            {"label": "Clean",
             "Matthew": [("8:3", "And immediately his skin disease was made clean.", [])],
             "Mark": [("1:42", None, [])],
             "Luke": [("5:13", "And immediately the leprosy left him.", [])]},
            {"label": "Sent off",
             "Mark": [("1:43", None, ["with a stern warning"])]},
            {"label": "“Tell no one, go to the priest”",
             "Matthew": [("8:4", None, [])],
             "Mark": [("1:44", None, [])],
             "Luke": [("5:14", None, [])]},
            {"label": "Afterward",
             "Mark": [("1:45", None, ["openly began to proclaim and spread the news",
                                      "Jesus could no longer enter a town in plain view"])],
             "Luke": [("5:15", None, []), ("5:16", None, ["to pray"])]},
        ],
        "after": {"Matthew": "A centurion’s boy (8:5–13)",
                  "Mark": "The paralyzed man (2:1–12)",
                  "Luke": "The paralyzed man (5:17–26)"},
        "alike": "The heart of the story is nearly word for word in all three: “if you want, you are able to make me "
                 "clean”, the hand stretched out, the touch, “I want. Be clean”, and the command to show himself to "
                 "the priest with the offering Moses commanded, “as a witness to them”. What Jesus says is the same "
                 "every time.",
        "point": "The Sermon has just said: “Don’t suppose that I have come to do away with the Torah or the Prophets. "
                 "I have not come to do away with, but to fill them full” (5:17). Now, coming down the mountain like Moses, the first "
                 "thing Jesus does looks like doing away with the Torah: he touches an unclean man. Then he sends him to the "
                 "priest with the offering Moses commanded. Matthew cuts everything else so the story ends there. "
                 "The Torah could only declare a man clean; Jesus makes him clean, and then honors the Torah.\n"
                 "Near its end the Sermon warned: “Not everyone who says to me, ‘Master, master!’ will enter into "
                 "the kingdom of the skies, but rather the one who does the desire of my Father in the skies” (7:21). "
                 "The first person down the mountain calls Jesus “Master”, and then leaves it to what Jesus wants: "
                 "“if you want”.",
    },
    {
        "id": "centurion",
        "title": "The centurion’s boy",
        "matthew": {"ref": "8:5–13", "unit": "kata-matthew-8-5-13"},
        "accounts": {"Luke": "7:1–10"},
        # The one word this story turns on: what is the sick one called?
        "words": {
            "Matthew": {"8:6": [("my boy", "παῖς", "blue")], "8:8": [("my boy", "παῖς", "blue")],
                        "8:9": [("my slave", "δούλῳ", "purple")], "8:13": [("the boy", "παῖς", "blue")]},
            "Luke": {"7:2": [("servant", "δοῦλος", "purple")], "7:3": [("servant", "δοῦλον", "purple")],
                     "7:7": [("my servant", "παῖς", "blue")], "7:8": [("my servant", "δούλῳ", "purple")],
                     "7:10": [("servant", "δοῦλον", "purple")]},
        },
        "key": [("boy (παῖς)", "blue"), ("slave, servant (δοῦλος)", "purple")],
        "before": {"Matthew": "A man with a skin disease (8:1–4)",
                   "Luke": "The Sermon on the Plain (6:20–49)"},
        "beats": [
            {"label": "Capernaum",
             "Matthew": [("8:5", "Now when he entered into Kapharnaoum,", [])],
             "Luke": [("7:1", None, [])]},
            {"label": "Asking for the boy",
             "Matthew": [("8:5", "a centurion approached him, pleading with him", ["approached him"]),
                         ("8:6", None, ["paralyzed, terribly tormented"])],
             "Luke": [("7:2", None, ["highly valued"]), ("7:3", None, ["he sent some Jewish elders"]),
                      ("7:4", None, ["This man is worthy"]), ("7:5", None, ["he loves our nation and has built our synagogue"])]},
            {"label": "Will he come?",
             "Matthew": [("8:7", None, [])],
             "Luke": [("7:6", "So Jesus went with them.", [])]},
            {"label": "“I am not worthy”",
             "Matthew": [("8:8", "And responding, the centurion said, “Master, I am not worthy that you come in under my roof,", [])],
             "Luke": [("7:6", "But when He was not far from the house, the centurion sent friends with the message: "
                              "“Lord, do not trouble Yourself, for I am not worthy to have You come under my roof.",
                       ["sent friends"]),
                      ("7:7", "That is why I did not consider myself worthy to come to You.",
                       ["I did not consider myself worthy to come to You"])]},
            {"label": "“Only say a word”",
             "Matthew": [("8:8", "but only speak with a word, and my boy will be healed.", [])],
             "Luke": [("7:7", "But just say the word, and my servant will be healed.", [])]},
            {"label": "“I too am a man under authority”",
             "Matthew": [("8:9", None, [])],
             "Luke": [("7:8", None, [])]},
            {"label": "Jesus is amazed",
             "Matthew": [("8:10", None, [])],
             "Luke": [("7:9", None, [])]},
            {"label": "From east and west",
             "asides": {"Luke": "Luke has this saying later, on the way to Jerusalem:"},
             "Matthew": [("8:11", None, []), ("8:12", None, ["the sons of the kingdom"])],
             "Luke": [("13:28", None, []), ("13:29", None, ["and north and south"])]},
            {"label": "“Go!”",
             "Matthew": [("8:13", "And Iesous said to the centurion, “Go! As you trusted, may it be done for you.”", [])]},
            {"label": "Healed",
             "Matthew": [("8:13", "And the boy was healed in that hour.", [])],
             "Luke": [("7:10", None, [])]},
        ],
        "after": {"Matthew": "Peter’s mother-in-law (8:14–17)",
                  "Luke": "A widow’s son at Nain (7:11–17)"},
        "alike": "Matthew and Luke tell the centurion’s words almost exactly alike: “I am not worthy that you come "
                 "under my roof”, “only say a word”. “I too am a man under authority…” is the same thirty Greek "
                 "words in both (Luke adds one). And in both, Jesus is amazed: not even in Israel has he found such "
                 "trust.",
        "different": [
            "Son or servant? Follow the colors. Matthew says boy (παῖς, pais) every time, a word that can mean a "
            "son or a servant (or slave). Matthew even uses it of Jesus: 12:18 quotes Isaiah 42:1, “Look, my παῖς, "
            "whom I chose.” Luke’s narrator, however, says a highly valued slave (δοῦλος, doulos), but in the "
            "centurion’s own words he is still “my boy” (7:7). Perhaps παῖς was handed down as the centurion’s own "
            "word, and Luke, knowing it meant a highly valued slave, made that plain for his readers when speaking "
            "as narrator but left the quote unchanged. Either way the two don’t clash: in Greek παῖς is the ordinary "
            "word for a boy and for a household servant, and a **highly valued** δοῦλος is a παῖς.",
            "John 4:46–54 also has a similar story: a royal official’s son, in Capernaum, healed from a distance.",
        ],
        "point": "The first two people down the mountain: a man of Israel, then a man from outside it. The man "
                 "with the skin disease is sent to Israel’s priest with the offering Moses commanded, “as a witness "
                 "to them”. The centurion is a Gentile: “with no one in Israel have I found such trust.”\n"
                 "Matthew tells the story more briefly than Luke: no elders, no friends, one word for the boy. Yet "
                 "he makes room for two verses Luke keeps for later (Luke 13:28–29), and here they turn the story "
                 "into a warning: outsiders like this centurion will recline at table with Abraham, Isaac and Jacob, "
                 "while “the sons of the kingdom”, the ones who assumed they had a place, are thrown out.\n"
                 "Warnings are important to Matthew’s audience. For example, Matthew says the phrase “crying and "
                 "grinding of teeth” six times, but Luke uses it only once, and it never appears in Mark or John.",
    },
]


def bsb(book):
    path = os.path.join(ROOT, "data", f"{book.lower()}_bsb.json")
    return {c["chapter"]: {v["verse"]: v["text"] for v in c["verses"]}
            for c in json.load(open(path, encoding="utf-8"))}


GREEK_FILES = {"Matthew": "matthew", "Mark": "mark", "Luke": "luke", "John": "john"}
_greek = {}


def greek_verse(book, ref):
    if book not in _greek:
        prefix = {"Matthew": "Matt"}.get(book, book) + " "
        _greek[book] = {}
        for line in open(os.path.join(ROOT, "data", f"{GREEK_FILES[book]}_greek.txt"), encoding="utf-8"):
            r, _, text = line.rstrip("\n").partition("\t")
            if r.startswith(prefix):
                _greek[book][r[len(prefix):]] = re.sub(r"[⸀⸁⸂⸃]", "", text).strip()
    return _greek[book][ref]


def bold(text):
    """**words** in a bullet become <strong>."""
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)


def marked(text, only, words=(), used=None):
    """HTML-escape text: each "only" phrase in <mark>; each key word bold and colored,
    its Greek in brackets after it. A word is matched as a whole word."""
    found = []
    for phrase in only:
        at = text.find(phrase)
        if at < 0:
            raise SystemExit(f"{phrase!r} not found in {text!r}")
        found.append((at, at + len(phrase), "<mark>" + html.escape(phrase) + "</mark>"))
    for en, gk, color in words:
        hit = re.search(r"(?<!\w)" + re.escape(en) + r"(?!\w)", text)
        if not hit:
            continue  # the verse is split over beats: this word is in another piece
        if used is not None:
            used.add((en, gk))
        found.append((hit.start(), hit.end(),
                      f'<span class="hl hl-{color}"><strong>{html.escape(en)}</strong> '
                      f'(<span lang="grc">{html.escape(gk)}</span>)</span>'))
    out, pos = [], 0
    for start, end, rendered in sorted(found):
        if start < pos:
            raise SystemExit(f"overlapping marks in {text!r}")
        out += [html.escape(text[pos:start]), rendered]
        pos = end
    return "".join(out) + html.escape(text[pos:])


def main():
    texts = {}
    out = []
    for story in STORIES:
        m = story["matthew"]
        books = ["Matthew"] + [b for b in BOOKS if b in story["accounts"]]
        refs = {"Matthew": m["ref"], **story["accounts"]}

        def verse(book, ref):
            if book == "Matthew":
                if m.get("bsb"):
                    c, v = (int(n) for n in ref.split(":"))
                    return bsb("Matthew")[c][v]
                return unit_verse(m["unit"], ref)
            if book not in texts:
                texts[book] = bsb(book)
            c, v = (int(n) for n in ref.split(":"))
            return texts[book][c][v]

        used = set()
        beats = []
        for beat in story["beats"]:
            row = {"label": beat["label"], "cells": {}}
            for book in books:
                pieces = []
                for ref, piece, only in beat.get(book, []):
                    text = verse(book, ref)
                    if piece is not None:
                        if piece not in text:
                            raise SystemExit(f"{book} {ref}: {piece!r} not in {text!r}")
                        text = piece
                    # a verse outside the account's own chapter shows its full reference
                    home = refs[book].split(":")[0]
                    shown = ref if ref.split(":")[0] != home else ref.split(":")[1]
                    words = story.get("words", {}).get(book, {}).get(ref, [])
                    for en, gk, color in words:
                        if gk not in greek_verse(book, ref):
                            raise SystemExit(f"{book} {ref}: {gk!r} not in the Greek")
                    pieces.append(f'<sup>{shown}</sup>' + marked(text, only, words, used))
                if pieces:
                    aside = beat.get("asides", {}).get(book)
                    row["cells"][book] = (f'<span class="aside">{html.escape(aside)}</span> ' if aside else "") + " ".join(pieces)
            beats.append(row)
        for book, by_ref in story.get("words", {}).items():
            for ref, words in by_ref.items():
                for en, gk, _ in words:
                    if (en, gk) not in used:
                        raise SystemExit(f"{story['id']}: {book} {ref} word {en!r} is in no beat")
        source = "Berean Standard Bible (public domain)" if m.get("bsb") else "kata Matthew"
        out.append({
            "id": story["id"],
            "title": story["title"],
            "books": books,
            "refs": refs,
            "headnotes": story.get("headnotes", {}),  # e.g. John: "perhaps the same event"
            "sources": f"Matthew: {source}. "
                       + ", ".join(b for b in books if b != "Matthew") + ": Berean Standard Bible (public domain).",
            "before": story["before"],
            "beats": beats,
            "after": story["after"],
            "alike": comment(story["alike"]),
            # "different" is optional: only when the differences are interesting to a general reader.
            **({"different": "<ul>" + "".join(f"<li>{bold(html.escape(d))}</li>" for d in story["different"]) + "</ul>"}
               if story.get("different") else {}),
            "point": comment(story["point"]),
            **({"key": " · ".join(f'<span class="hl hl-{c}">{html.escape(t)}</span>' for t, c in story["key"])}
               if story.get("key") else {}),
        })
    path = os.path.join(ROOT, "public", "data", "ninemiraclestories_gospels.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"stories": out}, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"wrote {len(out)} stor{'y' if len(out) == 1 else 'ies'} to {os.path.relpath(path, ROOT)}")


if __name__ == "__main__":
    main()
