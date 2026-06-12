from typing import Any, Literal

from pydantic import BaseModel, HttpUrl


SourceType = Literal["auto", "website", "instagram", "facebook", "shopify", "daraz"]


class BrandDNAAnalyzeRequest(BaseModel):
    website_url: HttpUrl
    source_type: SourceType = "auto"


class BrandDNAData(BaseModel):
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

    raw_context: str
    confidence: float


class BrandDNAAnalyzeResponse(BaseModel):
    id: str
    source_url: str
    source_type: str
    dna: BrandDNAData