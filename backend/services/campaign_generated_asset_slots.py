from datetime import datetime, timezone

from services.supabase_service import get_supabase


def build_default_asset_slots(asset_brief: dict) -> list[dict]:
    asset_brief_id = asset_brief["id"]
    output_id = asset_brief["output_id"]
    draft_id = asset_brief["draft_id"]

    return [
        {
            "asset_brief_id": asset_brief_id,
            "output_id": output_id,
            "draft_id": draft_id,

            "asset_type": "poster",
            "asset_slot": "primary_poster",

            "title": "Primary Poster",
            "description": "Main static poster generated from this campaign creative brief.",
            "source_prompt": asset_brief["poster_prompt"],
            "generation_prompt": asset_brief["image_generation_prompt"],

            "status": "planned",
            "provider": None,
            "generation_metadata": {
                "source": "campaign_asset_brief",
                "format": "static_poster",
                "recommended_ratio": "4:5 or 1:1",
            },
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "asset_brief_id": asset_brief_id,
            "output_id": output_id,
            "draft_id": draft_id,

            "asset_type": "reel",
            "asset_slot": "primary_reel",

            "title": "Primary Reel",
            "description": "Main short-form video/reel generated from this campaign creative brief.",
            "source_prompt": asset_brief["reel_prompt"],
            "generation_prompt": asset_brief["video_generation_prompt"],

            "status": "planned",
            "provider": None,
            "generation_metadata": {
                "source": "campaign_asset_brief",
                "format": "vertical_reel",
                "recommended_ratio": "9:16",
            },
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
    ]


def create_default_asset_slots(asset_brief: dict) -> list[dict]:
    rows = build_default_asset_slots(asset_brief)
    supabase = get_supabase()

    result = (
        supabase.table("campaign_generated_assets")
        .upsert(
            rows,
            on_conflict="asset_brief_id,asset_slot",
        )
        .execute()
    )

    return result.data or []
