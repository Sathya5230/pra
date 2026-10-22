"""Shared layout and section components for the static build."""
import re
from html import escape as esc
from pathlib import Path

from PIL import Image

SITE = Path(__file__).resolve().parent.parent
BRAND = "Praline"
FONTS = "https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;700&family=Big+Shoulders+Display:wght@600;800;900&family=Caveat+Brush&family=Gilda+Display&display=swap"

# Current page path. Set by build.py before each page renders.
CTX = {"depth": 0, "path": "/"}


def u(path: str) -> str:
    """Root-absolute clean URL. Pages keep their Shopify sitemap path ("/collections/all#x");
    assets become "/assets/...". The host (or serve.py) maps "/x" to "x.html"."""
    if path.startswith(("http", "mailto:", "tel:", "#", "/")):
        return path
    return "/" + path


_dims = {}


def img(key_or_path: str, alt: str, cls: str = "", eager: bool = False, sizes: str = "") -> str:
    """<img> for an editorial key ("hero") or an asset path, with real width/height."""
    path = key_or_path if key_or_path.startswith("assets/") else f"assets/img/{key_or_path}.jpg"
    if path not in _dims:
        with Image.open(SITE / path) as im:
            _dims[path] = im.size
    w, h = _dims[path]
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img src="{u(path)}" alt="{esc(alt)}" width="{w}" height="{h}" {load} decoding="async"{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}{f" sizes={chr(34)}{sizes}{chr(34)}" if sizes else ""}>'


# ---------- Icons & ornaments ----------
ICON = {
    "bag": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M5 8h14l-1.2 12H6.2L5 8Z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>',
    "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="m16 16 4.5 4.5"/></svg>',
    "user": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="8.5" r="3.5"/><path d="M5 20c1.2-3.6 4-5 7-5s5.8 1.4 7 5"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    "close": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18"/></svg>',
    "left": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m14.5 6-6 6 6 6"/></svg>',
    "right": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m9.5 6 6 6-6 6"/></svg>',
    "truck": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M3 6h11v10H3zM14 10h4l3 3v3h-7"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/></svg>',
    "snow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12 3v18M4.2 7.5l15.6 9M4.2 16.5l15.6-9M9.5 4.5 12 7l2.5-2.5M9.5 19.5 12 17l2.5 2.5"/></svg>',
    "gift": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M4 10h16v10H4zM3 7h18v3H3zM12 7v13"/><path d="M12 7c-1.5-3-5-3.5-5-1.2S10 7 12 7Zm0 0c1.5-3 5-3.5 5-1.2S14 7 12 7Z"/></svg>',
    "calendar": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="4" y="5" width="16" height="15" rx="2"/><path d="M4 10h16M9 3v4M15 3v4"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12 3 5 6v5c0 4.5 3 8 7 10 4-2 7-5.5 7-10V6l-7-3Z"/><path d="m9 12 2 2 4-4"/></svg>',
    "leaf": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 19C5 10 10 5 20 4c0 10-5 15-14 15"/><path d="M5 19 13 11"/></svg>',
    "hand": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M7 12V6.5a1.5 1.5 0 0 1 3 0V11M10 10V5a1.5 1.5 0 0 1 3 0v5M13 10V6a1.5 1.5 0 0 1 3 0v6"/><path d="M16 9.5a1.5 1.5 0 0 1 3 0V14a7 7 0 0 1-7 7h-.5A6.5 6.5 0 0 1 6 18l-2.3-4a1.5 1.5 0 0 1 2.6-1.5L7 14"/></svg>',
    "box": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M3 8l9-4 9 4-9 4-9-4Z"/><path d="M3 8v8l9 4 9-4V8M12 12v8"/></svg>',
    "upload": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12 16V4M7 9l5-5 5 5M4 16v4h16v-4"/></svg>',
    "thermo": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M10 14V5a2 2 0 0 1 4 0v9a4 4 0 1 1-4 0Z"/><path d="M12 9v7"/></svg>',
    "info": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8v.5"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "insta": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r=".8" fill="currentColor"/></svg>',
    "pinterest": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M10.5 20l1.7-7.3M12.2 12.7c.3 1.4 1.3 2 2.4 2 2 0 3.2-2 3.2-4.4C17.8 7.6 15.6 6 12.8 6 9.6 6 7.5 8.2 7.5 10.8c0 1 .4 2 1.1 2.4"/></svg>',
}


