// The title bar shared by every page. Each page loads this script in its <head>
// and puts <site-header current="..."></site-header> first in its <body>
// ("current" is the link to highlight: "home", "matthew" or "reader").
// Section pages (/otconnections, /sotm, ...) aren't listed here; /matthew links to them.
const SITE_LINKS = [
  { id: "matthew", href: "/matthew", label: "Matthew" },
  { id: "reader", href: "/reader", label: "Reader" },
];

class SiteHeader extends HTMLElement {
  connectedCallback() {
    if (this.shadowRoot) return;
    const current = this.getAttribute("current");
    // Shadow DOM keeps the bar looking the same whatever CSS the page uses (e.g. Bootstrap on the calendar).
    this.attachShadow({ mode: "open" }).innerHTML = `
      <style>
        :host{display:block;--bar-height:48px}
        nav{display:flex;align-items:center;flex-wrap:wrap;gap:4px 20px;min-height:var(--bar-height);box-sizing:border-box;padding:6px 16px;
          background:#657A55;color:#fff;font-family:"Graphik Web",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;line-height:1.2}
        a{color:inherit;text-decoration:none}
        .title{flex:1;font-size:1.15rem;font-weight:600;white-space:nowrap}
        .title i{font-weight:400}
        .links{display:flex;gap:4px}
        .links a{padding:6px 10px;border-radius:6px;font-size:.95rem;opacity:.9}
        .links a:hover{background:rgba(255,255,255,.15);opacity:1}
        .links a[aria-current="page"]{background:rgba(255,255,255,.22);opacity:1;font-weight:600}
        @media (max-width:480px){.title{font-size:1rem}}
      </style>
      <nav>
        <a class="title" href="/"${current === "home" ? ' aria-current="page"' : ""}>The Good News <i>kata</i> Matthew</a>
        <div class="links">${SITE_LINKS.map(
          (link) => `<a href="${link.href}"${link.id === current ? ' aria-current="page"' : ""}>${link.label}</a>`
        ).join("")}</div>
      </nav>`;
  }
}
customElements.define("site-header", SiteHeader);
