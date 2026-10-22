"""Product catalogue and collection rules.

Field names follow product_metafield_schema.csv. Collection handles follow the
workbook Sitemap sheet exactly. Prices, SKUs and lead times are PLACEHOLDERS
until the Gate 1 trading sign-off.
"""

STD = dict(
    vegan=False, organic=False, fairtrade=False, belgian_made=True,
    gift_eligible=True, corporate_eligible=True, contains_alcohol=False,
    logo_personalisation_available=False, quote_only=False, click_and_collect_available=True, available=True,
    shelf_life="6 weeks from dispatch",
    storage_advice="Keep between 15 and 18 °C, away from light and strong smells. Not in the fridge.",
    delivery_lead_time="Dispatch time to be confirmed (Open Decision #8)",
    warm_weather_shipping="Cool pack added automatically from June to September",
    extra=["cut", "hazelnuts"],
)


def product(**kw):
    p = {**STD, **kw}
    p["images"] = [f"assets/img/products/{p['id']}-{i}" for i in (1, 2)]
    return p


PRODUCTS = [
    product(
        id="signature-gift-box", title="Signature praline gift box", product_format="Gift box",
        collections=["pralines-and-truffles", "gift-boxes"],
        chocolate_type=["Dark", "Milk", "White"], filling_type=["Praliné", "Ganache", "Caramel"],
        variants=[
            {"label": "12 pcs", "piece_count": 12, "net_weight": "150 g", "price": 22},
            {"label": "24 pcs", "piece_count": 24, "net_weight": "300 g", "price": 39},
            {"label": "36 pcs", "piece_count": 36, "net_weight": "450 g", "price": 55},
        ],
        flavour_profile="Our house selection: roasted hazelnut praliné, single-origin ganaches and a soft salted caramel, in dark, milk and white shells.",
        ingredients="Cocoa mass, sugar, cocoa butter, whole milk powder, hazelnuts, cream, butter, glucose syrup, sea salt, emulsifier (sunflower lecithin), natural vanilla.",
        allergens=["Milk", "Hazelnut"], occasion=["Birthday", "Thank You", "Dinner Party"],
        gift_level="Proper Gift", bestseller=True,
        flavours=[("Praliné noisette", "milk"), ("Ganache Madagascar 68%", "dark"), ("Caramel salé", "milk"), ("Vanille blanche", "white"), ("Gianduja", "milk"), ("Ganache café", "dark")],
    ),
    product(
        id="heritage-ballotin", title="Heritage ballotin", product_format="Ballotin",
        collections=["ballotins", "pralines-and-truffles", "belgian-classics", "premium-gifts"],
        chocolate_type=["Dark", "Milk", "White"], filling_type=["Praliné", "Cream", "Marzipan", "Nut"],
        variants=[
            {"label": "250 g", "piece_count": 20, "net_weight": "250 g", "price": 19},
            {"label": "500 g", "piece_count": 40, "net_weight": "500 g", "price": 36},
            {"label": "1 kg", "piece_count": 80, "net_weight": "1 kg", "price": 68},
        ],
        flavour_profile="The classic Belgian counter selection, priced by weight: butter creams, marzipan, gianduja and a few liqueur-filled pieces.",
        ingredients="Sugar, cocoa butter, cocoa mass, almonds, hazelnuts, whole milk powder, butter, cream, liqueur (kirsch), emulsifier (soy lecithin), natural vanilla.",
        allergens=["Milk", "Almond", "Hazelnut", "Soy"], contains_alcohol=True,
        occasion=["Dinner Party", "Thank You", "Seasonal"], gift_level="Proper Gift", bestseller=True,
        shelf_life="5 weeks from dispatch",
        flavours=[("Crème au beurre vanille", "white"), ("Massepain", "dark"), ("Gianduja", "milk"), ("Praliné amande", "milk"), ("Cerise au kirsch", "dark"), ("Moka", "milk")],
    ),
    product(
        id="noir-ganache-collection", title="Noir ganache collection", product_format="Gift box",
        collections=["pralines-and-truffles", "gift-boxes"],
        chocolate_type=["Dark"], filling_type=["Ganache"],
        variants=[{"label": "24 pcs", "piece_count": 24, "net_weight": "290 g", "price": 44}],
        flavour_profile="Twenty-four dark ganaches, from bright Madagascan 68% to smoky Ecuadorian 75%, each with a short tasting note.",
        ingredients="Cocoa mass, cream, sugar, cocoa butter, invert sugar, butter, emulsifier (sunflower lecithin).",
        allergens=["Milk"], occasion=["Love", "Dinner Party"], gift_level="Proper Gift", bestseller=True,
        shelf_life="4 weeks from dispatch", extra=["cut", "cocoa-pods"],
        flavours=[("Madagascar 68%", "dark"), ("Équateur 75%", "dark"), ("Pérou 70%", "dark"), ("Thé fumé", "dark"), ("Poivre de Timut", "dark"), ("Miel de Bruxelles", "dark")],
    ),
    product(
        id="vegan-praline-box", title="Vegan praline box", product_format="Gift box",
        collections=["gift-boxes", "pralines-and-truffles"],
        chocolate_type=["Dark"], filling_type=["Praliné", "Ganache", "Fruit"],
        variants=[
            {"label": "Small · 9 pcs", "piece_count": 9, "net_weight": "110 g", "price": 18},
            {"label": "Medium · 16 pcs", "piece_count": 16, "net_weight": "200 g", "price": 32},
            {"label": "Premium · 30 pcs", "piece_count": 30, "net_weight": "370 g", "price": 54},
        ],
        flavour_profile="Oat-milk praliné, coconut ganache and raspberry pâte de fruit in dark shells. Built to stand next to our classic boxes, not behind them.",
        ingredients="Cocoa mass, sugar, cocoa butter, hazelnuts, coconut cream, oat drink powder, raspberry purée, pectin, sea salt.",
        allergens=["Hazelnut", "Oats (gluten)"], vegan=True,
        occasion=["Birthday", "Thank You", "Love"], gift_level="Proper Gift", bestseller=True,
        extra=["raspberry", "cocoa-hands"],
        flavours=[("Praliné avoine", "dark"), ("Ganache coco", "dark"), ("Framboise", "dark"), ("Caramel dattes", "milk")],
    ),
    product(
        id="noisette-praline-box", title="Noisette praliné box", product_format="Gift box",
        collections=["pralines-and-truffles", "gift-boxes", "belgian-classics"],
        chocolate_type=["Milk"], filling_type=["Praliné", "Nut"],
        variants=[{"label": "16 pcs", "piece_count": 16, "net_weight": "200 g", "price": 29}],
        flavour_profile="Sixteen milk-chocolate pralinés built around slow-roasted Piedmont hazelnuts, from smooth to crunchy feuilletine.",
        ingredients="Sugar, hazelnuts, cocoa butter, whole milk powder, cocoa mass, feuilletine (wheat flour, butter), emulsifier (sunflower lecithin).",
        allergens=["Milk", "Hazelnut", "Wheat (gluten)"],
        occasion=["Birthday", "Thank You"], gift_level="Proper Gift", extra=["hazel-shells", "cut"],
        flavours=[("Praliné lisse", "milk"), ("Praliné croustillant", "milk"), ("Noisette entière", "milk"), ("Gianduja", "milk")],
    ),
    product(
        id="grand-coffret", title="Grand coffret, two layers", product_format="Premium gift",
        collections=["premium-gifts", "gift-boxes"],
        chocolate_type=["Dark", "Milk", "White"], filling_type=["Praliné", "Ganache", "Caramel", "Truffle", "Marzipan", "Fruit"],
        variants=[{"label": "64 pcs", "piece_count": 64, "net_weight": "780 g", "price": 119}],
        flavour_profile="Two lacquered layers with the full range: pralinés, ganaches, pâtes de fruit, candied orange and mendiants, with a printed flavour map.",
        ingredients="Cocoa mass, sugar, cocoa butter, whole milk powder, hazelnuts, almonds, pistachios, cream, butter, glucose syrup, candied orange, fruit purée, pectin, emulsifier (sunflower lecithin).",
        allergens=["Milk", "Hazelnut", "Almond", "Pistachio"],
        occasion=["Love", "Thank You", "Wedding"], gift_level="Premium Gift",
        shelf_life="4 weeks from dispatch", extra=["mendiants", "cut"],
        flavours=[("Orangettes", "dark"), ("Mendiant pistache", "dark"), ("Pâte de fruit", "white"), ("Praliné", "milk"), ("Ganache", "dark"), ("Caramel", "milk")],
    ),
    product(
        id="prestige-48", title="Prestige collection, 48 pieces", product_format="Premium gift",
        collections=["premium-gifts", "gift-boxes"],
        chocolate_type=["Dark", "Milk"], filling_type=["Ganache", "Praliné", "Caramel"],
        variants=[{"label": "48 pcs", "piece_count": 48, "net_weight": "560 g", "price": 84}],
        flavour_profile="Forty-eight squares, each stamped and finished with a fleck of cocoa or gold-coloured cocoa butter. Our most-ordered premium box.",
        ingredients="Cocoa mass, sugar, cocoa butter, cream, whole milk powder, hazelnuts, butter, glucose syrup, natural colouring (cocoa butter, mica-free).",
        allergens=["Milk", "Hazelnut"],
        occasion=["Thank You", "Love", "Wedding"], gift_level="Premium Gift",
        flavours=[("Ganache 70%", "dark"), ("Praliné", "milk"), ("Caramel beurre salé", "milk"), ("Café", "dark")],
    ),
    product(
        id="truffle-box", title="Cocoa-dusted truffles", product_format="Truffles",
        collections=["pralines-and-truffles", "belgian-classics"],
        chocolate_type=["Dark", "Milk"], filling_type=["Truffle"],
        variants=[{"label": "18 pcs", "piece_count": 18, "net_weight": "220 g", "price": 27}],
        flavour_profile="Fresh cream truffles rolled by hand in Dutch-process cocoa. Soft, short-lived and best within three weeks.",
        ingredients="Cocoa mass, cream, sugar, cocoa butter, butter, cocoa powder.",
        allergens=["Milk"], corporate_eligible=False,
        occasion=["Dinner Party", "Love"], gift_level="Proper Gift",
        shelf_life="3 weeks from dispatch", storage_advice="Keep between 12 and 16 °C. These are fresh truffles.",
        extra=["truffle-bowl", "cream-pour"],
        flavours=[("Truffe nature", "dark"), ("Truffe lait", "milk")],
    ),
    product(
        id="raspberry-ganache-hearts", title="Raspberry ganache hearts", product_format="Gift box",
        collections=["pralines-and-truffles", "gift-boxes"],
        chocolate_type=["Dark", "White"], filling_type=["Ganache", "Fruit"],
        variants=[{"label": "12 pcs", "piece_count": 12, "net_weight": "140 g", "price": 26}],
        flavour_profile="Painted shells around a sharp raspberry ganache, with a few cinnamon-dusted pieces for warmth.",
        ingredients="Cocoa mass, sugar, cream, cocoa butter, raspberry purée (12%), butter, cinnamon, natural colouring (beetroot).",
        allergens=["Milk"], occasion=["Love", "Birthday"], gift_level="Proper Gift",
        shelf_life="4 weeks from dispatch", extra=["heart-box", "cut"],
        flavours=[("Framboise", "dark"), ("Framboise cannelle", "white")],
    ),
    product(
        id="hazelnut-rochers", title="Hazelnut rochers", product_format="Small treat",
        collections=["pralines-and-truffles", "small-gifts"],
        chocolate_type=["Milk", "White"], filling_type=["Praliné", "Nut"],
        variants=[{"label": "9 pcs", "piece_count": 9, "net_weight": "120 g", "price": 16}],
        flavour_profile="Crunchy praliné domes rolled in chopped roasted hazelnuts, almonds and toasted coconut.",
        ingredients="Hazelnuts, sugar, cocoa butter, whole milk powder, almonds, desiccated coconut, cocoa mass, emulsifier (sunflower lecithin).",
        allergens=["Milk", "Hazelnut", "Almond", "Coconut"],
        occasion=["Dinner Party", "Birthday"], gift_level="Small Attention", extra=["hazel-shells", "hazel-white"],
        flavours=[("Rocher noisette", "milk"), ("Rocher coco", "white"), ("Rocher amande", "milk")],
    ),
    product(
        id="mendiants", title="Dark chocolate mendiants", product_format="Small treat",
        collections=["small-gifts", "belgian-classics"],
        chocolate_type=["Dark"], filling_type=["Nut", "Fruit"],
        variants=[{"label": "10 pcs", "piece_count": 10, "net_weight": "110 g", "price": 14}],
        flavour_profile="Thin discs of 70% dark chocolate topped with roasted hazelnuts, almonds, pistachios and dried cranberries.",
        ingredients="Cocoa mass, sugar, cocoa butter, hazelnuts, almonds, pistachios, dried cranberries (cranberries, sugar, sunflower oil).",
        allergens=["Hazelnut", "Almond", "Pistachio"], vegan=True,
        occasion=["Dinner Party", "Thank You"], gift_level="Small Attention", extra=["hazelnuts", "cocoa-hands"],
        flavours=[("Noisette", "dark"), ("Pistache", "dark"), ("Cranberry", "dark")],
    ),
    product(
        id="salted-caramel-mini", title="Salted caramel mini box", product_format="Small treat",
        collections=["small-gifts"],
        chocolate_type=["Milk", "Dark"], filling_type=["Caramel"],
        variants=[{"label": "6 pcs", "piece_count": 6, "net_weight": "75 g", "price": 12}],
        flavour_profile="Six soft caramels with Guérande salt. A small thank-you that still feels like a proper box.",
        ingredients="Sugar, cream, cocoa mass, cocoa butter, butter, whole milk powder, glucose syrup, sea salt.",
        allergens=["Milk"], occasion=["Thank You", "Birthday"], gift_level="Small Attention",
        extra=["cream-pour", "cut"],
        flavours=[("Caramel salé lait", "milk"), ("Caramel salé noir", "dark")],
    ),
    product(
        id="thank-you-four", title="Thank-you four", product_format="Small treat",
        collections=["small-gifts", "corporate-gifts"],
        chocolate_type=["Dark", "Milk", "White"], filling_type=["Praliné", "Ganache"],
        variants=[{"label": "4 pcs", "piece_count": 4, "net_weight": "50 g", "price": 9}],
        flavour_profile="Four bestsellers in a slim box with a blank card. Fits through most letterboxes.",
        ingredients="Cocoa mass, sugar, cocoa butter, whole milk powder, hazelnuts, cream, emulsifier (sunflower lecithin).",
        allergens=["Milk", "Hazelnut"], occasion=["Thank You"], gift_level="Small Attention",
        extra=["gift-small", "cut"],
        flavours=[("Praliné", "milk"), ("Ganache", "dark"), ("Vanille", "white"), ("Framboise", "dark")],
    ),
    product(
        id="tablet-noir-72", title="Noir 72% tablet", product_format="Tablet",
        collections=["chocolate-tablets", "small-gifts"],
        chocolate_type=["Dark"], filling_type=[],
        variants=[{"label": "100 g", "piece_count": 1, "net_weight": "100 g", "price": 6.5}],
        flavour_profile="Our everyday dark: red fruit up front, roasted cocoa to finish. Three ingredients and a little vanilla.",
        ingredients="Cocoa mass, sugar, cocoa butter, natural vanilla.",
        allergens=["May contain traces of milk and nuts"], vegan=True,
        occasion=[], gift_level="Small Attention", shelf_life="12 months", storage_advice="Keep cool and dry.",
        extra=["cocoa-pods", "beans-bar"], flavours=[],
    ),
    product(
        id="tablet-noir-85", title="Noir 85% intense tablet", product_format="Tablet",
        collections=["chocolate-tablets", "small-gifts"],
        chocolate_type=["Dark"], filling_type=[],
        variants=[{"label": "100 g", "piece_count": 1, "net_weight": "100 g", "price": 7}],
        flavour_profile="Deep and dry, with notes of black tea and toasted bread. For people who take their coffee black.",
        ingredients="Cocoa mass, cocoa butter, sugar.",
        allergens=["May contain traces of milk and nuts"], vegan=True,
        occasion=[], gift_level="Small Attention", shelf_life="12 months", storage_advice="Keep cool and dry.",
        extra=["cocoa-tree", "beans-bar"], flavours=[],
    ),
    product(
        id="tablet-lait-noisette", title="Milk & roasted hazelnut tablet", product_format="Tablet",
        collections=["chocolate-tablets", "small-gifts"],
        chocolate_type=["Milk"], filling_type=["Nut"],
        variants=[{"label": "100 g", "piece_count": 1, "net_weight": "100 g", "price": 6.5}],
        flavour_profile="Creamy 38% milk chocolate packed with whole roasted hazelnuts.",
        ingredients="Sugar, cocoa butter, whole milk powder, hazelnuts (20%), cocoa mass, emulsifier (sunflower lecithin).",
        allergens=["Milk", "Hazelnut"],
        occasion=[], gift_level="Small Attention", shelf_life="12 months", storage_advice="Keep cool and dry.",
        extra=["hazelnuts", "hazel-shells"], flavours=[],
    ),
    product(
        id="winter-spice-edition", title="Winter spice edition", product_format="Gift box",
        collections=["seasonal-drops", "gift-boxes"],
        chocolate_type=["Dark", "Milk"], filling_type=["Ganache", "Praliné", "Caramel"],
        variants=[{"label": "20 pcs", "piece_count": 20, "net_weight": "250 g", "price": 36}],
        flavour_profile="Speculoos praliné, clementine ganache and cardamom caramel, moulded as little winter figures. Made in small batches from November to January.",
        ingredients="Cocoa mass, sugar, cream, cocoa butter, speculoos biscuit (wheat), whole milk powder, clementine purée, spices.",
        allergens=["Milk", "Wheat (gluten)", "Soy"],
        occasion=["Seasonal", "Dinner Party"], gift_level="Proper Gift", limited=True,
        shelf_life="5 weeks from dispatch", extra=["christmas", "cut"],
        flavours=[("Spéculoos", "milk"), ("Clémentine", "dark"), ("Cardamome", "milk")],
    ),
    product(
        id="corporate-24", title="Corporate box, 24 pieces", product_format="Gift box",
        collections=["corporate-gifts"],
        chocolate_type=["Dark", "Milk", "White"], filling_type=["Praliné", "Ganache", "Caramel"],
        variants=[{"label": "24 pcs", "piece_count": 24, "net_weight": "300 g", "price": 45}],
        flavour_profile="Our signature 24 in a sleeve you can brand. Order one to taste it; order a hundred through a quote.",
        ingredients="Cocoa mass, sugar, cocoa butter, whole milk powder, hazelnuts, cream, butter, glucose syrup, emulsifier (sunflower lecithin).",
        allergens=["Milk", "Hazelnut"], occasion=["Thank You"], gift_level="Corporate Ready",
        extra=["logo-box", "cut"],
        flavours=[("Praliné", "milk"), ("Ganache", "dark"), ("Caramel", "milk"), ("Vanille", "white")],
    ),
    product(
        id="logo-pralines", title="Pralines with your logo", product_format="Logo pralines",
        collections=["corporate-gifts"],
        chocolate_type=["Dark", "Milk", "White"], filling_type=["Praliné", "Ganache"],
        variants=[{"label": "Quote only", "piece_count": 0, "net_weight": "By quote", "price": None}],
        flavour_profile="Your logo printed in cocoa butter on the top of each praline. Sold by quote, with a sample pack first.",
        ingredients="Depends on the selection you choose. Sent with your quote.",
        allergens=["Milk", "Hazelnut"], gift_eligible=False, logo_personalisation_available=True, quote_only=True,
        occasion=[], gift_level="Corporate Ready", shelf_life="4 weeks from dispatch",
        delivery_lead_time="From 3 weeks after artwork approval", extra=["premium-box", "cut"],
        flavours=[],
    ),
]