def icon(name, cls="ico"):
    return ICON[name].replace("<svg ", f'<svg class="{cls}" ', 1)


# Hand-drawn ornaments in the spirit of the reference site’s leaves and cocoa dots.
DOODLE = {
    "bean": '<svg viewBox="0 0 60 40"><ellipse cx="30" cy="20" rx="26" ry="16" fill="currentColor"/><path d="M8 20c10-8 34-8 44 0" stroke="var(--cream)" stroke-width="2.5" fill="none" stroke-linecap="round" opacity=".55"/></svg>',
    "hazelnut": '<svg viewBox="0 0 48 52"><path d="M24 50C10 50 4 38 6 28 8 18 16 12 24 12s16 6 18 16c2 10-4 22-18 22Z" fill="currentColor"/><path d="M10 16c2-8 8-12 14-12s12 4 14 12c-8-3-20-3-28 0Z" fill="currentColor" opacity=".65"/><path d="M16 30c2 6 6 10 8 12" stroke="var(--cream)" stroke-width="2" fill="none" opacity=".5" stroke-linecap="round"/></svg>',
    "leaf": '<svg viewBox="0 0 70 40"><path d="M4 36C14 10 42 2 66 6 58 28 32 40 4 36Z" fill="currentColor"/><path d="M6 35C24 26 40 16 62 8" stroke="var(--cream)" stroke-width="2" fill="none" opacity=".55" stroke-linecap="round"/></svg>',
    "sparkle": '<svg viewBox="0 0 40 40"><path d="M20 2c2 10 8 16 18 18-10 2-16 8-18 18-2-10-8-16-18-18C12 18 18 12 20 2Z" fill="currentColor"/></svg>',
    "swirl": '<svg viewBox="0 0 80 40"><path d="M4 30c10-22 30-22 30-8s-16 10-12 0 26-18 40-6 12 14 14 6" stroke="currentColor" stroke-width="4" fill="none" stroke-linecap="round"/></svg>',
    "dots": '<svg viewBox="0 0 60 60"><g fill="currentColor"><circle cx="8" cy="8" r="4"/><circle cx="30" cy="8" r="4"/><circle cx="52" cy="8" r="4"/><circle cx="8" cy="30" r="4"/><circle cx="30" cy="30" r="4"/><circle cx="52" cy="30" r="4"/><circle cx="8" cy="52" r="4"/><circle cx="30" cy="52" r="4"/><circle cx="52" cy="52" r="4"/></g></svg>',
}


def doodle(kind, style, color="var(--milk)", cls=""):
    """An absolutely positioned decorative ornament. style: inline CSS for position/size."""
    return f'<span class="doodle {cls}" aria-hidden="true" style="color:{color};{style}">{DOODLE[kind]}</span>'


_stamps = [0]


def stamp(text="PRALINE · FAIT MAIN À BRUXELLES · ", style="", inner="bean", cls=""):
    """Circular rotating text badge."""
    _stamps[0] += 1
    sid = f"sp-{_stamps[0]}"
    return f'''<span class="stamp {cls}" aria-hidden="true" style="{style}">
      <svg viewBox="0 0 120 120"><defs><path id="{sid}" d="M60 60m-46 0a46 46 0 1 1 92 0a46 46 0 1 1-92 0"/></defs>
      <text><textPath href="#{sid}" textLength="286">{esc(text)}</textPath></text></svg>
      <i>{DOODLE[inner]}</i></span>'''


