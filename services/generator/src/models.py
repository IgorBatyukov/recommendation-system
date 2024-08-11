from pydantic import BaseModel


class RecommendationRequest(BaseModel):
    rec_model_name: str
    viewer_id: str


class RecommendationResponse(BaseModel):
    reason: str
    result: int
