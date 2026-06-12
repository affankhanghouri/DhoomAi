from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException

from schemas.brand_dna_enrichment import (
    BrandDNAEnrichRequest,
    BrandDNAEnrichResponse,
)
from services.brand_dna_enrichment import fallback_enrich_brand_dna
from services.llm_client import enrich_brand_dna_with_llm
from services.supabase_service import get_supabase


router = APIRouter(prefix="/brand-dna", tags=["Brand DNA Enrichment"])


@router.post("/enrich", response_model=BrandDNAEnrichResponse)
async def enrich_brand_dna_route(payload: BrandDNAEnrichRequest):
    supabase = get_supabase()

    brand_result = (
        supabase.table("brand_profiles")
        .select("*")
        .eq("id", payload.brand_profile_id)
        .single()
        .execute()
    )

    if not brand_result.data:
        raise HTTPException(status_code=404, detail="Brand profile not found.")

    brand_profile = brand_result.data

    answers = {
        "mostly_sell": payload.mostly_sell,
        "usual_buyers": payload.usual_buyers,
        "product_strength": payload.product_strength,
        "brand_tone_preference": payload.brand_tone_preference,
        "avoid_preference": payload.avoid_preference,
    }

    try:
        enriched_dna = enrich_brand_dna_with_llm(
            brand_profile=brand_profile,
            answers=answers,
        )
    except Exception:
        enriched_dna = fallback_enrich_brand_dna(
            brand_profile=brand_profile,
            answers=answers,
        )

    previous_confidence = brand_profile.get("confidence")
    new_confidence = enriched_dna["confidence"]

    update_payload = {
        "brand_name": enriched_dna["brand_name"],
        "business_type": enriched_dna["business_type"],
        "category": enriched_dna["category"],
        "summary": enriched_dna["summary"],
        "target_audience": enriched_dna["target_audience"],
        "tone": enriched_dna["tone"],
        "visual_style": enriched_dna["visual_style"],
        "price_positioning": enriched_dna["price_positioning"],
        "pakistani_market_context": enriched_dna["pakistani_market_context"],
        "selling_points": enriched_dna["selling_points"],
        "trust_signals": enriched_dna["trust_signals"],
        "weaknesses": enriched_dna["weaknesses"],
        "campaign_rules": enriched_dna["campaign_rules"],
        "angle_strategy": enriched_dna["angle_strategy"],
        "content_language_strategy": enriched_dna["content_language_strategy"],
        "confidence": new_confidence,
        "is_enriched": True,
        "enrichment_count": int(brand_profile.get("enrichment_count") or 0) + 1,
        "last_enriched_at": datetime.now(UTC).isoformat(),
    }

    update_result = (
        supabase.table("brand_profiles")
        .update(update_payload)
        .eq("id", payload.brand_profile_id)
        .execute()
    )

    if not update_result.data:
        raise HTTPException(
            status_code=500,
            detail="Could not update enriched Brand DNA.",
        )

    supabase.table("brand_profile_enrichments").insert(
        {
            "brand_profile_id": payload.brand_profile_id,
            "mostly_sell": payload.mostly_sell,
            "usual_buyers": payload.usual_buyers,
            "product_strength": payload.product_strength,
            "brand_tone_preference": payload.brand_tone_preference,
            "avoid_preference": payload.avoid_preference,
            "previous_confidence": previous_confidence,
            "new_confidence": new_confidence,
        }
    ).execute()

    return {
        "brand_profile_id": payload.brand_profile_id,
        "dna": enriched_dna,
    }
