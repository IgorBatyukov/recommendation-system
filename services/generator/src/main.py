import random
import uvicorn
from fastapi import FastAPI

from services.generator.src.models import RecommendationRequest, RecommendationResponse

app = FastAPI()


@app.get('/')
async def health_check():
    return {'healthy': True}


@app.post('/generate')
async def generate_recommendation(request: RecommendationRequest) -> RecommendationResponse:
    return RecommendationResponse(
        reason=request.rec_model_name,
        result=random.randint(0, 10000)
    )


if __name__ == '__main__':
    try:
        uvicorn.run(app, host='0.0.0.0', port=8890)
    except KeyboardInterrupt:
        pass
