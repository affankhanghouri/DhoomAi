import re


def contains_any(text: str, words: list[str]) -> bool:
    text = text.lower()
    return any(word.lower() in text for word in words)


def guess_category(text: str) -> str:
    checks = [
        ("Fashion / Clothing", ["fashion", "clothing", "wear", "dress", "kurti", "suit", "abaya", "shirt", "jeans"]),
        ("Food / Restaurant", ["restaurant", "food", "menu", "burger", "pizza", "biryani", "cafe", "kitchen"]),
        ("Beauty / Cosmetics", ["beauty", "cosmetic", "skin", "makeup", "serum", "cream", "salon"]),
        ("Shoes / Footwear", ["shoes", "footwear", "sneaker", "sandals", "heels", "chappal"]),
        ("Electronics", ["mobile", "phone", "laptop", "watch", "earbuds", "charger", "electronics"]),
        ("Home / Lifestyle", ["home", "decor", "furniture", "bedsheet", "curtain", "kitchen"]),
    ]

    for category, words in checks:
        if contains_any(text, words):
            return category

    return "General Business"


def guess_tone(text: str) -> str:
    if contains_any(text, ["premium", "luxury", "elegant", "exclusive", "signature"]):
        return "Premium, polished, confident"

    if contains_any(text, ["sale", "discount", "offer", "deal", "free delivery"]):
        return "Direct, offer-led, conversion-focused"

    if contains_any(text, ["handmade", "homemade", "family", "crafted", "organic"]):
        return "Warm, personal, trust-building"

    return "Simple, helpful, seller-friendly"


def guess_price_positioning(text: str) -> str:
    if contains_any(text, ["luxury", "premium", "exclusive", "signature"]):
        return "Premium"

    if contains_any(text, ["cheap", "affordable", "budget", "low price", "discount"]):
        return "Affordable"

    if contains_any(text, ["sale", "offer", "deal"]):
        return "Value / offer-driven"

    return "Mid-market"


def guess_target_audience(category: str) -> str:
    if category == "Fashion / Clothing":
        return "Style-conscious Pakistani buyers looking for outfits, daily wear, or occasion wear."

    if category == "Food / Restaurant":
        return "Local food buyers who want taste, convenience, and quick ordering."

    if category == "Beauty / Cosmetics":
        return "Beauty-conscious buyers looking for trust, results, and product quality."

    if category == "Shoes / Footwear":
        return "Buyers looking for comfort, style, and reliable everyday footwear."

    if category == "Electronics":
        return "Practical buyers comparing features, price, and trust before ordering."

    return "Pakistani online buyers who need clarity, trust, and a simple reason to order."


def extract_brand_name(context: dict) -> str:
    title = context.get("title", "")
    domain = context.get("domain", "")

    if title:
        cleaned = re.split(r"[-|–—]", title)[0].strip()
        if cleaned:
            return cleaned[:60]

    return domain.replace("www.", "").split(".")[0].title()


def build_selling_points(text: str) -> list[str]:
    points = []

    if contains_any(text, ["free delivery", "delivery", "shipping"]):
        points.append("Delivery / shipping available")

    if contains_any(text, ["cash on delivery", "cod"]):
        points.append("Cash on delivery option")

    if contains_any(text, ["premium", "quality", "best quality", "original"]):
        points.append("Quality-focused product positioning")

    if contains_any(text, ["discount", "sale", "offer", "deal"]):
        points.append("Offer or discount potential")

    if contains_any(text, ["new arrival", "new collection", "latest"]):
        points.append("New arrival / fresh collection angle")

    if not points:
        points.append("Needs clearer product benefits for stronger campaign positioning")

    return points[:5]


def build_trust_signals(text: str) -> list[str]:
    signals = []

    if contains_any(text, ["reviews", "rating", "testimonial"]):
        signals.append("Customer reviews or ratings mentioned")

    if contains_any(text, ["delivery", "shipping"]):
        signals.append("Delivery information mentioned")

    if contains_any(text, ["return", "exchange", "refund"]):
        signals.append("Return or exchange policy mentioned")

    if contains_any(text, ["contact", "whatsapp", "phone"]):
        signals.append("Contact or WhatsApp ordering available")

    if not signals:
        signals.append("Trust signals are weak or not clearly visible")

    return signals[:5]


