from pydantic import BaseModel, Field


class GenerateFinalCampaignRequest(BaseModel):
    draft_id: str


class FinalCampaignOutput(BaseModel):
    id: str
    draft_id: str

    campaign_headline: str
    campaign_angle: str
    buyer_insight: str

    caption: str
    whatsapp_copy: str
    offer_idea: str
    story_flow: list[str]

    poster_direction: str
    reel_direction: str
    primary_cta: str

    do_rules: list[str]
    avoid_rules: list[str]

    confidence: float
    campaign_score: int | None = None
    quality_status: str | None = None
    quality_notes: list[str] = Field(default_factory=list)
    improvements_applied: list[str] = Field(default_factory=list)
    risk_flags: list[str] = Field(default_factory=list)
    status: str


class GenerateFinalCampaignResponse(BaseModel):
    output: FinalCampaignOutput
