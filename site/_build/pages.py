"""Page bodies, one function per Sitemap template."""
from html import escape as esc

from catalogue import COLLECTIONS, PRODUCTS, get, members
from components import (ICON, btn, crumbs, doodle, drip, faq, figure, head_row, icon, img, marquee,
                        newsletter_band, page_hero, quote_form, rail, split, stamp, steps, tiles, ticks,
                        trust_strip, u, wave)

# Shared FAQ content, reused on /pages/faq and topic pages.
FAQ = {
    "Shipping": [
        ("How long does delivery take?", "<p>In Belgium, usually 1–2 working days after dispatch. Orders placed before 14:00 on a working day leave the atelier the next working day. See <a class='link' href='{shipping}'>shipping & delivery</a> for other countries.</p>"),
        ("Do you ship when it’s hot?", "<p>Yes, with an insulated liner and cool packs. When the forecast on the route is too warm, we hold the order and email you a new dispatch date. <a class='link' href='{warm}'>Read the warm-weather policy</a>.</p>"),
        ("Can I choose a delivery date?", "<p>Yes. Pick a date in the cart and we’ll plan dispatch so it arrives on time, weather permitting. The <a class='link' href='{calendar}'>delivery calendar</a> shows the cut-offs for holidays.</p>"),
    ],
    "Gifting": [
        ("Can I send it straight to someone?", "<p>Yes. Add their address at checkout and a gift message in the cart. We print your message on a card and never put prices in the box.</p>"),
        ("How long do pralines keep?", "<p>Most boxes keep 4–6 weeks from dispatch at 15–18 °C. Fresh truffles are best within three weeks. Every product page lists its own shelf life.</p>"),
        ("Can I build my own box?", "<p>Yes, with <a class='link' href='{builder}'>Build a ballotin</a>: choose a size, then pick each praline.</p>"),
    ],
    "Vegan & dietary": [
        ("Which products are vegan?", "<p>Everything in <a class='link' href='{vegan}'>vegan chocolates</a>. They contain no milk, butter, cream or honey, but are made in an atelier that also handles milk.</p>"),
        ("Which boxes are alcohol-free?", "<p>Everything in <a class='link' href='{noalc}'>no alcohol chocolates</a>. Products with liqueur pieces say so next to the add-to-cart button.</p>"),
    ],
    "Allergens": [
        ("Where do I find allergen information?", "<p>On every product page, right next to the add-to-cart button, and in the Ingredients & allergens tab. See the <a class='link' href='{allergens}'>allergen guide</a> for an overview.</p>"),
        ("Are your pralines nut-free?", "<p>No. Our atelier roasts hazelnuts and almonds every day, so traces of nuts are possible in every product.</p>"),
    ],
    "Corporate": [
        ("What’s the minimum corporate order?", "<p>Quotes start at 25 boxes. Logo pralines start at 100 pieces. For fewer, order directly from <a class='link' href='{corpbox}'>corporate gift boxes</a>.</p>"),
        ("Can you deliver to every recipient?", "<p>Yes. Send us a spreadsheet of addresses and we ship each box separately with tracking.</p>"),
        ("How do you handle our logo?", "<p>Upload it with your quote or on <a class='link' href='{upload}'>upload your logo</a>. We send a digital proof and print nothing until you approve it in writing.</p>"),
    ],
}


def faq_items(*groups):
    links = dict(shipping=u("/pages/shipping-and-delivery"), warm=u("/pages/warm-weather-shipping"), calendar=u("/pages/delivery-calendar"),
                 builder=u("/pages/build-a-ballotin"), vegan=u("/collections/vegan-chocolates"), noalc=u("/collections/no-alcohol-chocolates"),
                 allergens=u("/pages/allergens"), corpbox=u("/collections/corporate-gifts"), upload=u("/pages/upload-your-logo"))
    return [(q, a.format(**links)) for g in groups for q, a in FAQ[g]]


def faq_section(title="Questions before you order", groups=("Gifting", "Shipping"), bg="section--butter"):
    return f'''<section class="section {bg}"><div class="wrap narrow">
  <div class="center" style="margin-bottom:2rem"><p class="script">Good to know</p><h2 class="h2">{esc(title)}</h2></div>
  {faq(faq_items(*groups))}
  <p class="center" style="margin-top:2rem"><a class="link" href="{u("/pages/faq")}">All questions</a></p>
</div></section>'''


def cta_band(script, title, text, ctas, image, tone="ganache", flip=False):
    return f'''<section class="section section--{tone}{" on-dark" if tone == "ganache" else ""} band">
  {doodle("sparkle", "left:4%;top:14%;width:26px", "var(--milk)")}
  {split(image, "", f'<p class="script">{esc(script)}</p><h2 class="h2">{esc(title)}</h2><p class="lead">{text}</p><div class="hero-actions">{ctas}</div>', flip=flip, frame="round")}
</section>'''


def collection_cards(handles):
    cards = "".join(
        f'<a class="col-card" href="{u("/collections/" + h)}">{img(COLLECTIONS[h]["image"], "")}<span class="col-card-copy"><span class="script">{esc(COLLECTIONS[h]["script"])}</span><span class="h3">{esc(COLLECTIONS[h]["title"])}</span></span></a>'
        for h in handles)
    return f'<div class="col-cards">{cards}</div>'


def journal_cards():
    items = [("/blogs/stories/how-to-store-pralines", "cream-pour", "Product care", "How to store pralines"),
             ("/pages/belgian-pralines", "pour", "Our chocolate", "What makes a praline Belgian"),
             ("/pages/ingredients", "hazelnuts", "Ingredients", "What goes into every box")]
    return '<div class="journal">' + "".join(
        f'<a class="journal-card" href="{u(h)}"><figure class="ph ph--round">{img(k, "")}</figure><span class="tag">{t}</span><h3 class="h3">{esc(n)}</h3><span class="link">Read</span></a>'
        for h, k, t, n in items) + "</div>"


