"""Generates the static site (index.html, en/, sv/) from content.json.

Run:  python3 build.py
"""

import html
import json
from pathlib import Path

ROOT = Path(__file__).parent
CURRENT = ' aria-current="true"'
LANGS = {"es": "", "en": "en/", "sv": "sv/"}  # language -> output folder

ICONS = {
    "laptop": '<path d="M4 6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v9H4z"/><path d="M2 18h20"/>',
    "fiber": '<circle cx="12" cy="12" r="3"/><path d="M12 2v4M12 18v4M2 12h4M18 12h4M4.9 4.9l2.8 2.8M16.3 16.3l2.8 2.8M4.9 19.1l2.8-2.8M16.3 7.7l2.8-2.8"/>',
    "phone": '<rect x="6" y="2" width="12" height="20" rx="2"/><path d="M11 18h2"/>',
    "megaphone": '<path d="M3 11v2a1 1 0 0 0 1 1h3l6 4V6L7 10H4a1 1 0 0 0-1 1z"/><path d="M17 9a4 4 0 0 1 0 6"/><path d="M20 6a8 8 0 0 1 0 12"/>',
}

HERO_ART = """<svg viewBox="0 0 480 360" role="img" aria-hidden="true" class="hero-art">
  <rect x="8" y="8" width="464" height="344" rx="28" fill="var(--panel)"/>
  <g stroke="var(--accent)" stroke-width="3" fill="none" opacity=".9">
    <path d="M240 180 L110 90 M240 180 L370 90 M240 180 L110 270 M240 180 L370 270 M240 180 L240 60 M240 180 L240 300"/>
    <path d="M110 90 L240 60 L370 90 M110 270 L240 300 L370 270" stroke-dasharray="6 8" opacity=".6"/>
  </g>
  <g fill="var(--bg)" stroke="var(--accent)" stroke-width="4">
    <circle cx="110" cy="90" r="18"/><circle cx="370" cy="90" r="18"/>
    <circle cx="110" cy="270" r="18"/><circle cx="370" cy="270" r="18"/>
    <circle cx="240" cy="60" r="14"/><circle cx="240" cy="300" r="14"/>
  </g>
  <rect x="196" y="140" width="88" height="80" rx="14" fill="var(--accent)"/>
  <g stroke="var(--bg)" stroke-width="5" stroke-linecap="round">
    <path d="M214 162h52M214 180h52M214 198h52"/>
  </g>
</svg>"""


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def icon(name: str) -> str:
    return (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
        f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'
    )


def page(lang: str, t: dict, all_langs: dict) -> str:
    prefix = "../" if LANGS[lang] else ""
    switcher = "".join(
        f'<a href="{prefix}{LANGS[code]}" hreflang="{code}" lang="{code}"'
        f'{CURRENT if code == lang else ""}>{code.upper()}</a>'
        for code in LANGS
    )
    alternates = "".join(
        f'<link rel="alternate" hreflang="{code}" href="https://lerouxconsultancy.com/{LANGS[code]}">'
        for code in LANGS
    )
    services = "".join(
        f'<article class="card"><div class="card-icon">{icon(s["icon"])}</div>'
        f'<h3>{esc(s["title"])}</h3><p>{esc(s["text"])}</p></article>'
        for s in t["services"]["items"]
    )
    features = "".join(
        f'<div class="feature"><h3>{esc(f["title"])}</h3><p>{esc(f["text"])}</p></div>'
        for f in t["about"]["features"]
    )
    team = "".join(
        '<article class="member">'
        + (
            f'<img class="avatar" src="{prefix}{esc(m["photo"])}" alt="{esc(m["name"])}" width="120" height="120">'
            if m.get("photo")
            else f'<div class="avatar avatar-initials" aria-hidden="true">{esc("".join(w[0] for w in m["name"].split()[:2]))}</div>'
        )
        + f'<h3>{esc(m["name"])}</h3><p class="role">{esc(m["role"])}</p><p>{esc(m["text"])}</p></article>'
        for m in t["team"]["members"]
    )
    faq = "".join(
        f'<details class="faq-item"><summary>{esc(q["q"])}</summary><p>{esc(q["a"])}</p></details>'
        for q in t["faq"]["items"]
    )
    contact_items = "".join(
        f'<li><span>{esc(c["label"])}</span>{c["value_html"]}</li>' for c in t["contact"]["items"]
    )
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(t["meta"]["title"])}</title>
<meta name="description" content="{esc(t["meta"]["description"])}">
{alternates}
<link rel="icon" href="{prefix}assets/logo.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Roboto+Condensed:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}assets/styles.css">
</head>
<body>
<header class="site-header">
  <div class="wrap header-row">
    <a class="brand" href="{prefix}{LANGS[lang]}"><img src="{prefix}assets/logo.svg" alt="" width="34" height="34"><span>Leroux <b>Consultancy</b></span></a>
    <nav class="nav" aria-label="{esc(t["nav"]["label"])}">
      <a href="#servicios">{esc(t["nav"]["services"])}</a>
      <a href="#nosotros">{esc(t["nav"]["about"])}</a>
      <a href="#equipo">{esc(t["nav"]["team"])}</a>
      <a href="#contacto">{esc(t["nav"]["contact"])}</a>
    </nav>
    <div class="lang" aria-label="Language">{switcher}</div>
  </div>
