def fallback_refine_campaign_asset_brief(
    asset_brief: dict,
    refine_instruction: str,
) -> dict:
    instruction = refine_instruction.strip()

    refined = {
        "creative_brief_title": asset_brief.get("creative_brief_title")
        or "Refined Creative Brief",

        "poster_prompt": (
            f"{asset_brief.get('poster_prompt', '')}\n\n"
            f"Refinement direction: {instruction}. "
            "Make the poster more focused, cleaner, and easier to execute."
        ),

        "image_generation_prompt": (
            f"{asset_brief.get('image_generation_prompt', '')}\n\n"
            f"Apply this refinement: {instruction}. "
            "Keep the product as hero, avoid clutter, maintain premium composition, "
            "and do not add unsupported claims."
        ),

        "poster_layout_direction": (
            f"{asset_brief.get('poster_layout_direction', '')} "
            f"Refine with this direction: {instruction}. "
            "Improve hierarchy, spacing, CTA visibility, and visual clarity."
        ),

        "poster_text_hierarchy": asset_brief.get("poster_text_hierarchy") or [
            "Main headline",
            "One buyer benefit",
            "CTA",
        ],

        "poster_design_rules": list(
            dict.fromkeys(
                (asset_brief.get("poster_design_rules") or [])
                + [
                    "Keep product as the hero",
                    "Reduce clutter",
                    "Improve CTA visibility",
                    "Do not add fake claims",
                ]
            )
        )[:8],

        "reel_prompt": (
            f"{asset_brief.get('reel_prompt', '')}\n\n"
            f"Refinement direction: {instruction}. "
            "Make the reel more focused, practical, and conversion-ready."
        ),

        "video_generation_prompt": (
            f"{asset_brief.get('video_generation_prompt', '')}\n\n"
            f"Apply this refinement: {instruction}. "
            "Keep vertical 9:16, product-focused shots, clear ending CTA, and modern editing."
        ),

        "reel_shot_list": asset_brief.get("reel_shot_list") or [
            "Opening product close-up",
            "Product detail shot",
            "Buyer benefit frame",
            "Value/offer frame",
            "CTA ending",
        ],

        "reel_sound_direction": (
            asset_brief.get("reel_sound_direction")
            or "Modern upbeat sound with clean transitions."
        ),

        "reel_editing_style": (
            asset_brief.get("reel_editing_style")
            or "Clean product-focused cuts with readable CTA ending."
        ),

        "designer_notes": list(
            dict.fromkeys(
                (asset_brief.get("designer_notes") or [])
                + [
                    f"User refinement: {instruction}",
                    "Keep strategy intact",
                    "Do not add unsupported claims",
                ]
            )
        )[:8],

        "asset_risks": asset_brief.get("asset_risks") or [],
        "confidence": min(float(asset_brief.get("confidence") or 0.72) + 0.04, 0.88),
    }

    return refined
