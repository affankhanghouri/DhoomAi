from fastapi import APIRouter, HTTPException

from schemas.final_campaign import GenerateFinalCampaignRequest, GenerateFinalCampaignResponse
from services.campaign_asset_brief_generator import fallback_campaign_asset_brief
from services.campaign_generated_asset_slots import create_default_asset_slots
from services.final_campaign_generator import fallback_final_campaign
from services.campaign_quality_gate import fallback_quality_check
from services.llm_client import (
    generate_campaign_asset_brief_with_llm,
    generate_final_campaign_with_llm,
    quality_check_final_campaign_with_llm,
)
from services.supabase_service import get_supabase


router = APIRouter(prefix="/campaigns", tags=["Final Campaign"])


def get_draft_and_brand(draft_id: str):
    supabase = get_supabase()
    draft_result = (
        supabase.table("campaign_drafts")
        .select("*")
        .eq("id", draft_id)
        .single()
        .execute()
    )

    if not draft_result.data:
        raise HTTPException(status_code=404, detail="Campaign draft not found.")

    draft = draft_result.data
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

    return draft, brand_profile


@router.post("/generate-final", response_model=GenerateFinalCampaignResponse)
async def generate_final_campaign_route(payload: GenerateFinalCampaignRequest):
    supabase = get_supabase()
    draft, brand_profile = get_draft_and_brand(payload.draft_id)

    if not draft.get("selected_angle_id"):
        raise HTTPException(
            status_code=400,
            detail="Select a campaign angle before final generation.",
        )

    if not draft.get("selected_variant_id"):
        raise HTTPException(
            status_code=400,
            detail="Select a campaign variant before final generation.",
        )

    try:
        final_campaign = generate_final_campaign_with_llm(
            brand_profile=brand_profile,
            campaign_draft=draft,
        )
    except Exception:
        final_campaign = fallback_final_campaign(
            brand_profile=brand_profile,
            campaign_draft=draft,
        )

    try:
        quality_result = quality_check_final_campaign_with_llm(
            brand_profile=brand_profile,
            campaign_draft=draft,
            final_campaign=final_campaign,
        )
    except Exception:
        quality_result = fallback_quality_check(final_campaign)

    final_campaign = quality_result["final_campaign"]
    quality_report = quality_result["quality_report"]

    insert_payload = {
        "draft_id": draft["id"],

        "campaign_headline": final_campaign["campaign_headline"],
        "campaign_angle": final_campaign["campaign_angle"],
        "buyer_insight": final_campaign["buyer_insight"],

        "caption": final_campaign["caption"],
        "whatsapp_copy": final_campaign["whatsapp_copy"],
        "offer_idea": final_campaign["offer_idea"],
        "story_flow": final_campaign["story_flow"],

        "poster_direction": final_campaign["poster_direction"],
        "reel_direction": final_campaign["reel_direction"],
        "primary_cta": final_campaign["primary_cta"],

        "do_rules": final_campaign["do_rules"],
        "avoid_rules": final_campaign["avoid_rules"],

        "confidence": final_campaign["confidence"],

        "campaign_score": quality_report["campaign_score"],
        "quality_status": quality_report["quality_status"],
        "quality_notes": quality_report["quality_notes"],
        "improvements_applied": quality_report["improvements_applied"],
        "risk_flags": quality_report["risk_flags"],

        "status": "ready",
    }

    output_result = (
        supabase.table("campaign_outputs")
        .insert(insert_payload)
        .execute()
    )

    if not output_result.data:
        raise HTTPException(
            status_code=500,
            detail="Could not save final campaign output.",
        )

    supabase.table("campaign_drafts").update({"status": "ready"}).eq(
        "id",
        draft["id"],
    ).execute()

    saved = output_result.data[0]

    try:
        asset_brief = generate_campaign_asset_brief_with_llm(
            brand_profile=brand_profile,
            campaign_draft=draft,
            final_campaign=final_campaign,
            quality_report=quality_report,
        )
    except Exception:
        asset_brief = fallback_campaign_asset_brief(
            campaign_draft=draft,
            final_campaign=final_campaign,
            quality_report=quality_report,
        )

    asset_payload = {
        "output_id": saved["id"],
        "draft_id": draft["id"],

        "creative_brief_title": asset_brief["creative_brief_title"],

        "poster_prompt": asset_brief["poster_prompt"],
        "image_generation_prompt": asset_brief["image_generation_prompt"],
        "poster_layout_direction": asset_brief["poster_layout_direction"],
        "poster_text_hierarchy": asset_brief["poster_text_hierarchy"],
        "poster_design_rules": asset_brief["poster_design_rules"],

        "reel_prompt": asset_brief["reel_prompt"],
        "video_generation_prompt": asset_brief["video_generation_prompt"],
        "reel_shot_list": asset_brief["reel_shot_list"],
        "reel_sound_direction": asset_brief["reel_sound_direction"],
        "reel_editing_style": asset_brief["reel_editing_style"],

        "designer_notes": asset_brief["designer_notes"],
        "asset_risks": asset_brief["asset_risks"],

        "confidence": asset_brief["confidence"],
        "status": "ready",
    }

    asset_insert_result = (
        supabase.table("campaign_asset_briefs")
        .insert(asset_payload)
        .execute()
    )

    if asset_insert_result.data:
        create_default_asset_slots(asset_insert_result.data[0])

    return {
        "output": {
            "id": saved["id"],
            "draft_id": saved["draft_id"],

            "campaign_headline": saved["campaign_headline"],
            "campaign_angle": saved["campaign_angle"],
            "buyer_insight": saved["buyer_insight"],

            "caption": saved["caption"],
            "whatsapp_copy": saved["whatsapp_copy"],
            "offer_idea": saved["offer_idea"],
            "story_flow": saved["story_flow"] or [],

            "poster_direction": saved["poster_direction"],
            "reel_direction": saved["reel_direction"],
            "primary_cta": saved["primary_cta"],

            "do_rules": saved["do_rules"] or [],
            "avoid_rules": saved["avoid_rules"] or [],

            "confidence": float(saved["confidence"] or 0.75),
            "campaign_score": saved["campaign_score"],
            "quality_status": saved["quality_status"],
            "quality_notes": saved["quality_notes"] or [],
            "improvements_applied": saved["improvements_applied"] or [],
            "risk_flags": saved["risk_flags"] or [],
            "status": saved["status"],
        }
    }
