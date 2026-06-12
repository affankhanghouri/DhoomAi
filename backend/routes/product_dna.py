from fastapi import APIRouter, HTTPException

from schemas.product_dna import AnalyzeProductDNARequest, AnalyzeProductDNAResponse
from services.llm_client import generate_product_dna_with_llm
from services.product_dna_generator import fallback_product_dna
from services.supabase_service import get_supabase


router = APIRouter(prefix="/product-dna", tags=["Product DNA"])


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


@router.post("/analyze", response_model=AnalyzeProductDNAResponse)
async def analyze_product_dna_route(payload: AnalyzeProductDNARequest):
    supabase = get_supabase()
    draft, brand_profile = get_draft_and_brand(payload.draft_id)

    try:
        product_dna = generate_product_dna_with_llm(
            brand_profile=brand_profile,
            campaign_draft=draft,
        )
    except Exception:
        product_dna = fallback_product_dna(
            brand_profile=brand_profile,
            campaign_draft=draft,
        )

    update_payload = {
        "product_type": product_dna["product_type"],
        "product_dna_summary": product_dna["product_dna_summary"],
        "product_visual_notes": product_dna["product_visual_notes"],
        "product_features": product_dna["product_features"],
        "buyer_reasons": product_dna["buyer_reasons"],
        "buyer_objections": product_dna["buyer_objections"],
        "suggested_use_cases": product_dna["suggested_use_cases"],
        "product_positioning": product_dna["product_positioning"],
        "product_confidence": product_dna["confidence"],
    }

    update_result = (
        supabase.table("campaign_drafts")
        .update(update_payload)
        .eq("id", payload.draft_id)
        .execute()
    )

    if not update_result.data:
        raise HTTPException(
            status_code=500,
            detail="Could not save Product DNA.",
        )

    return {
        "draft_id": payload.draft_id,
        "product_dna": product_dna,
    }
