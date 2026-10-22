"""Static site build. Reads the Sitemap sheet from the build-pack workbook and
renders every row, plus product pages and Shopify system pages.

    /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 site/_build/build.py

Needs Python 3.12+ (nested f-strings) and Pillow.
"""
import csv
import io
import json
import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import catalogue as cat
import components as C
import pages as P

SITE = C.SITE
WORKBOOK = SITE.parent / "source_files" / "pralines shopify build pack.xlsx"
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}


def read_sheet(name):
    """Minimal .xlsx reader (no openpyxl dependency)."""
    z = zipfile.ZipFile(WORKBOOK)
    strings = [''.join(t.text or '' for t in si.iter(f"{{{NS['m']}}}t"))
               for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS)]
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
    sheet = next(s for s in wb.find("m:sheets", NS) if s.get("name") == name)
    target = rels[sheet.get(f"{{{NS['r']}}}id")].lstrip("/").replace("xl/", "")
    rows = []
    for row in ET.fromstring(z.read("xl/" + target)).iter(f"{{{NS['m']}}}row"):
        vals = {}
        for c in row.findall("m:c", NS):
            col = sum((ord(ch) - 64) * 26 ** i for i, ch in enumerate(reversed(re.match(r"[A-Z]+", c.get("r")).group())))
            v = c.find("m:v", NS)
            vals[col - 1] = strings[int(v.text)] if c.get("t") == "s" and v is not None else (v.text if v is not None else "")
        rows.append([vals.get(i, "") for i in range(max(vals) + 1)] if vals else [])
    header, *body = rows
    return [dict(zip(header, r)) for r in body if any(r)]


# Sitemap path -> (renderer, body data-page). The nav group comes from the sheet.
EDITORIAL = {
    "/pages/corporate-gifting": (P.corporate_gifting, "corporate"),
    "/pages/pralines-with-logo": (P.pralines_with_logo, "corporate"),
    "/pages/client-gifts": (lambda: P.corp_usecase_page("client"), "corporate"),
    "/pages/employee-gifts": (lambda: P.corp_usecase_page("employee"), "corporate"),
    "/pages/request-a-quote": (P.request_a_quote, "quote"),
    "/pages/upload-your-logo": (P.upload_your_logo, "upload"),
    "/pages/belgian-pralines": (P.belgian_pralines, "editorial"),
    "/pages/ingredients": (P.ingredients, "editorial"),
    "/pages/organic-and-fairtrade": (P.organic_and_fairtrade, "editorial"),
    "/pages/allergens": (P.allergens, "editorial"),
    "/pages/shipping-and-delivery": (P.shipping, "service"),
    "/pages/delivery-calendar": (P.delivery_calendar, "calendar"),
    "/pages/warm-weather-shipping": (P.warm_weather, "service"),
    "/pages/returns-and-quality-guarantee": (P.returns, "service"),
    "/pages/faq": (P.faq_page, "faq"),
    "/blogs/stories/how-to-store-pralines": (P.article_store, "article"),
    "/blogs/stories": (P.stories, "blog"),
    "/pages/about": (P.about, "editorial"),
    "/pages/sustainability": (P.sustainability, "editorial"),
    "/pages/contact": (P.contact, "service"),
    "/pages/build-a-ballotin": (P.build_a_ballotin, "builder"),
}

DESCRIPTIONS = {
    "/": "Belgian praline gift boxes, ballotins and vegan pralines, made by hand in Brussels and packed to travel cool.",
}


def nav_group(row):
    """Sitemap "Nav group" ("Shop/Gifts" -> "Shop"); Home and Footer rows have no top-nav item."""
    g = row["Nav group"].split("/")[0].strip()
    return g if g in C.NAV_META else ""


def lead_text(body, fallback):
    """Meta description: the page's lead paragraph, not the sheet's internal "Page job" note."""
    m = re.search(r'<p class="lead">(.*?)</p>', body, re.S)
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else ""
    return text or fallback


def ld(*objs):
    return "".join(f'<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", **o}, ensure_ascii=False)}</script>' for o in objs if o)