def wave(fill, bg, flip=False):
    d = "M0 30c120-30 240-30 360 0s240 30 360 0 240-30 360 0 240 30 360 0v30H0Z" if not flip else "M0 30c120 30 240 30 360 0s240-30 360 0 240 30 360 0 240-30 360 0V0H0Z"
    return f'<svg class="wave" viewBox="0 0 1440 60" preserveAspectRatio="none" aria-hidden="true" style="color:{fill};background:{bg}"><path fill="currentColor" d="{d}"/></svg>'


def drip(fill="var(--cocoa)", bg="var(--cream)"):
    return f'''<svg class="drip" viewBox="0 0 1440 44" preserveAspectRatio="none" aria-hidden="true" style="color:{fill};background:{bg}"><path fill="currentColor" d="M0 0h1440v8c-20 0-24 6-28 14s-10 14-16 0-8-14-30-14h-80c-16 0-18 4-20 18s-4 18-10 18-8-6-9-18-4-18-22-18H980c-14 0-18 6-20 12s-6 8-10 0-6-12-24-12H760c-18 0-20 8-22 22s-5 20-11 20-9-6-10-20-5-22-24-22H520c-14 0-18 4-20 10s-6 8-10 0-8-10-22-10H300c-16 0-20 6-22 16s-6 14-11 14-8-4-9-14-6-16-22-16H90c-14 0-18 6-20 12s-6 6-10 0-8-12-24-12H0Z"/></svg>'''


def marquee(words, cls=""):
    items = "".join(f"<span>{esc(w)}</span>" for w in words)
    return f'<div class="marquee {cls}" aria-hidden="true"><div class="marquee-track">{items}{items}</div></div>'


# ---------- Navigation: workbook Navigation sheet, in sheet order ----------
# Items come from the sheet (build.py calls set_nav); only the top-level link and
# the mega-menu feature tile live here.
NAV_META = {
    "Shop": ("/collections/all", ("premium-box", "Prestige collection", "/products/prestige-48")),
    "Gifts": ("/collections/gift-boxes", ("gift-ribbon", "Every order includes a free gift card", "/collections/gift-boxes")),
    "Corporate Gifts": ("/pages/corporate-gifting", ("logo-box", "Your logo, in cocoa butter", "/pages/pralines-with-logo")),
    "Vegan & Conscious": ("/collections/vegan-chocolates", ("raspberry", "Vegan pralines, no second best", "/collections/vegan-chocolates")),
    "Our Chocolate": ("/pages/belgian-pralines", ("pour", "How a praline is made", "/pages/belgian-pralines")),
    "Delivery": ("/pages/shipping-and-delivery", ("delivery-hands", "Packed to travel cool", "/pages/warm-weather-shipping")),
    "About": ("/pages/about", ("grand-place", "Made in Brussels", "/pages/about")),
}
# Navigation sheet "Build note" values that change how a link looks.
NAV_NOTE_CLASS = {"Use disruptor accent": "nav-accent", "Visible CTA": "nav-cta", "Top-priority path": "nav-priority"}
NAV = []  # [(top label, href, [(item label, url, css class)], feature)]


def set_nav(rows):
    """rows: Navigation sheet dicts. Top-level order is first appearance (the brief's order);
    items keep sheet order. Rows without a URL yet (TBD) stay out until decided."""
    groups = {}
    for r in rows:
        url = r["URL"].strip()
        if not url.startswith("/"):
            continue
        label = re.sub(r".*\(label: (.+)\)", r"\1", r["Dropdown item"]).strip()
        groups.setdefault(r["Top nav (brief)"], []).append((label, url, NAV_NOTE_CLASS.get(r["Build note"], "")))
    NAV[:] = [(top, NAV_META[top][0], items, NAV_META[top][1]) for top, items in groups.items()]


MARK = "assets/img/brand/mark.png"  # crowned cacao pod, stamped on every praline


