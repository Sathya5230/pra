# Pralines Shopify Build Pack: Analysis

Covers every file in [`source_files/`](source_files/): 2 briefs, 10 CSVs (one is a duplicate) and `pralines shopify build pack.xlsx` (6 sheets, one of them hidden). Each section below says what a file contains, what it decides, and where it disagrees with the other files.

---

## 1. Executive summary

**The project:** a premium Shopify store for Belgian pralines. It has four buyer routes: **retail gifting, Vegan & Conscious, corporate (B2B) gifting, and heritage/Belgian classics**. Delivery confidence, especially shipping in warm weather, is treated as a conversion issue as much as an operations one. The guiding UX principle is **"Guide, do not overwhelm."**

**Where it stands:**

| Signal | Status |
|---|---|
| Strategy and architecture docs | Mostly complete (sitemap, nav, filters, metafields, SEO map, GA4 plan, integrations, phased plan) |
| Reconciliation | Done in the workbook: sitemap 34 → 45 rows, nav 32 → 40 rows, 2 redirects, 8 added pages |
| Build checklist | 43 tasks, **0 done, 0 blocked, all "Not started"** |
| Open decisions | **13, all unanswered**, kept on a **hidden** sheet |
| Trading inputs (SKUs, prices, margins, shipping rules, MOQ) | **Not yet decided.** These block most other work |
| Design assets | Referenced (`07_VISUALS_AND_WIREFRAMES`, "all 5 designs") but **not in this folder** |
| Target markets / languages | **Not stated anywhere** (prices are in €; checklist #7 sets up Markets) |

**Bottom line:** the planning is careful and strongly focused on compliance: it guards against greenwashing, needs proof for every claim, and keeps filtered URLs out of the index. The project is blocked mainly by commercial decisions, not technical ones. Until the Ecommerce Trader and Founder answer Gate 1 and Gate 2 questions, design and build cannot move forward safely.

---

## 2. File inventory

| File | Type | Rows | Purpose | Note |
|---|---|---|---|---|
| `ECOMMERCE_TRADER_BRIEF.md` | Brief | — | Commercial priorities and trading decisions | Lists decisions but makes none of them |
| `SHOPIFY_UX_DESIGNER_BRIEF.md` | Brief | — | UX principles, nav, templates, components | Points to wireframes that are not in the folder |
| `sitemap_inventory.csv` | Data | 34 pages | Original page list | Superseded by workbook "Sitemap" sheet (45) |
| `navigation_menu.csv` | Data | 32 links | Original menu | Superseded by workbook "Navigation" sheet (40) |
| `filter_matrix_by_collection.csv` | Data | 14 filter groups | Filters per collection | — |
| `filter_matrix_by_collection (1).csv` | Data | 14 | — | **Byte-identical duplicate. Delete it** |
| `product_metafield_schema.csv` | Data | 21 metafields | Product data model | Some types still "X or Y" |
| `launch_assortment_matrix.csv` | Data | 9 families | Product families and price logic | No actual SKUs or prices yet |
| `seo_keyword_page_map.csv` | Data | 10 targets | Keyword → page | Covers only a small share of pages |
| `ga4_event_tracking_plan.csv` | Data | 14 events | Measurement | Event names differ from GA4's standard names |
| `shopify_integration_stack.csv` | Data | 12 capabilities | Apps and approaches | Several "pick later" decisions |
| `project_plan_and_approval_gates.csv` | Data | 15 tasks / 8 phases | Phases and gates | — |
| `pralines shopify build pack.xlsx` | Workbook | 6 sheets | **Master, reconciled version** of the above | "Open Decisions" sheet is hidden |

> **Use the workbook as the master.** The CSVs are the earlier inputs. The workbook's Sitemap and Navigation sheets already fix most of the gaps between those CSVs and record a Change and Reason column for each fix.

### 2.1 Workbook details

| Sheet | Contents | Notes |
|---|---|---|
| Summary | Live counts (formulas) and a "How to use" guide | Counts: 45 sitemap rows (8 Added, 4 Modified, 2 Redirect, 1 Decision), 40 nav rows (6 Added), 43 tasks (0 Done, 0 Blocked), 13 decisions (13 unanswered) |
| Sitemap | 45 rows, the CSV columns plus **Change** and **Reason for change** | Has filters on every column |
| Navigation | 40 rows, the CSV columns plus **Closest label in design**, **Change** and **Reason** | Maps each brief menu item to the label used in the design |
| Redirects & Canonicals | 6 rules | Handed to the SEO Specialist and Developer |
| Build Checklist | 43 tasks with Template, Type, Owner, Dependency, Gate, Status | Status is a dropdown: *Not started / In progress / Blocked / Done* |
| Open Decisions | 13 decisions with Who decides, Needed by, Note (recommendation), Answer | **Hidden sheet** |

- The "How to use" guide says: review the Change and Reason columns; hand Redirects to SEO/Dev; update checklist Status (the Summary updates itself); fill in the Answer column on Open Decisions.
- The **Summary has no count for "In progress"**. It counts only Done and Blocked, so it can't show work in progress.
- File metadata: generated with openpyxl on 7 Oct 2026, last saved in Excel by "Lakshman, Arshad". The CSVs and briefs are dated 7 Oct 2026, the same day.

---

## 3. Business model and commercial logic

From `ECOMMERCE_TRADER_BRIEF.md` and `launch_assortment_matrix.csv`.

**Mission (Trader):** build the commercial offer and trading logic behind the site.

| Priority | Role | Product families |
|---|---|---|
| 1 | Core revenue | Praline Gift Boxes (12/24/36 pcs, **hero family**, AOV ladder), Ballotins (250 g / 500 g / 1 kg, heritage anchor, "Mary-inspired format", priced by weight) |
| 2 | Raise average order value (AOV) | Premium Gifts (€50–€100, €100+, hero photography), Seasonal Drops (Christmas, Easter, Valentine, corporate season; limited-time / premium; "disruptor accent" in design) |
| 3 | Growth | Vegan Boxes (small / medium / premium, priced in line with non-vegan boxes, "not a compromise shelf") |
| 4 | Highest-value leads | Logo Pralines (quote only + sample pack, MOQ-based, **kept out of the standard checkout**) |
| 5 | Protect conversion | Delivery clarity, warm-weather policy |
| — | Entry / add-on | Small Attentions (mini boxes, tablets, small treats; under €25; "human label"), Chocolate Tablets (dark, milk, vegan, fruit/nut; lower price; cart upsell), No Alcohol Boxes (mixed sizes; "important for gifting") |

**Trading decisions the brief lists (none answered)**
Final SKU list · variant structure · product family margins · pricing bands · gift message rules · shipping rules · warm-weather shipping policy · corporate MOQ · sample pack offer · seasonal campaign calendar.

**Shipping decisions the brief lists (none answered)**
Shipping zones · courier partners · cut-off times · blackout dates · heat threshold · cold-pack logic · damaged product policy · replacement rules.

**Per-SKU content the brief requires, and the metafield for each**
Every required item has a matching metafield:

| Brief item | Metafield |
|---|---|
| Product format, piece count, net weight | `product_format`, `piece_count`, `net_weight` |
| Chocolate type, filling type, flavour profile | `chocolate_type`, `filling_type`, `flavour_profile` |
| Ingredients, allergens, alcohol status | `ingredients`, `allergens`, `contains_alcohol` |
| Shelf life, storage advice | `shelf_life`, `storage_advice` |
| Vegan / organic / Fairtrade claims | `vegan`, `organic`, `fairtrade` |
| Gift eligibility, corporate eligibility | `gift_eligible`, `corporate_eligible` |
| Delivery lead time | `delivery_lead_time` |

**Takeaways**
- The **AOV ladder** (12 → 24 → 36 pcs, then Premium) is the main revenue mechanism. Tablets work as the cart add-on.
- Corporate is a **lead-generation funnel, not a checkout flow**. The quote form, logo upload and CRM routing are must-haves, not extras.
- The assortment lists Tablets under an **"Add-ons"** collection and Small Attentions under a **"Gifts"** collection. Neither collection exists in the sitemap (see §13).

---

## 4. Information architecture

### 4.1 Top navigation

| Brief (UX brief) | Design labels (workbook "Closest label in design") |
|---|---|
| Shop | Pralines & Ballotins |
| Gifts | Shop Gifts |
| Corporate Gifts | Corporate Gifting |
| Vegan & Conscious | Vegan & Conscious |
| Our Chocolate | Our Chocolate |
| Delivery | **Not in design** (trust strip and footer only) |
| About | About Us |

Open Decision #1 asks which version to follow. The recommendation is to keep the brief structure and add Delivery to the design.

### 4.2 Pages by group (workbook Sitemap sheet, 45 rows)

| Group | Pages | Must launch |
|---|---|---|
| Home | 1 | 1 |
| Shop collections | 9 + Build a Ballotin (TBD) | 6 |
| Gifts (occasion) | 4 | 1 (Thank You) |
| Vegan & Conscious | 4 collections | 2 (+2 conditional on claims) |
| Corporate | 1 collection + 4 landing + 2 forms | 5 |
| Our Chocolate / trust | 4 + blog index + 1 post | 3 |
| Delivery / service | 5 | 5 (calendar "if app ready") |
| About | 3 (about, sustainability, contact) | 2 |
| Legal (Shopify policies) | 3 | 3 |
| Redirects | 2 | — |

**Launch priority counts:** 28 Must launch (2 of them redirects) · 1 Must launch if data supports · 1 Must launch if app ready · 10 Phase 1 · 4 Phase 1 if claims exist · 1 TBD.

> "Phase 1" isn't defined anywhere. It's unclear whether it means *at launch* or *first release after launch*. Define it so the launch scope is unambiguous.

### 4.3 Template inventory (16 templates)

| Template | Pages using it |
|---|---|
| Homepage | `/` |
| Collection PLP | 12 (all, pralines, ballotins, gift boxes, tablets, small, premium, classics, seasonal, organic, fairtrade, no-alcohol) |
| Gift PLP | 4 occasion collections |
| Vegan PLP | vegan-chocolates |
| Corporate PLP | corporate-gifts |
| Corporate Landing | corporate-gifting, pralines-with-logo, client-gifts, employee-gifts |
| Quote Form / Upload Form | request-a-quote / upload-your-logo |
| Editorial Trust | belgian-pralines, ingredients, organic-and-fairtrade, about, sustainability |
| FAQ/Trust, FAQ | allergens; faq |
| Service | shipping-and-delivery, delivery-calendar, warm-weather-shipping, returns, contact |
| Blog, Blog article | /blogs/stories, how-to-store-pralines |
| Shopify policy | privacy, terms, refund |
| Custom | build-a-ballotin |

### 4.4 Fixes the workbook already made (CSV → workbook)

| Issue in CSVs | Resolution |
|---|---|
| `/collections/small-attentions` in nav, not in sitemap; duplicates small-gifts | 301 → `/collections/small-gifts`; keep "Small Attentions" as the label |
| `/pages/ingredient-transparency` in nav only; duplicates `/pages/ingredients` | 301 → `/pages/ingredients`. The nav item becomes "Ingredients & Transparency" |
| `/pages/ingredients` under both Vegan & Conscious and Our Chocolate | Kept on purpose as a cross-link, not a duplicate page |
| "About" top nav had no destination | Added `/pages/about` (Our Story), `/pages/sustainability`, `/pages/contact` |
| SEO blog post `/blogs/stories/how-to-store-pralines` missing from sitemap | Added, plus `/blogs/stories` index (blog handle "stories") |
| `/collections/corporate-gifts`, `/pages/organic-and-fairtrade`, `/pages/returns-and-quality-guarantee` in sitemap but not nav | Added to nav ("Corporate Gift Boxes", "Organic & Fairtrade (proof)", "Returns & Quality Guarantee") |
| Footer links in the designs had no pages | Added sustainability, contact and 3 Shopify policy pages (refund policy must match the returns page) |
| Vegan page mockup shows Organic, Fair Trade and "No palm oil" tiles | Marked Modified: show only if there is SKU-level proof |
| Corporate mockup adds Seasonal and Hospitality use cases, multiple addresses, invoicing | Marked Modified: confirm scope before build |
| Design adds a "Build a Ballotin" feature (Home CTA and footer) that no brief covers | Flagged as a decision: cut it or scope it |

### 4.5 Gaps the workbook still has

1. **No `/collections/gifts` page.** The filter matrix defines filters for a "Gifts" collection, checklist items #13–17 build a "Gifts" PLP, and the assortment assigns products to "Gifts", but no such URL appears in the sitemap or nav.
2. **No "Add-ons" collection.** The assortment assigns Tablets to it; the sitemap has none.
3. **Seasonal / Hospitality corporate pages** appear in the corporate mockup with URL "TBD" (Open Decision #6).
4. **Vegan & Conscious "landing page"** in the UX brief is built as a collection (`/collections/vegan-chocolates`, Vegan PLP template). Confirm the editorial blocks (hero, 5 claim tiles) fit a collection template.
5. **No click & collect page**, although a `click_and_collect_available` metafield exists.

---

## 5. UX requirements (UX brief + Build Checklist)

**Mission (UX):** a premium but practical Shopify experience for Belgian pralines, gifts, vegan/conscious buyers and corporate gifting.

### 5.1 UX priorities and the checklist tasks that deliver them

| # | Priority | Delivered by |
|---|---|---|
| 1 | Buyer can find a gift in **under 30 seconds** | Homepage intent cards (#9), gift PLPs, occasion chips, Gift Level filter |
| 2 | Corporate buyer can request a quote **without entering the retail checkout** | Inline quote form (#22), standalone quote page (#32), Logo Pralines as quote-only |
| 3 | Vegan/conscious buyer finds **claim-safe** products immediately | Vegan landing (#18–20), claim badges driven by metafields |
| 4 | **Delivery confidence before checkout** | Delivery panel (#10), PDP delivery estimate and heat notice (#28), cart drawer delivery date (#6) |
| 5 | Filters are **collection-specific and restrained** | #14 ("not all 8 groups") |

There is no measurement for priority 1. Consider a usability test, or tracking time from landing to add-to-cart.

### 5.2 Templates to design first and their design status

Design status is inferred from the checklist, because the designs aren't in this folder.

| # | Template | Status |
|---|---|---|
| 1 | Homepage | Designed |
| 2 | Main collection page | Designed (PLP) |
| 3 | Pralines & Truffles collection | Designed (shares the PLP) |
| 4 | Gift Boxes collection | Designed (shares the PLP) |
| 5 | Vegan & Conscious landing | Designed |
| 6 | Corporate Gifting page | Designed |
| 7 | Pralines with Logo page | **Not designed** (#25) |
| 8 | Product detail page | Designed |
| 9 | Request a Quote page | **Not designed** (#32) |
| 10 | Delivery / Warm Weather page | **Not designed** (#33) |
| — | Cart drawer (required component) | **Design missing** (#6) |

That matches the "5 designs" the checklist mentions: Home, PLP, Vegan, Corporate and PDP. An "About Us (design)" label in the Navigation sheet suggests an About page design may also exist.

### 5.3 Required components (18)

Header · mega menu · mobile menu · hero block · collection card · product card · filter drawer · badge system · trust strip · product tabs · gift message block · delivery estimate block · corporate CTA · quote form · logo upload module · FAQ accordion · testimonial block · cart drawer.

- **Testimonial block** depends on Decision #3 (real backing) and #24 (written permission for client logos and testimonials).
- **Badge system** must draw only on proven claim metafields (#19–20).

### 5.4 Build requirements per template (Build Checklist)

| Area | Requirements |
|---|---|
| Global | Theme with filter drawer, mega menu, quick-add and cart drawer, checked against all 5 designs (#1) · automated collections from metafields/tags (#2) · metafield definitions (#3) · mega and mobile menu from the reconciled nav (#4) · **announcement bar with 3 USPs, verified claims only** (#5) · cart drawer with gift message, delivery date and tablet upsell (#6) · **Markets: country, currency, language selector** (#7) · footer linked to real pages and policies (#8) |
| Homepage | Hero + trust chips, **4 intent cards**, bestsellers carousel (#9) · collection banners, corporate band, delivery confidence panel (#10) · **replace placeholder "12,000+ reviews"** with a real feed or remove it (#11) · Build a Ballotin card: build or remove (#12) |
| Collection PLP | Product card: badges, piece count, price, quick add, wishlist (if kept) (#13) · filter set per collection (#14) · price filter: buckets vs. slider (#15) · category chips (#16) · gifting strip, trust strip, FAQ, related collections (#17) |
| Vegan & Conscious | Vegan hero, **5 claim tiles**, vegan carousel (#18) · badges from vegan/organic/fairtrade/palm-oil metafields, **supplier proof on file** (#19) · remove unproven tiles (#20) |
| Corporate Gifting | Use-case cards, format cards, personalisation row, delivery strip (#21) · inline quote form: **name, email, company, use case, qty, date, notes** (#22) · logo upload: file types, size limit, artwork approval (#23) · client logos and testimonials only with **written permission** (#24) |
| Pralines with Logo | Design and build: MOQ, **sample pack CTA**, quote CTA (#25) |
| Product detail page | Gallery (**4 views**), price + badges, piece count + net weight (#26) · gift message on PDP and cart (#27) · delivery estimate + warm-weather notice from metafields (#28) · **allergen summary near Add to Cart**, not only in a tab (#29) · **5 tabs**: Inside the Box, Flavour, Ingredients & Allergens, Delivery & Care, Gifting & Corporate (#30) · related products: small add-on, premium upgrade, vegan alternative, corporate-eligible (#31) |
| Request a Quote | Standalone page reusing the inline form (#32). The sitemap also lists **budget** and **upload logo** as fields, which the inline form (#22) lacks |
| Delivery | Shipping, calendar, warm-weather and returns pages (#33) · date picker app checked against heat rules (#34) · courier/label app (Sendcloud, ShipStation) (#35) |
| Trading data | SKUs, variants, price bands, margins (#36) · per-SKU content (#37) · shipping zones, cut-offs, blackout dates, heat threshold, cold pack, damage policy (#38) |
| SEO / Analytics / QA | Meta, canonicals, schema (#39) · 301s and filter canonicals (#40) · submit sitemap to GSC (#41) · 14 GA4 events (#42) · mobile, checkout, filters, forms, delivery, analytics QA (#43) |

---

## 6. Product data model (metafields)

`product_metafield_schema.csv` defines **21** metafields. Build Checklist #3 says **"all 20"**, so one of the two counts is wrong.

| Metafield | Type | Used for | Required |
|---|---|---|---|
| product_format | single line text **or** metaobject | Filters, PDP, badges | Yes |
| piece_count | integer | PDP, filters, product card | Yes |
| net_weight | single line text | PDP, product card | Yes |
| chocolate_type | list | Filters, PDP | Yes |
| filling_type | list | Filters, PDP | Yes for pralines |
| flavour_profile | multi-line text | PDP story | Yes |
| ingredients | rich text | PDP trust and compliance | Yes |
| allergens | list **or** single line text | PDP trust and compliance | Yes |
| contains_alcohol | boolean | No alcohol filter | Yes |
| shelf_life | single line text | PDP and delivery trust | Yes |
| storage_advice | rich text | PDP and delivery trust | Yes |
| vegan | boolean | Filters, badges, SEO | Yes if vegan line |
| organic | boolean | Filters, badges, SEO | If true |
| fairtrade | boolean | Filters, badges, SEO | If true |
| belgian_made | boolean | Badges, trust | Yes |
| gift_eligible | boolean | Gift filters, product cards | Yes |
| corporate_eligible | boolean | B2B route, badges | Yes |
| logo_personalisation_available | boolean | Corporate pages | If true |
| warm_weather_shipping | boolean **or** text | Shipping warnings | Yes |
| delivery_lead_time | single line text | PDP, cart | Yes |
| click_and_collect_available | boolean | **Delivery filter** | If offered |

**Issues to settle before Gate 2 (schema sign-off)**

- **Types still undecided:** `product_format`, `allergens`, `warm_weather_shipping`. Changing a type after products are loaded means migrating the data.
- **`net_weight` is text.** A number-with-unit (weight) type would allow sorting and filtering by weight. The Box Size filter mixes piece counts and weights (250 g / 500 g / 1 kg).
- **The filter matrix needs fields the schema doesn't have:**
  - `occasion`, `recipient`, `gift_level` (Gifts filters)
  - `corporate_use_case`, `personalisation_available` (Corporate filters). The schema only has `logo_personalisation_available`, which doesn't cover sleeve, card, ribbon or custom packaging.
  - `palm_oil_free` (in the vegan mockup; checklist #3 says "add if claimed")
- **`click_and_collect_available` is "used for: Delivery filter"**, but the filter matrix has no delivery filter and the site has no click & collect page.
- **No price-band field.** The filter matrix wants price *buckets*. Shopify's native price filter is a min–max range, which is closer to the design's slider. Buckets would need a custom `price_band` field or tag (relevant to Open Decision #5).

---

## 7. Filtering (`filter_matrix_by_collection.csv`)

| Collection | Filter group | Values | Source | Owner | Rule |
|---|---|---|---|---|---|
| All Chocolates | Availability | In stock, Out of stock | Inventory | Trader | Broad pages only |
| All Chocolates | Price | Under €25, €25–50, €50–100, €100+ | Price | Trader | Use buckets |
| All Chocolates | Product Type | Pralines, Truffles, Ballotins, Gift Boxes, Tablets, Small Treats, Premium Gifts | product_type / product_format | Trader | Metafield-backed if needed |
| All Chocolates | Chocolate Type | Dark, Milk, White, Mixed | chocolate_type | Trader | Product-led pages |
| All Chocolates | Conscious Choices | Vegan, Organic, Fairtrade, No alcohol, Belgian made | claim metafields | Trader/SEO | Only true product-level claims |
| Pralines & Truffles | Box Size | 12/24/36 pcs, 250 g, 500 g, 1 kg | piece_count / net_weight | Trader | Keep simple |
| Pralines & Truffles | Filling | Praliné, Ganache, Caramel, Cream, Marzipan, Fruit, Nut, Truffle | filling_type | Trader | PDP and filter |
| Gifts | Occasion | Birthday, Thank You, Love, Dinner Party, Wedding, Seasonal | occasion | Trader | Gift intent |
| Gifts | Recipient | Client, Employee, Team, Host, Partner, Family, Self Treat | recipient | Trader | Only if enough products |
| Gifts | Gift Level | Small Attention, Proper Gift, Premium Gift, Corporate Ready | gift_level | Trader | Human labels |
| Vegan & Conscious | Conscious Choices | Vegan, Organic, Fairtrade, No alcohol, Dark Chocolate, Fruit & Nut | claim metafields | SEO/Trader | Do not clutter |
| Corporate Gifts | Use Case | Client, Employee, Event, Trade Fair, Campaign | corporate_use_case | Trader | B2B-specific |
| Corporate Gifts | Personalisation | Logo Pralines, Branded Sleeve, Card, Ribbon, Custom Packaging | personalisation_available | Designer/Dev | B2B-specific |
| Corporate Gifts | Quantity Range | 25–50, 51–100, 101–250, 250+ | quote form field | Trader | Quote flow, not a retail filter |

The approach is good: restrained, collection-specific filters match "Guide, do not overwhelm". Issues:

- **Pralines & Truffles disagrees with the sitemap.** The sitemap note lists *price, box size, chocolate type, filling, alcohol*; the matrix lists only *box size, filling*. State whether the All Chocolates filters carry over to other collections.
- **No filters are defined** for Ballotins, Gift Boxes (sitemap says "occasion chips"), Tablets, Premium, Small Gifts, Seasonal or the occasion collections.
- **The Vegan "Conscious Choices" values mix claims and attributes.** "Dark Chocolate" and "Fruit & Nut" aren't claims. Keep them separate so claim badges never draw on non-claim data.
- **The "Wedding" occasion** has no collection, unlike the other occasions.
- **Corporate quantity "25–50"** suggests an MOQ of 25, but Corporate MOQ is still an open trading decision.

---

## 8. SEO (`seo_keyword_page_map.csv` + workbook Redirects sheet)

| Keyword / theme | Page | Intent | Canonical | Note |
|---|---|---|---|---|
| Belgian pralines | /pages/belgian-pralines | Informational + trust | Self | Heritage and education |
| Belgian praline gift box | /collections/gift-boxes | Commercial | Self | **Core money page** |
| Pralines with logo | /pages/pralines-with-logo | B2B commercial | Self | Van Parijs-inspired |
| Corporate chocolate gifts | /pages/corporate-gifting | B2B commercial | Self | Quote CTA |
| Vegan Belgian chocolate | /collections/vegan-chocolates | Commercial + values | Self | Growth route |
| Organic Belgian chocolate | /collections/organic-chocolate | Commercial + claim | Self, only if products exist | Avoid greenwashing |
| Fairtrade Belgian chocolate | /collections/fairtrade-chocolate | Commercial + claim | Self, only if products exist | Avoid greenwashing |
| Warm weather chocolate delivery | /pages/warm-weather-shipping | Trust and service | Self | Fewer support queries |
| How to store pralines | /blogs/stories/how-to-store-pralines | Informational | Self | Product care |
| Filtered URLs | any filtered collection | UX only | **Canonical to parent** | Do not index |

**Redirects & Canonicals sheet:** 2 × 301 (small-attentions, ingredient-transparency) · filtered URLs `?filter.*` → canonical + noindex · organic and Fairtrade collections conditional on SKUs · `/collections/all` self-canonical.

**Strengths**
- The claim-safety rule is consistent across all files: Organic and Fairtrade pages are created **only if SKU-level proof exists**.
- Shopify's automatic sitemap.xml is used, and is submitted to Google Search Console (GSC) after launch.

**Gaps**
- **Only 10 keyword targets for about 40 indexable pages.** These must-launch pages have no target keyword: Pralines & Truffles, Ballotins, Small Gifts, Premium Gifts, Thank You Gifts, No Alcohol, Corporate Gifts collection, Allergens, Shipping & Delivery, About.
- **No language plan.** Checklist #7 includes a language selector, but nothing says which languages, or covers translated URLs and hreflang tags. In Belgium that likely means NL / FR / EN. Confirm.
- **No list of structured-data types.** Checklist #39 says "schema" without naming which (Product, Organization, FAQPage, BreadcrumbList, Article).
- **Competitor references in planning notes** ("Inspired by Van Parijs", "Mary-inspired format") are fine internally. Make sure no copy, imagery or naming is taken from them on the live site.
- **No redirect map from an existing site.** If the brand already has a site or store, its legacy URLs need 301s. Nothing says whether this is a new domain or a migration.

---

## 9. Analytics (`ga4_event_tracking_plan.csv`)

| Event | Where triggered | Why | Implementation |
|---|---|---|---|
| view_collection | Collection pages | Category traffic | GA4 ecommerce |
| filter_used | Filter drawer | Filter usefulness | Custom |
| search_used | Site search | Discovery behaviour | Include query |
| no_results | Search, no results | Fix synonyms and content gaps | Track query |
| view_product | PDP | Product interest | GA4 ecommerce |
| add_to_cart | PDP / PLP / cart | Conversion intent | GA4 ecommerce |
| gift_message_added | PDP / cart | Gifting behaviour | Custom |
| delivery_date_selected | PDP / cart / **checkout** | Delivery confidence | Custom |
| corporate_quote_clicked | Corporate / PDP / cart | B2B intent | Custom |
| logo_upload_started | Corporate pages | B2B personalisation intent | Custom |
| quote_form_submitted | Quote form | B2B lead conversion | CRM + GA4 |
| checkout_started | Cart | Checkout funnel | GA4 ecommerce |
| purchase | Thank-you page | Revenue | GA4 ecommerce |
| newsletter_signup | Footer / modal | Audience growth | Email integration |

Coverage of the gifting and B2B journeys is good. The checklist (#42) also counts 14 events.

**Problem 1: event names.** Events marked "GA4 ecommerce" don't use GA4's recommended event names. Under these names, GA4's built-in ecommerce reports and funnels won't fill in.

| Plan name | GA4 recommended name |
|---|---|
| view_collection | `view_item_list` |
| view_product | `view_item` |
| checkout_started | `begin_checkout` |
| search_used | `search` (param `search_term`) |
| quote_form_submitted | `generate_lead` (can also send a custom event) |
| newsletter_signup | `sign_up` or `generate_lead` |
| add_to_cart, purchase | Already correct |

**Problem 2: checkout and thank-you tracking.** Events in checkout (`delivery_date_selected`) and on the thank-you page (`purchase`) have to go through Shopify's Customer Events (web pixels). Custom checkout UI depends on the Shopify plan (Decision #9).

**Missing events:** `select_item` (product card click from a PLP), sample-pack request, Build a Ballotin interactions (if kept), wishlist (if kept).

---

## 10. Integrations (`shopify_integration_stack.csv`)

| Capability | Approach | Priority | Blocking decision |
|---|---|---|---|
| Search, filters, synonyms, recommendations | Shopify Search & Discovery | Must have | Theme must support a filter drawer |
| Product data and badges | Metafields / metaobjects | Must have | Schema sign-off before product load |
| Sitemap | Shopify auto sitemap.xml | Must have | Submit to GSC after launch |
| Checkout customisation | Checkout UI extensions | Should have | **Needs Shopify Plus** (Decision #9) |
| Delivery date picker | App or custom extension | Must have for gifting | Pick after shipping and heat rules are defined |
| Courier automation (labels, tracking, returns) | Sendcloud / ShipStation / carrier app | Must have | Countries, courier, fulfilment model |
| Corporate quote request | App or custom form | Must have | Where quotes go: email, CRM or draft orders (Decision #10) |
| Logo upload | App or custom field | Must have for B2B | File formats and artwork approval flow |
| Gift message | App or theme | Must have | Placement: PDP, cart or checkout |
| Reviews | Judge.me / Yotpo | Should have | Budget |
| Email / SMS (abandoned cart, gifting calendar, corporate reminders) | Klaviyo or Shopify Email | Must have | "Klaviyo if serious ecommerce" |
| Analytics | GA4, GSC, Shopify Analytics, pixels | Must have | Before soft launch |

**Sources cited in the CSV:** [Search & Discovery app](https://apps.shopify.com/search-and-discovery) · [Shopify sitemap help](https://help.shopify.com/en/manual/promoting-marketing/seo/find-site-map) · [Checkout UI Extensions docs](https://shopify.dev/docs/api/checkout-ui-extensions/latest).

**Not listed but implied elsewhere:** a box-builder app (Build a Ballotin), a wishlist app (Decision #12), a multi-address shipping app (Decision #6), Shopify Markets and translation (checklist #7), and invoicing for corporate orders (Decision #6).

---

## 11. Project plan and gates

| Phase | Workstream | Task | Owner | Output | Gate |
|---|---|---|---|---|---|
| 1 Strategy | Commercial | Approve positioning and revenue priorities | Founder/Trader | Strategy one-pager | Gate 1 |
| 1 Strategy | Assortment | Define launch SKUs and variants | Trader | Launch assortment matrix | Gate 1 |
| 1 Strategy | Brand | Approve brand direction and tone | Brand Designer | Brand board | Gate 1 |
| 2 Architecture | UX | Approve sitemap and navigation | UX Designer | Sitemap and nav matrix | Gate 2 |
| 2 Architecture | Shopify | Approve metafield schema and collection rules | Developer | Data schema | Gate 2 |
| 2 Architecture | SEO | Approve keyword-to-page map | SEO | SEO map | Gate 2 |
| 3 Design | UX/UI | Homepage, PLP, PDP, corporate, vegan, delivery | UX Designer | Figma pages | Gate 3 |
| 3 Design | Brand | Photography/media direction, component system | Brand Designer | Design system | Gate 3 |
| 4 Build | Shopify | Theme, metafields, collections, filters | Developer | Working store | Gate 4 |
| 4 Build | Integrations | Search, delivery, quotes, upload, email, analytics apps | Developer | Integration test sheet | Gate 4 |
| 5 Content | Trading | Products, pricing, shipping rules, copy | Trader | Product catalogue | Gate 5 |
| 5 Content | SEO | Meta, schema, sitemap, redirects | SEO | SEO QA sheet | Gate 5 |
| 6 QA | Cross-functional | Mobile, checkout, filters, forms, delivery, analytics | All | QA checklist | Launch gate |
| 7 Launch | Marketing/Trading | Soft launch; monitor orders, leads, search | Trader | Launch dashboard | Post-launch |
| 8 Optimise | Growth | Conversion, filters, search, corporate leads, SEO | All | Optimisation backlog | 30-day review |

**Build checklist: 43 tasks by gate**

| Gate 1 | Gate 2 | Gate 3 | Gate 4 | Gate 5 | Launch / Post |
|---|---|---|---|---|---|
| 2 | 4 | 7 | 20 | 8 | 2 |

**Sequencing notes**
- Gate 4 holds 20 of 43 tasks, so it will be the bottleneck. Most of them wait on Gate 1 and 2 trading inputs.
- Checklist #38 (shipping rules) is at **Gate 2**, while the project plan loads shipping rules in **Phase 5**. These don't conflict (define at Gate 2, load at Phase 5), but the plan should say so.
- Checklist #1 (choose theme) is at Gate 2 but depends on "all 5 designs", which are Gate 3 outputs.
- Several design-first templates are still **not designed**: Pralines with Logo, Request a Quote, Delivery pages, cart drawer.
- The plan has **no dates, durations or budget**, and no brief covers photography production, although several tasks depend on it (#9, Premium hero photography).

---

## 12. Open decisions (hidden workbook sheet)

All 13 are unanswered. They are grouped here by the gate they block, with the workbook's own recommendation:

| # | Decision | Owner | Gate | Workbook note / recommendation |
|---|---|---|---|---|
| 2 | Build a Ballotin in launch scope? | Founder/Trader | **1** | No brief, CSV or schema covers it; needs app or dev |
| 6 | Corporate scope: seasonal/hospitality, multi-address, invoicing, courier integration | Trader | **1** | Multi-address needs an app |
| 7 | Small-gift entry price: under €15 (design) or under €25 (assortment)? | Trader | **1** | Align copy and filter |
| 1 | Navigation: brief or design structure? | Founder/UX | 2 | Keep the brief structure; add Delivery to the design |
| 8 | Is "1–2 business days" deliverable under heat rules? | Trader | 2 | Don't publish until confirmed |
| 9 | Shopify Plus? | Founder | 2 | Decides where gift message and delivery date can go |
| 10 | Where quotes go: email, CRM or draft orders? | Dev/Trader | 2 | Needed to pick the quote app |
| 11 | Delivery: one page or two? | Trader/SEO | 2 | Sitemap has two; UX brief says one |
| 5 | Price filter: slider or buckets? | UX/Trader | 3 | Matrix says buckets |
| 12 | Wishlist hearts on product cards? | UX | 3 | Optional; needs an app |
| 13 | Replace placeholder brand "Maison Atelier Praline", phone, email, © 2024 | Founder | 3 | Placeholder data in mockups |
| 3 | Real backing for "12,000+ reviews", "since 1956", client logos? | Founder | 5 | Replace with verified data or remove |
| 4 | Which claims are provable per SKU (vegan, organic, Fairtrade, palm-oil-free)? | Trader/SEO | 5 | Add `palm_oil_free` metafield if kept |

> **Unhide this sheet.** It is the most important sheet for moving the project forward, and it can't be seen in the workbook as delivered.

---

## 13. Risks

| Risk | Severity | Why | Mitigation |
|---|---|---|---|
| Unproven claims (reviews count, "since 1956", organic, Fairtrade, palm oil, client logos, announcement-bar USPs) | **High** | Consumer-protection and greenwashing exposure; loss of trust | Decisions #3 and #4 before Gate 5; supplier proof on file; remove anything unproven |
| Heat damage / delivery promise | **High** | Chocolate melts; "1–2 days" may not hold in summer | Set heat threshold, cold-pack logic and blackout dates before publishing any promise |
| Trading inputs missing | **High** | SKUs, prices, margins, MOQ block design copy, filters and product load | Run a Gate 1 workshop with Founder and Trader |
| Allergen data | **High** | Food safety; legal requirement | Allergen summary near Add to Cart (#29), per-SKU data from supplier |
| Shopify plan unknown | Medium | Decides where gift message and delivery date can go | Decide Plus vs. not at Gate 2 |
| Scope creep (box builder, multi-address, invoicing, wishlist, hospitality) | Medium | Each needs an app or custom development | Cut or phase at Gate 1 |
| Placeholder brand data in designs | Medium | Could ship by mistake | Decision #13; add a QA check |
| Markets and languages undefined | Medium | Affects shipping zones, currency, translations, SEO | Decide target countries and languages at Gate 1 |
| Logo artwork intake | Medium | Wrong formats or no approval step means production errors | Define file types, size limit and approval flow (#23) |
| Analytics naming | Low–Med | GA4 ecommerce reports won't fill in | Rename to GA4's recommended events |
| Missing design files | Low–Med | Folder can't be checked against the designs | Add `07_VISUALS_AND_WIREFRAMES` to the pack |

---

## 14. Cross-file inconsistencies

1. Two identical filter-matrix CSVs.
2. Metafield count: schema has 21, checklist #3 says 20.
3. Small-gift price ceiling: €25 (assortment, filter buckets) vs. €15 (design).
4. Price filter: buckets (matrix) vs. slider (design) vs. range (Shopify native).
5. Pralines & Truffles filters: sitemap lists 5, matrix lists 2.
6. "Gifts" collection used in the filter matrix, checklist and assortment, but not in the sitemap.
7. "Add-ons" collection used in the assortment, but not in the sitemap.
8. Delivery: one template in the UX brief vs. two pages in the sitemap.
9. Top nav: "Delivery" is in the brief but missing from the design nav; labels differ ("Pralines & Ballotins", "Shop Gifts", "About Us").
10. Filter matrix data sources (`occasion`, `recipient`, `gift_level`, `corporate_use_case`, `personalisation_available`) missing from the metafield schema.
11. `click_and_collect_available` is meant for a "Delivery filter" that doesn't exist.
12. Quote form fields: inline form (#22) has no budget or logo upload; the sitemap's quote page lists both.
13. "Wedding" occasion filter has no matching collection.
14. Checklist #1 (Gate 2) depends on designs that are Gate 3 outputs.
15. The workbook Summary doesn't count "In progress" tasks.
16. Owner labels vary ("Shopify Designer/Developer", "Developer/Trader", "SEO/Ecommerce Trader"). Standardise them to the 6 roles: Founder, Ecommerce Trader, Shopify UX Designer, Shopify Developer, SEO Specialist, Brand Designer.
17. Only 2 of the 6 roles have a brief. SEO Specialist, Shopify Developer and Brand Designer have none.

---

## 15. Recommended next steps

**Immediately (housekeeping)**
1. Delete `filter_matrix_by_collection (1).csv`.
2. Unhide the "Open Decisions" sheet; treat the workbook as the master and retire the CSVs or mark them as superseded.
3. Add the wireframes/designs folder to the pack.
4. Add an "In progress" count to the workbook Summary.

**Gate 1 workshop (Founder + Trader)**
5. Answer decisions #2, #6, #7.
6. Lock the final SKU list, variants, price bands, margins, MOQ, sample-pack offer and seasonal campaign calendar.
7. Decide target countries, currencies and languages.
8. Define what "Phase 1" means.

**Gate 2 (architecture sign-off)**
9. Answer #1, #8, #9, #10, #11.
10. Finalise the metafield schema: fix the undecided types and add `occasion`, `recipient`, `gift_level`, `corporate_use_case`, a personalisation options list, and `palm_oil_free` / `price_band` if needed. Correct the count in checklist #3.
11. Decide on `/collections/gifts` and an Add-ons collection; settle filters for every collection.
12. Extend the SEO map to every must-launch indexable page; list structured-data types; confirm whether legacy redirects and hreflang are needed.
13. Rename GA4 events to GA4's recommended names; plan checkout and purchase tracking through Customer Events.
14. Define shipping zones, cut-offs, heat threshold, cold pack, blackout dates, damage and replacement rules (#38).
15. Make the inline quote form and the standalone quote page use the same fields.

**Gate 3 onward**
16. Design the missing templates: Pralines with Logo, Request a Quote, Delivery pages, cart drawer.
17. Run a claims and placeholder audit (decisions #3, #4, #13; announcement-bar USPs; client-logo permissions) as a hard condition for Gate 5.
18. Write short briefs for the SEO Specialist, Shopify Developer and Brand Designer, and add dates and owners to the project plan.