# =====================================================================
# Homepage
# =====================================================================
def home():
    sig = get("signature-gift-box")
    ladder_imgs = ["cups", "assets/img/products/signature-gift-box-1.jpg", "premium-box"]
    ladder = "".join(f'''<a class="step-card" href="{u("/products/signature-gift-box")}?v={i}">
        <figure class="ph ph--round">{img(ladder_imgs[i], f"Signature praline gift box, {v['label']}")}</figure>
        <div class="row"><span class="h3">{v["label"]}</span><span class="price">€{v["price"]}</span></div>
        <span class="small">{["A thoughtful thank-you", "Our most-given size", "For a table, a team or a family"][i]}</span>
        {'<span class="badge badge--best">Most given</span>' if i == 1 else ""}</a>''' for i, v in enumerate(sig["variants"]))

    intents = [
        ("/collections/gift-boxes", "gift-ribbon", "A gift", "Boxes by occasion and budget, from a €9 thank-you to a two-layer coffret.", "Shop gifts", ""),
        ("/collections/vegan-chocolates", "raspberry", "Vegan & conscious", "Vegan pralines made to the same standard as the rest of the counter.", "See vegan chocolates", "intent--vegan"),
        ("/pages/corporate-gifting", "logo-box", "For clients or a team", "Branded boxes and logo pralines, quoted without going through checkout.", "Corporate gifting", "intent--corp"),
        ("/collections/belgian-classics", "assorted-beige", "The Belgian classics", "Ballotins chosen by weight: butter creams, marzipan and gianduja.", "Shop the classics", ""),
    ]
    intent_html = "".join(f'''<a class="intent {c}" href="{u(h)}">
        <figure class="intent-img">{img(k, "")}</figure>
        <div class="intent-copy"><span class="h3">{t}</span><p>{d}</p><span class="go">{g} {ICON["right"]}</span></div></a>''' for h, k, t, d, g, c in intents)

    flavours = [("Praliné", "Roasted hazelnut and almond", "assets/img/products/noisette-praline-box-1-sm.jpg", "/collections/pralines-and-truffles"),
                ("Ganache", "Single-origin dark", "assets/img/products/noir-ganache-collection-1-sm.jpg", "/collections/pralines-and-truffles"),
                ("Caramel", "Soft, with Guérande salt", "assets/img/products/salted-caramel-mini-1-sm.jpg", "/collections/small-gifts"),
                ("Truffle", "Fresh cream, cocoa-dusted", "assets/img/products/truffle-box-1-sm.jpg", "/collections/pralines-and-truffles"),
                ("Fruit", "Raspberry and clementine", "assets/img/products/raspberry-ganache-hearts-1-sm.jpg", "/collections/love-and-romance"),
                ("Rocher", "Crunchy nut-coated domes", "assets/img/products/hazelnut-rochers-1-sm.jpg", "/collections/small-gifts"),
                ("Mendiant", "Dark discs, nuts and fruit", "assets/img/products/mendiants-1-sm.jpg", "/collections/belgian-classics"),
                ("Tablet", "Noir 72%, 85% and milk", "assets/img/products/tablet-noir-72-1-sm.jpg", "/collections/chocolate-tablets")]
    flavour_html = "".join(f'<a class="flavour-tile" href="{u(h)}"><span class="ft-img">{img(i, "")}</span><span class="h3">{n}</span><small>{d}</small></a>' for n, d, i, h in flavours)

    mosaic = ["rows", "mixing", "hazel-shells", "truffle-bowl", "tablet-foil", "gift-roses"]
    mosaic_html = "".join(f'<figure class="m-{i}">{img(k, "")}</figure>' for i, k in enumerate(mosaic))

    return f'''
<section class="hero grain">
  {doodle("leaf", "left:3%;bottom:14%;width:74px;transform:rotate(-12deg)", "var(--latte)")}
  {doodle("sparkle", "left:43%;bottom:24%;width:22px", "var(--cocoa)")}
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <h1><span class="script">Pralines belges, faites main à Bruxelles</span>The box they keep the ribbon from</h1>
      <p class="lead">Pralinés, ganaches and caramels finished by hand in small batches, packed to arrive the way they left the counter.</p>
      <div class="hero-actions">{btn("Shop gift boxes", "/collections/gift-boxes")}{btn("Find a gift", "/collections/thank-you-gifts", "btn-lg")}</div>
      <ul class="trust-chips" aria-label="Why order here">
        <li>{icon("hand", "ico-s")}Made in Belgium</li><li>{icon("info", "ico-s")}Allergens on every product</li>
        <li>{icon("gift", "ico-s")}Free printed gift card</li><li>{icon("snow", "ico-s")}Packed for warm weather</li>
      </ul>
    </div>
    <div class="hero-art">
      <figure class="hero-ballotin">{img("hero-box", "An open box of square pralines with stamped and gilded tops", eager=True)}</figure>
      <a class="hero-label" href="{u("/products/signature-gift-box")}">
        <span class="hero-label-name">Signature praline box</span>
        <span class="hero-label-price">From €22.00</span>
      </a>
    </div>
  </div>
  {wave("var(--cream)", "transparent")}
</section>

{trust_strip()}

<section class="section">
  <div class="wrap">
    {head_row("Where would you like to start?", "Four ways in", f'<p class="side-note">Find the right box in under a minute.</p>')}
    <div class="intents">{intent_html}</div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">{rail("bestsellers", "bestsellers", 10, "What people give most", "Nos favoris", ("Shop all", "/collections/all"))}</div>
</section>

{marquee(["Fait main à Bruxelles", "Praliné noisette", "Ganache noire", "Caramel salé", "Ballotins au poids", "Truffes fraîches"])}
{drip("var(--cocoa)", "var(--butter)")}

<section class="section section--butter grain" style="padding-top:clamp(2.5rem,5vw,4rem)">
  {doodle("hazelnut", "right:4%;top:8%;width:44px;transform:rotate(18deg)", "var(--milk)")}
  <div class="wrap">
    {head_row("The signature box", "Pick the size, we do the rest", '<p class="side-note">Same selection in every size: hazelnut praliné, single-origin ganache and salted caramel in dark, milk and white.</p>')}
    <div class="ladder">{ladder}</div>
  </div>
</section>

<section class="section atelier">
  {doodle("swirl", "right:3%;bottom:10%;width:110px", "var(--latte)")}
  {split("pour", "Melted dark chocolate running off a spatula into a bowl", f'''
    <p class="script">Inside the atelier</p>
    <h2 class="h2">Four steps, all by hand</h2>
    <p class="lead">Every praline goes through the same four stages in our Brussels workshop, in batches small enough to taste each one.</p>
    {steps([("Roast", "Hazelnuts and almonds roasted and ground into praliné."), ("Temper", "Couverture brought to 31 °C for snap and shine."), ("Fill", "Shells cast, filled and sealed by hand."), ("Pack", "Boxed to order and wrapped for the journey.")])}
    {btn("Read how we make them", "/pages/belgian-pralines", "btn")}''', frame="arch", extra=stamp("31 °C · TEMPÉRÉ À LA MAIN · ", "right:-26px;top:8%", "sparkle"))}
</section>

<section class="section section--cream heritage">
  {split("assorted", "Assorted Belgian pralines and truffles laid out on white marble", f'''
    <p class="script">Chosen by weight</p>
    <h2 class="h2">The ballotin, the Belgian way</h2>
    <p class="lead">The folded paper box you remember from the chocolate shop counter: 250 g, 500 g or a full kilo, filled with the classics.</p>
    {ticks(["Butter creams, marzipan, gianduja and pralinés", "A few liqueur pieces, clearly marked on the product page", "Priced by weight, from €19"])}
    <div class="hero-actions">{btn("Choose a ballotin", "/products/heritage-ballotin")}{btn("Build your own", "/pages/build-a-ballotin", "btn-lg")}</div>''', flip=True, frame="offset", extra=f'<figure class="ph ph--circle inset-tr">{img("grand-place", "The Grand-Place in Brussels")}</figure>')}
</section>

<section class="section section--ganache on-dark band">
  {doodle("dots", "right:5%;top:10%;width:60px", "rgba(231,207,174,.25)")}
  {split("logo-box", "A box of square pralines stamped with a rose pattern", f'''
    <p class="script">Cadeaux d’entreprise</p>
    <h2 class="h2">Your logo, in cocoa butter</h2>
    <p class="lead">Client gifts, employee thank-yous and event giveaways. Tell us the quantity and date, and we reply with a quote and a sample pack.</p>
    {ticks(["Branded sleeves, cards, ribbons or logo pralines", "One delivery or many addresses", "No checkout: a written quote first"])}
    <div class="hero-actions">{btn("Request a quote", "/pages/request-a-quote", "btn-light btn-full btn-lg", 'data-quote')}{btn("How it works", "/pages/corporate-gifting", "btn-light btn-lg")}</div>''', frame="round")}
</section>

<section class="section section--pistachio">
  {doodle("leaf", "right:4%;top:10%;width:80px;transform:rotate(20deg)", "#B9CFBB")}
  <div class="wrap">{rail("vegan-chocolates", "vegan-rail", 8, "Not a compromise shelf", "Vegan & conscious", ("See all vegan", "/collections/vegan-chocolates"))}</div>
</section>

<section class="section">
  <div class="wrap">
    {head_row("Choose by taste", "Find your favourite filling", '<p class="side-note">Every filling links to the boxes that contain it.</p>')}
    <div class="flavour-tiles">{flavour_html}</div>
  </div>
</section>

<section class="seasonal-band">
  {img("christmas", "Chocolate figures shaped like snowmen and Christmas trees")}
  <div class="wrap seasonal-copy">
    <span class="badge badge--limited">Limited edition</span>
    <p class="script">Seasonal drop</p>
    <h2 class="h2">Winter spice edition</h2>
    <p>Speculoos praliné, clementine ganache and cardamom caramel, moulded as little winter figures. Made from November to January only.</p>
    {btn("Shop seasonal drops", "/collections/seasonal-drops", "btn-light btn-full btn-lg")}
  </div>
</section>

<section class="section">
  <div class="wrap">
    {head_row("Before you check out", "How your box gets there", f'<a class="link" href="{u("/pages/shipping-and-delivery")}">Shipping & delivery details</a>')}
    <div class="delivery-layout">
      <figure class="ph ph--round">{img("delivery-hands", "A parcel being handed over")}</figure>
      <div class="delivery-panel">
        <div>{icon("clock")}<h3>Order by 14:00</h3><p>Weekday orders placed before the cut-off leave the atelier the next working day.</p></div>
        <div>{icon("snow")}<h3>Packed for heat</h3><p>Insulated liner on every order, cool packs in warm months. We hold a box rather than send it into a heatwave.</p></div>
        <div>{icon("calendar")}<h3>Pick the day</h3><p>Choose a delivery date in the cart, so a birthday box doesn’t arrive a week early.</p></div>
        <div>{icon("shield")}<h3>Arrives right</h3><p>If a box arrives melted or damaged, send us a photo and we’ll replace it.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="section section--butter grain">
  <div class="wrap">
    {head_row("From the journal", "Stories from the atelier", f'<a class="link" href="{u("/blogs/stories")}">All stories</a>')}
    {journal_cards()}
  </div>
</section>

<section class="section">
  <div class="wrap">
    {head_row("Follow along", "A day at the counter", f'<a class="link" href="#">@praline.bruxelles</a>')}
    <div class="mosaic">{mosaic_html}</div>
  </div>
</section>

{newsletter_band()}'''


# =====================================================================
# Collections (Collection PLP, Gift PLP, Vegan PLP, Corporate PLP)
# =====================================================================
SHOP_CHIPS = ["all", "pralines-and-truffles", "ballotins", "gift-boxes", "chocolate-tablets", "small-gifts", "premium-gifts", "belgian-classics", "seasonal-drops"]
GIFT_CHIPS = ["birthday-gifts", "thank-you-gifts", "love-and-romance", "dinner-party-gifts", "small-gifts", "gift-boxes"]
CONSCIOUS_CHIPS = ["vegan-chocolates", "no-alcohol-chocolates", "organic-chocolate", "fairtrade-chocolate"]
NAV_GROUP = {"Collection PLP": "Shop", "Gift PLP": "Gifts", "Vegan PLP": "Vegan & Conscious", "Corporate PLP": "Corporate Gifts"}


def chips(handles, current):
    return '<div class="chips" aria-label="Collections">' + "".join(
        f'<a class="chip" href="{u("/collections/" + h)}"{" aria-current=page" if h == current else ""}>{esc(COLLECTIONS[h]["title"] if h != "small-gifts" else "Small attentions")}</a>'
        for h in handles) + "</div>"


