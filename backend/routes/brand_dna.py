from fastapi import APIRouter, HTTPException

from schemas.brand_dna import BrandDNAAnalyzeRequest, BrandDNAAnalyzeResponse
from services.brand_dna_analyzer import analyze_brand_dna
from services.llm_client import generate_brand_dna_with_llm
from services.source_detector import detect_source_type
from services.supabase_service import get_supabase
from services.web_extractor import WebsiteExtractionError, extract_website_context


router = APIRouter(prefix="/brand-dna", tags=["Brand DNA"])


@router.post("/analyze", response_model=BrandDNAAnalyzeResponse)
async def analyze_brand_dna_route(payload: BrandDNAAnalyzeRequest):
    supabase = get_supabase()
    website_url = str(payload.website_url)
    source_type = detect_source_type(website_url, payload.source_type)

    try:
        context = await extract_website_context(website_url, source_type=source_type)

        try:
            dna = generate_brand_dna_with_llm(context)
        except Exception:
            dna = analyze_brand_dna(context)

        dna["raw_context"] = context["text"][:5000]

    except WebsiteExtractionError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Brand DNA analysis failed.",
        ) from exc

    insert_payload = {
        "source_url": website_url,
        "source_type": source_type,
        "source_platform": source_type,

        "brand_name": dna["brand_name"],
        "business_type": dna["business_type"],
        "category": dna["category"],
        "summary": dna["summary"],
        "target_audience": dna["target_audience"],
        "tone": dna["tone"],
        "visual_style": dna["visual_style"],
        "price_positioning": dna["price_positioning"],
        "pakistani_market_context": dna.get("pakistani_market_context", {}),
        "selling_points": dna["selling_points"],
        "trust_signals": dna["trust_signals"],
        "weaknesses": dna["weaknesses"],
        "campaign_rules": dna["campaign_rules"],
        "angle_strategy": dna.get("angle_strategy", {}),
        "content_language_strategy": dna.get("content_language_strategy", {}),
        "raw_context": dna["raw_context"],
        "raw_source_data": context.get("raw_source_data", {}),
        "confidence": dna["confidence"],
        "status": "active",
    }

    result = supabase.table("brand_profiles").insert(insert_payload).execute()

    if not result.data:
        raise HTTPException(
            status_code=500,
            detail="Could not save Brand DNA.",
        )

    saved = result.data[0]

    return {
        "id": saved["id"],
        "source_url": website_url,
        "source_type": source_type,
        "dna": dna,
    }
