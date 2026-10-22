"""Download the storefront photography and apply one mild chocolate colour grade.

Photos are from Unsplash (free under the Unsplash License). Run from anywhere:
    python3 site/_build/fetch_images.py
Re-running skips files that already exist; pass --force to rebuild them.
"""
import io
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img"
CDN = "https://images.unsplash.com/photo-{id}?w={w}&h={h}&fit=crop&crop={crop}&q=85&fm=jpg"

# Product photography: two images per product (main, alternate).
PRODUCTS = {
    "signature-gift-box": ["1526081347589-7fa3cb41b4b2", "1526081715791-7c538f86060e"],
    "heritage-ballotin": ["1599599810769-bcde5a160d32", "1734692928513-351516b38869"],
    "noir-ganache-collection": ["1621134283184-5e7881013013", "1604496803614-b42681ceb74d"],
    "vegan-praline-box": ["1526823127573-0fda76b6c24f", "1769433509476-bd68b1229916"],
    "noisette-praline-box": ["1682120501920-7ce18b00237a", "1615485925822-77040a19d84b"],
    "grand-coffret": [("1609074458316-3e282975bb1e", "bottom"), "1548741487-18d363dc4469"],
    "truffle-box": ["1775201630951-665651af1747", "1549007994-cb92caebd54b"],
    "salted-caramel-mini": ["1763700667398-24ae7f2289fc", "1545015451-f05567aa6bcc"],
    "thank-you-four": ["1566565286951-f81c7ba5619d", "1668463876833-339717e58c4c"],
    "raspberry-ganache-hearts": ["1567270745444-ca3f1e2ba6c1", "1656821991459-ae723d90d648"],
    "hazelnut-rochers": ["1787788629722-02cf905bb188", "1761591470313-003c5a243356"],
    "mendiants": ["1514481372798-c8b2f7e6f708", "1767709383373-2e7c2e192e6d"],
    "tablet-noir-72": ["1737976685095-833ed51e7fcc", "1646303339019-a57056b180ae"],
    "tablet-lait-noisette": ["1600070338156-c39c9b594cd1", "1626697556651-67ebdcb8cbd6"],
    "tablet-noir-85": ["1592290321458-49b80f943a26", "1750765239895-1702df302671"],
    "winter-spice-edition": ["1702744217578-109f77831534", "1702744217978-233e3cfd92ca"],
    "corporate-24": ["1614631016624-cb89bceec02c", "1526081715791-7c538f86060e"],
    "prestige-48": ["1548741487-18d363dc4469", "1604496803614-b42681ceb74d"],
    "logo-pralines": ["1573013792262-761a3e17fb39", ("1573013835014-60d1590bfa38", "bottom,right")],
}