def collection(handle):
    c = COLLECTIONS[handle]
    t = c["template"]
    n = len(members(handle))
    if handle in CONSCIOUS_CHIPS:
        chip_set, group = CONSCIOUS_CHIPS, ("Vegan & Conscious", "/collections/vegan-chocolates")
    elif t == "Gift PLP":
        chip_set, group = GIFT_CHIPS, ("Gifts", "/collections/gift-boxes")
    elif t == "Corporate PLP":
        chip_set, group = [], ("Corporate Gifts", "/pages/corporate-gifting")
    else:
        chip_set, group = SHOP_CHIPS, ("Shop", "/collections/all")
    tone = {"Vegan PLP": "pistachio", "Corporate PLP": "ganache"}.get(t, "butter")
    if handle in ("organic-chocolate", "fairtrade-chocolate"):
        tone = "pistachio"

    head = f'''<section class="plp-head plp-head--{tone}{" on-dark" if tone == "ganache" else ""} grain">
  {doodle("bean", "right:42%;top:16%;width:40px;transform:rotate(-20deg)", "var(--milk)" if tone != "ganache" else "rgba(231,207,174,.3)")}
  <div class="wrap plp-head-grid">
    <div>
      {crumbs([group, (c["title"], None)])}
      <p class="script">{esc(c["script"])}</p>
      <h1 class="h1">{esc(c["title"])}</h1>
      <p class="lead">{esc(c["intro"])}</p>
      <p class="small plp-meta">{n} {"product" if n == 1 else "products"}{" · Free gift card with every box" if t != "Corporate PLP" else " · Quotes from 25 boxes"}</p>
    </div>
    <figure class="ph ph--arch plp-art">{img(c["image"], "")}{stamp("PRALINE · BRUXELLES · " + c["title"].upper() + " · ", "left:-30px;bottom:6%") if t in ("Gift PLP", "Vegan PLP") else ""}</figure>
  </div>
  <div class="wrap">{chips(chip_set, handle) if chip_set else ""}</div>
</section>
{wave("var(--cream)", {"butter": "var(--butter)", "pistachio": "#DCE8DA", "ganache": "var(--ganache)"}[tone])}'''

    pre = ""
    if t == "Vegan PLP":
        pre = f'''<section class="section" style="padding-bottom:0"><div class="wrap">
  {head_row("What we can show you", "Claims we stand behind", '<p class="side-note">A claim appears here only when at least one product carries it and the proof is on file.</p>')}
  <div class="tiles" id="claims"></div></div></section>'''
    if c.get("claim"):
        pre = f'''<section class="section" style="padding-bottom:0"><div class="wrap narrow">
  <div class="notice">{icon("shield")}<div><h2 class="h3">No certified {esc(c["claim"])} products yet</h2>
  <p>We only use the word {esc(c["claim"])} on a product when we hold the certificate for that exact product. None of our current range is certified, so this page is empty on purpose and hidden from search engines. <a class="link" href="{u("/pages/organic-and-fairtrade")}">How we handle claims</a>.</p></div></div></div></section>'''
    if c.get("seasonal"):
        pre = f'<div class="wrap"><div class="season-note">{icon("calendar")}<span><b>On sale until 31 January.</b> Christmas orders by 18 December for delivery in Belgium.</span></div></div>'

    corp_band = ""
    if t == "Corporate PLP":
        corp_band = f'''<section class="section section--butter"><div class="wrap quote-layout">
  <div><p class="script">Ordering 25 or more?</p><h2 class="h2">Get a quote with your branding</h2>
  <p class="lead">Every box here can be ordered once to taste, then by quote with branded sleeves, cards, ribbons or logo pralines.</p>
  {ticks(["Quotes from 25 boxes", "Logo pralines from 100 pieces", "Delivery to one address or many"])}
  <figure class="ph ph--round" style="margin-top:1.5rem">{img("open-box", "An open box of pralines with tissue paper")}</figure></div>
  {quote_form("Tell us about your order")}
</div></section>'''

    related = {"Gift PLP": ["gift-boxes", "small-gifts", "premium-gifts"], "Vegan PLP": ["no-alcohol-chocolates", "chocolate-tablets", "gift-boxes"],
               "Corporate PLP": ["gift-boxes", "premium-gifts", "small-gifts"]}.get(t, ["gift-boxes", "vegan-chocolates", "small-gifts"])
    related = [r for r in related if r != handle][:3]

    return f'''{head}
{pre}
<div class="wrap plp-layout">
  <aside class="filters-desktop" aria-label="Filters"><div id="filters-desktop"></div></aside>
  <div>
    <div class="toolbar">
      <div style="display:flex;gap:.75rem;align-items:center"><button class="btn filter-btn" id="filter-open" data-open="filter-drawer">Filter</button><span id="count" class="muted" aria-live="polite"></span></div>
      <label><span class="sr-only">Sort by</span><select id="sort"><option value="featured">Bestsellers first</option><option value="price-asc">Price, low to high</option><option value="price-desc">Price, high to low</option></select></label>
    </div>
    <div class="active-filters" id="active"></div>
    <div class="grid" id="grid"></div>
    {f'<div class="gift-strip">{doodle("sparkle", "right:30%;top:-10px;width:22px", "var(--milk)")}<div><p class="script">Sending it as a gift?</p><span class="h3">Free gift card, no prices inside</span></div><a class="btn btn-light" href="{u("/pages/request-a-quote")}" data-quote>Ordering 25 or more? Get a quote</a></div>' if t != "Corporate PLP" else ""}
  </div>
</div>
{corp_band}
<section class="section{" section--butter" if t != "Corporate PLP" else ""}" style="padding-bottom:clamp(2rem,5vw,4rem)"><div class="wrap">
  {head_row("Keep browsing", "You might also like")}
  {collection_cards(related)}
</div></section>
{faq_section(groups=("Corporate", "Shipping") if t == "Corporate PLP" else ("Vegan & dietary", "Allergens") if t == "Vegan PLP" else ("Gifting", "Shipping"), bg="")}
<aside class="drawer drawer--left" id="filter-drawer" aria-label="Filters" aria-hidden="true">
  <div class="drawer-head"><h2>Filter</h2><button class="icon-btn" data-close aria-label="Close filters">{ICON["close"]}</button></div>
  <div class="drawer-body" id="filters-mobile"></div>
  <div class="drawer-foot" style="display:flex;gap:.5rem"><button class="btn" id="filters-clear" style="flex:1">Clear all</button><button class="btn btn-full" data-close style="flex:1">Show products</button></div>
</aside>'''


# =====================================================================
# Product (Shopify /products/<handle>)
# =====================================================================
def product_page(p):
    col = p["collections"][0]
    return f'''<div class="wrap">
  <div style="margin-top:1.5rem">{crumbs([(COLLECTIONS[col]["title"], "/collections/" + col), (p["title"], None)])}</div>
  <div class="pdp">
    <div class="gallery"><div class="thumbs" id="thumbs"></div><div class="stage" id="stage"></div></div>
    <div class="pdp-info"><div id="pdp-info"></div><div class="tabs" id="tabs"></div></div>
  </div>
</div>
<section class="section section--butter grain flavour-key-section" id="flavour-key-wrap" hidden>
  {doodle("hazelnut", "right:5%;top:12%;width:40px", "var(--milk)")}
  <div class="wrap">{head_row("Inside the box", "Your flavour map", '<p class="side-note">A printed copy of this map comes in every box.</p>')}<div class="flavour-key" id="flavour-key"></div></div>
</section>
{trust_strip()}
<section class="section"><div class="wrap">{rail("related", "related", 4, "Add one, upgrade or swap", "Goes well with")}</div></section>
<div class="sticky-buy" id="sticky-buy" hidden></div>'''


# =====================================================================
# Corporate landing pages
# =====================================================================
def corp_usecases():
    items = [("/pages/client-gifts", "premium-box", "Client gifts", "Year-end thank-yous and deal-closing boxes, sent to each client’s address."),
             ("/pages/employee-gifts", "gift-small", "Employee gifts", "Welcome boxes, work anniversaries and the end-of-year team gift."),
             ("/pages/request-a-quote", "rows", "Events & trade fairs", "Single logo pralines for the stand, or small boxes for every seat."),
             ("/pages/request-a-quote", "gift-ribbon", "Campaigns", "Direct-mail boxes with a printed card and your campaign message.")]
    return '<div class="usecases">' + "".join(
        f'<a class="usecase" href="{u(h)}">{img(k, "")}<span><span class="h3">{t}</span><small>{d}</small></span></a>' for h, k, t, d in items) + "</div>"


def corp_formats():
    items = [("logo-box", "Logo pralines", "Your logo printed in cocoa butter on each piece. From 100 pieces, about three weeks after artwork approval.", "/pages/pralines-with-logo"),
             ("open-box", "Branded sleeve", "Our signature box in a printed sleeve in your colours.", "/products/corporate-24"),
             ("gift-ribbon", "Card & ribbon", "A printed card with your message and a ribbon in your brand colour.", "/pages/request-a-quote"),
             ("red-box", "Custom packaging", "Fully custom boxes for larger runs. We’ll talk you through lead times.", "/pages/request-a-quote")]
    return '<div class="formats">' + "".join(
        f'<a class="format" href="{u(h)}"><figure class="ph ph--round">{img(k, "")}</figure><h3 class="h3">{t}</h3><p class="small">{d}</p></a>' for k, t, d, h in items) + "</div>"


def corp_process():
    return steps([("Tell us the brief", "Quantity, date, budget per gift and where it’s going."),
                  ("Taste the sample", "We send a sample pack and a written quote within two working days."),
                  ("Approve the artwork", "Upload your logo and approve a digital proof before anything is made."),
                  ("We deliver", "To one address, or to each recipient with tracking for every parcel.")])


