from pydantic import BaseModel, Field


class CreateAssetSlotsRequest(BaseModel):
    asset_brief_id: str


class CampaignGeneratedAssetData(BaseModel):
    id: str
    asset_brief_id: str
    output_id: str
    draft_id: str

    asset_type: str
    asset_slot: str

    title: str
    description: str | None = None
    source_prompt: str
    generation_prompt: str

    asset_url: str | None = None
    asset_path: str | None = None
    thumbnail_url: str | None = None

    status: str
    provider: str | None = None
    generation_metadata: dict = Field(default_factory=dict)


class CreateAssetSlotsResponse(BaseModel):
    assets: list[CampaignGeneratedAssetData]