# Editorial photography: key -> (id, width, height, crop)
EDITORIAL = {
    "hero": ("1682120501920-7ce18b00237a", 1600, 1300, "entropy"),
    "hero-box": ("1548741487-18d363dc4469", 1100, 1300, "focalpoint&fp-x=.62&fp-y=.5"),
    "hero-truffles": ("1545015451-f05567aa6bcc", 900, 1100, "entropy"),
    "melt": ("1676817167465-38a0fe938c53", 1800, 700, "center"),
    "melt-dark": ("1657502096852-340a75dc56f7", 1800, 900, "center"),
    "pour": ("1760445528687-3528e6e5ea73", 1200, 1400, "entropy"),
    "mixing": ("1760445528671-5f923d72b82d", 1200, 1400, "entropy"),
    "cream-pour": ("1760445529130-230c28c38b2e", 1200, 900, "entropy"),
    "cocoa-hands": ("1493925410384-84f842e616fb", 1200, 1400, "entropy"),
    "cocoa-pods": ("1743252878695-367d69dc87a8", 1600, 1000, "entropy"),
    "cocoa-tree": ("1573710661345-610f790e1218", 1000, 1300, "entropy"),
    "beans-bar": ("1638194645412-1d0b4c53ffed", 1200, 900, "entropy"),
    "hazelnuts": ("1767709383373-2e7c2e192e6d", 1200, 900, "entropy"),
    "hazel-shells": ("1761591470313-003c5a243356", 1600, 900, "entropy"),
    "hazel-white": ("1615485925822-77040a19d84b", 1000, 1000, "entropy"),
    "gift-ribbon": ("1513885045260-6b3086b24c17", 1600, 1000, "entropy"),
    "gift-small": ("1668463876833-339717e58c4c", 1200, 1200, "entropy"),
    "gift-pink": ("1513201099705-a9746e1e201f", 1200, 1200, "entropy"),
    "gift-roses": ("1625552186152-668cd2f0b707", 1200, 1200, "entropy"),
    "delivery-hands": ("1566576721346-d4a3b4eaeb55", 1600, 1100, "entropy"),
    "delivery-door": ("1758523670564-d1d6a734dc0b", 1200, 1300, "entropy"),
    "boxes": ("1631010231931-d2c396b444ec", 1200, 1000, "entropy"),
    "grand-place": ("1786521642914-3027f5e34836", 1400, 1600, "entropy"),
    "brussels-street": ("1786521642980-40f38a7d10c1", 1200, 1400, "entropy"),
    "truffle-bowl": ("1769433509476-bd68b1229916", 1200, 1200, "entropy"),
    "open-box": ("1614631016624-cb89bceec02c", 1600, 1200, "entropy"),
    "tablets-stack": ("1750765239895-1702df302671", 1200, 1200, "entropy"),
    "tablet-foil": ("1640678345762-ae16b0ee6a1e", 1600, 900, "entropy"),
    "tablets-mint": ("1636450525985-f38e86fd4759", 1200, 1200, "entropy"),
    "bark": ("1702743692629-b11e94c63b0a", 1600, 900, "entropy"),
    "mendiants": ("1514481372798-c8b2f7e6f708", 1200, 1200, "entropy"),
    "cut": ("1604496803614-b42681ceb74d", 1400, 1000, "entropy"),
    "rows": ("1706147602203-6e2c340fb6db", 1600, 1000, "entropy"),
    "dark-bonbons": ("1621134283184-5e7881013013", 1400, 1000, "entropy"),
    "heart-box": ("1656821991459-ae723d90d648", 1200, 1200, "entropy"),
    "christmas": ("1702744217578-109f77831534", 1600, 1000, "entropy"),
    "nut-truffles": ("1787788629722-02cf905bb188", 1200, 1200, "entropy"),
    "assorted": ("1599599810769-bcde5a160d32", 1600, 1100, "entropy"),
    "assorted-beige": ("1734692928513-351516b38869", 1200, 1200, "entropy"),
    "cups": ("1566565286951-f81c7ba5619d", 1200, 1200, "entropy"),
    "premium-box": ("1548741487-18d363dc4469", 1400, 1400, "entropy"),
    "logo-box": ("1573013792262-761a3e17fb39", 1400, 1200, "entropy"),
    "red-box": ("1609074458316-3e282975bb1e", 1200, 1300, "bottom"),
    "raspberry": ("1567270745444-ca3f1e2ba6c1", 1200, 1200, "entropy"),
    "bars-rows": ("1633273169950-4265bcc1cefc", 1400, 1000, "entropy"),
}

SHADOW = np.array([43, 25, 15], dtype=np.float32)      # bitter cocoa
HIGHLIGHT = np.array([255, 247, 232], dtype=np.float32)  # cream


def grade(img: Image.Image) -> Image.Image:
    """Mild chocolate grade: a warm cocoa-to-cream duotone blended at 20%,
    slightly lower saturation, and lifted blacks so photos sit on cream pages."""
    img = ImageEnhance.Color(img.convert("RGB")).enhance(0.9)
    a = np.asarray(img).astype(np.float32)
    lum = (0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2])[..., None] / 255.0
    duo = SHADOW + (HIGHLIGHT - SHADOW) * lum
    out = a * 0.8 + duo * 0.2
    out = 14 + out * (241 / 255)  # lift shadows, soften whites
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def fetch(photo_id, w, h, crop, dest: Path, force=False):
    if dest.exists() and not force:
        return "skip"
    url = CDN.format(id=photo_id, w=w, h=h, crop=crop)
    # curl uses the system certificate store, which python.org builds often lack.
    data = subprocess.run(["curl", "-sfL", "--max-time", "60", url], check=True, capture_output=True).stdout
    img = Image.open(io.BytesIO(data))
    dest.parent.mkdir(parents=True, exist_ok=True)
    grade(img).save(dest, "JPEG", quality=80, optimize=True, progressive=True)
    return "ok"


def main():
    force = "--force" in sys.argv
    jobs = []
    for handle, ids in PRODUCTS.items():
        for i, entry in enumerate(ids, start=1):
            pid, crop = entry if isinstance(entry, tuple) else (entry, "entropy")
            jobs.append((pid, 1000, 1000, crop, OUT / "products" / f"{handle}-{i}.jpg"))
            jobs.append((pid, 520, 520, crop, OUT / "products" / f"{handle}-{i}-sm.jpg"))
    for key, (pid, w, h, crop) in EDITORIAL.items():
        jobs.append((pid, w, h, crop, OUT / f"{key}.jpg"))
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(8) as ex:
        for job, res in zip(jobs, ex.map(lambda j: fetch(*j, force=force), jobs)):
            print(res, job[-1].relative_to(ROOT))


if __name__ == "__main__":
    main()
