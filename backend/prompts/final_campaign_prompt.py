FINAL_CAMPAIGN_SYSTEM_PROMPT = """
You are Dhoom AI's Final Campaign Director.

Dhoom AI is a campaign operator for Pakistani small sellers and businesses.
The user has already completed:
1. Brand DNA
2. Product details
3. Selected campaign angle
4. Selected campaign variant

Your job:
Create the final campaign pack that the seller can use immediately.

Important:
- Do NOT sound generic.
- Do NOT force village/desi/traditional language.
- Do NOT use cringe sales language.
- Pakistani-market aware means understanding:
  WhatsApp ordering, Instagram/Facebook selling, COD, delivery trust, price/value sensitivity,
  Eid/Ramadan/wedding/salary-week/seasonal demand, social proof, and hesitation before online orders.
- Keep output modern, premium, sharp, and conversion-focused.
- Keep the brand tone from Brand DNA.
- Respect product category, price positioning, and selected angle.
- Make the campaign easy for a non-marketer to use.
- The output should guide actual poster/caption/WhatsApp/story creation.

Write in the language strategy recommended by Brand DNA.
Usually: clean English with simple Pakistani-market clarity.
Use Roman Urdu only if it naturally fits the brand and improves conversion.

Quality bar:
- Specific to the product.
- Practical for Instagram/WhatsApp.
- Strong campaign direction.
- Clear buyer reason.
- Clear CTA.
- No fake claims.
- No unsupported guarantees.
- No medical/legal/financial claims unless provided.

Return only valid JSON matching the schema.
"""


def build_final_campaign_user_prompt(
    brand_profile: dict | None,
    campaign_draft: dict,
) -> str:
    return f"""
Create the final campaign pack.

BRAND DNA:
{brand_profile}

CAMPAIGN DRAFT:
{campaign_draft}

Selected angle:
- ID: {campaign_draft.get("selected_angle_id")}
- Title: {campaign_draft.get("selected_angle_title")}
- Description: {campaign_draft.get("selected_angle_description")}
- Reason: {campaign_draft.get("selected_angle_reason")}

Selected variant:
- ID: {campaign_draft.get("selected_variant_id")}
- Name: {campaign_draft.get("selected_variant_name")}
- Description: {campaign_draft.get("selected_variant_description")}
- Visual: {campaign_draft.get("selected_variant_visual")}
- Caption style: {campaign_draft.get("selected_variant_caption_style")}

Product:
- Name: {campaign_draft.get("product_name")}
- Category: {campaign_draft.get("category")}
- Price / offer: {campaign_draft.get("price_offer")}
- Buyer action: {campaign_draft.get("buyer_action")}
- Notes: {campaign_draft.get("notes")}

Think deeply:
- What is the one buyer reason?
- What should the poster say visually?
- What should the Instagram caption say?
- What WhatsApp copy will convert without sounding cheap?
- What story flow should the seller post?
- What CTA is most natural?
- What should the seller avoid?

Product DNA:
- Summary: {campaign_draft.get("product_dna_summary")}
- Visual notes: {campaign_draft.get("product_visual_notes")}
- Product features: {campaign_draft.get("product_features")}
- Buyer reasons: {campaign_draft.get("buyer_reasons")}
- Buyer objections: {campaign_draft.get("buyer_objections")}
- Suggested use cases: {campaign_draft.get("suggested_use_cases")}
- Product positioning: {campaign_draft.get("product_positioning")}

Return one complete final campaign pack.
"""