def corporate_gifting():
    return f'''{page_hero([("Corporate Gifts", None)], "Cadeaux d’entreprise", "Gifts your clients will open at their desk",
        "Belgian pralines in your colours, for 25 boxes or 2,500. Tell us what you need and we send a written quote and a sample pack, with no checkout or card details.",
        btn("Request a quote", "/pages/request-a-quote", "btn-light btn-full btn-lg", "data-quote") + btn("See corporate boxes", "/collections/corporate-gifts", "btn-light btn-lg"),
        "open-box", "An open box of pralines with tissue paper", "ganache", stamp_text="CADEAUX D’ENTREPRISE · PRALINE · ")}
{wave("var(--cream)", "var(--ganache)")}
<section class="section"><div class="wrap">{head_row("What it’s for", "Pick the occasion")}{corp_usecases()}</div></section>
<section class="section section--butter grain" id="formats"><div class="wrap">{head_row("Personalisation", "Four ways to make it yours")}{corp_formats()}</div></section>
<section class="section"><div class="wrap">{head_row("How it works", "From request to delivery")}{corp_process()}</div></section>
{marquee(["Logo pralines", "Branded sleeves", "Cards & ribbons", "Multi-address delivery", "Invoice payment"], "marquee--slim")}
<section class="section"><div class="wrap">{rail("corporate-gifts", "corp-rail", 8, "Taste before you order", "Corporate gift boxes", ("All corporate boxes", "/collections/corporate-gifts"))}</div></section>
<section class="section section--ganache on-dark"><div class="wrap quote-layout">
  <div><p class="script">Request a quote</p><h2 class="h2">Get a quote and a sample pack</h2><p class="lead">This doesn’t place an order or take payment. We reply by email within two working days.</p>
  {ticks(["Quotes from 25 boxes", "Logo pralines from 100 pieces", "Invoice payment for registered companies"])}
  <p class="small">Rather talk it through? Email <a href="mailto:corporate@example.com">corporate@example.com</a>.</p></div>
  {quote_form()}
</div></section>
{faq_section("Before you request a quote", ("Corporate",))}'''


def pralines_with_logo():
    specs = [("Minimum order", "100 pieces (MOQ placeholder, to confirm)"), ("Lead time", "About 3 weeks after artwork approval"),
             ("Print", "Cocoa butter transfer, one or two colours"), ("Chocolate", "Dark, milk or white shells"),
             ("Packaging", "Boxes of 4, 9, 16 or 24, or loose for events"), ("Artwork", "SVG, AI, EPS or PDF vector; 300 dpi PNG accepted")]
    rows = "".join(f"<tr><th scope='row'>{a}</th><td>{b}</td></tr>" for a, b in specs)
    return f'''{page_hero([("Corporate Gifts", "/pages/corporate-gifting"), ("Pralines with Logo", None)], "Pralines avec logo", "Your logo on every praline",
        "We print your logo in cocoa butter on the top of each praline, then pack them in boxes or loose for events. Start with a sample pack, then order by quote.",
        btn("Request a quote", "/pages/request-a-quote", "btn-full btn-lg", "data-quote") + btn("Order a sample pack", "/pages/request-a-quote#quote", "btn-lg"),
        "logo-box", "Square pralines stamped with a rose pattern", stamp_text="VOTRE LOGO · EN BEURRE DE CACAO · ")}
{wave("var(--cream)", "var(--butter)")}
<section class="section"><div class="wrap split-2">
  <div><p class="script">The details</p><h2 class="h2">What you can order</h2>
    <div class="table-wrap"><table class="table spec">{rows}</table></div>
    <p class="small muted" style="margin-top:1rem">MOQ and lead times are placeholders until the corporate trading rules are signed off.</p></div>
  <div class="sample-card">
    {img("premium-box", "A box of pralines with printed tops")}
    <div><span class="badge badge--quote">Sample pack</span><h3 class="h3">Taste and see the print first</h3>
    <p>Nine pralines with a test print of your logo, sent with your written quote. Credited against your first order.</p>
    {btn("Ask for a sample pack", "/pages/request-a-quote", "btn-full")}</div>
  </div>
</div></section>
<section class="section section--butter grain"><div class="wrap">{head_row("How it works", "From logo to praline")}
  {steps([("Send your logo", "Upload a vector file with your quote request."), ("Approve a proof", "We send a digital proof showing size and colour on the praline."), ("Taste the sample", "A sample pack with a test print, sent before production."), ("We make and deliver", "Printed, filled and packed in about three weeks.")])}
</div></section>
<section class="section"><div class="wrap quote-layout">
  <div>{figure("cut", "Pralines cut in half showing the filling", "arch")}</div>
  {quote_form("Quote for logo pralines")}
</div></section>
{faq_section("Logo praline questions", ("Corporate",), "section--butter")}'''


def corp_usecase_page(kind):
    data = {
        "client": dict(t="Client gifts", s="Pour vos clients", h="Thank clients with something they’ll remember",
                       lead="Year-end gifts, deal-closing thank-yous and anniversaries. We ship to each client’s address with your card inside.",
                       img="premium-box", points=[("gift", "One box, many addresses", "Send us a list and we post each box separately with tracking."), ("mail", "Your message, printed", "A card in your brand colours with a personal note for each client."), ("calendar", "Arrives on the day", "Choose the delivery date, so it lands before the holidays, not after.")]),
        "employee": dict(t="Employee gifts", s="Pour vos équipes", h="Team gifts that feel personal",
                         lead="Welcome boxes, work anniversaries and the end-of-year gift. Vegan and alcohol-free options for every team.",
                         img="gift-small", points=[("leaf", "For every diet", "Vegan and alcohol-free boxes in the same formats, so nobody gets a lesser gift."), ("box", "Office or home", "Bulk delivery to the office, or to each employee’s home."), ("hand", "Simple for HR", "One quote, one invoice, one contact person.")]),
    }[kind]
    tiles_html = tiles([(i, t, x) for i, t, x in data["points"]])
    return f'''{page_hero([("Corporate Gifts", "/pages/corporate-gifting"), (data["t"], None)], data["s"], data["h"], data["lead"],
        btn("Request a quote", "/pages/request-a-quote", "btn-full btn-lg", "data-quote") + btn("See corporate boxes", "/collections/corporate-gifts", "btn-lg"),
        data["img"], "")}
{wave("var(--cream)", "var(--butter)")}
<section class="section"><div class="wrap">{head_row("Why companies choose us", "Less admin, better gifts")}{tiles_html}</div></section>
<section class="section section--butter grain"><div class="wrap">{rail("corporate-gifts", "corp-rail", 8, "Popular choices", "Corporate gift boxes", ("All corporate boxes", "/collections/corporate-gifts"))}</div></section>
<section class="section"><div class="wrap">{head_row("Personalisation", "Make it yours")}{corp_formats()}</div></section>
<section class="section section--ganache on-dark"><div class="wrap quote-layout">
  <div><p class="script">Request a quote</p><h2 class="h2">Tell us about your {data["t"].lower()}</h2><p class="lead">We reply within two working days with a written quote and a sample pack.</p>{figure("rows", "", "round")}</div>
  {quote_form("Quote for " + data["t"].lower(), "Client gifts" if kind == "client" else "Employee gifts")}
</div></section>'''


def request_a_quote():
    return f'''<section class="page-hero page-hero--butter grain compact"><div class="wrap">
  {crumbs([("Corporate Gifts", "/pages/corporate-gifting"), ("Request a Quote", None)])}
  <p class="script">Demande de devis</p><h1 class="h1">Request a quote</h1>
  <p class="lead">Tell us the quantity, date and budget. We reply within two working days with a written quote and, if you like, a sample pack. Nothing is charged.</p>
</div></section>
{wave("var(--cream)", "var(--butter)")}
<section class="section" style="padding-top:2rem"><div class="wrap quote-layout">
  <div>
    {figure("premium-box", "A box of pralines", "arch", extra=stamp("DEVIS · ÉCHANTILLON · PRALINE · ", "right:-24px;bottom:10%"))}
    <h2 class="h3" style="margin-top:2rem">What happens next</h2>
    {corp_process()}
  </div>
  {quote_form("Tell us about your order")}
</div></section>
{faq_section("Before you send it", ("Corporate",), "section--butter")}'''


def upload_your_logo():
    specs = [("Best", "SVG, AI, EPS or PDF (vector)"), ("Accepted", "PNG at 300 dpi, at least 1000 px wide"), ("Size limit", "10 MB per file"),
             ("Colours", "One or two solid colours print best"), ("Not suitable", "Photos, gradients, very thin lines under 0.3 mm")]
    rows = "".join(f"<tr><th scope='row'>{a}</th><td>{b}</td></tr>" for a, b in specs)
    return f'''<section class="page-hero page-hero--butter grain compact"><div class="wrap">
  {crumbs([("Corporate Gifts", "/pages/corporate-gifting"), ("Upload Your Logo", None)])}
  <p class="script">Votre logo</p><h1 class="h1">Upload your logo</h1>
  <p class="lead">Already have a quote? Send your artwork here. We check it, send a digital proof, and print nothing until you approve it.</p>
</div></section>
{wave("var(--cream)", "var(--butter)")}
<section class="section" style="padding-top:2rem"><div class="wrap quote-layout">
  <div>
    <h2 class="h3">File guidelines</h2>
    <div class="table-wrap"><table class="table spec">{rows}</table></div>
    {figure("logo-box", "Pralines with a printed pattern", "round")}
  </div>
  <div class="quote-card">
    <form class="quote-form" data-upload-form novalidate>
      <p class="script">Artwork</p><h2 class="h3" style="margin-bottom:1.25rem">Send your artwork</h2>
      <div class="form-grid">
        <div class="field"><label for="u-name">Your name</label><input class="input" id="u-name" required autocomplete="name"><span class="err">Enter your name.</span></div>
        <div class="field"><label for="u-email">Work email</label><input class="input" id="u-email" type="email" required autocomplete="email"><span class="err">Enter an email address like name@company.com.</span></div>
        <div class="field"><label for="u-company">Company</label><input class="input" id="u-company" required autocomplete="organization"><span class="err">Enter your company name.</span></div>
        <div class="field"><label for="u-ref">Quote reference <span class="muted">(optional)</span></label><input class="input" id="u-ref" placeholder="e.g. Q-2026-104"></div>
        <div class="field full">
          <span class="label" id="u-logo-label">Logo file</span>
          <label class="dropzone" data-dropzone for="u-file" aria-labelledby="u-logo-label">
            <input type="file" id="u-file" accept=".svg,.ai,.eps,.pdf,.png" required>
            <span class="dz-ico">{ICON["upload"]}</span><b>Drop a file or browse</b><br><span class="small muted">SVG, AI, EPS, PDF or 300 dpi PNG, up to 10 MB.</span>
          </label>
          <span class="file-name small" aria-live="polite"></span><span class="err">Attach your logo file.</span>
        </div>
        <div class="field"><label for="u-colours">Print colours</label><select class="input" id="u-colours"><option>As in the file</option><option>One colour: white</option><option>One colour: gold-coloured</option><option>Two colours</option></select></div>
        <div class="field"><label for="u-shell">Shell</label><select class="input" id="u-shell"><option>Dark</option><option>Milk</option><option>White</option><option>Mixed</option></select></div>
        <div class="field full"><label for="u-notes">Notes for our designer</label><textarea class="input" id="u-notes" placeholder="Pantone references, placement, anything we should know"></textarea></div>
        <div class="field full"><label class="check"><input type="checkbox" id="u-ok" required> <span>I have the right to use this logo and understand that production starts only after I approve a proof.</span></label><span class="err">Confirm before sending.</span></div>
      </div>
      <button class="btn btn-full btn-lg btn-block" type="submit">Send artwork</button>
    </form>
    <div class="success" tabindex="-1"><p class="script">Merci!</p><h2 class="h2">Artwork received</h2><p>We’ll check the file and email you a digital proof within two working days.</p>{btn("Back to corporate gifting", "/pages/corporate-gifting", "btn-full")}</div>
  </div>
</div></section>'''