def logo(tag="a", mark=True):
    m = f'<img class="logo-mark" src="{u(MARK)}" alt="" width="173" height="320">' if mark else ""
    return f'<a class="logo" href="{u("/")}" aria-label="{BRAND} home">{m}<span class="logo-word"><b>{BRAND}</b><i>chocolatier à Bruxelles</i></span></a>'


def crest():
    return f'<div class="crest" role="img" aria-label="Established 1977"><span>Est.</span><img src="{u(MARK)}" alt="" width="173" height="320"><span>1977</span></div>'


def head(title, desc, canonical, noindex=False, extra=""):
    full = title if title.endswith(BRAND) else f"{title} | {BRAND}"
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(full)}</title>
  <meta name="description" content="{esc(desc)}">
  <link rel="canonical" href="https://www.example.com{canonical}">
  {'<meta name="robots" content="noindex, follow">' if noindex else ''}
  <meta property="og:title" content="{esc(full)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta name="theme-color" content="#3D2617">
  <link rel="icon" type="image/png" href="{u('assets/img/brand/favicon.png')}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="{FONTS}">
  <link rel="stylesheet" href="{u('assets/css/styles.css')}">
  {extra}
</head>'''


def header(active=""):
    def link(n, h, cls):
        return f'<li><a href="{u(h)}"{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}>{esc(n)}</a></li>'
    items = []
    for label, href, links, feat in NAV:
        ncols = -(-len(links) // 5)
        per = -(-len(links) // ncols)
        cols = "".join(f'<div><ul>{"".join(link(*x) for x in links[c:c + per])}</ul></div>' for c in range(0, len(links), per))
        fk, ft, fh = feat
        feature = f'<a class="mega-feature" href="{u(fh)}">{img(fk, "")}<span>{esc(ft)}</span></a>'
        cur = ' aria-current="true"' if label == active else ""
        items.append(f'''<li class="nav-item">
          <a class="nav-link" href="{u(href)}" aria-haspopup="true" aria-expanded="false"{cur}>{esc(label)}</a>
          <div class="mega" style="--cols:{ncols}">{cols}{feature}</div></li>''')
    mobile = "".join(f"<details><summary>{esc(label)}</summary><ul>" + "".join(link(*x) for x in links) + "</ul></details>"
                     for label, _, links, _ in NAV)
    popular = "".join(f'<a class="chip" href="{u("/search")}?q={t.replace(" ", "+")}">{t}</a>' for t in ["gift box", "ballotin", "vegan", "caramel", "tablet", "logo"])
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="announce"><div class="wrap">
  <span>{icon("truck", "ico-s")} Free delivery in Belgium from €60</span>
  <span>{icon("gift", "ico-s")} Free printed gift card on every order</span>
  <span>{icon("box", "ico-s")} Corporate orders? <a href="{u("/pages/request-a-quote")}">Request a quote</a></span>
</div></div>
<header class="site-header"><div class="wrap header-row">
  <button class="icon-btn menu-toggle" data-open="menu" aria-label="Open menu">{ICON["menu"]}</button>
  {logo()}
  <nav class="nav" aria-label="Main"><ul>{"".join(items)}</ul></nav>
  <div class="tools">
    <button class="icon-btn" data-open="search" aria-label="Search">{ICON["search"]}</button>
    <a class="icon-btn hide-s" href="{u("/pages/contact")}" aria-label="Contact">{ICON["user"]}</a>
    <button class="icon-btn" data-open="cart" aria-label="Open cart">{ICON["bag"]}<span class="cart-count" aria-live="polite"></span></button>
  </div>
</div></header>
<div class="scrim" data-close></div>
<aside class="drawer drawer--left" id="menu" aria-label="Menu" aria-hidden="true">
  <div class="drawer-head">{logo()}<button class="icon-btn" data-close aria-label="Close menu">{ICON["close"]}</button></div>
  <div class="drawer-body mobile-nav">{mobile}</div>
  <div class="drawer-foot"><a class="btn btn-full btn-block" href="{u("/pages/request-a-quote")}">Request a corporate quote</a></div>
</aside>
<aside class="drawer drawer--right" id="search" aria-label="Search" aria-hidden="true">
  <div class="drawer-head"><h2>Search</h2><button class="icon-btn" data-close aria-label="Close search">{ICON["close"]}</button></div>
  <div class="drawer-body">
    <form action="{u("/search")}" role="search">
      <label class="sr-only" for="q">Search the shop</label>
      <input class="input" id="q" name="q" type="search" placeholder="Try “hazelnut”, “vegan” or “24 pcs”" autocomplete="off">
    </form>
    <p class="script" style="margin-top:1.5rem">Popular right now</p>
    <div class="chips chips--wrap">{popular}</div>
    <div id="search-live"></div>
  </div>
</aside>
<aside class="drawer drawer--right" id="cart" aria-label="Cart" aria-hidden="true">
  <div class="drawer-head"><h2>Your box</h2><button class="icon-btn" data-close aria-label="Close cart">{ICON["close"]}</button></div>
  <div class="drawer-body" id="cart-body"></div>
  <div class="drawer-foot" id="cart-foot"></div>
</aside>
<div class="toast" role="status" aria-live="polite"><span></span><button data-open="cart">View cart</button></div>'''


