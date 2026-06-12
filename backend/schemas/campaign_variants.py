from pydantic import BaseModel


class GenerateVariantsRequest(BaseModel):
    draft_id: str


class RefineVariantRequest(BaseModel):
    draft_id: str
    variant_id: str
    refine_instruction: str


class CampaignVariantOption(BaseModel):
    variant_id: str
    name: str
    description: str
    visual_direction: str
    caption_style: str
    whatsapp_style: str
    poster_layout: str
    why_it_fits: str
    confidence: float
    refinement_count: int = 0
    is_refined: bool = False


class GenerateVariantsResponse(BaseModel):
    draft_id: str
    brand_profile_id: str | None
    selected_angle_id: str | None
    variants: list[CampaignVariantOption]


class RefineVariantResponse(BaseModel):
    draft_id: str
    variant: CampaignVariantOption