def build_weaknesses(text: str) -> list[str]:
    weaknesses = []

    if not contains_any(text, ["whatsapp", "order", "buy", "shop", "contact"]):
        weaknesses.append("Ordering action is not very clear")

    if not contains_any(text, ["delivery", "shipping", "cod", "return", "exchange"]):
        weaknesses.append("Delivery, COD, or return trust signals are not clear")

    if len(text) < 1200:
        weaknesses.append("Website has limited text for strong brand understanding")

    if not weaknesses:
        weaknesses.append("Brand can improve by making campaign angles sharper")

    return weaknesses[:4]


def analyze_brand_dna(context: dict) -> dict:
    text = context["text"]
    category = guess_category(text)
    brand_name = extract_brand_name(context)
    tone = guess_tone(text)
    price_positioning = guess_price_positioning(text)
    target_audience = guess_target_audience(category)

    selling_points = build_selling_points(text)
    trust_signals = build_trust_signals(text)
    weaknesses = build_weaknesses(text)

    summary = (
        f"{brand_name} appears to be a {category.lower()} brand. "
        f"The brand should communicate with a {tone.lower()} style and focus on "
        f"clear product benefits, trust, and easy ordering."
    )

    visual_style = (
        "Use clean product-focused visuals, strong contrast, readable offer text, "
        "and a direct WhatsApp/order CTA."
    )

    campaign_rules = {
        "do": [
            "Keep product as the hero.",
            "Use one clear campaign angle per post.",
            "Make the buyer action obvious.",
            "Use Pakistani buyer context and simple language.",
        ],
        "avoid": [
            "Do not overload poster with too much text.",
            "Do not create generic captions.",
            "Do not use a campaign angle that ignores product category.",
        ],
        "poster_rules": [
            "Keep the product clearly visible.",
            "Use one strong headline and one direct CTA.",
            "Make offer or delivery details readable.",
        ],
        "caption_rules": [
            "Start with the main buyer reason.",
            "Keep the language simple and conversion-focused.",
            "End with one clear WhatsApp/order action.",
        ],
    }

    confidence = 0.7
    if "limited text" in " ".join(weaknesses).lower():
        confidence = 0.55

    return {
        "brand_name": brand_name,
        "business_type": "Online seller / small business",
        "category": category,
        "summary": summary,
        "target_audience": target_audience,
        "tone": tone,
        "visual_style": visual_style,
        "price_positioning": price_positioning,
        "selling_points": selling_points,
        "trust_signals": trust_signals,
        "weaknesses": weaknesses,
        "campaign_rules": campaign_rules,
        "pakistani_market_context": {
            "buyer_mindset": "Pakistani buyers usually need clear value, trust, simple ordering, and confidence before purchasing online.",
            "trust_barriers": [
                "Product quality uncertainty",
                "Delivery reliability",
                "Return/exchange clarity",
                "Seller trust on social platforms",
            ],
            "purchase_triggers": [
                "Clear offer",
                "Strong product visual",
                "Delivery/COD clarity",
                "Social proof",
            ],
            "seasonal_relevance": [
                "Ramadan",
                "Eid",
                "Wedding season",
                "Salary week",
                "Weekend buying",
            ],
            "platform_behavior": "Campaigns should work well for Instagram, Facebook, and WhatsApp ordering behavior.",
        },
        "angle_strategy": {
            "best_angles": [
                {
                    "title": "Premium look",
                    "why_it_works": "It improves perceived value without looking cheap.",
                    "when_to_use": "Use when product visuals look polished or aspirational.",
                },
                {
                    "title": "Offer push",
                    "why_it_works": "Pakistani buyers respond well when value and urgency are clear.",
                    "when_to_use": "Use when there is discount, bundle, free delivery, or limited stock.",
                },
                {
                    "title": "Trust and delivery",
                    "why_it_works": "It reduces hesitation for online ordering.",
                    "when_to_use": "Use when seller needs more WhatsApp conversions.",
                },
            ],
            "bad_angles": [
                "Overly generic lifestyle claims",
                "Too much text on poster",
                "Forced slang that does not match the brand",
            ],
            "default_campaign_direction": "Use a clear product-first campaign with one strong buyer reason and one direct CTA.",
        },
        "content_language_strategy": {
            "primary_language": "English with simple Pakistani-market wording",
            "roman_urdu_usage": "Use lightly only when it improves relatability or matches the brand.",
            "english_usage": "Use for premium, clean, and modern positioning.",
            "tone_warning": "Avoid forced desi slang, village stereotypes, or overly casual language unless brand requires it.",
        },
        "raw_context": text[:5000],
        "confidence": confidence,
    }
