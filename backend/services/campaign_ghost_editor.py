def build_current_campaign_from_output(output: dict) -> dict:
    return {
        "campaign_headline": output.get("campaign_headline") or "",
        "campaign_angle": output.get("campaign_angle") or "",
        "buyer_insight": output.get("buyer_insight") or "",
        "caption": output.get("caption") or "",
        "whatsapp_copy": output.get("whatsapp_copy") or "",
        "offer_idea": output.get("offer_idea") or "",
        "story_flow": output.get("story_flow") or [],
        "poster_direction": output.get("poster_direction") or "",
        "reel_direction": output.get("reel_direction") or "",
        "primary_cta": output.get("primary_cta") or "",
        "do_rules": output.get("do_rules") or [],
        "avoid_rules": output.get("avoid_rules") or [],
        "confidence": output.get("confidence") or 0.75,
    }


def fallback_ghost_edit_campaign(
    instruction: str,
    current_campaign: dict,
    current_asset_brief: dict | None,
) -> dict:
    updated_campaign = {
        **current_campaign,
        "caption": (
            f"{current_campaign.get('caption', '')}\n\n"
            f"Refinement applied: {instruction}"
        ).strip(),
        "whatsapp_copy": (
            f"{current_campaign.get('whatsapp_copy', '')}\n\n"
            f"Update: {instruction}"
        ).strip(),
        "poster_direction": (
            f"{current_campaign.get('poster_direction', '')} "
            f"Refine the poster direction with this instruction: {instruction}."
        ).strip(),
        "reel_direction": (
            f"{current_campaign.get('reel_direction', '')} "
            f"Refine the reel direction with this instruction: {instruction}."
        ).strip(),
        "confidence": min(float(current_campaign.get("confidence") or 0.75) + 0.03, 0.88),
    }

    if current_asset_brief:
        updated_asset_brief = {
            **current_asset_brief,
            "poster_prompt": (
                f"{current_asset_brief.get('poster_prompt', '')}\n\n"
                f"Ghost Editor refinement: {instruction}"
            ).strip(),
            "image_generation_prompt": (
                f"{current_asset_brief.get('image_generation_prompt', '')}\n\n"
                f"Apply this refinement: {instruction}. Keep product as hero."
            ).strip(),
            "reel_prompt": (
                f"{current_asset_brief.get('reel_prompt', '')}\n\n"
                f"Ghost Editor refinement: {instruction}"
            ).strip(),
            "video_generation_prompt": (
                f"{current_asset_brief.get('video_generation_prompt', '')}\n\n"
                f"Apply this refinement: {instruction}."
            ).strip(),
            "designer_notes": list(
                dict.fromkeys(
                    (current_asset_brief.get("designer_notes") or [])
                    + [f"Ghost Editor instruction: {instruction}"]
                )
            )[:8],
            "confidence": min(float(current_asset_brief.get("confidence") or 0.75) + 0.03, 0.88),
        }
    else:
        updated_asset_brief = {
            "creative_brief_title": "Ghost Edited Creative Brief",
            "poster_prompt": f"Create a refined poster based on this instruction: {instruction}",
            "image_generation_prompt": f"Premium product poster, product as hero, refinement: {instruction}",
            "poster_layout_direction": "Clean hierarchy, product hero, clear CTA.",
            "poster_text_hierarchy": ["Headline", "Buyer benefit", "CTA"],
            "poster_design_rules": [
                "Keep product as hero",
                "Avoid clutter",
                "Do not add fake claims",
            ],
            "reel_prompt": f"Create a refined reel based on this instruction: {instruction}",
            "video_generation_prompt": f"Vertical 9:16 product reel, refinement: {instruction}",
            "reel_shot_list": [
                "Opening product close-up",
                "Product detail",
                "Buyer benefit",
                "CTA ending",
            ],
            "reel_sound_direction": "Modern clean sound.",
            "reel_editing_style": "Clean product-focused cuts.",
            "designer_notes": [f"Ghost Editor instruction: {instruction}"],
            "asset_risks": [],
            "confidence": 0.7,
        }

    return {
        "action_summary": "Applied the instruction as a lightweight Ghost Editor refinement.",
        "changed_fields": [
            "caption",
            "whatsapp_copy",
            "poster_direction",
            "reel_direction",
            "asset_brief",
        ],
        "updated_campaign": updated_campaign,
        "updated_asset_brief": updated_asset_brief,
    }