# =====================================================================
# Editorial trust pages
# =====================================================================
def belgian_pralines():
    return f'''{page_hero([("Our Chocolate", None), ("Belgian Pralines", None)], "Pralines belges", "What makes a praline Belgian",
        "In Belgium, a praline is any filled chocolate: a thin shell of couverture around a soft centre. Here’s how ours are made, and why they keep for weeks rather than months.",
        btn("Shop pralines & truffles", "/collections/pralines-and-truffles"), "rows", "Rows of pralines on a production table", stamp_text="BRUXELLES · PRALINES · BELGES · ")}
{wave("var(--cream)", "var(--butter)")}
<section class="section"><div class="wrap narrow prose">
  <p class="dropcap">The word comes from praliné, the paste of caramelised roasted nuts at the heart of the most traditional pieces. Belgian chocolatiers took the name and gave it to the whole category: anything with a shell and a filling became a praline. A ballotin, the folded paper box sold by weight at the counter, is how most Belgians still buy them.</p>
</div></section>
<section class="section section--butter grain">{split("hazel-shells", "Cracked hazelnut shells and whole hazelnuts", f'<p class="script">Le praliné</p><h2 class="h2">It starts with roasted nuts</h2><p>We roast hazelnuts and almonds in small batches, caramelise them with sugar and grind them slowly until smooth. A coarser grind gives crunch; a longer one gives the silky praliné in our noisette box.</p>{btn("Shop the noisette box", "/products/noisette-praline-box", "btn")}', frame="round")}</section>
<section class="section">{split("mixing", "Melted chocolate being mixed in a glass bowl", f'<p class="script">La couverture</p><h2 class="h2">Tempered by hand</h2><p>Couverture is chocolate with a high share of cocoa butter. Tempering it, heating and cooling to exactly 31 °C for dark, sets the crystals that give a clean snap and a glossy shell.</p>', flip=True, frame="arch")}</section>
<section class="section section--butter grain">{split("cut", "Pralines cut in half to show the filling", f'<p class="script">Le fourrage</p><h2 class="h2">Fresh fillings, short shelf life</h2><p>Our ganaches use fresh cream and butter, which is why a box keeps four to six weeks, not a year. It’s also why we pack to order and ship cool.</p>{btn("How to store pralines", "/blogs/stories/how-to-store-pralines", "btn")}', frame="round")}</section>
<section class="section"><div class="wrap">{head_row("The classics", "Pieces you’ll find in every Belgian shop")}
  {tiles([(None, "Praliné", "Roasted nut paste, smooth or crunchy, in milk or dark."), (None, "Gianduja", "Hazelnut paste blended with milk chocolate."), (None, "Crème au beurre", "Butter cream flavoured with vanilla, coffee or praliné."), (None, "Massepain", "Almond marzipan, often with a cherry or pistachio."), (None, "Truffe", "Fresh cream ganache rolled in cocoa."), (None, "Manon", "White chocolate around butter cream and a walnut.")])}
</div></section>
<section class="section section--butter"><div class="wrap">{rail("belgian-classics", "classics-rail", 8, "Taste the classics", "Belgian classics", ("Shop all classics", "/collections/belgian-classics"))}</div></section>'''


def ingredients():
    return f'''{page_hero([("Our Chocolate", "/pages/belgian-pralines"), ("Ingredients", None)], "Ingrédients & transparence", "What goes into every box",
        "Every product page lists its full ingredients, in order of quantity, and its allergens next to the add-to-cart button. Here’s what we use and why.",
        btn("Allergen guide", "/pages/allergens", "btn-full btn-lg"), "hazelnuts", "A pile of roasted hazelnuts", stamp_text="INGRÉDIENTS · TRANSPARENCE · ")}
{wave("var(--cream)", "var(--butter)")}
<section class="section"><div class="wrap">{head_row("Our pantry", "Short lists, real ingredients")}
  <div class="ingredients">
    {"".join(f'<div class="ingredient"><figure class="ph ph--circle">{img(k, "")}</figure><h3 class="h3">{t}</h3><p>{d}</p></div>' for k, t, d in [
        ("cocoa-hands", "Belgian couverture", "Cocoa mass, cocoa butter and sugar. No vegetable fats, ever."),
        ("hazel-white", "Nuts roasted in-house", "Hazelnuts and almonds roasted in small batches for praliné."),
        ("cream-pour", "Fresh cream & butter", "For ganaches and butter creams. The reason for our shorter shelf life."),
        ("raspberry", "Real fruit", "Fruit purées and freeze-dried fruit, not flavourings."),
    ])}
  </div>
</div></section>
<section class="section section--butter grain"><div class="wrap split-2">
  <div><p class="script">What we leave out</p><h2 class="h2">Not in our chocolate</h2>
    {ticks(["Vegetable fats in the couverture", "Artificial flavours: we use vanilla pods, spices and fruit", "Preservatives: freshness comes from small batches and cool storage", "Palm oil in fillings"])}
    <p class="small muted">Claims on this page apply to the whole range. Product-level claims like vegan appear as badges only where they apply.</p></div>
  <div><p class="script">Reading a label</p><h2 class="h2">How we list ingredients</h2>
    <p>Ingredients appear in order of weight, with allergens named in the allergen line. "May contain" warnings cover traces from shared equipment in our atelier.</p>
    {btn("See the allergen guide", "/pages/allergens", "btn")}</div>
</div></section>
<section class="section"><div class="wrap">{rail("all", "ing-rail", 8, "Check any product", "Full ingredients on every page", ("All chocolates", "/collections/all"))}</div></section>'''


def organic_and_fairtrade():
    return f'''{page_hero([("Vegan & Conscious", "/collections/vegan-chocolates"), ("Organic & Fairtrade", None)], "Preuves & certificats", "Organic and Fairtrade, only with proof",
        "We’d rather say less and be sure of it. This page explains when we use these words, and what we can show you today.",
        "", "cocoa-pods", "Cocoa pods growing on a tree", "pistachio")}
{wave("var(--cream)", "#DCE8DA")}
<section class="section"><div class="wrap narrow">
  <div class="notice">{icon("shield")}<div><h2 class="h3">Current status: no certified products</h2><p>None of our current products carries an organic or Fairtrade certificate. Until one does, our <a class="link" href="{u("/collections/organic-chocolate")}">organic</a> and <a class="link" href="{u("/collections/fairtrade-chocolate")}">Fairtrade</a> collections stay empty and out of search results.</p></div></div>
  <div class="prose" style="margin-top:2.5rem">
    <h2 class="h3">Our rules for claims</h2>
    {ticks(["A claim appears on a product only when we hold the certificate for that exact product.", "Certificates are kept on file and checked before every new batch.", "We don’t use vague words like 'ethical' or 'sustainable' as product badges.", "If a supplier certificate lapses, the badge comes off the same day."])}
  </div>
</div></section>
<section class="section section--butter grain">{split("cocoa-hands", "Hands holding cocoa beans", f'<p class="script">Where we are going</p><h2 class="h2">Tracing our cocoa</h2><p>We buy couverture from Belgian makers who publish the origin of their beans. Read what we do today, and what we don’t claim yet, on our sustainability page.</p>{btn("Sustainability", "/pages/sustainability", "btn")}', frame="arch")}</section>'''


