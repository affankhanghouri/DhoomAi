"""Campaign angle prompt placeholder."""
def build_campaign_angles_user_prompt(
    brand_profile: dict | None,
    campaign_draft: dict,
) -> str:
    return f"""
Generate 4 smart marketing angle cards for this campaign.

BRAND DNA:
{brand_profile}

PRODUCT DNA + CAMPAIGN DRAFT:
{campaign_draft}

Important product understanding:
- Product DNA summary: {campaign_draft.get("product_dna_summary")}
- Visual notes: {campaign_draft.get("product_visual_notes")}
- Product features: {campaign_draft.get("product_features")}
- Buyer reasons: {campaign_draft.get("buyer_reasons")}
- Buyer objections: {campaign_draft.get("buyer_objections")}
- Product positioning: {campaign_draft.get("product_positioning")}

Think deeply:
- What story should this product tell?
- What would make Pakistani online buyers stop and consider it?
- What angle fits the brand tone?
- What angle answers buyer objections?
- What angle can convert on Instagram/WhatsApp?
- What angle should be avoided because it feels generic?

Return only 4 strong angle cards.
"""