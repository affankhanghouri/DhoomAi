from pydantic import BaseModel, HttpUrl


class StartBrandIntakeRequest(BaseModel):
    source_url: HttpUrl
    source_type: str = "auto"


class BrandIntakeJobData(BaseModel):
    id: str
    source_url: str
    source_type: str

    status: str
    current_step: str | None = None
    progress: int

    steps: list[dict]

    brand_profile_id: str | None = None
    error_message: str | None = None


class StartBrandIntakeResponse(BaseModel):
    job: BrandIntakeJobData


class GetBrandIntakeResponse(BaseModel):
    job: BrandIntakeJobData