def about():
    return f'''{page_hero([("About", None), ("Our Story", None)], "Notre histoire", "A small atelier with a long counter",
        "We make Belgian pralines in small batches in Brussels: shells cast by hand, fillings made in-house, every box packed to order.",
        btn("Shop our bestsellers", "/collections/all") + btn("Visit the atelier", "/pages/contact", "btn-lg"), "grand-place", "The Grand-Place in Brussels", stamp_text="PRALINE · BRUXELLES · ATELIER · ")}
{wave("var(--cream)", "var(--butter)")}
<section class="section"><div class="wrap narrow prose center">
  <p class="script">Why Praline</p>
  <p class="big-quote">We named the shop after the thing we love most: a thin shell, a soft centre, and a box you want to keep.</p>
</div></section>
<section class="section section--butter grain">{split("mixing", "Chocolate being mixed by hand", f'<p class="script">Le métier</p><h2 class="h2">Made by hand, tasted every batch</h2><p>Our chocolatiers temper, cast and fill every praline in our Brussels workshop. Batches are small enough that we taste each one before it’s boxed.</p>{ticks(["Fillings made in-house, from roasted nuts to fresh cream", "Boxed to order, never warehoused for months", "Packed to travel cool"])}', frame="arch")}</section>
<section class="section">{split("brussels-street", "A cobbled shopping street in Brussels", f'<p class="script">Notre quartier</p><h2 class="h2">A Brussels counter</h2><p>Come by the atelier to taste before you choose, collect an order or build a ballotin at the counter.</p>{btn("Opening hours & contact", "/pages/contact", "btn")}', flip=True, frame="round")}</section>
<section class="section section--butter"><div class="wrap">
  {head_row("What we care about", "Our promises")}
  {tiles([("hand", "Made by hand", "Every praline is cast, filled and finished in our atelier."), ("info", "Honest labels", "Full ingredients and allergens on every product, next to the buy button."), ("snow", "Packed to arrive right", "Insulated packaging and a replacement if anything goes wrong."), ("leaf", "Claims with proof", "We only say organic, Fairtrade or vegan when we can show it.")])}
</div></section>
{newsletter_band("gift-roses")}'''


def sustainability():
    return f'''{page_hero([("About", "/pages/about"), ("Sustainability", None)], "Durabilité", "What we do, and what we don’t claim",
        "We’d rather tell you less and be sure of it. Here’s what we can show today, and what we’re still working on.",
        "", "cocoa-tree", "Cocoa pods on a tree", "pistachio")}
{wave("var(--cream)", "#DCE8DA")}
<section class="section"><div class="wrap">
  {head_row("Today", "What we can show you")}
  {tiles([("box", "Paper-based packaging", "Boxes, ballotins and fillers are paper-based and recyclable."), ("snow", "Reusable cool packs", "Cool packs can be reused, or returned at the atelier."), ("pin", "Short routes", "Everything ships from one atelier in Brussels."), ("leaf", "No palm oil in fillings", "Our fillings use cocoa butter, cream and butter.")])}
</div></section>
<section class="section section--butter grain">{split("cocoa-pods", "Ripe cocoa pods", f'<p class="script">In progress</p><h2 class="h2">Cocoa sourcing</h2><p>We buy Belgian couverture from makers who publish bean origins. We don’t yet hold organic or Fairtrade certificates for any product, so we don’t use those words.</p>{btn("How we handle claims", "/pages/organic-and-fairtrade", "btn")}', frame="round")}</section>
<section class="section"><div class="wrap narrow"><p class="small muted center">Every claim on this page needs supplier proof on file before launch (Open Decision #4).</p></div></section>'''


def allergens():
    rows = [("Milk", "Milk and white chocolate, ganaches, butter creams, caramels, truffles", "Vegan range, Noir 72% and 85% tablets"),
            ("Hazelnut", "Pralinés, gianduja, rochers, signature and noisette boxes", "Noir ganache collection, truffles"),
            ("Almond", "Marzipan, ballotin, grand coffret, rochers, mendiants", "Most boxes"),
            ("Pistachio", "Grand coffret, mendiants", "Most boxes"),
            ("Gluten", "Feuilletine crunch, speculoos, oat-milk pieces", "Most boxes"),
            ("Soy", "Some fillings in the ballotin and seasonal box", "Most boxes"),
            ("Coconut", "Hazelnut rochers, vegan ganache", "Most boxes")]
    table = "".join(f"<tr><th scope='row'>{a}</th><td>{b}</td><td>{c}</td></tr>" for a, b, c in rows)
    return f'''{page_hero([("Our Chocolate", "/pages/belgian-pralines"), ("Allergens", None)], "Allergènes", "Allergens, in plain words",
        "Each product page shows its allergens next to the add-to-cart button, not hidden in a tab. This page gives the overview.",
        "", "cut", "Pralines cut in half showing their fillings")}
{wave("var(--cream)", "var(--butter)")}
<section class="section"><div class="wrap">
  <div class="notice">{icon("info")}<div><h2 class="h3">Shared atelier</h2><p>We handle milk, hazelnuts, almonds, pistachios, soy, gluten, coconut and eggs. Traces are possible in every product, including our vegan range.</p></div></div>
  <div class="table-wrap" style="margin-top:2rem"><table class="table"><thead><tr><th>Allergen</th><th>Where you’ll find it</th><th>Free from it (recipe)</th></tr></thead><tbody>{table}</tbody></table></div>
</div></section>
<section class="section section--butter">{split("assorted-beige", "Assorted pralines", f'<p class="script">Alcohol</p><h2 class="h2">Alcohol-free boxes</h2><p>Only the heritage ballotin contains liqueur pieces, and its product page says so next to the add-to-cart button. Everything else is alcohol-free.</p>{btn("Shop no alcohol chocolates", "/collections/no-alcohol-chocolates", "btn")}', frame="round")}</section>
<section class="section"><div class="wrap narrow">{faq(faq_items("Allergens", "Vegan & dietary"))}</div></section>'''


# =====================================================================
# Service pages
# =====================================================================
def shipping():
    rows = [("Belgium", "Standard", "1–2 working days after dispatch", "€6.90, free from €60"), ("Belgium", "Express", "Next working day", "€12.90"),
            ("Netherlands, Luxembourg", "Standard", "2–3 working days", "€9.90"), ("France, Germany", "Standard", "2–4 working days", "€12.90"),
            ("Brussels atelier", "Click & collect", "Same day if ordered by 12:00", "Free")]
    table = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in rows)
    return f'''{page_hero([("Delivery", None), ("Shipping Information", None)], "Livraison", "Shipping & delivery",
        "Chocolate is happiest between 15 and 18 °C. Here’s how we keep it there on the way to you.",
        btn("Delivery calendar", "/pages/delivery-calendar", "btn-full btn-lg") + btn("Warm-weather shipping", "/pages/warm-weather-shipping", "btn-lg"),
        "delivery-hands", "A parcel being handed over", stamp_text="LIVRAISON · AU FRAIS · PRALINE · ")}
{wave("var(--cream)", "var(--butter)")}
<section class="section"><div class="wrap">
  {head_row("Where and how fast", "Delivery times", '<span class="placeholder-note">Rates are placeholders until Gate 2</span>')}
  <div class="table-wrap"><table class="table"><thead><tr><th>Destination</th><th>Service</th><th>Usually arrives</th><th>Price</th></tr></thead><tbody>{table}</tbody></table></div>
  <p class="small muted" style="margin-top:1rem">Orders placed before 14:00 on a working day are dispatched the next working day.</p>
</div></section>
<section class="section section--butter grain"><div class="wrap">{head_row("Every order", "How we pack")}
  {steps([("Boxed to order", "Your pralines are boxed the day they ship, never weeks before."), ("Insulated liner", "A recyclable liner keeps the temperature stable."), ("Cool pack if needed", "Added automatically in warm months, at no charge."), ("Tracked", "You get a tracking link the moment it leaves.")])}
</div></section>
<section class="section"><div class="wrap">{tiles([("calendar", "Delivery calendar", f'Holiday cut-offs and a date picker. <a class="link" href="{u("/pages/delivery-calendar")}">See the calendar</a>'), ("thermo", "Warm weather", f'What happens above 25 °C. <a class="link" href="{u("/pages/warm-weather-shipping")}">Read the policy</a>'), ("shield", "Quality guarantee", f'Melted or damaged? We replace it. <a class="link" href="{u("/pages/returns-and-quality-guarantee")}">How it works</a>')])}</div></section>
{faq_section("Delivery questions", ("Shipping",), "section--butter")}'''


def delivery_calendar():
    return f'''{page_hero([("Delivery", "/pages/shipping-and-delivery"), ("Delivery Calendar", None)], "Calendrier", "Delivery calendar",
        "See when we dispatch, the cut-offs for the big gifting dates and the days we don’t ship. Choose a delivery date in the cart.",
        "", "gift-ribbon", "A gift box tied with gold ribbon")}
{wave("var(--cream)", "var(--butter)")}
<section class="section"><div class="wrap">
  {head_row("Next two months", "Dispatch days", '<span class="placeholder-note">Blackout dates are placeholders</span>')}
  <div class="cal-legend"><span><i class="d-ship"></i>Dispatch day</span><span><i class="d-off"></i>No dispatch</span><span><i class="d-cut"></i>Gifting cut-off</span><span><i class="d-today"></i>Today</span></div>
  <div class="calendar" id="calendar"></div>
</div></section>
<section class="section section--butter grain"><div class="wrap">{head_row("Plan ahead", "Gifting cut-offs")}
  <div class="tiles">
    <div class="tile">{icon("gift")}<h3 class="h3">Valentine’s Day</h3><p>Order by 10 February for delivery in Belgium.</p></div>
    <div class="tile">{icon("calendar")}<h3 class="h3">Easter</h3><p>Order by the Tuesday before Easter Sunday.</p></div>
    <div class="tile">{icon("snow")}<h3 class="h3">Christmas</h3><p>Order by 18 December. Corporate orders by 1 December.</p></div>
    <div class="tile tile--pending">{icon("clock")}<h3 class="h3">Any other day</h3><p>Pick a date in the cart and we’ll plan dispatch around it.</p></div>
  </div></div></section>'''