def breadcrumb_ld(path, title):
    items = C.CTX.get("crumbs")
    if not items:
        return None
    trail = [("Home", "/")] + [(label, href or path) for label, href in items]
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": f"{SITE_URL}{h}"} for i, (n, h) in enumerate(trail)]}


def product_ld(p):
    offers = [{"@type": "Offer", "name": v["label"], "price": v["price"], "priceCurrency": "EUR",
               "availability": "https://schema.org/InStock" if p["available"] else "https://schema.org/OutOfStock"}
              for v in p["variants"] if v["price"] is not None]
    return {"@type": "Product", "name": p["title"], "description": p["flavour_profile"], "sku": p["id"],
            "brand": {"@type": "Brand", "name": C.BRAND}, "image": [f"{SITE_URL}/{i}.jpg" for i in p["images"]],
            **({"offers": offers} if offers else {})}


def end_tone(body):
    """Background of the last section, so the footer wave blends into it."""
    last = body.rfind('class="section')
    chunk = body[last:last + 80] if last >= 0 else ""
    for cls, var in (("section--butter", "var(--butter)"), ("section--ganache", "var(--ganache)"), ("section--pistachio", "#DCE8DA")):
        if cls in chunk:
            return var
    return "var(--cream)"


SITE_URL = "https://www.example.com"


def rel_file(path):
    return "index.html" if path == "/" else path.strip("/") + ".html"


def enter(path):
    """Set the current page so components.u() builds links relative to it. Call before rendering a body."""
    C.CTX["depth"] = rel_file(path).count("/")
    C.CTX["crumbs"] = None


def write(path, title, desc, body, page, nav="", noindex=False, attrs="", head_extra=""):
    """path: Shopify-style path. Writes site/<path>.html (or index.html)."""
    rel = rel_file(path)
    enter(path)
    html = C.head(title, desc, path, noindex, head_extra)
    html += f'\n<body data-page="{page}" data-root="/" {attrs}>\n'
    html += C.header(nav) + f'\n<main id="main">\n{body}\n</main>\n' + C.footer(end_tone(body)) + "\n" + C.scripts() + "\n</body>\n</html>\n"
    out = SITE / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return rel


def data_js():
    data = {
        "products": cat.PRODUCTS,
        "collections": {h: {**{k: v for k, v in c.items() if k != "rule"}, "members": cat.members(h)} for h, c in cat.COLLECTIONS.items()},
    }
    (SITE / "assets/js/data.js").write_text(
        "/* Generated by _build/build.py from _build/catalogue.py. Do not edit by hand. */\nwindow.PRALINE = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8")


def redirects():
    """301s from the workbook "Redirects & Canonicals" sheet -> _redirects (Netlify/Cloudflare) and vercel.json."""
    rules = [(r["From"], r["To / Rule"]) for r in read_sheet("Redirects & Canonicals") if r["Type"].startswith("301")]
    lines = ["# Netlify / Cloudflare Pages. Both serve /x from x.html automatically (clean URLs).",
             "# 301s generated by _build/build.py from the workbook \"Redirects & Canonicals\" sheet."]
    lines += [f"{a:32} {b:26} 301" for a, b in rules] + [f"{'/_build/*':32} {'/404':26} 404"]
    (SITE / "_redirects").write_text("\n".join(lines) + "\n", encoding="utf-8")
    for cfg in (SITE / "vercel.json", SITE.parent / "vercel.json"):
        data = json.loads(cfg.read_text())
        data["redirects"] = [{"source": a, "destination": b, "permanent": True} for a, b in rules]
        cfg.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return rules