# Filter data that filter_matrix_by_collection.csv reads but the metafield schema
# doesn't define yet (recipient, corporate_use_case, personalisation_available).
FILTER_DATA = {
    "signature-gift-box":       dict(recipient=["Family", "Partner", "Client", "Host"]),
    "heritage-ballotin":        dict(recipient=["Family", "Host", "Self Treat"]),
    "noir-ganache-collection":  dict(recipient=["Partner", "Host", "Self Treat"]),
    "vegan-praline-box":        dict(recipient=["Family", "Partner", "Team"]),
    "noisette-praline-box":     dict(recipient=["Family", "Self Treat"]),
    "grand-coffret":            dict(recipient=["Partner", "Client"]),
    "prestige-48":              dict(recipient=["Client", "Partner"]),
    "truffle-box":              dict(recipient=["Host", "Partner", "Self Treat"]),
    "raspberry-ganache-hearts": dict(recipient=["Partner"]),
    "hazelnut-rochers":         dict(recipient=["Host", "Team"]),
    "mendiants":                dict(recipient=["Host", "Self Treat"]),
    "salted-caramel-mini":      dict(recipient=["Team", "Employee", "Host"]),
    "thank-you-four":           dict(recipient=["Employee", "Team", "Client"], corporate_use_case=["Employee Gifts", "Event Gifts"], personalisation_available=["Branded Card", "Branded Sleeve"]),
    "tablet-noir-72":           dict(recipient=["Self Treat"]),
    "tablet-noir-85":           dict(recipient=["Self Treat"]),
    "tablet-lait-noisette":     dict(recipient=["Self Treat"]),
    "winter-spice-edition":     dict(recipient=["Family", "Host"]),
    "corporate-24":             dict(recipient=["Client", "Employee", "Team"], corporate_use_case=["Client Gifts", "Employee Gifts", "Campaign Gifts"], personalisation_available=["Branded Sleeve", "Branded Card", "Branded Ribbon"]),
    "logo-pralines":            dict(recipient=["Client", "Employee"], corporate_use_case=["Client Gifts", "Event Gifts", "Trade Fair Gifts", "Campaign Gifts"], personalisation_available=["Logo Pralines", "Custom Packaging"]),
}
for _p in PRODUCTS:
    _p.update({"corporate_use_case": [], "personalisation_available": [], **FILTER_DATA[_p["id"]]})

