from pydantic import BaseModel
from typing import Any


class AnalyzeProductDNARequest(BaseModel):
    draft_id: str


class ProductDNAData(BaseModel):
    product_type: str
    product_dna_summary: str
    product_visual_notes: str

    product_features: list[str]
    buyer_reasons: list[str]
    buyer_objections: list[str]
    suggested_use_cases: list[str]

    product_positioning: str
    campaign_implications: dict[str, Any]

    confidence: float


class AnalyzeProductDNAResponse(BaseModel):
    draft_id: str
    product_dna: ProductDNAData