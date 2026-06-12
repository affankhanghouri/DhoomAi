from fastapi import APIRouter, HTTPException

from schemas.campaign_generated_assets import (
    CreateAssetSlotsRequest,
    CreateAssetSlotsResponse,
)
from schemas.generated_asset_versions import (
    GetAssetVersionsResponse,
    SelectAssetVersionRequest,
    SelectAssetVersionResponse,
)
from services.campaign_generated_asset_slots import create_default_asset_slots
from services.generated_asset_versions import map_asset_version
from services.supabase_service import get_supabase


router = APIRouter(
    prefix="/campaign-generated-assets",
    tags=["Campaign Generated Assets"],
)


@router.post("/create-slots", response_model=CreateAssetSlotsResponse)
async def create_generated_asset_slots_route(payload: CreateAssetSlotsRequest):
    supabase = get_supabase()

    asset_brief_result = (
        supabase.table("campaign_asset_briefs")
        .select("*")
        .eq("id", payload.asset_brief_id)
        .single()
        .execute()
    )

    if not asset_brief_result.data:
        raise HTTPException(status_code=404, detail="Asset brief not found.")

    assets = create_default_asset_slots(asset_brief_result.data)

    return {"assets": assets}


@router.get(
    "/{generated_asset_id}/versions",
    response_model=GetAssetVersionsResponse,
)
async def get_generated_asset_versions_route(generated_asset_id: str):
    supabase = get_supabase()

    result = (
        supabase.table("campaign_generated_asset_versions")
        .select("*")
        .eq("generated_asset_id", generated_asset_id)
        .order("version_number", desc=True)
        .execute()
    )

    return {
        "versions": [map_asset_version(row) for row in result.data or []]
    }


@router.post(
    "/select-version",
    response_model=SelectAssetVersionResponse,
)
async def select_generated_asset_version_route(payload: SelectAssetVersionRequest):
    supabase = get_supabase()

    version_result = (
        supabase.table("campaign_generated_asset_versions")
        .select("*")
        .eq("id", payload.version_id)
        .single()
        .execute()
    )

    if not version_result.data:
        raise HTTPException(status_code=404, detail="Asset version not found.")

    version = version_result.data
    generated_asset_id = version["generated_asset_id"]

    supabase.table("campaign_generated_asset_versions").update(
        {"is_selected": False}
    ).eq("generated_asset_id", generated_asset_id).execute()

    selected_result = (
        supabase.table("campaign_generated_asset_versions")
        .update({"is_selected": True})
        .eq("id", payload.version_id)
        .execute()
    )

    if not selected_result.data:
        raise HTTPException(status_code=500, detail="Could not select version.")

    supabase.table("campaign_generated_assets").update(
        {
            "asset_url": version["asset_url"],
            "asset_path": version["asset_path"],
            "thumbnail_url": version["thumbnail_url"],
            "status": "generated",
            "provider": version["provider"],
            "generation_metadata": {
                **(version.get("generation_metadata") or {}),
                "selected_version_id": version["id"],
                "selected_version_number": version["version_number"],
            },
        }
    ).eq("id", generated_asset_id).execute()

    return {
        "version": map_asset_version(selected_result.data[0])
    }