def main():
    C.set_nav(read_sheet("Navigation"))
    rows = read_sheet("Sitemap")
    written, report = [], []
    for row in rows:
        path, template, ptype = row["Path"], row["Template"], row["Page type"]
        noindex = False
        enter(path)
        if ptype == "Redirect":
            target = re.search(r"(/[\w/-]+)", row["Page job"]).group(1)
            extra = f'<meta http-equiv="refresh" content="0; url={C.u(target)}"><script>location.replace("{C.u(target)}" + location.hash)</script>'
            rel = write(path, "Page moved", f"Moved to {target}", P.redirect(target), "redirect", noindex=True, head_extra=extra)
        elif path == "/":
            org = {"@type": "Organization", "name": C.BRAND, "url": SITE_URL, "logo": f"{SITE_URL}/{C.MARK}", "email": "hello@example.com"}
            site = {"@type": "WebSite", "name": C.BRAND, "url": SITE_URL,
                    "potentialAction": {"@type": "SearchAction", "target": f"{SITE_URL}/search?q={{q}}", "query-input": "required name=q"}}
            rel = write(path, "Belgian pralines and gift boxes", DESCRIPTIONS["/"], P.home(), "home", head_extra=ld(org, site))
        elif path.startswith("/collections/"):
            handle = path.split("/")[-1]
            c = cat.COLLECTIONS[handle]
            noindex = bool(c.get("claim")) and not cat.members(handle)
            body = P.collection(handle)
            rel = write(path, c["title"], c["intro"], body, "collection", nav_group(row), noindex, f'data-collection="{handle}"',
                        ld({"@type": "CollectionPage", "name": c["title"], "description": c["intro"], "url": SITE_URL + path}, breadcrumb_ld(path, c["title"])))
        elif path.startswith("/policies/"):
            handle = path.split("/")[-1]
            body = P.policy(handle)
            rel = write(path, P.POLICY[handle][0], lead_text(body, P.POLICY[handle][0]), body, "policy", head_extra=ld(breadcrumb_ld(path, P.POLICY[handle][0])))
        elif path in EDITORIAL:
            fn, page = EDITORIAL[path]
            body = fn()
            title = re.search(r'<h1[^>]*>(.*?)</h1>', body, re.S).group(1)
            title = re.sub(r"<[^>]+>", "", title).strip()
            noindex = path == "/pages/build-a-ballotin"
            desc = lead_text(body, title)
            extra = [breadcrumb_ld(path, title)]
            if path == "/pages/faq":
                extra.append({"@type": "FAQPage", "mainEntity": [
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}}
                    for group in P.FAQ.values() for q, a in group]})
            if path.startswith("/blogs/stories/"):
                extra.append({"@type": "BlogPosting", "headline": title, "description": desc, "author": {"@type": "Organization", "name": C.BRAND},
                              "mainEntityOfPage": SITE_URL + path})
            rel = write(path, title, desc, body, page, nav_group(row), noindex, head_extra=ld(*extra))
        else:
            raise SystemExit(f"No renderer for sitemap path {path} ({template})")
        written.append((path, rel, row["Launch priority"], noindex or ptype == "Redirect"))
        report.append(f"{path:45} {template:18} -> {rel}")

    # Shopify system routes that the sitemap doesn't list but the store needs.
    for p in cat.PRODUCTS:
        path = f"/products/{p['id']}"
        enter(path)
        body = P.product_page(p)
        write(path, p["title"], p["flavour_profile"], body, "product", "Shop", attrs=f'data-product="{p["id"]}"',
              head_extra=ld(product_ld(p), breadcrumb_ld(path, p["title"])))
        written.append((path, path.strip("/") + ".html", "System", False))
    for path, title, fn, page in (("/search", "Search", P.search, "search"), ("/checkout", "Checkout", P.checkout, "checkout"), ("/404", "Page not found", P.not_found, "404")):
        enter(path)
        write(path, title, title, fn(), page, noindex=True)
    data_js()
    rules = redirects()

    # Every Navigation sheet URL must resolve to a page this build wrote.
    built = {p for p, *_ in written}
    missing = [(n, h) for _, _, links, _ in C.NAV for n, h, _ in links if h not in built]
    if missing:
        raise SystemExit(f"Navigation links with no page: {missing}")

    # sitemap.xml with indexable pages only (redirects, empty claim pages and system pages excluded).
    urls = "".join(f"<url><loc>https://www.example.com{p}</loc></url>" for p, _, _, skip in written if not skip)
    (SITE / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")

    print("\n".join(report))
    print(f"\n{len(rows)} sitemap rows rendered, {len(cat.PRODUCTS)} product pages, 3 system pages.")
    print(f"{sum(len(l) for _, _, l, _ in C.NAV)} nav links in {len(C.NAV)} groups, {len(rules)} redirects.")


if __name__ == "__main__":
    main()