def warm_weather():
    return f'''{page_hero([("Delivery", "/pages/shipping-and-delivery"), ("Warm Weather Shipping", None)], "Quand il fait chaud", "Warm-weather chocolate delivery",
        "From June to September, or whenever a heatwave is forecast, we change how we pack and when we ship. Here’s exactly what happens.",
        "", "melt-dark", "Swirls of melted chocolate", "ganache")}
{wave("var(--cream)", "var(--ganache)")}
<section class="section"><div class="wrap">
  <div class="temp-scale" aria-label="Temperature guide">
    <div style="--c:#93B79B"><b>15–18 °C</b><span>Ideal storage</span></div>
    <div style="--c:#D7A46B"><b>18–25 °C</b><span>Ships with a cool pack</span></div>
    <div style="--c:#B5474A"><b>Above 25 °C</b><span>We hold your order</span></div>
  </div>
  <p class="center small muted" style="margin-top:.75rem"><span class="placeholder-note">Heat threshold and cool-pack rules are placeholders (Open Decision #8)</span></p>
</div></section>
<section class="section section--butter grain">{split("boxes", "Cardboard shipping boxes", f'''<p class="script">Our rules</p><h2 class="h2">What we do in heat</h2>
  {ticks(["Every order travels in an insulated liner. Cool packs are added in warm months at no charge.", "If the forecast on the route is above 25 °C, we hold your order and email you the new dispatch date.", "We don’t dispatch on Fridays in summer, so no box waits in a depot over the weekend.", "Fresh truffles may be paused during heatwaves."])}''', frame="round")}</section>
<section class="section"><div class="wrap">{head_row("When it arrives", "Four tips")}
  {steps([("Bring it inside", "Don’t leave the parcel in a car or a sunny porch."), ("Let it rest", "If it feels warm, leave it closed somewhere cool for an hour."), ("Skip the fridge", "Condensation leaves a white bloom on the shell."), ("Tell us", "Melted anyway? Send a photo and we replace it.")])}
</div></section>
{faq_section("Heat questions", ("Shipping",), "section--butter")}'''


def returns():
    return f'''{page_hero([("Delivery", "/pages/shipping-and-delivery"), ("Returns & Quality Guarantee", None)], "Garantie qualité", "Returns & quality guarantee",
        "Chocolate can’t be returned once it has left us, but if your box arrives melted, broken or late because of us, we’ll make it right.",
        "", "open-box", "An open box of pralines")}
{wave("var(--cream)", "var(--butter)")}
<section class="section"><div class="wrap">{head_row("If something went wrong", "Three steps")}
  {steps([("Take a photo", "Of the box and the pralines, within 48 hours of delivery."), ("Email us", "Send it to hello@example.com with your order number."), ("Choose", "A replacement or a full refund, whichever you prefer.")])}
</div></section>
<section class="section section--butter grain"><div class="wrap split-2">
  <div><p class="script">Covered</p><h2 class="h2">What the guarantee covers</h2>{ticks(["Melted or bloomed chocolate on arrival", "Broken pieces or a damaged box", "Late delivery against the date you chose, caused by us", "Wrong items"])}</div>
  <div><p class="script">Not covered</p><h2 class="h2">What it doesn’t</h2>{ticks(["Change of mind after dispatch (it’s fresh food)", "Parcels left in heat after delivery", "Wrong address entered at checkout"])}
  <p class="small">The Shopify <a class="link" href="{u("/policies/refund-policy")}">refund policy</a> says the same thing in legal language.</p></div>
</div></section>'''


def contact():
    return f'''{page_hero([("About", "/pages/about"), ("Contact", None)], "Contact", "Write to us, or come by",
        "Order questions, allergies or a gift that needs to arrive on a certain day: we reply within one working day.",
        "", "brussels-street", "A Brussels street")}
{wave("var(--cream)", "var(--butter)")}
<section class="section"><div class="wrap quote-layout">
  <div class="contact-cards">
    <div class="tile">{icon("mail")}<h3 class="h3">Email</h3><p><a class="link" href="mailto:hello@example.com">hello@example.com</a><br>Corporate: <a class="link" href="mailto:corporate@example.com">corporate@example.com</a></p></div>
    <div class="tile">{icon("pin")}<h3 class="h3">Atelier & click and collect</h3><p>Address to be confirmed<br>Brussels, Belgium</p></div>
    <div class="tile">{icon("clock")}<h3 class="h3">Opening hours</h3><p>Tuesday–Saturday, 10:00–18:00<br>Sunday & Monday closed</p></div>
  </div>
  <div class="quote-card">
    <form id="contact-form" data-success="Message sent. We reply within one working day." data-event="contact_submitted" novalidate>
      <p class="script">Message</p><h2 class="h3" style="margin-bottom:1.25rem">Send us a message</h2>
      <div class="form-grid">
        <div class="field"><label for="c-name">Name</label><input class="input" id="c-name" required autocomplete="name"><span class="err">Enter your name.</span></div>
        <div class="field"><label for="c-email">Email</label><input class="input" id="c-email" type="email" required autocomplete="email"><span class="err">Enter an email address like name@example.com.</span></div>
        <div class="field"><label for="c-topic">Topic</label><select class="input" id="c-topic"><option>An order</option><option>Allergies & ingredients</option><option>Corporate gifts</option><option>Something else</option></select></div>
        <div class="field"><label for="c-order">Order number <span class="muted">(optional)</span></label><input class="input" id="c-order"></div>
        <div class="field full"><label for="c-msg">Message</label><textarea class="input" id="c-msg" required></textarea><span class="err">Write a short message.</span></div>
      </div>
      <button class="btn btn-full btn-block" type="submit">Send message</button>
    </form>
  </div>
</div></section>
{faq_section("Quick answers", ("Shipping", "Gifting"), "section--butter")}'''


def faq_page():
    groups = list(FAQ.keys())
    nav = "".join(f'<a class="chip" href="#{g.lower().replace(" & ", "-").replace(" ", "-")}">{g}</a>' for g in groups)
    body = "".join(f'<section class="faq-group" id="{g.lower().replace(" & ", "-").replace(" ", "-")}"><h2 class="h2">{g}</h2>{faq(faq_items(g))}</section>' for g in groups)
    return f'''<section class="page-hero page-hero--butter grain compact"><div class="wrap">
  {crumbs([("Delivery", "/pages/shipping-and-delivery"), ("FAQ", None)])}
  <p class="script">Questions fréquentes</p><h1 class="h1">FAQ</h1>
  <p class="lead">Shipping, gifting, vegan, allergens and corporate orders. Can’t find it? <a class="link" href="{u("/pages/contact")}">Write to us</a>.</p>
  <div class="chips">{nav}</div>
</div></section>
{wave("var(--cream)", "var(--butter)")}
<div class="wrap narrow faq-page">{body}</div>'''


# =====================================================================
# Blog
# =====================================================================
def stories():
    return f'''<section class="page-hero page-hero--butter grain compact"><div class="wrap">
  {crumbs([("Our Chocolate", "/pages/belgian-pralines"), ("Stories", None)])}
  <p class="script">Le journal</p><h1 class="h1">Stories</h1>
  <p class="lead">Notes from the atelier: how we make things, how to look after them, and what’s coming next.</p>
</div></section>
{wave("var(--cream)", "var(--butter)")}
<section class="section" style="padding-top:2rem"><div class="wrap">
  <a class="feature-post" href="{u("/blogs/stories/how-to-store-pralines")}">
    <figure class="ph ph--round">{img("cream-pour", "Cream being poured into melted chocolate")}</figure>
    <div><span class="tag">Product care · 4 min read</span><h2 class="h2">How to store pralines</h2><p class="lead">Cool, dark and not in the fridge. Everything you need to keep a box at its best, from the day it arrives to the last piece.</p><span class="btn btn-full">Read the story</span></div>
  </a>
</div></section>
<section class="section section--butter grain"><div class="wrap">{head_row("More reading", "From our chocolate pages")}{journal_cards()}</div></section>'''


def article_store():
    return f'''<article>
<header class="article-head"><div class="wrap narrow center">
  {crumbs([("Stories", "/blogs/stories"), ("How to store pralines", None)])}
  <span class="tag">Product care · 4 min read</span>
  <h1 class="h1">How to store pralines</h1>
  <p class="lead" style="margin-inline:auto">Cool, dark and not in the fridge. Here’s how to keep a box at its best, from the day it arrives to the last piece.</p>
</div></header>
<div class="wrap"><figure class="ph ph--round article-hero">{img("truffle-bowl", "Chocolate truffles in a small bowl")}</figure></div>
<div class="wrap narrow prose">
  <p class="dropcap">Fresh pralines are closer to pastry than to a candy bar. Their fillings use cream, butter and roasted nuts, so they keep for weeks rather than months, and they react to heat, light, moisture and smells.</p>
  <h2 class="h3">The short version</h2>
  {ticks(["Keep them between 15 and 18 °C.", "Keep them out of direct sunlight.", "Keep the lid on and away from strong smells.", "Eat within the shelf life on the box, usually 4–6 weeks."])}
  <h2 class="h3">Why not the fridge?</h2>
  <p>A fridge is too cold and too humid. When you take a praline out, moisture condenses on the shell and dissolves a little sugar. As it dries, the sugar crystallises into a dull white film called sugar bloom. It’s safe to eat, but it changes the texture.</p>
  <figure class="ph ph--round inline-fig">{img("melt", "Smooth swirls of milk chocolate")}<figcaption>Tempered chocolate keeps its gloss only between about 15 and 18 °C.</figcaption></figure>
  <h2 class="h3">If you must chill them</h2>
  <p>In a heatwave, the fridge is better than a melted box. Seal the box in an airtight bag, put it in the warmest part of the fridge, and let it come back to room temperature for an hour before opening the bag.</p>
  <h2 class="h3">Fresh truffles are different</h2>
  <p>Our <a class="link" href="{u("/products/truffle-box")}">cocoa-dusted truffles</a> have a higher share of fresh cream. Keep them a little cooler, at 12–16 °C, and eat them within three weeks.</p>
  <blockquote class="pull">Take pralines out of their box 15 minutes before serving. The flavour opens up as they warm slightly.</blockquote>
  <h2 class="h3">Freezing</h2>
  <p>We don’t recommend it. If you do, wrap the box tightly, freeze for no more than a month, then thaw slowly: a day in the fridge, then a few hours at room temperature, all without opening the bag.</p>
</div>
</article>
<section class="section section--butter"><div class="wrap">{rail("pralines-and-truffles", "article-rail", 8, "Fresh from the atelier", "Shop pralines", ("All pralines", "/collections/pralines-and-truffles"))}</div></section>'''


