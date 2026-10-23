// Renders BibleProject literary-design units saved under /visuals/<id>.json
// (see tools/fetch_visuals.py) as plain HTML styled by styles/literary-design.css.
// Mirrors the bp-literary-design web component, so no external site is needed.
const LiteraryDesign = (() => {
  // "5:1" -> 5001; a bare "2" is resolved against the current chapter.
  function verseKey(chapter, verse) {
    return chapter * 1000 + verse;
  }

  function parseRef(ref, chapter) {
    const parts = ref.trim().split(":");
    return parts.length === 2
      ? verseKey(+parts[0], +parts[1])
      : verseKey(chapter, +parts[0]);
  }

  // Leaf groups are the lines of the design.
  function leafGroups(doc) {
    return [...doc.getElementsByTagName("group")].filter(
      (g) => !g.getElementsByTagName("group").length
    );
  }

  // Remove every line that holds no verse in [from, to]. Verse markers that go
  // backwards (e.g. the footnote-style 1..7 inside Matthew 4:23-24) are ignored.
  function sliceToRange(doc, startChapter, from, to) {
    let chapter = startChapter;
    let current = 0;
    for (const line of leafGroups(doc)) {
      const keys = [];
      if (current) keys.push(current);
      for (const v of line.getElementsByTagName("verse")) {
        const n = v.getAttribute("number");
        if (n.includes(":")) chapter = +n.split(":")[0];
        const key = parseRef(n, chapter);
        if (key > current) {
          current = key;
          keys.push(key);
        }
      }
      // A line that opens with a new verse does not belong to the previous one.
      const opensWithVerse = (() => {
        for (const child of line.childNodes) {
          if (child.nodeType === Node.ELEMENT_NODE) return child.tagName === "verse";
          if (child.textContent.trim()) return false;
        }
        return false;
      })();
      const lineKeys = opensWithVerse && keys.length > 1 ? keys.slice(1) : keys;
      if (!lineKeys.some((k) => k >= from && k <= to)) line.remove();
    }
    // Drop containers that are now empty, then stray optbreaks.
    let removed = true;
    while (removed) {
      removed = false;
      for (const el of [...doc.querySelectorAll("group, para")]) {
        if (!el.getElementsByTagName("group").length && !el.textContent.trim()) {
          el.remove();
          removed = true;
        }
      }
    }
    for (const br of [...doc.getElementsByTagName("optbreak")]) {
      const prev = br.previousElementSibling;
      const next = br.nextElementSibling;
      if (!prev || !next || next.tagName === "optbreak") br.remove();
    }
  }

  function convert(node) {
    if (node.nodeType === Node.TEXT_NODE) {
      return document.createTextNode(node.textContent);
    }
    if (node.nodeType !== Node.ELEMENT_NODE) return null;
    const children = () => {
      const frag = document.createDocumentFragment();
      for (const child of node.childNodes) {
        const out = convert(child);
        if (out) frag.appendChild(out);
      }
      return frag;
    };
    const attr = (name) => node.getAttribute(name);
    let el;
    switch (node.tagName) {
      case "usx":
        el = document.createElement("div");
        el.className = "ld-body";
        el.appendChild(children());
        return el;
      case "para":
        el = document.createElement("div");
        el.className = "ld-para";
        el.appendChild(children());
        return el;
      case "group":
        el = document.createElement("div");
        el.className = "ld-group";
        for (const name of ["type", "indent"]) {
          if (attr(name)) el.dataset[name] = attr(name);
        }
        if (attr("title")) {
          const title = document.createElement("div");
          title.className = "ld-group-title";
          title.textContent = attr("title");
          el.appendChild(title);
        }
        if (attr("sidebar-value")) {
          const side = document.createElement("span");
          side.className = "ld-sidebar-value";
          side.textContent = attr("sidebar-value");
          el.appendChild(side);
        }
        el.appendChild(children());
        return el;
      case "verse":
        el = document.createElement("sup");
        el.className = "ld-verse";
        el.textContent = attr("number");
        return el;
      case "optbreak":
        el = document.createElement("div");
        el.className = "ld-optbreak";
        return el;
      case "char": {
        const variant = attr("mark-variant");
        const color = attr("mark-color");
        el = document.createElement(variant || color ? "mark" : "span");
        if (variant || color) {
          el.className = ["ld-mark", color, variant].filter(Boolean).join(" ");
        }
        el.appendChild(children());
        if (attr("word-original")) {
          const word = document.createElement("span");
          word.className = "ld-word-original";
          word.textContent = ` (${attr("word-original")})`;
          el.appendChild(word);
        }
        return el;
      }
      case "note":
        return null;
      default:
        return children();
    }
  }

  // "5:3–5:16" or "5:13" -> [from, to] verse keys. Ranges must give the chapter.
  function rangeKeys(range) {
    const [a, b] = range.split(/[–-]/);
    const from = parseRef(a, 0);
    const to = b ? parseRef(b, Math.floor(from / 1000)) : from;
    return [from, to];
  }

  // visuals: one { reference, title, caption, usx } or a list of consecutive units.
  // range: optional "5:1–5:2" or "5:13"; each unit is cut down to it.
  function render(visuals, range) {
    visuals = [].concat(visuals);
    const root = document.createElement("div");
    root.className = "ld";
    const ref = document.createElement("div");
    ref.className = "ld-reference";
    ref.textContent = range
      ? `${visuals[0].reference.replace(/\s[\d:–-]+$/, "")} ${range}`
      : visuals.map((v) => v.reference).join("; ");
    root.appendChild(ref);
    const credits = new Set();
    for (const visual of visuals) {
      const doc = new DOMParser().parseFromString(visual.usx, "text/xml");
      // Units without verse markers (e.g. Matthew 6:9-13) can't be sliced; show them whole.
      if (range && doc.getElementsByTagName("verse").length) {
        const startChapter = +visual.reference.match(/(\d+):\d+/)[1];
        sliceToRange(doc, startChapter, ...rangeKeys(range));
        if (!doc.getElementsByTagName("group").length) continue;
      }
      root.appendChild(convert(doc.documentElement));
      // Captions read "<bp-cite>Matthew 5:3-12</bp-cite>. Translation and ..."; show each credit once.
      credits.add(
        visual.caption
          .replace(/^<bp-cite>.*?<\/bp-cite>\.?\s*/, "")
          .replace(/<[^>]+>/g, "")
          .replace(/[.\s]+$/, "")
      );
    }
    const caption = document.createElement("div");
    caption.className = "ld-caption";
    caption.textContent = [...credits].map((c) => c + ".").join(" ");
    root.appendChild(caption);
    return root;
  }

  // Loaded units by id, kept for the life of the page.
  const cache = new Map();
  let bundles = Promise.resolve();

  // Start fetching a book's bundle (e.g. "matthew") so later loads are instant.
  function preload(book) {
    bundles = bundles.then(async () => {
      try {
        const response = await fetch(`/visuals/bundle-${book}.json`);
        if (!response.ok) return;
        for (const [id, visual] of Object.entries(await response.json())) {
          if (!cache.has(id)) cache.set(id, Promise.resolve(visual));
        }
      } catch (error) {
        // Fall back to fetching units one at a time.
      }
    });
    return bundles;
  }

  async function load(unitId) {
    await bundles;
    if (!cache.has(unitId)) {
      cache.set(
        unitId,
        fetch(`/visuals/${unitId}.json`).then((response) => {
          if (!response.ok) throw new Error(`Could not load ${unitId}`);
          return response.json();
        })
      );
      cache.get(unitId).catch(() => cache.delete(unitId));
    }
    return cache.get(unitId);
  }

  return { render, load, preload, rangeKeys };
})();