</header>

<main>
  <section class="hero">
    <div class="wrap hero-grid">
      <div>
        <p class="eyebrow">{esc(t["hero"]["eyebrow"])}</p>
        <h1>{esc(t["hero"]["title"])}</h1>
        <p class="lead">{esc(t["hero"]["lead"])}</p>
        <div class="actions">
          <a class="btn btn-primary" href="#contacto">{esc(t["hero"]["cta"])}</a>
          <a class="btn btn-ghost" href="#servicios">{esc(t["hero"]["secondary"])}</a>
        </div>
      </div>
      {HERO_ART}
    </div>
  </section>

  <section id="servicios" class="section">
    <div class="wrap">
      <p class="eyebrow">{esc(t["services"]["eyebrow"])}</p>
      <h2>{esc(t["services"]["title"])}</h2>
      <p class="section-lead">{esc(t["services"]["lead"])}</p>
      <div class="cards">{services}</div>
    </div>
  </section>

  <section id="nosotros" class="section section-alt">
    <div class="wrap about-grid">
      <div>
        <p class="eyebrow">{esc(t["about"]["eyebrow"])}</p>
        <h2>{esc(t["about"]["title"])}</h2>
        <p class="section-lead">{esc(t["about"]["lead"])}</p>
      </div>
      <div class="features">{features}</div>
    </div>
  </section>

  <section id="equipo" class="section">
    <div class="wrap">
      <p class="eyebrow">{esc(t["team"]["eyebrow"])}</p>
      <h2>{esc(t["team"]["title"])}</h2>
      <p class="section-lead">{esc(t["team"]["lead"])}</p>
      <div class="team">{team}</div>
    </div>
  </section>

  <section id="faq" class="section section-dark">
    <div class="wrap">
      <p class="eyebrow">{esc(t["faq"]["eyebrow"])}</p>
      <h2>{esc(t["faq"]["title"])}</h2>
      <div class="faq">{faq}</div>
    </div>
  </section>

  <section id="contacto" class="section">
    <div class="wrap contact">
      <div>
        <p class="eyebrow">{esc(t["contact"]["eyebrow"])}</p>
        <h2>{esc(t["contact"]["title"])}</h2>
        <p class="section-lead">{esc(t["contact"]["lead"])}</p>
      </div>
      <ul class="contact-list">{contact_items}</ul>
    </div>
  </section>
</main>

<footer class="site-footer">
  <div class="wrap footer-row">
    <span>© <span id="year">2026</span> Leroux Consultancy</span>
    <div class="lang">{switcher}</div>
  </div>
</footer>
<script>document.getElementById("year").textContent = new Date().getFullYear();</script>
</body>
</html>
"""


def main() -> None:
    content = json.loads((ROOT / "content.json").read_text(encoding="utf-8"))
    for lang, folder in LANGS.items():
        out = ROOT / folder / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page(lang, content[lang], content), encoding="utf-8")
        print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
