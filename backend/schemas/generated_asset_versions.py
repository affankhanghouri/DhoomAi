from pydantic import BaseModel, Field


class GeneratedAssetVersionData(BaseModel):
    id: str
    generated_asset_id: str
    asset_brief_id: str
    output_id: str
    draft_id: str

    version_number: int

    asset_url: str
    asset_path: str
    thumbnail_url: str | None = None

    source_prompt: str
    generation_prompt: str

    provider: str | None = None
    generation_metadata: dict = Field(default_factory=dict)

    is_selected: bool


class GetAssetVersionsResponse(BaseModel):
    versions: list[GeneratedAssetVersionData]


class SelectAssetVersionRequest(BaseModel):
    version_id: str


class SelectAssetVersionResponse(BaseModel):
    version: GeneratedAssetVersionData
