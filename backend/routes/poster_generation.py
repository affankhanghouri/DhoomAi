from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from schemas.poster_generation import GeneratePosterRequest, GeneratePosterResponse
from services.generated_asset_versions import create_asset_version
from services.poster_generation_service import (
    PosterGenerationError,
    generate_poster_image,
    map_generated_asset,
    upload_generated_image_to_supabase,
)
from services.supabase_service import get_supabase


router = APIRouter(prefix="/poster-generation", tags=["Poster Generation"])


@router.post("/generate", response_model=GeneratePosterResponse)
async def generate_poster_route(payload: GeneratePosterRequest):
    supabase = get_supabase()

    asset_result = (
        supabase.table("campaign_generated_assets")
        .select("*")
        .eq("id", payload.generated_asset_id)
        .single()
        .execute()
    )

    if not asset_result.data:
        raise HTTPException(status_code=404, detail="Generated asset slot not found.")

    asset = asset_result.data

    if asset.get("asset_type") != "poster":
        raise HTTPException(
            status_code=400,
            detail="Only poster assets can be generated from this endpoint.",
        )

    draft_result = (
        supabase.table("campaign_drafts")
        .select("*")
        .eq("id", asset["draft_id"])
        .single()
        .execute()
    )

    if not draft_result.data:
        raise HTTPException(status_code=404, detail="Campaign draft not found.")

    draft = draft_result.data

    supabase.table("campaign_generated_assets").update(
        {
            "status": "generating",
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
    ).eq("id", asset["id"]).execute()

    try:
        image_bytes, generation_metadata = await generate_poster_image(
            asset=asset,
            draft=draft,
        )

        asset_path, asset_url = upload_generated_image_to_supabase(
            image_bytes=image_bytes,
            generated_asset_id=asset["id"],
        )

        version = create_asset_version(
            asset=asset,
            asset_url=asset_url,
            asset_path=asset_path,
            generation_metadata=generation_metadata,
        )

        update_result = (
            supabase.table("campaign_generated_assets")
            .update(
                {
                    "asset_url": asset_url,
                    "asset_path": asset_path,
                    "thumbnail_url": asset_url,
                    "status": "generated",
                    "provider": "openai",
                    "generation_metadata": {
                        **generation_metadata,
                        "selected_version_id": version["id"],
                        "selected_version_number": version["version_number"],
                    },
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                }
            )
            .eq("id", asset["id"])
            .execute()
        )

        if not update_result.data:
            raise HTTPException(
                status_code=500,
                detail="Could not save generated poster asset.",
            )

        return {"asset": map_generated_asset(update_result.data[0])}

    except PosterGenerationError as exc:
        supabase.table("campaign_generated_assets").update(
            {
                "status": "failed",
                "generation_metadata": {
                    "error": str(exc),
                    "failed_at": datetime.now(timezone.utc).isoformat(),
                },
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
        ).eq("id", asset["id"]).execute()

        raise HTTPException(status_code=500, detail=str(exc)) from exc
