import uvicorn
from fastapi import FastAPI

from services.invoker.src.utils import recommend

app = FastAPI()


@app.get('/')
async def health_check():
    return {'healthy': True}


@app.get('/recommend')
async def get_recommendation(viewer_id: str):
    return await recommend(viewer_id)


if __name__ == '__main__':
    try:
        uvicorn.run(app, host='0.0.0.0', port=8891)
    except KeyboardInterrupt:
        pass