def footer(bg_above="var(--cream)"):
    # Link groups are <details> so they collapse into tap-to-open sections on phones (see app.js).
    col = lambda title, links: f'<details class="foot-col" open><summary><h4>{title}</h4></summary><ul>{"".join(f"<li><a href={chr(34)}{u(h)}{chr(34)}>{n}</a></li>" for n, h in links)}</ul></details>'
    return f'''{wave("var(--bitter)", bg_above)}
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-top">
      <div class="foot-brand">
        {crest()}
        {logo(mark=False)}
        <p>Belgian pralines made in small batches in Brussels and packed to travel cool. Questions about an order? <a href="mailto:hello@example.com">hello@example.com</a></p>
        <div class="socials"><a class="icon-btn" href="#" aria-label="Instagram">{ICON["insta"]}</a><a class="icon-btn" href="#" aria-label="Pinterest">{ICON["pinterest"]}</a></div>
      </div>
      <form class="foot-news" data-success="You’re on the list. The first letter arrives next month." data-event="newsletter_signup" novalidate>
        <p class="script">Lettre de l’atelier</p>
        <p>New flavours first, and a reminder before the big gifting dates.</p>
        <div class="field"><label class="sr-only" for="foot-email">Email address</label>
          <div class="inline-form"><input class="input" id="foot-email" type="email" required placeholder="you@example.com" autocomplete="email"><button class="btn btn-light btn-full" type="submit">Subscribe</button></div>
          <span class="err">Enter an email address like name@example.com.</span></div>
      </form>
    </div>
    <div class="foot-grid">
      {col("Shop", [("All chocolates", "/collections/all"), ("Pralines & truffles", "/collections/pralines-and-truffles"), ("Ballotins", "/collections/ballotins"), ("Chocolate tablets", "/collections/chocolate-tablets"), ("Build a ballotin", "/pages/build-a-ballotin")])}
      {col("Gifts", [("Gift boxes", "/collections/gift-boxes"), ("Small attentions", "/collections/small-gifts"), ("Premium gifts", "/collections/premium-gifts"), ("Seasonal drops", "/collections/seasonal-drops"), ("Vegan chocolates", "/collections/vegan-chocolates")])}
      {col("Corporate", [("Corporate gifting", "/pages/corporate-gifting"), ("Pralines with logo", "/pages/pralines-with-logo"), ("Request a quote", "/pages/request-a-quote"), ("Upload your logo", "/pages/upload-your-logo")])}
      {col("Help", [("Shipping & delivery", "/pages/shipping-and-delivery"), ("Warm-weather shipping", "/pages/warm-weather-shipping"), ("Returns & quality guarantee", "/pages/returns-and-quality-guarantee"), ("Allergens", "/pages/allergens"), ("FAQ", "/pages/faq")])}
      {col("About", [("Our story", "/pages/about"), ("Belgian pralines", "/pages/belgian-pralines"), ("Sustainability", "/pages/sustainability"), ("Stories", "/blogs/stories"), ("Contact", "/pages/contact")])}
    </div>
  </div>
  <div class="foot-word" aria-hidden="true">{BRAND}</div>
  <div class="foot-base-wrap"><div class="wrap foot-base">
    <span>© 2026 {BRAND} · <a href="{u("/policies/privacy-policy")}">Privacy policy</a> · <a href="{u("/policies/terms-of-service")}">Terms of service</a> · <a href="{u("/policies/refund-policy")}">Refund policy</a></span>
    <span class="pay" aria-label="Payment methods">{"".join(f"<i>{m}</i>" for m in ["Bancontact", "Visa", "Mastercard", "PayPal", "Apple Pay"])}</span>
    <label><span class="sr-only">Country and language</span>
      <select aria-label="Country and language"><option>Belgium · English · EUR</option><option>Belgique · Français · EUR</option><option>België · Nederlands · EUR</option><option>Nederland · Nederlands · EUR</option></select>
    </label>
  </div></div>
</footer>'''