# Collection handles and copy, in Sitemap sheet order.
# filters: groups from filter_matrix_by_collection.csv (assets/js/app.js FILTERS).
# rule: "explicit" (product.collections), or a function name the build evaluates.
COLLECTIONS = {
    "all":                    dict(title="All chocolates", script="Every box, bar and ballotin", rule="all", template="Collection PLP", image="assorted", filters=["availability", "price", "type", "chocolate", "conscious"], intro="The full counter: pralines, ballotins, truffles, tablets and seasonal boxes."),
    "pralines-and-truffles":  dict(title="Pralines & truffles", script="Filled, enrobed, finished by hand", rule="explicit", template="Collection PLP", image="rows", filters=["price", "size", "chocolate", "filling", "alcohol"], intro="Belgian pralines are filled chocolates: a thin shell around a soft centre. Ours are made in small batches and packed to order."),
    "ballotins":              dict(title="Ballotins", script="Chosen by weight, the Belgian way", rule="explicit", template="Collection PLP", image="assorted-beige", filters=["size", "chocolate"], intro="The folded paper box from the chocolate shop counter, in 250 g, 500 g and 1 kg."),
    "gift-boxes":             dict(title="Praline gift boxes", script="12, 24 or 36, ready to give", rule="explicit", template="Collection PLP", image="premium-box", filters=["price", "size", "chocolate"], chips="occasion", intro="Our most-given boxes. Every one ships with a free printed gift card and no prices inside."),
    "chocolate-tablets":      dict(title="Chocolate tablets", script="For the cart, or for you", rule="explicit", template="Collection PLP", image="tablets-stack", filters=["chocolate", "conscious"], intro="100 g bars of the couverture we use in our pralines. Two of the three are vegan."),
    "small-gifts":            dict(title="Small attentions", script="Under €25, still a proper gift", rule="explicit", template="Collection PLP", image="gift-small", filters=["occasion", "recipient", "chocolate"], intro="For the neighbour, the host or the colleague who covered for you. Every one comes with a gift card."),
    "premium-gifts":          dict(title="Premium gifts", script="For the moments that count", rule="explicit", template="Collection PLP", image="red-box", filters=["price", "chocolate"], intro="Two-layer coffrets, a full kilo ballotin and our stamped prestige squares."),
    "belgian-classics":       dict(title="Belgian classics", script="The counter favourites", rule="explicit", template="Collection PLP", image="grand-place", filters=["type", "chocolate", "filling"], intro="Ballotins, pralinés, truffles and mendiants: the pieces Belgian chocolate shops have sold for generations."),
    "seasonal-drops":         dict(title="Seasonal drops", script="Here for a short while", rule="explicit", template="Collection PLP", image="christmas", filters=[], seasonal=True, intro="Small-batch flavours for Christmas, Easter and Valentine’s Day. When they’re gone, they’re gone."),
    "birthday-gifts":         dict(title="Birthday gifts", script="Something better than a card", rule="occasion:Birthday", template="Gift PLP", image="gift-pink", filters=["recipient", "level", "price"], intro="Boxes that arrive on the day, with your message printed on a card inside."),
    "thank-you-gifts":        dict(title="Thank you gifts", script="Say it properly", rule="occasion:Thank You", template="Gift PLP", image="gift-small", filters=["recipient", "level", "price"], intro="From a €9 slim box to a two-layer coffret. Popular with teams and clients too."),
    "love-and-romance":       dict(title="Love & romance", script="For the one who gets the last piece", rule="occasion:Love", template="Gift PLP", image="heart-box", filters=["recipient", "level", "price"], intro="Dark ganaches, raspberry hearts and the grand coffret. Valentine’s boxes arrive in late January."),
    "dinner-party-gifts":     dict(title="Dinner party gifts", script="Bring something better than wine", rule="occasion:Dinner Party", template="Gift PLP", image="mendiants", filters=["recipient", "level", "price"], intro="Host gifts that go straight on the table with coffee."),
    "vegan-chocolates":       dict(title="Vegan chocolates", script="Not a compromise shelf", rule="vegan", template="Vegan PLP", image="raspberry", filters=["vconscious", "type"], intro="No milk, butter, cream or honey. Same atelier, same care, same price as the classic boxes."),
    "organic-chocolate":      dict(title="Organic chocolate", script="Certified, or not listed", rule="organic", template="Collection PLP", image="cocoa-pods", filters=[], claim="organic", intro="This page lists only products with an organic certificate for that exact product."),
    "fairtrade-chocolate":    dict(title="Fairtrade chocolate", script="Certified, or not listed", rule="fairtrade", template="Collection PLP", image="cocoa-hands", filters=[], claim="Fairtrade", intro="This page lists only products made with certified Fairtrade cocoa."),
    "no-alcohol-chocolates":  dict(title="No alcohol chocolates", script="Every piece alcohol-free", rule="no-alcohol", template="Collection PLP", image="cups", filters=["price", "type", "chocolate"], intro="No liqueur and no alcohol-based flavourings. Safe to send to anyone who doesn’t drink."),
    "corporate-gifts":        dict(title="Corporate gift boxes", script="Order a sample, then by the hundred", rule="explicit", template="Corporate PLP", image="open-box", filters=["use_case", "personalisation"], intro="Boxes you can order one at a time to taste, then by quote with your branding."),
}


def members(handle):
    rule = COLLECTIONS[handle]["rule"]
    if rule == "all":
        return [p["id"] for p in PRODUCTS]
    if rule == "explicit":
        return [p["id"] for p in PRODUCTS if handle in p["collections"]]
    if rule.startswith("occasion:"):
        occ = rule.split(":", 1)[1]
        return [p["id"] for p in PRODUCTS if occ in p["occasion"]]
    if rule == "vegan":
        return [p["id"] for p in PRODUCTS if p["vegan"]]
    if rule == "organic":
        return [p["id"] for p in PRODUCTS if p["organic"]]
    if rule == "fairtrade":
        return [p["id"] for p in PRODUCTS if p["fairtrade"]]
    if rule == "no-alcohol":
        return [p["id"] for p in PRODUCTS if not p["contains_alcohol"] and not p["quote_only"]]
    raise ValueError(rule)


def get(pid):
    return next(p for p in PRODUCTS if p["id"] == pid)
