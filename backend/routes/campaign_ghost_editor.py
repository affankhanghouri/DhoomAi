from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from schemas.campaign_ghost_editor import (
    RefineCampaignWithGhostEditorRequest,
    RefineCampaignWithGhostEditorResponse,
)
from services.campaign_ghost_editor import (
    build_current_campaign_from_output,
    fallback_ghost_edit_campaign,
)
from services.llm_client import refine_campaign_with_ghost_editor_llm
from services.supabase_service import get_supabase


router = APIRouter(prefix="/ghost-editor", tags=["Ghost Editor"])


def map_output(row: dict) -> dict:
    return {
        "id": row["id"],

        "campaign_headline": row["campaign_headline"],
        "campaign_angle": row["campaign_angle"],
        "buyer_insight": row["buyer_insight"],

        "caption": row["caption"],
        "whatsapp_copy": row["whatsapp_copy"],
        "offer_idea": row["offer_idea"],
        "story_flow": row["story_flow"] or [],

        "poster_direction": row["poster_direction"],
        "reel_direction": row["reel_direction"],
        "primary_cta": row["primary_cta"],

        "do_rules": row["do_rules"] or [],
        "avoid_rules": row["avoid_rules"] or [],

        "confidence": row.get("confidence"),

        "campaign_score": row.get("campaign_score"),
        "quality_status": row.get("quality_status"),
        "quality_notes": row.get("quality_notes") or [],
        "improvements_applied": row.get("improvements_applied") or [],
        "risk_flags": row.get("risk_flags") or [],

        "edit_count": int(row.get("edit_count") or 0),
        "edit_notes": row.get("edit_notes") or [],
    }


@router.post(
    "/campaign/refine",
    response_model=RefineCampaignWithGhostEditorResponse,
)
async def refine_campaign_with_ghost_editor_route(
    payload: RefineCampaignWithGhostEditorRequest,
):
    instruction = payload.instruction.strip()

    if not instruction:
        raise HTTPException(status_code=400, detail="Instruction is required.")

    supabase = get_supabase()

    output_result = (
        supabase.table("campaign_outputs")
        .select("*")
        .eq("id", payload.campaign_output_id)
        .single()
        .execute()
    )

    if not output_result.data:
        raise HTTPException(status_code=404, detail="Campaign output not found.")

    output = output_result.data

    draft_result = (
        supabase.table("campaign_drafts")
        .select("*")
        .eq("id", output["draft_id"])
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

    asset_brief_result = (
        supabase.table("campaign_asset_briefs")
        .select("*")
        .eq("output_id", output["id"])
        .execute()
    )

    asset_brief = asset_brief_result.data[0] if asset_brief_result.data else None

    current_campaign = build_current_campaign_from_output(output)

    try:
        edited = refine_campaign_with_ghost_editor_llm(
            instruction=instruction,
            brand_profile=brand_profile,
            campaign_draft=draft,
            current_campaign=current_campaign,
            current_asset_brief=asset_brief,
        )
    except Exception:
        edited = fallback_ghost_edit_campaign(
            instruction=instruction,
            current_campaign=current_campaign,
            current_asset_brief=asset_brief,
        )

    updated_campaign = edited["updated_campaign"]
    updated_asset_brief = edited["updated_asset_brief"]
    action_summary = edited["action_summary"]
    changed_fields = edited["changed_fields"]

    edit_notes = output.get("edit_notes") or []
    edit_notes.append(instruction)

    new_edit_count = int(output.get("edit_count") or 0) + 1

    output_update_payload = {
        "campaign_headline": updated_campaign["campaign_headline"],
        "campaign_angle": updated_campaign["campaign_angle"],
        "buyer_insight": updated_campaign["buyer_insight"],

        "caption": updated_campaign["caption"],
        "whatsapp_copy": updated_campaign["whatsapp_copy"],
        "offer_idea": updated_campaign["offer_idea"],
        "story_flow": updated_campaign["story_flow"],

        "poster_direction": updated_campaign["poster_direction"],
        "reel_direction": updated_campaign["reel_direction"],
        "primary_cta": updated_campaign["primary_cta"],

        "do_rules": updated_campaign["do_rules"],
        "avoid_rules": updated_campaign["avoid_rules"],
        "confidence": updated_campaign["confidence"],

        "edit_count": new_edit_count,
        "edit_notes": edit_notes,
        "last_edited_at": datetime.now(timezone.utc).isoformat(),
    }

    output_update_result = (
        supabase.table("campaign_outputs")
        .update(output_update_payload)
        .eq("id", output["id"])
        .execute()
    )

    if not output_update_result.data:
        raise HTTPException(status_code=500, detail="Could not update campaign.")

    saved_output = output_update_result.data[0]

    if asset_brief:
        asset_notes = asset_brief.get("refinement_notes") or []
        asset_notes.append(instruction)

        asset_update_payload = {
            "creative_brief_title": updated_asset_brief["creative_brief_title"],
            "poster_prompt": updated_asset_brief["poster_prompt"],
            "image_generation_prompt": updated_asset_brief["image_generation_prompt"],
            "poster_layout_direction": updated_asset_brief["poster_layout_direction"],
            "poster_text_hierarchy": updated_asset_brief["poster_text_hierarchy"],
            "poster_design_rules": updated_asset_brief["poster_design_rules"],

            "reel_prompt": updated_asset_brief["reel_prompt"],
            "video_generation_prompt": updated_asset_brief["video_generation_prompt"],
            "reel_shot_list": updated_asset_brief["reel_shot_list"],
            "reel_sound_direction": updated_asset_brief["reel_sound_direction"],
            "reel_editing_style": updated_asset_brief["reel_editing_style"],

            "designer_notes": updated_asset_brief["designer_notes"],
            "asset_risks": updated_asset_brief["asset_risks"],
            "confidence": updated_asset_brief["confidence"],

            "refinement_count": int(asset_brief.get("refinement_count") or 0) + 1,
            "refinement_notes": asset_notes,
            "last_refined_at": datetime.now(timezone.utc).isoformat(),
        }

        supabase.table("campaign_asset_briefs").update(
            asset_update_payload
        ).eq("id", asset_brief["id"]).execute()

    supabase.table("campaign_command_logs").insert(
        {
            "target_type": "campaign_output",
            "target_id": output["id"],
            "instruction": instruction,
            "status": "completed",
            "action_summary": action_summary,
            "changed_fields": changed_fields,
        }
    ).execute()

    return {
        "output": map_output(saved_output),
        "action_summary": action_summary,
        "changed_fields": changed_fields,
    }
