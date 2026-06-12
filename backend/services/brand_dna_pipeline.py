from services.brand_dna_analyzer import analyze_brand_dna
from services.llm_client import generate_brand_dna_with_llm
from services.source_detector import detect_source_type
from services.supabase_service import get_supabase
from services.web_extractor import extract_website_context


def fallback_brand_dna_from_context(context: dict, source_type: str) -> dict:
    title = context.get("title") or context.get("url") or "Untitled Brand"
    raw_text = context.get("raw_text") or context.get("text") or ""

    return {
        "brand_name": title[:80],
        "business_type": "Online seller",
        "category": "General products",
        "summary": raw_text[:500] if raw_text else "Brand DNA generated from public source.",
        "target_audience": "Pakistani online buyers",
        "tone": "Clear, trustworthy, and modern",
        "visual_style": "Clean social-commerce style",
        "price_positioning": "Value-focused",
        "pakistani_market_context": {
            "buyer_behavior": "Trust, price clarity, product look, and delivery confidence matter.",
            "commerce_channels": ["Instagram", "Facebook", "WhatsApp"],
        },
        "selling_points": ["Public brand source available"],
        "trust_signals": ["Online presence"],
        "weaknesses": ["Limited public information available"],
        "campaign_rules": {
            "avoid": ["Do not invent fake claims", "Do not overpromise"],
            "use": ["Clear CTA", "Product-first messaging"],
        },
        "angle_strategy": {
            "recommended_angles": ["Trust builder", "Product clarity", "Value offer"],
        },
        "content_language_strategy": {
            "primary": "Simple English",
            "secondary": "Roman Urdu only if brand tone supports it",
        },
        "raw_context": raw_text[:3000],
        "confidence": 0.45,
    }


async def analyze_and_save_brand_dna(source_url: str, source_type: str = "auto") -> dict:
    detected_source_type = detect_source_type(
        source_url,
        requested_source_type=source_type,
    )

    context = await extract_website_context(
        source_url,
        source_type=detected_source_type,
    )

    try:
        dna = generate_brand_dna_with_llm(context)
    except Exception:
        try:
            dna = analyze_brand_dna(context)
        except Exception:
            dna = fallback_brand_dna_from_context(
                context=context,
                source_type=detected_source_type,
            )

    dna["raw_context"] = dna.get("raw_context") or context["text"][:5000]

    raw_source_data = {
        "source_type": detected_source_type,
        "context": context,
    }

    insert_payload = {
        "source_url": source_url,
        "source_type": detected_source_type,
        "source_platform": context.get("source_platform") or detected_source_type,

        "brand_name": dna["brand_name"],
        "business_type": dna["business_type"],
        "category": dna["category"],
        "summary": dna["summary"],
        "target_audience": dna["target_audience"],
        "tone": dna["tone"],
        "visual_style": dna["visual_style"],
        "price_positioning": dna["price_positioning"],

        "selling_points": dna["selling_points"],
        "trust_signals": dna["trust_signals"],
        "weaknesses": dna["weaknesses"],
        "campaign_rules": dna["campaign_rules"],

        "pakistani_market_context": dna.get("pakistani_market_context", {}),
        "angle_strategy": dna.get("angle_strategy", {}),
        "content_language_strategy": dna.get("content_language_strategy", {}),

        "raw_context": dna["raw_context"],
        "raw_source_data": raw_source_data,

        "confidence": dna["confidence"],
        "status": "active",
    }

    supabase = get_supabase()
    result = supabase.table("brand_profiles").insert(insert_payload).execute()

    if not result.data:
        raise RuntimeError("Could not save Brand DNA profile.")

    saved = result.data[0]

    return {
        "id": saved["id"],
        "source_url": saved["source_url"],
        "source_type": saved["source_type"],
        "dna": dna,
    }
