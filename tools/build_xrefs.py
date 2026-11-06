"""Build public/data/xrefs.json: the cross-references behind the ⓘ icons in our
translation units (<note style="x" xref="ID"> in translation/*/*.usx).

Each cross-reference shows evidence, not opinion: the Matthew verse (our English) and
the passage it links to (Brenton's English of the Septuagint, or Tim's English for
another verse of Matthew), with the matching
words in bold and only those Greek words shown, inline, checked against the
Greek (SBLGNT, Brenton's Septuagint). A short note at the bottom
says what the match shows; an optional "intro" goes above the passages. Texts come from the repo; only what's below is
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
        ],
        # "- " lines become a bulleted list.
        "intro": "The same two words for a man who can't move: paralyzed, and thrown down (the same perfect tense "
                 "of βάλλω):\n"
                 "- has been thrown down (βέβληται): the centurion's boy / servant\n"
                 "- lying (βεβλημένον, lit. thrown down): the paralyzed man on a mat",
        "note": "Matthew is connecting these stories in your mind. Both turn on authority (8:9; 9:6) and "
                "trust (8:10; 9:2), and end with “Go” (8:13; 9:6).",
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
        "intro": "Matthew's stories use this healing word (ἰάομαι) for only two people: a Gentile centurion's "
                 "boy / servant and a Canaanite woman's daughter.",
        "note": "In both cases Jesus heals from a distance, after he praises these Gentiles' trust.",
    },
    {
        "id": "matthew-8-7-question",
        "title": "Question or statement?",
        "matthew": {"ref": "8:7", "unit": "kata-matthew-8-5-13",
                    "match": [("I, coming", "Ἐγὼ ἐλθὼν", None)]},
        "passages": [
            {"ref": "Matthew 3:14", "unit": "matthew-3-13-17",
             "match": [("I need", "Ἐγὼ χρείαν ἔχω", None), ("you would come to me?!", "σὺ ἔρχῃ πρός με;", None)]},
        ],
        "intro": "Fun fact: the oldest Greek manuscripts have almost no punctuation and no question marks; "
                 "scribes and editors added them later. The Greek question mark (;) came into use around the "
                 "8th–9th centuries. It looks like our semicolon: σὺ ἔρχῃ πρός με; is “you would come to me?” So to this day we are not 100% sure whether Jesus asks this "
                 "as a question or says it as a declarative statement. Our English Bibles are split, most print it "
                 "as a statement, but others, like NIV, print it as a question. "
                 "We print it as a ‘declarative question’. For example, “You want me to come to your house?” is a "
                 "declaration but a question, so we call it a declarative question and punctuate with a ? symbol. "
                 "Does it really matter?",
        "note": "The “I” (Ἐγὼ) is emphatic, like John's surprised question when Jesus comes to him.",
    },
    {
        "id": "matthew-5-32-divorce",
        "title": "Divorce: Jesus comes back to it",
        "matthew": {"ref": "5:32", "unit": "adapted-matthew-5-31-32",
                    "match": [("sends away his wife", "ἀπολύων τὴν γυναῖκα αὐτοῦ", None),
                              ("except on the ground of sexual immorality", "παρεκτὸς λόγου πορνείας", None),
                              ("commits adultery", "μοιχᾶται", None)]},
        "intro": "In the Sermon on the Mount Jesus gives a short summary of his teaching on divorce. "
                 "He comes back to it in chapter 19 and says more. The Pharisees point to Moses (Deuteronomy 24:1); "
                 "Jesus goes back to creation: Genesis 1:27 and 2:24 in the Septuagint, the Greek Bible of Matthew's day.",
        # Passages and commentary in reading order: {"comment": "..."} is a commentary block between passages.
        "passages": [
            {"ref": "Matthew 19:3", "bsb": True,
             "match": [("divorce his wife", "ἀπολῦσαι τὴν γυναῖκα αὐτοῦ", "send away his wife")],
             "mark": ["for any reason"]},
            {"comment": "The debate of the day was over Deuteronomy 24:1: a man may divorce his wife if “she does not find "
                        "favor in his eyes, because he has found some indecency in her” (Hebrew ʿervat davar, "
                        "lit. “nakedness of a matter”). The Mishnah (Gittin 9:10, written down around AD 200) "
                        "records the readings:\n"
                        "- School of Shammai: only for “a matter of indecency”, sexual immorality.\n"
                        "- School of Hillel: for any cause at all, “even if she spoiled his dish.”\n"
                        "- Rabbi Akiva (early 2nd century): “even if he found another more beautiful than she”, "
                        "from “she does not find favor in his eyes.”\n"
                        "The Pharisees' “for any reason” is Hillel's side, put to Jesus as a test."},
            # A range of BSB verses: "verses" holds each verse's matches.
            {"ref": "Matthew 19:4–6", "bsb": True, "verses": {
                4: {"match": [("made them male and female", "ἄρσεν καὶ θῆλυ ἐποίησεν αὐτοὺς", None, "blue")],
                    "mark": ["from the beginning"]},
                5: {"match": [("a man will leave his father", "καταλείψει ἄνθρωπος τὸν πατέρα", None),
                              ("be united to his wife", "κολληθήσεται τῇ γυναικὶ αὐτοῦ", "cleave to his wife", "green"),
                              ("the two will become one flesh", "ἔσονται οἱ δύο εἰς σάρκα μίαν", "the two will be into one flesh")]},
                6: {"match": [("what God has joined together", "ὃ οὖν ὁ θεὸς συνέζευξεν", "what God yoked together")],
                    "mark": ["no longer two"]},
            }},
            {"ref": "Genesis 1:27",
             "match": [("male and female he made them", "ἄρσεν καὶ θῆλυ ἐποίησεν αὐτούς", None, "blue")]},
            {"ref": "Genesis 2:24",
             "match": [("shall a man leave his father", "καταλείψει ἄνθρωπος τὸν πατέρα", None),
                       ("shall cleave to his wife", "προσκολληθήσεται πρὸς τὴν γυναῖκα αὐτοῦ", None, "green"),
                       ("they two shall be one flesh", "ἔσονται οἱ δύο εἰς σάρκα μίαν", "the two shall be into one flesh")]},
            {"ref": "Deuteronomy 10:20",
             "match": [("shalt cleave to him", "πρὸς αὐτὸν κολληθήσῃ", None, "green")],
             "mark": ["fear the Lord thy God", "serve him"]},
            {"comment": "“Male and female he made them” is Genesis 1:27 word for word. The Hebrew of Genesis 2:24 says only "
                        "“they shall become one flesh”; “the two” (οἱ δύο) is in the Septuagint, and Jesus builds on it: "
                        "the two become one, so they are “no longer two”. What God yoked together (ὃ, “what”, is the union "
                        "itself) a man has no authority to pull apart.\n"
                        "“Cleave to his wife” (κολλάω, to glue, to cling) is the verb Moses uses for Israel's loyalty to God: "
                        "“to him you shall cleave” (κολληθήσῃ, Deuteronomy 10:20). A husband holds fast to his wife the way "
                        "Israel is to hold fast to the LORD. (Genesis 2:24 and many manuscripts of Matthew have "
                        "προσκολληθήσεται, the same verb with προς, “toward”, in front; the oldest have the plain "
                        "κολληθήσεται, exactly Deuteronomy's word.)"},
            {"ref": "Matthew 19:7–9", "bsb": True, "verses": {
                7: {"match": [("certificate of divorce", "βιβλίον ἀποστασίου", None, "purple")]},
                8: {"mark": ["hardness of heart", "not this way from the beginning"]},
                9: {"match": [("except for sexual immorality", "μὴ ἐπὶ πορνείᾳ", None),
                              ("commits adultery", "μοιχᾶται", None)]},
            }},
            # The Pharisees' text. Brenton's English numbers Deuteronomy 23-24 two verses off from
            # the Greek, so its 24:1 is filed as 24:3: "en_ref" says where to find the English.
            {"ref": "Deuteronomy 24:1", "en_ref": "Deuteronomy 24:3",
             "match": [("a bill of divorcement", "βιβλίον ἀποστασίου", None, "purple")],
             "mark": ["she should not have found favour before him", "some unbecoming thing"]},
            {"comment": "In 5:32 Jesus' “a matter (λόγου) of sexual immorality” sounds like Shammai's wording. But here he "
                        "doesn't argue from Deuteronomy at all: Moses only permitted divorce, “because of your hardness of "
                        "heart”; Jesus goes back to the beginning.\n"
                        "Who was listening: Jewish men, most in their 20s to 40s, in marriages their families had arranged, "
                        "often to a wife about ten years younger who was married in her teens and had little say. Only the "
                        "husband could write a certificate of divorce, and a sent-away wife could be left with nothing.\n"
                        "Into that world Jesus takes away the power these men thought the Law gave them. He shuts the easy "
                        "exits and puts the weight on the man: he makes her a victim of adultery. He is calling them to go the "
                        "extra mile toward unity, not division.\n"
                        "This is wisdom, not a rule to lift out of its setting. It is not telling a woman today that she may "
                        "only consider divorce if there is adultery. Wisdom names the conditions and the response; without "
                        "seeing both you can't apply it to new situations. Paul does exactly that for cases Jesus didn't "
                        "address, in 1 Corinthians 7."},
            {"comment": "Bonus: how the disciples heard it, and Jesus offers another way, staying unmarried, as an ideal "
                        "for those who can accept it."},
            {"ref": "Matthew 19:10–12", "bsb": True, "verses": {
                10: {"mark": ["it is better not to marry"]},
                12: {"mark": ["for the sake of the kingdom of heaven", "The one who can accept this should accept it"]},
            }},
        ],
    },]


TIM = "Tim Mackie’s translation (BibleProject)"


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
            text = re.sub(r"</?char\b[^>]*>", "", text)  # inline marks: no space
            return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text)).replace(" ,", ",").replace(" .", ".").replace("“ ", "“").replace(" ”", "”").replace("‘ ", "‘").replace(" ’", "’").replace(" !", "!").strip()
    raise SystemExit(f"{unit} has no verse {ref}")


def comment(text):
    """Commentary as HTML: plain paragraphs, with "- " lines as a bulleted list."""
    out, items = [], []
    for line in text.split("\n"):
        if line.startswith("- "):
            items.append(f"<li>{html.escape(line[2:])}</li>")
            continue
        if items:
            out.append("<ul>" + "".join(items) + "</ul>")
            items = []
        out.append(f"<p>{html.escape(line)}</p>")
    if items:
        out.append("<ul>" + "".join(items) + "</ul>")
    return "".join(out)


def emphasize(text, greek, match=(), mark=()):
    """HTML-escape the English, bolding each matching phrase with its Greek
    inline after it, and wrapping other phrases worth seeing in <mark>."""
    spans = []
    for en, gk, lit, *color in match:
        if gk not in greek:
            raise SystemExit(f"{gk!r} not found in {greek!r}")
        extra = f" lit. {html.escape(lit)}" if lit else ""
        rendered = f'<strong>{html.escape(en)}</strong> (<strong lang="grc">{html.escape(gk)}</strong>{extra})'
        if color:  # an optional 4th item colors a match repeated across passages ("blue", "green")
            rendered = f'<span class="hl hl-{color[0]}">{rendered}</span>'
        spans.append((en, rendered))
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
            "sources": ("kata Matthew" if m["unit"].startswith("kata-") else TIM) + " · Greek: SBLGNT",
        }]
        for p in x["passages"]:
            if "comment" in p:
                passages.append({"note": comment(p["comment"])})
                continue
            if p.get("bsb") and "–" in p["ref"]:
                c, _, span = p["ref"].removeprefix("Matthew ").partition(":")
                a, b = (int(n) for n in span.split("–"))
                lines = []
                for v in range(a, b + 1):
                    want = p.get("verses", {}).get(v, {})
                    lines.append(f"<sup>{v}</sup> " + emphasize(bsb[int(c)][v], mt_gk[f"{c}:{v}"],
                                                               want.get("match", ()), want.get("mark", ())))
                passages.append({
                    "ref": html.escape(p["ref"]),
                    "en": " ".join(lines),
                    "sources": "Berean Standard Bible (public domain) · Greek: SBLGNT",
                })
                continue
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
                    "sources": TIM + " · Greek: SBLGNT",
                })
                continue
            passages.append({
                "ref": html.escape(p["ref"] + " (LXX, the Greek translation of the Hebrew Bible)"),
                "en": emphasize(lxx_en[p.get("en_ref", p["ref"])], lxx_gk[p["ref"]], p.get("match", ()), p.get("mark", ())),
                "sources": "Brenton’s English (1851) · Greek: Brenton’s Septuagint",
            })
        entry = {"id": x["id"], "title": x["title"]}
        if x.get("intro"):
            entry["intro"] = comment(x["intro"])  # commentary above the passages
        entry["passages"] = passages
        if x.get("note"):
            entry["note"] = comment(x["note"])  # commentary below them
        out.append(entry)
    path = os.path.join(ROOT, "public", "data", "xrefs.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"xrefs": out}, f, ensure_ascii=False, indent=1)
    print(f"wrote {len(out)} cross-reference(s) to public/data/xrefs.json")


if __name__ == "__main__":
    main()
