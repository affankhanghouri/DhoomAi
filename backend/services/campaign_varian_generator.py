def fallback_campaign_variants(
    brand_profile: dict | None,
    campaign_draft: dict,
) -> list[dict]:
    product = campaign_draft.get("product_name") or "this product"
    angle = campaign_draft.get("selected_angle_title") or "selected angle"
    category = campaign_draft.get("category") or "product"
    tone = "modern and clear"

    if brand_profile:
        tone = brand_profile.get("tone") or tone

    return [
        {
            "variant_id": "minimal-premium",
            "name": "Minimal Premium",
            "description": f"A clean, polished campaign for {product} built around {angle}.",
            "visual_direction": "Use product as the hero, dark or clean background, limited text, premium spacing, and one clear CTA.",
            "caption_style": f"Short, confident, and {tone}. Focus on quality and clarity.",
            "whatsapp_style": "Direct and polite. Make ordering simple without sounding pushy.",
            "poster_layout": "Product center, small offer/benefit badge, CTA at bottom, minimal extra elements.",
            "why_it_fits": f"This works when {category} needs to look more valuable and trustworthy.",
            "confidence": 0.8,
        },
        {
            "variant_id": "bold-sales-ad",
            "name": "Bold Sales Ad",
            "description": f"A high-energy campaign for {product} with a stronger selling push.",
            "visual_direction": "Use bold headline, strong contrast, visible offer, product close-up, and clear WhatsApp/order CTA.",
            "caption_style": "Punchy, benefit-led, conversion-focused, and easy to understand.",
            "whatsapp_style": "Fast and action-oriented. Mention availability, offer, and how to order.",
            "poster_layout": "Large headline on top, product in middle, offer badge on side, CTA button at bottom.",
            "why_it_fits": "This works when the seller wants quick inquiries, clicks, or WhatsApp orders.",
            "confidence": 0.76,
        },
        {
            "variant_id": "story-lifestyle",
            "name": "Story / Lifestyle",
            "description": f"A more relatable campaign for {product} using buyer context and product benefit.",
            "visual_direction": "Use lifestyle framing, soft background, human-use context if possible, and benefit-led text.",
            "caption_style": "Warm, relatable, and story-driven while staying concise.",
            "whatsapp_style": "Helpful and conversational. Make the buyer feel guided, not pressured.",
            "poster_layout": "Problem/need hook, product visual, benefit line, soft CTA.",
            "why_it_fits": "This works when the product needs emotional relevance or daily-use connection.",
            "confidence": 0.72,
        },
    ]


def fallback_refine_variant(
    variant: dict,
    refine_instruction: str,
) -> dict:
    return {
        **variant,
        "name": f"{variant.get('name', 'Variant')} — refined",
        "description": f"{variant.get('description', '')} Refined with this direction: {refine_instruction}",
        "visual_direction": f"{variant.get('visual_direction', '')} Make the layout cleaner and the CTA stronger.",
        "caption_style": f"{variant.get('caption_style', '')} Make the message sharper and more conversion-focused.",
        "whatsapp_style": f"{variant.get('whatsapp_style', '')} Keep it simple, direct, and easy to reply to.",
        "poster_layout": f"{variant.get('poster_layout', '')} Reduce clutter and improve hierarchy.",
        "why_it_fits": f"{variant.get('why_it_fits', '')} The refinement improves clarity and buyer action.",
        "confidence": min(float(variant.get("confidence", 0.75)) + 0.03, 0.92),
    }