def fallback_campaign_asset_brief(
    campaign_draft: dict,
    final_campaign: dict,
    quality_report: dict,
) -> dict:
    product = campaign_draft.get("product_name") or "the product"
    category = campaign_draft.get("category") or "product"
    headline = final_campaign.get("campaign_headline") or product
    cta = final_campaign.get("primary_cta") or "Message to order"
    poster_direction = final_campaign.get("poster_direction") or ""
    reel_direction = final_campaign.get("reel_direction") or ""

    return {
        "creative_brief_title": f"{product} Creative Execution Brief",
        "poster_prompt": (
            f"Create a premium Instagram/Facebook product poster for {product}. "
            f"Category: {category}. Use the campaign headline: {headline}. "
            f"Keep product as the hero, use clean spacing, strong hierarchy, and CTA: {cta}. "
            f"Direction: {poster_direction}"
        ),
        "image_generation_prompt": (
            f"Premium social media product ad for {product}, clean modern layout, "
            f"product-centered composition, polished lighting, minimal clutter, "
            f"high-end ecommerce look, clear space for headline and CTA. "
            f"No fake badges, no fake reviews, no unsupported claims."
        ),
        "poster_layout_direction": (
            "Product in center or right side, headline at top-left, one benefit line below, "
            "CTA button at bottom, offer/value badge only if provided by seller."
        ),
        "poster_text_hierarchy": [
            f"Headline: {headline}",
            "One short buyer benefit",
            f"CTA: {cta}",
        ],
        "poster_design_rules": [
            "Keep product as the hero",
            "Use one main headline only",
            "Avoid too much text",
            "Do not add fake discounts or fake reviews",
            "Make CTA clearly visible",
        ],
        "reel_prompt": (
            f"Create a short vertical reel for {product}. Open with a strong product shot, "
            f"show the main buyer reason, show product detail, then end with CTA: {cta}. "
            f"Direction: {reel_direction}"
        ),
        "video_generation_prompt": (
            f"Vertical 9:16 premium product ad video for {product}. Fast clean cuts, "
            f"macro product shots, social-commerce style, modern Pakistani ecommerce feel, "
            f"clear final CTA frame. Avoid fake claims and clutter."
        ),
        "reel_shot_list": [
            "Shot 1: Fast opening product close-up",
            "Shot 2: Show product texture/detail/use-case",
            "Shot 3: Add one buyer benefit visually",
            "Shot 4: Show offer/value if provided",
            f"Shot 5: End with CTA: {cta}",
        ],
        "reel_sound_direction": (
            "Modern upbeat sound, clean transitions, not overly dramatic unless brand is bold."
        ),
        "reel_editing_style": (
            "Short vertical cuts, product-focused, polished pacing, readable CTA ending."
        ),
        "designer_notes": [
            "Use campaign output as source of truth",
            "Do not add unsupported claims",
            "Keep visuals aligned with brand tone",
            "Make design usable for Instagram and Facebook",
        ],
        "asset_risks": quality_report.get("risk_flags", []),
        "confidence": 0.72,
    }