from pydantic import BaseModel, Field


class RefineCampaignAssetBriefRequest(BaseModel):
    asset_brief_id: str
    refine_instruction: str


class RefinedCampaignAssetBriefData(BaseModel):
    id: str
    output_id: str
    draft_id: str

    creative_brief_title: str

    poster_prompt: str
    image_generation_prompt: str
    poster_layout_direction: str
    poster_text_hierarchy: list[str] = Field(default_factory=list)
    poster_design_rules: list[str] = Field(default_factory=list)

    reel_prompt: str
    video_generation_prompt: str
    reel_shot_list: list[str] = Field(default_factory=list)
    reel_sound_direction: str | None = None
    reel_editing_style: str | None = None

    designer_notes: list[str] = Field(default_factory=list)
    asset_risks: list[str] = Field(default_factory=list)

    confidence: float | None = None
    status: str

    refinement_count: int
    refinement_notes: list[str] = Field(default_factory=list)


class RefineCampaignAssetBriefResponse(BaseModel):
    brief: RefinedCampaignAssetBriefData