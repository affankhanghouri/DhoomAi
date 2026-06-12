from typing import Any

from pydantic import BaseModel


class BrandDNAEnrichRequest(BaseModel):
    brand_profile_id: str

    mostly_sell: str
    usual_buyers: str
    product_strength: str
    brand_tone_preference: str
    avoid_preference: str


class EnrichedBrandDNAData(BaseModel):
    brand_name: str
    business_type: str
    category: str
    summary: str

    target_audience: str
    tone: str
    visual_style: str
    price_positioning: str

    pakistani_market_context: dict[str, Any]

    selling_points: list[str]
    trust_signals: list[str]
    weaknesses: list[str]

    campaign_rules: dict[str, Any]
    angle_strategy: dict[str, Any]
    content_language_strategy: dict[str, Any]

    confidence: float


class BrandDNAEnrichResponse(BaseModel):
    brand_profile_id: str
    dna: EnrichedBrandDNAData