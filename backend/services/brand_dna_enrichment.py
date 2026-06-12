def fallback_enrich_brand_dna(
    brand_profile: dict,
    answers: dict,
) -> dict:
    previous_confidence = float(brand_profile.get("confidence") or 0.55)

    mostly_sell = answers.get("mostly_sell") or "the seller's products"
    usual_buyers = answers.get("usual_buyers") or brand_profile.get("target_audience") or "online buyers"
    product_strength = answers.get("product_strength") or "clear value and product quality"
    tone_preference = answers.get("brand_tone_preference") or brand_profile.get("tone") or "modern and clear"
    avoid_preference = answers.get("avoid_preference") or "generic claims and cluttered content"

    new_confidence = min(max(previous_confidence + 0.18, 0.70), 0.84)

    return {
        "brand_name": brand_profile.get("brand_name") or "Untitled brand",
        "business_type": brand_profile.get("business_type") or "online seller",
        "category": mostly_sell,
        "summary": (
            f"This brand mainly sells {mostly_sell} to {usual_buyers}. "
            f"The campaign direction should focus on {product_strength}, while keeping "
            f"the tone {tone_preference}."
        ),
        "target_audience": usual_buyers,
        "tone": tone_preference,
        "visual_style": brand_profile.get("visual_style") or "clean, product-focused, and modern",
        "price_positioning": brand_profile.get("price_positioning") or "value-focused",
        "pakistani_market_context": {
            "buyer_behavior": (
                "Buyers need quick clarity, product trust, and simple order instructions before messaging."
            ),
            "trust_barriers": (
                "Quality uncertainty, delivery confidence, price comparison, and fear of overpromising."
            ),
            "selling_channels": (
                "Instagram/Facebook posts, WhatsApp messages/status, and direct inquiry-based selling."
            ),
            "seasonal_moments": (
                "Can use Eid, Ramadan, wedding season, salary-week, weekend drops, and category-specific moments."
            ),
            "price_sensitivity": (
                "Price/value must be clear without making the brand feel cheap."
            ),
        },
        "selling_points": [
            product_strength,
            f"Clear fit for {usual_buyers}",
            "Easy WhatsApp/social ordering",
        ],
        "trust_signals": [
            "Clear product visuals",
            "Simple ordering instructions",
            "Consistent brand tone",
        ],
        "weaknesses": [
            "Needs more real customer proof if not already shown",
            "Needs clear delivery/order information",
            f"Should avoid: {avoid_preference}",
        ],
        "campaign_rules": {
            "do": [
                "Keep product benefit clear",
                "Use the selected brand tone consistently",
                "Make ordering action obvious",
                "Show trust and value without overclaiming",
            ],
            "avoid": [
                avoid_preference,
                "Too much text on posters",
                "Unsupported claims",
                "Generic AI-style captions",
            ],
            "best_campaign_angles": [
                "Product value angle",
                "Trust and clarity angle",
                "Lifestyle/use-case angle",
                "Offer or drop angle",
            ],
            "poster_rules": [
                "Use product as hero",
                "One main hook only",
                "Clear CTA",
                "Avoid clutter",
            ],
            "caption_rules": [
                "Start with buyer reason",
                "Keep it short and direct",
                "Mention order action",
                "Avoid fake urgency",
            ],
        },
        "angle_strategy": {
            "strongest_angles": [
                "Clear product value",
                "Trust-building",
                "Use-case/lifestyle",
                "Offer/drop campaign",
            ],
            "avoid_angles": [
                "Cheap-looking sale spam",
                "Forced slang",
                "Generic product captions",
            ],
            "positioning_notes": (
                f"Position around {product_strength} for {usual_buyers}, with a {tone_preference} tone."
            ),
        },
        "content_language_strategy": {
            "primary_language": "Simple English or mixed English depending on brand tone",
            "roman_urdu_usage": "Use only if it feels natural for the audience",
            "emoji_usage": "Use lightly, not excessively",
            "tone_notes": tone_preference,
        },
        "confidence": new_confidence,
    }