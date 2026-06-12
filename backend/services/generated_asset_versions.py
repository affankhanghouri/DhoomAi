from services.supabase_service import get_supabase


def get_next_version_number(generated_asset_id: str) -> int:
    supabase = get_supabase()

    result = (
        supabase.table("campaign_generated_asset_versions")
        .select("version_number")
        .eq("generated_asset_id", generated_asset_id)
        .order("version_number", desc=True)
        .limit(1)
        .execute()
    )

    if not result.data:
        return 1

    return int(result.data[0]["version_number"]) + 1


def create_asset_version(
    asset: dict,
    asset_url: str,
    asset_path: str,
    generation_metadata: dict,
) -> dict:
    supabase = get_supabase()
    version_number = get_next_version_number(asset["id"])

    supabase.table("campaign_generated_asset_versions").update(
        {"is_selected": False}
    ).eq("generated_asset_id", asset["id"]).execute()

    insert_payload = {
        "generated_asset_id": asset["id"],
        "asset_brief_id": asset["asset_brief_id"],
        "output_id": asset["output_id"],
        "draft_id": asset["draft_id"],

        "version_number": version_number,

        "asset_url": asset_url,
        "asset_path": asset_path,
        "thumbnail_url": asset_url,

        "source_prompt": asset["source_prompt"],
        "generation_prompt": asset["generation_prompt"],

        "provider": "openai",
        "generation_metadata": generation_metadata,

        "is_selected": True,
    }

    result = (
        supabase.table("campaign_generated_asset_versions")
        .insert(insert_payload)
        .execute()
    )

    return result.data[0]


def map_asset_version(row: dict) -> dict:
    return {
        "id": row["id"],
        "generated_asset_id": row["generated_asset_id"],
        "asset_brief_id": row["asset_brief_id"],
        "output_id": row["output_id"],
        "draft_id": row["draft_id"],
        "version_number": int(row["version_number"]),
        "asset_url": row["asset_url"],
        "asset_path": row["asset_path"],
        "thumbnail_url": row.get("thumbnail_url"),
        "source_prompt": row["source_prompt"],
        "generation_prompt": row["generation_prompt"],
        "provider": row.get("provider"),
        "generation_metadata": row.get("generation_metadata") or {},
        "is_selected": bool(row["is_selected"]),
    }
