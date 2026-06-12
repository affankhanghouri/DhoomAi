def fallback_final_campaign(
    brand_profile: dict | None,
    campaign_draft: dict,
) -> dict:
    product = campaign_draft.get("product_name") or "your product"
    category = campaign_draft.get("category") or "your category"
    offer = campaign_draft.get("price_offer") or "available now"
    action = campaign_draft.get("buyer_action") or "message to order"

    angle = campaign_draft.get("selected_angle_title") or "Clear product push"
    variant = campaign_draft.get("selected_variant_name") or "Bold Ad"
    visual = campaign_draft.get("selected_variant_visual") or (
        "Keep product as hero with clear CTA."
    )

    tone = "modern, clear, and seller-friendly"
    if brand_profile:
        tone = brand_profile.get("tone") or tone

    return {
        "campaign_headline": f"{product} — ready for your next order",
        "campaign_angle": (
            f"Use the {angle} angle to position {product} as a clear, "
            f"worth-considering choice in {category}."
        ),
        "buyer_insight": (
            "Pakistani online buyers usually need product clarity, trust, "
            "price/value clarity, and an easy order action before they message."
        ),
        "caption": (
            f"{product} is available now.\n\n"
            f"Built around: {angle}.\n"
            f"Offer: {offer}.\n\n"
            f"{action}."
        ),
        "whatsapp_copy": (
            f"Hi! {product} is available now. {offer}. "
            f"Reply here and we’ll help you order quickly."
        ),
        "offer_idea": offer,
        "story_flow": [
            f"Story 1: Show {product} clearly with a clean product visual.",
            f"Story 2: Highlight the main buyer reason using the {angle} angle.",
            f"Story 3: Show offer/value: {offer}.",
            f"Story 4: End with CTA: {action}.",
        ],
        "poster_direction": (
            f"{variant} style. {visual} Keep text minimal, make the product "
            "the hero, show one buyer reason, and place CTA clearly."
        ),
        "reel_direction": (
            f"Open with a close product shot, show one main benefit, add quick "
            f"offer/value frame, then end with CTA: {action}."
        ),
        "primary_cta": action,
        "do_rules": [
            "Keep product as the hero.",
            "Use one clear buyer reason.",
            "Make ordering action obvious.",
            f"Keep tone {tone}.",
        ],
        "avoid_rules": [
            "Do not overload the poster with text.",
            "Do not use generic claims without proof.",
            "Do not force slang if it does not match the brand.",
        ],
        "confidence": 0.72,
    }