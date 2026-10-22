"""Save local copies of the BibleProject Classroom literary-design units.

Reads every URL in public/scripts/*text_visuals.json, pulls the visual data
(reference, title, caption, and the text as USX, or as
HTML for older units such as Ephesians) out of each page's window.__remixContext,
and writes it to public/visuals/<id>.json so the site no longer depends on
d3kfvpfexuy5fk.cloudfront.net.

Usage: python3 tools/fetch_visuals.py [--force]
"""
import glob
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "public", "visuals")
ROUTE = "routes/visuals/literary-design-units/$id/index"


def extract(html):
    m = re.search(r"window\.__remixContext = (\{.*?\});</script>", html, re.S)
    if not m:
        raise ValueError("no __remixContext found")
    data = json.loads(m.group(1))["state"]["loaderData"][ROUTE]["data"]
    v = data["visualData"]
    return {
        "id": data["id"],
        "reference": v["reference"],
        "title": v["title"],
        "caption": v["caption"],
        "updatedAt": v.get("updatedAt"),
        "usx": v.get("usx"),
        "html": v.get("html"),
    }


def main():
    force = "--force" in sys.argv
    os.makedirs(OUT_DIR, exist_ok=True)
    urls = []
    for path in sorted(glob.glob(os.path.join(ROOT, "public", "scripts", "*text_visuals.json"))):
        urls += [entry["url"] for entry in json.load(open(path))]
    for url in urls:
        unit_id = url.strip().rstrip("/").split("/")[-1]
        out = os.path.join(OUT_DIR, unit_id + ".json")
        if os.path.exists(out) and not force:
            print("skip ", unit_id)
            continue
        with urllib.request.urlopen(url.strip(), timeout=30) as resp:
            html = resp.read().decode("utf-8")
        visual = extract(html)
        if not visual["usx"] and not visual["html"]:
            print("NO TEXT", unit_id)
            continue
        with open(out, "w", encoding="utf-8") as f:
            json.dump(visual, f, ensure_ascii=False, indent=2)
        print("saved", unit_id)


if __name__ == "__main__":
    main()
