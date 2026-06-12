from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from schemas.campaign_asset_brief_refinement import (
    RefineCampaignAssetBriefRequest,
    RefineCampaignAssetBriefResponse,
)
from services.campaign_asset_brief_refinement import (
    fallback_refine_campaign_asset_brief,
)
from services.llm_client import refine_campaign_asset_brief_with_llm
from services.supabase_service import get_supabase


router = APIRouter(prefix="/campaign-asset-briefs", tags=["Campaign Asset Briefs"])


def build_final_campaign_from_output(output: dict) -> dict:
    return {
        "campaign_headline": output.get("campaign_headline"),
        "campaign_angle": output.get("campaign_angle"),
        "buyer_insight": output.get("buyer_insight"),
        "caption": output.get("caption"),
        "whatsapp_copy": output.get("whatsapp_copy"),
        "offer_idea": output.get("offer_idea"),
        "story_flow": output.get("story_flow") or [],
        "poster_direction": output.get("poster_direction"),
        "reel_direction": output.get("reel_direction"),
        "primary_cta": output.get("primary_cta"),
        "do_rules": output.get("do_rules") or [],
        "avoid_rules": output.get("avoid_rules") or [],
        "confidence": output.get("confidence"),
        "campaign_score": output.get("campaign_score"),
        "quality_status": output.get("quality_status"),
        "quality_notes": output.get("quality_notes") or [],
        "improvements_applied": output.get("improvements_applied") or [],
        "risk_flags": output.get("risk_flags") or [],
    }


@router.post("/refine", response_model=RefineCampaignAssetBriefResponse)
async def refine_campaign_asset_brief_route(
    payload: RefineCampaignAssetBriefRequest,
):
    if not payload.refine_instruction.strip():
        raise HTTPException(
            status_code=400,
            detail="Refinement instruction is required.",
        )

    supabase = get_supabase()

    asset_result = (
        supabase.table("campaign_asset_briefs")
        .select("*")
        .eq("id", payload.asset_brief_id)
        .single()
        .execute()
    )

    if not asset_result.data:
        raise HTTPException(status_code=404, detail="Asset brief not found.")

    asset_brief = asset_result.data

    draft_result = (
        supabase.table("campaign_drafts")
        .select("*")
        .eq("id", asset_brief["draft_id"])
        .single()
        .execute()
    )

    if not draft_result.data:
        raise HTTPException(status_code=404, detail="Campaign draft not found.")

    draft = draft_result.data

    output_result = (
        supabase.table("campaign_outputs")
        .select("*")
        .eq("id", asset_brief["output_id"])
        .single()
        .execute()
    )

    if not output_result.data:
        raise HTTPException(status_code=404, detail="Campaign output not found.")

    final_campaign = build_final_campaign_from_output(output_result.data)

    brand_profile = None
    brand_profile_id = draft.get("brand_profile_id")

    if brand_profile_id:
        brand_result = (
            supabase.table("brand_profiles")
            .select("*")
            .eq("id", brand_profile_id)
            .single()
            .execute()
        )
        brand_profile = brand_result.data

    try:
        refined = refine_campaign_asset_brief_with_llm(
            brand_profile=brand_profile,
            campaign_draft=draft,
            final_campaign=final_campaign,
            asset_brief=asset_brief,
            refine_instruction=payload.refine_instruction,
        )
    except Exception:
        refined = fallback_refine_campaign_asset_brief(
            asset_brief=asset_brief,
            refine_instruction=payload.refine_instruction,
        )

    refinement_notes = asset_brief.get("refinement_notes") or []
    refinement_notes.append(payload.refine_instruction)

    new_refinement_count = int(asset_brief.get("refinement_count") or 0) + 1

    update_payload = {
        "creative_brief_title": refined["creative_brief_title"],

        "poster_prompt": refined["poster_prompt"],
        "image_generation_prompt": refined["image_generation_prompt"],
        "poster_layout_direction": refined["poster_layout_direction"],
        "poster_text_hierarchy": refined["poster_text_hierarchy"],
        "poster_design_rules": refined["poster_design_rules"],

        "reel_prompt": refined["reel_prompt"],
        "video_generation_prompt": refined["video_generation_prompt"],
        "reel_shot_list": refined["reel_shot_list"],
        "reel_sound_direction": refined["reel_sound_direction"],
        "reel_editing_style": refined["reel_editing_style"],

        "designer_notes": refined["designer_notes"],
        "asset_risks": refined["asset_risks"],

        "confidence": refined["confidence"],
        "status": "ready",

        "refinement_count": new_refinement_count,
        "last_refined_at": datetime.now(timezone.utc).isoformat(),
        "refinement_notes": refinement_notes,
    }

    update_result = (
        supabase.table("campaign_asset_briefs")
        .update(update_payload)
        .eq("id", payload.asset_brief_id)
        .execute()
    )

    if not update_result.data:
        raise HTTPException(
            status_code=500,
            detail="Could not update refined asset brief.",
        )

    row = update_result.data[0]

    return {
        "brief": {
            "id": row["id"],
            "output_id": row["output_id"],
            "draft_id": row["draft_id"],

            "creative_brief_title": row["creative_brief_title"],

            "poster_prompt": row["poster_prompt"],
            "image_generation_prompt": row["image_generation_prompt"],
            "poster_layout_direction": row["poster_layout_direction"],
            "poster_text_hierarchy": row["poster_text_hierarchy"] or [],
            "poster_design_rules": row["poster_design_rules"] or [],

            "reel_prompt": row["reel_prompt"],
            "video_generation_prompt": row["video_generation_prompt"],
            "reel_shot_list": row["reel_shot_list"] or [],
            "reel_sound_direction": row["reel_sound_direction"],
            "reel_editing_style": row["reel_editing_style"],

            "designer_notes": row["designer_notes"] or [],
            "asset_risks": row["asset_risks"] or [],

            "confidence": float(row["confidence"] or 0.75),
            "status": row["status"],

            "refinement_count": int(row["refinement_count"] or 0),
            "refinement_notes": row["refinement_notes"] or [],
        }
    }