def scripts():
    return f'''<script src="{u("assets/js/data.js")}"></script>
<script src="{u("assets/js/art.js")}"></script>
<script src="{u("assets/js/app.js")}"></script>'''


def crumbs(items):
    """items: list of (label, path or None). The build reuses them for BreadcrumbList JSON-LD."""
    CTX["crumbs"] = items
    parts = [f'<a href="{u("/")}">Home</a>']
    for label, path in items:
        parts.append('<span aria-hidden="true">/</span>')
        parts.append(f'<a href="{u(path)}">{esc(label)}</a>' if path else f'<span aria-current="page">{esc(label)}</span>')
    return f'<nav class="crumbs" aria-label="Breadcrumb">{"".join(parts)}</nav>'


def btn(label, path, kind="btn-full btn-lg", attrs=""):
    return f'<a class="btn {kind}" href="{u(path)}" {attrs}>{esc(label)}</a>'


def ticks(items):
    return '<ul class="ticks">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def tiles(items, cls=""):
    """items: (icon or None, title, text_html)"""
    return f'<div class="tiles {cls}">' + "".join(
        f'<div class="tile">{icon(i) if i else ""}<h3 class="h3">{esc(t)}</h3><p>{x}</p></div>' for i, t, x in items) + "</div>"


def steps(items):
    return '<ol class="steps">' + "".join(f"<li><h3>{esc(t)}</h3><p>{x}</p></li>" for t, x in items) + "</ol>"


def faq(items, open_first=False):
    return '<div class="faq">' + "".join(
        f'<details{" open" if open_first and i == 0 else ""}><summary>{esc(q)}</summary><div>{a}</div></details>' for i, (q, a) in enumerate(items)) + "</div>"


def head_row(script, title, side=""):
    return f'<div class="section-head"><div><p class="script">{esc(script)}</p><h2 class="h2">{esc(title)}</h2></div>{side}</div>'


def rail(source, rid, limit=8, title=None, script=None, link=None, exclude=""):
    side = '<div class="rail-controls">'
    if link:
        side += f'<a class="btn" href="{u(link[1])}">{esc(link[0])}</a>'
    side += f'<button class="icon-btn" data-rail="{rid}" data-dir="prev" aria-label="Previous products">{ICON["left"]}</button><button class="icon-btn" data-rail="{rid}" data-dir="next" aria-label="Next products">{ICON["right"]}</button></div>'
    top = head_row(script, title, side) if title else ""
    return f'{top}<div class="rail" id="{rid}" data-products="{source}" data-limit="{limit}" data-exclude="{exclude}"></div>'


