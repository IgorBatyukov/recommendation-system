import json
import os
import random
from urllib.parse import urljoin
from typing import Awaitable, Any

import aiohttp
from cashews import Cache

GENERATOR_URL = os.getenv('GENERATOR_URL', 'http://0.0.0.0:8890')
MODEL_REGISTRY_PATH = os.getenv('MODEL_REGISTRY', '../../../resources/model_registry.json')
NUM_MODELS = int(os.getenv('NUM_MODELS', 5))
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost')

local_cache = Cache()
local_cache.setup("mem://", size=3, ttl=10)
redis_cache = Cache()
redis_cache.setup(REDIS_URL)


def get_model_names(registry_path: str, num: int) -> list[str]:
    with open(registry_path, 'r') as registry:
        js = json.loads(registry.read())
        model_names = [
            model['name'] for model in js['models']
        ]
        return random.sample(model_names, num)


async def call_generator(url: str, model_name: str, viewer_id: str) -> Awaitable[dict]:
    async with aiohttp.ClientSession() as session:
        endpoint = urljoin(url, '/generate')
        data = {
            'rec_model_name': model_name,
            'viewer_id': viewer_id
        }
        async with session.post(endpoint, json=data) as response:
            return await response.json()


async def runcascade(viewer_id: str, model_names: list[str]) -> list[Any]:
    return [
        await call_generator(GENERATOR_URL, model, viewer_id) for model in model_names
    ]


async def get_recommendations(viewer_id: str, model_names: list[str]) -> list[Any]:
    cached_data = await local_cache.get(viewer_id)
    if cached_data:
        return cached_data

    cached_data = await redis_cache.get(viewer_id)
    if cached_data:
        return cached_data

    data = await runcascade(viewer_id, model_names)
    await local_cache.set(viewer_id, data)
    await redis_cache.set(viewer_id, data)
    return data


async def recommend(user_id: str) -> list[Any]:
    model_names = get_model_names(MODEL_REGISTRY_PATH, NUM_MODELS)
    return await get_recommendations(user_id, model_names)
