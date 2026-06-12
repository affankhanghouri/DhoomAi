from pydantic import BaseModel, Field


class RefineCampaignWithGhostEditorRequest(BaseModel):
    campaign_output_id: str
    instruction: str = Field(min_length=2)


class GhostEditedCampaignOutput(BaseModel):
    id: str

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

    confidence: float | None = None

    campaign_score: int | None = None
    quality_status: str | None = None
    quality_notes: list[str] = Field(default_factory=list)
    improvements_applied: list[str] = Field(default_factory=list)
    risk_flags: list[str] = Field(default_factory=list)

    edit_count: int
    edit_notes: list[str] = Field(default_factory=list)


class RefineCampaignWithGhostEditorResponse(BaseModel):
    output: GhostEditedCampaignOutput
    action_summary: str
    changed_fields: list[str] = Field(default_factory=list)
