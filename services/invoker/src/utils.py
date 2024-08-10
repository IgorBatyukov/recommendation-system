import os
import json
import random
import aiohttp
from asyncache import cached
from cachetools import TTLCache

GENERATOR_URL = os.getenv('GENERATOR_URL', 'http://0.0.0.0:8890')
MODEL_REGISTRY_PATH = os.getenv('MODEL_REGISTRY')
NUM_MODELS = int(os.getenv('NUM_MODELS', 5))


def get_model_names(registry_path: str, num: int) -> list[str]:
    with open(registry_path, 'r') as registry:
        js = json.loads(registry.read())
        model_names = [
            model['name'] for model in js['models']
        ]
        return random.sample(model_names, num)


async def call_generator(url: str, model_name: str, viewer_id: int):
    async with aiohttp.ClientSession() as session:
        endpoint = url + '/generate'
        data = {
            'rec_model_name': model_name,
            'viewer_id': viewer_id
        }
        async with session.post(endpoint, json=data) as response:
            return await response.json()


@cached(cache=TTLCache(maxsize=3, ttl=10))
async def recommend(user_id):
    model_names = get_model_names(MODEL_REGISTRY_PATH, NUM_MODELS)
    return await runcascade(user_id, model_names)


async def runcascade(viewer_id, model_names):
    return [
        await call_generator(GENERATOR_URL, model, viewer_id) for model in model_names
    ]
