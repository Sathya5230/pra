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


# Sitemap path -> (renderer, nav group, body data-page)
EDITORIAL = {
    "/pages/corporate-gifting": (P.corporate_gifting, "Corporate Gifts", "corporate"),
    "/pages/pralines-with-logo": (P.pralines_with_logo, "Corporate Gifts", "corporate"),
    "/pages/client-gifts": (lambda: P.corp_usecase_page("client"), "Corporate Gifts", "corporate"),
    "/pages/employee-gifts": (lambda: P.corp_usecase_page("employee"), "Corporate Gifts", "corporate"),
    "/pages/request-a-quote": (P.request_a_quote, "Corporate Gifts", "quote"),
    "/pages/upload-your-logo": (P.upload_your_logo, "Corporate Gifts", "upload"),
    "/pages/belgian-pralines": (P.belgian_pralines, "Our Chocolate", "editorial"),
    "/pages/ingredients": (P.ingredients, "Our Chocolate", "editorial"),
    "/pages/organic-and-fairtrade": (P.organic_and_fairtrade, "Vegan & Conscious", "editorial"),
    "/pages/allergens": (P.allergens, "Our Chocolate", "editorial"),
    "/pages/shipping-and-delivery": (P.shipping, "Delivery", "service"),
    "/pages/delivery-calendar": (P.delivery_calendar, "Delivery", "calendar"),
    "/pages/warm-weather-shipping": (P.warm_weather, "Delivery", "service"),
    "/pages/returns-and-quality-guarantee": (P.returns, "Delivery", "service"),
    "/pages/faq": (P.faq_page, "Delivery", "faq"),
    "/blogs/stories/how-to-store-pralines": (P.article_store, "Our Chocolate", "article"),
    "/blogs/stories": (P.stories, "Our Chocolate", "blog"),
    "/pages/about": (P.about, "About", "editorial"),
    "/pages/sustainability": (P.sustainability, "About", "editorial"),
    "/pages/contact": (P.contact, "About", "service"),
    "/pages/build-a-ballotin": (P.build_a_ballotin, "Shop", "builder"),
}

DESCRIPTIONS = {
    "/": "Belgian praline gift boxes, ballotins and vegan pralines, made by hand in Brussels and packed to travel cool.",
}


def end_tone(body):
    """Background of the last section, so the footer wave blends into it."""
    last = body.rfind('class="section')
    chunk = body[last:last + 80] if last >= 0 else ""
    for cls, var in (("section--butter", "var(--butter)"), ("section--ganache", "var(--ganache)"), ("section--pistachio", "#DCE8DA")):
        if cls in chunk:
            return var
    return "var(--cream)"


def rel_file(path):
    return "index.html" if path == "/" else path.strip("/") + ".html"


def enter(path):
    """Set the current page so components.u() builds links relative to it. Call before rendering a body."""
    C.CTX["depth"] = rel_file(path).count("/")


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


def main():
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
            rel = write(path, "Belgian pralines and gift boxes", DESCRIPTIONS["/"], P.home(), "home")
        elif path.startswith("/collections/"):
            handle = path.split("/")[-1]
            c = cat.COLLECTIONS[handle]
            noindex = bool(c.get("claim")) and not cat.members(handle)
            nav = P.NAV_GROUP.get(c["template"], "Shop")
            if handle in P.CONSCIOUS_CHIPS:
                nav = "Vegan & Conscious"
            rel = write(path, c["title"], c["intro"], P.collection(handle), "collection", nav, noindex, f'data-collection="{handle}"')
        elif path.startswith("/policies/"):
            handle = path.split("/")[-1]
            rel = write(path, P.POLICY[handle][0], P.POLICY[handle][0], P.policy(handle), "policy")
        elif path in EDITORIAL:
            fn, nav, page = EDITORIAL[path]
            body = fn()
            title = re.search(r'<h1[^>]*>(.*?)</h1>', body, re.S).group(1)
            title = re.sub(r"<[^>]+>", "", title).strip()
            noindex = path == "/pages/build-a-ballotin"
            rel = write(path, title, row["Page job"], body, page, nav, noindex)
        else:
            raise SystemExit(f"No renderer for sitemap path {path} ({template})")
        written.append((path, rel, row["Launch priority"], noindex or ptype == "Redirect"))
        report.append(f"{path:45} {template:18} -> {rel}")

    # Shopify system routes that the sitemap doesn't list but the store needs.
    for p in cat.PRODUCTS:
        path = f"/products/{p['id']}"
        enter(path)
        write(path, p["title"], p["flavour_profile"], P.product_page(p), "product", "Shop", attrs=f'data-product="{p["id"]}"')
        written.append((path, path.strip("/") + ".html", "System", False))
    for path, title, fn, page in (("/search", "Search", P.search, "search"), ("/checkout", "Checkout", P.checkout, "checkout"), ("/404", "Page not found", P.not_found, "404")):
        enter(path)
        write(path, title, title, fn(), page, noindex=True)
    data_js()

    # sitemap.xml with indexable pages only (redirects, empty claim pages and system pages excluded).
    urls = "".join(f"<url><loc>https://www.example.com{p}</loc></url>" for p, _, _, skip in written if not skip)
    (SITE / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")

    print("\n".join(report))
    print(f"\n{len(rows)} sitemap rows rendered, {len(cat.PRODUCTS)} product pages, 3 system pages.")


if __name__ == "__main__":
    main()