def figure(key, alt, frame="arch", caption="", extra=""):
    cap = f'<figcaption>{esc(caption)}</figcaption>' if caption else ""
    return f'<figure class="ph ph--{frame}">{img(key, alt)}{cap}{extra}</figure>'


def split(key, alt, inner, flip=False, frame="arch", caption="", extra=""):
    return f'<div class="wrap split{" split--flip" if flip else ""}"><div class="split-media">{figure(key, alt, frame, caption, extra)}</div><div class="split-copy">{inner}</div></div>'


def page_hero(crumb_items, script, title, lead, ctas="", image=None, alt="", tone="butter", extra_art="", stamp_text=None):
    art = ""
    if image:
        st = stamp(stamp_text, "right:-18px;top:-18px") if stamp_text else ""
        art = f'<div class="page-hero-art">{figure(image, alt, "arch", extra=st)}{extra_art}</div>'
    return f'''<section class="page-hero page-hero--{tone}{" on-dark" if tone == "ganache" else ""}">
  {doodle("dots", "left:2%;bottom:18%;width:54px", "var(--latte)" if tone != "ganache" else "rgba(231,207,174,.25)")}
  <div class="wrap page-hero-grid{" no-art" if not image else ""}">
    <div class="page-hero-copy">{crumbs(crumb_items)}<p class="script">{esc(script)}</p><h1 class="h1">{esc(title)}</h1><p class="lead">{lead}</p>{f'<div class="hero-actions">{ctas}</div>' if ctas else ""}</div>
    {art}
  </div>
</section>'''


QUOTE_FIELDS = [
    ("Your name", "q-name", "text", True, "name", "Enter your name."),
    ("Work email", "q-email", "email", True, "email", "Enter an email address like name@company.com."),
    ("Company", "q-company", "text", True, "organization", "Enter your company name."),
    ("Phone (optional)", "q-phone", "tel", False, "tel", ""),
]