# =====================================================================
# Policies, custom, redirects, system pages
# =====================================================================
POLICY = {
    "privacy-policy": ("Privacy policy", [("What we collect", "Your name, contact details, delivery addresses, order history and, for corporate quotes, company details and uploaded artwork."), ("Why", "To process orders, deliver gifts, answer questions and, if you subscribe, send our newsletter."), ("Who we share it with", "Our payment provider, courier and email platform, only as needed to deliver the service."), ("Your rights", "You can ask to see, correct or delete your data at any time by writing to hello@example.com.")]),
    "terms-of-service": ("Terms of service", [("Orders", "An order is accepted when we send a confirmation email. Prices include Belgian VAT."), ("Delivery", "Delivery dates are estimates. In warm weather we may hold an order to protect it, as described on our warm-weather page."), ("Corporate orders", "Quotes are valid for 30 days. Production of logo pralines starts after written artwork approval."), ("Liability", "Our liability is limited to the value of the order.")]),
    "refund-policy": ("Refund policy", [("Fresh food", "Chocolate is a perishable product, so we can’t accept returns for change of mind once an order has been dispatched."), ("Quality guarantee", "If an order arrives melted, damaged, late through our fault or incorrect, contact us within 48 hours with a photo and we’ll replace or refund it."), ("How refunds are paid", "Refunds go back to the original payment method within 10 working days."), ("More detail", "See our Returns & quality guarantee page for the plain-language version.")]),
}


def policy(handle):
    title, sections = POLICY[handle]
    toc = "".join(f'<li><a href="#s{i}">{esc(t)}</a></li>' for i, (t, _) in enumerate(sections))
    body = "".join(f'<section id="s{i}"><h2 class="h3">{i + 1}. {esc(t)}</h2><p>{esc(x)}</p></section>' for i, (t, x) in enumerate(sections))
    return f'''<section class="page-hero page-hero--butter compact"><div class="wrap">
  {crumbs([(title, None)])}<p class="script">Informations légales</p><h1 class="h1">{esc(title)}</h1>
  <p class="lead">Last updated: placeholder date. <span class="placeholder-note">Template text, needs legal review</span></p>
</div></section>
{wave("var(--cream)", "var(--butter)")}
<div class="wrap policy"><nav class="policy-toc" aria-label="On this page"><p class="script">On this page</p><ol>{toc}</ol></nav><div class="prose">{body}
  {"<p>Read the plain-language <a class='link' href='" + u("/pages/returns-and-quality-guarantee") + "'>returns & quality guarantee</a>.</p>" if handle == "refund-policy" else ""}</div></div>'''


def build_a_ballotin():
    return f'''<section class="page-hero page-hero--butter grain compact"><div class="wrap">
  {crumbs([("Shop", "/collections/all"), ("Build a Ballotin", None)])}
  <p class="script">Composez votre ballotin</p><h1 class="h1">Build a ballotin</h1>
  <p class="lead">Choose a size, then pick every praline yourself, just like at the counter. <span class="placeholder-note">Feature scope pending Open Decision #2</span></p>
</div></section>
{wave("var(--cream)", "var(--butter)")}
<section class="section builder" style="padding-top:2rem"><div class="wrap builder-grid">
  <div>
    <h2 class="h3">1. Choose a size</h2>
    <div class="variant-pills" id="b-sizes" role="group" aria-label="Ballotin size"></div>
    <h2 class="h3" style="margin-top:1.5rem">2. Pick your pralines</h2>
    <div class="b-pieces" id="b-pieces"></div>
  </div>
  <aside class="b-box" aria-live="polite">
    <div class="b-ballotin">
      <svg viewBox="0 0 200 150" aria-hidden="true"><path d="M20 30h160l-12 112H32Z" fill="#F5E6CC" stroke="#B98458" stroke-width="3"/><path d="M20 30h160l-5 14H25Z" fill="#E7CFAE"/><rect x="20" y="88" width="160" height="14" fill="#7B4B2A"/><text x="100" y="72" text-anchor="middle" font-family="'Big Shoulders Display',sans-serif" font-weight="800" font-size="20" fill="#3D2617" letter-spacing="2">PRALINE</text></svg>
      <div class="b-fill" id="b-fill"></div>
    </div>
    <div class="b-summary" id="b-summary"></div>
    <button class="btn btn-full btn-lg btn-block" id="b-add" disabled>Add to cart</button>
    <button class="btn btn-block" id="b-surprise" style="margin-top:.5rem">Fill the rest for me</button>
  </aside>
</div></section>'''


def redirect(target):
    return f'''<section class="section"><div class="wrap narrow center">
  <p class="script">This page has moved</p><h1 class="h2">Taking you to the new page</h1>
  <p>If nothing happens, <a class="link" href="{u(target)}">continue here</a>.</p>
</div></section>'''


def search():
    return f'''<section class="page-hero page-hero--butter compact"><div class="wrap">
  {crumbs([("Search", None)])}<p class="script">Recherche</p><h1 class="h1" id="search-title">Search</h1>
  <form action="" role="search" class="search-big"><label class="sr-only" for="q2">Search</label><input class="input" id="q2" name="q" type="search" placeholder="Search pralines, boxes, flavours"><button class="btn btn-full" type="submit">Search</button></form>
</div></section>
{wave("var(--cream)", "var(--butter)")}
<div class="wrap" style="padding-block:2rem 4rem"><p id="search-count" class="muted"></p><div class="grid" id="search-grid"></div></div>'''


def checkout():
    return f'''<div class="wrap">
  <div style="margin-top:1.5rem">{crumbs([("Checkout", None)])}</div>
  <h1 class="h2">Checkout</h1>
  <p class="small muted">Demo checkout. On Shopify this page is the secure Shopify checkout.</p>
  <div class="checkout" id="checkout">
    <form id="co-form" novalidate>
      <h2>Contact</h2>
      <div class="field"><label for="co-email">Email</label><input class="input" id="co-email" type="email" required autocomplete="email"><span class="err">Enter an email address like name@example.com.</span></div>
      <h2>Deliver to</h2>
      <div class="form-grid">
        <div class="field"><label for="co-first">First name</label><input class="input" id="co-first" required autocomplete="given-name"><span class="err">Enter a first name.</span></div>
        <div class="field"><label for="co-last">Last name</label><input class="input" id="co-last" required autocomplete="family-name"><span class="err">Enter a last name.</span></div>
        <div class="field full"><label for="co-addr">Address</label><input class="input" id="co-addr" required autocomplete="street-address"><span class="err">Enter a street address.</span></div>
        <div class="field"><label for="co-zip">Postcode</label><input class="input" id="co-zip" required autocomplete="postal-code"><span class="err">Enter a postcode.</span></div>
        <div class="field"><label for="co-city">City</label><input class="input" id="co-city" required autocomplete="address-level2"><span class="err">Enter a city.</span></div>
        <div class="field full"><label for="co-country">Country</label><select class="input" id="co-country" autocomplete="country-name"><option>Belgium</option><option>Netherlands</option><option>Luxembourg</option><option>France</option><option>Germany</option></select></div>
      </div>
      <h2>Delivery</h2>
      <label class="ship-opt"><span><input type="radio" name="ship" value="standard" checked> <b>Standard</b><br><span class="small muted">1–2 working days in Belgium</span></span><span id="std-label"></span></label>
      <label class="ship-opt"><span><input type="radio" name="ship" value="express"> <b>Express</b><br><span class="small muted">Next working day, best in warm weather</span></span><span id="exp-label"></span></label>
      <label class="ship-opt"><span><input type="radio" name="ship" value="pickup"> <b>Click & collect at the atelier</b><br><span class="small muted">Brussels, Tuesday–Saturday</span></span><span>Free</span></label>
      <div class="form-grid" style="margin-top:1rem"><div class="field"><label for="co-date">Preferred delivery date</label><input class="input" id="co-date" type="date"></div></div>
      <h2>Gift</h2>
      <div class="field"><label for="co-msg">Gift message <span class="muted">(printed on a card)</span></label><textarea class="input" id="co-msg" maxlength="200"></textarea></div>
      <label class="check"><input type="checkbox" checked> <span>Leave prices off the packing slip</span></label>
      <button class="btn btn-full btn-lg btn-block" type="submit" style="margin-top:1.5rem">Place order</button>
    </form>
    <aside class="summary" aria-label="Order summary"><h2 style="margin-top:0">Your box</h2><div id="summary"></div></aside>
  </div>
</div>'''


def not_found():
    return f'''<section class="section"><div class="wrap narrow center">
  <p class="script">Oups</p><h1 class="h1">This page melted</h1>
  <p class="lead" style="margin-inline:auto">The link may be old or mistyped. Try the shop or search instead.</p>
  <div class="hero-actions" style="justify-content:center">{btn("Shop all chocolates", "/collections/all")}{btn("Search", "/search", "btn-lg")}</div>
</div></section>'''
