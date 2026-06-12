def fallback_product_dna(
    brand_profile: dict | None,
    campaign_draft: dict,
) -> dict:
    product_name = campaign_draft.get("product_name") or "this product"
    category = campaign_draft.get("category") or "general product"
    offer = campaign_draft.get("price_offer") or "available now"
    action = campaign_draft.get("buyer_action") or "message to order"

    brand_tone = "modern, clear, and seller-friendly"
    if brand_profile:
        brand_tone = brand_profile.get("tone") or brand_tone

    return {
        "product_type": category,
        "product_dna_summary": (
            f"{product_name} is a {category} product that should be marketed "
            f"with clear value, product visibility, and a simple buyer action."
        ),
        "product_visual_notes": (
            "Use the uploaded product image as the main visual reference. "
            "Keep product clear, uncluttered, and easy to understand."
        ),
        "product_features": [
            f"Belongs to {category}",
            f"Offer/price context: {offer}",
            "Needs clear product-first presentation",
        ],
        "buyer_reasons": [
            "Buyer can quickly understand what is being offered",
            "Clear price/offer can reduce hesitation",
            "Simple ordering action can increase WhatsApp response",
        ],
        "buyer_objections": [
            "Buyer may be unsure about quality",
            "Buyer may need delivery or order clarity",
            "Buyer may compare price/value with other sellers",
        ],
        "suggested_use_cases": [
            "Instagram post",
            "WhatsApp status",
            "Facebook product post",
        ],
        "product_positioning": (
            f"Position {product_name} with a {brand_tone} tone, one clear buyer "
            f"reason, and a direct CTA: {action}."
        ),
        "campaign_implications": {
            "best_angle_direction": "Use a clear product-benefit or value angle.",
            "best_visual_direction": "Show product clearly with strong hierarchy and one CTA.",
            "best_caption_direction": "Short, direct, and easy to act on.",
            "best_whatsapp_direction": "Simple order message with price/offer and availability.",
            "avoid_in_campaign": [
                "Too much text on poster",
                "Generic claims without proof",
                "Forced slang that does not match the brand",
            ],
        },
        "confidence": 0.62,
    }