def quote_form(heading="Get a quote and a sample pack", use_case="", logo=True):
    """The one quote form used on every corporate page (fields reconcile checklist #22 and the sitemap)."""
    fields = "".join(
        f'<div class="field"><label for="{i}">{l}</label><input class="input" id="{i}" type="{t}"{" required" if r else ""} autocomplete="{a}">{f"<span class={chr(34)}err{chr(34)}>{e}</span>" if e else ""}</div>'
        for l, i, t, r, a, e in QUOTE_FIELDS)
    uses = ["Client Gifts", "Employee Gifts", "Event Gifts", "Trade Fair Gifts", "Campaign Gifts", "Something else"]
    opts = "".join(f'<option{" selected" if x == use_case else ""}>{x}</option>' for x in uses)
    logo_html = f'''<div class="field full">
        <span class="label" id="logo-label">Your logo <span class="muted">(optional)</span></span>
        <label class="dropzone" data-dropzone for="logo-file" aria-labelledby="logo-label">
          <input type="file" id="logo-file" accept=".svg,.ai,.eps,.pdf,.png">
          <span class="dz-ico">{ICON["upload"]}</span>
          <b>Drop a file or browse</b><br><span class="small muted">SVG, AI, EPS, PDF or 300 dpi PNG, up to 10 MB. You approve a proof before we print.</span>
        </label>
        <span class="file-name small" aria-live="polite"></span>
      </div>''' if logo else ""
    return f'''<div class="quote-card" id="quote">
  <form class="quote-form" data-quote-form novalidate>
    <p class="script">Request a quote</p>
    <h2 class="h3" style="margin-bottom:1.25rem">{esc(heading)}</h2>
    <div class="form-grid">
      {fields}
      <div class="field"><label for="q-use">What it’s for</label><select class="input" id="q-use" required><option value="">Choose one</option>{opts}</select><span class="err">Choose what the gifts are for.</span></div>
      <div class="field"><label for="q-qty">How many gifts</label><select class="input" id="q-qty" required><option value="">Choose a range</option><option>25–50</option><option>51–100</option><option>101–250</option><option>250+</option></select><span class="err">Choose how many gifts you need.</span></div>
      <div class="field"><label for="q-budget">Budget per gift</label><select class="input" id="q-budget"><option>Not sure yet</option><option>Under €25</option><option>€25–50</option><option>€50–100</option><option>€100+</option></select></div>
      <div class="field"><label for="q-date">Delivery needed by</label><input class="input" id="q-date" type="date" required><span class="hint">At least three weeks out for logo pralines.</span><span class="err">Choose a delivery date.</span></div>
      <div class="field full"><span class="label">Personalisation</span>
        <div class="check-row">{"".join(f'<label class="check"><input type="checkbox" name="q-pers" value="{x}"> <span>{x}</span></label>' for x in ["Logo Pralines", "Branded Sleeve", "Branded Card", "Branded Ribbon", "Custom Packaging"])}</div></div>
      <div class="field full"><span class="label">Delivery</span>
        <label class="check"><input type="radio" name="q-addr" value="one" checked> <span>One address</span></label>
        <label class="check"><input type="radio" name="q-addr" value="many"> <span>Several addresses (we’ll send you a spreadsheet template) <span class="placeholder-note">Scope pending Open Decision #6</span></span></label>
      </div>
      {logo_html}
      <div class="field full"><label for="q-notes">Anything else</label><textarea class="input" id="q-notes" placeholder="Colours, message on the card, dietary needs (vegan, no alcohol)…"></textarea></div>
      <div class="field full">
        <label class="check"><input type="checkbox" id="q-sample" checked> <span>Send me a sample pack with the quote</span></label>
        <label class="check"><input type="checkbox" id="q-consent" required> <span>I agree that you contact me about this request.</span></label>
        <span class="err">Tick the box so we can reply to you.</span>
      </div>
    </div>
    <button class="btn btn-full btn-lg btn-block" type="submit">Send quote request</button>
    <p class="small muted center" style="margin:.75rem auto 0">No payment, no checkout. We reply within two working days.</p>
  </form>
  <div class="success" tabindex="-1">
    <p class="script">Merci!</p>
    <h2 class="h2">Quote request sent</h2>
    <p>We’ll reply to your work email within two working days. If you asked for a sample pack, it ships with the quote.</p>
    <a class="btn btn-full" href="{u("/collections/corporate-gifts")}">Browse corporate boxes</a>
  </div>
</div>'''


def trust_strip(items=None):
    items = items or [("hand", "Finished by hand", "In small batches in Brussels"), ("snow", "Packed to travel cool", "Insulated liner on every order"),
                      ("gift", "Free gift card", "No prices in the box"), ("shield", "Arrives right", "Or we replace it")]
    return '<div class="trust-strip"><div class="wrap">' + "".join(
        f'<div>{icon(i)}<span><b>{t}</b><small>{s}</small></span></div>' for i, t, s in items) + "</div></div>"


def newsletter_band(image="gift-small"):
    return f'''<section class="section section--butter grain">
  {doodle("leaf", "right:6%;top:12%;width:70px;transform:rotate(-18deg)")}
  <div class="wrap newsletter">
    <figure class="ph ph--circle">{img(image, "A small gift box tied with ribbon")}</figure>
    <div>
      <p class="script">Lettre de l’atelier</p>
      <h2 class="h2">New flavours, first</h2>
      <p>One letter a month: seasonal boxes before they sell out, and a reminder before the big gifting dates.</p>
      <form data-success="You’re on the list. The first letter arrives next month." data-event="newsletter_signup" novalidate>
        <div class="field"><label class="sr-only" for="nl-email">Email address</label>
          <div class="inline-form"><input class="input" id="nl-email" type="email" required placeholder="you@example.com" autocomplete="email"><button class="btn btn-full" type="submit">Subscribe</button></div>
          <span class="err">Enter an email address like name@example.com.</span></div>
      </form>
    </div>
  </div>
</section>'''
