import json
import logging
import os
import random
from http import HTTPStatus
from typing import Awaitable, Any
from urllib.parse import urljoin

import aiohttp
from aiohttp.client_exceptions import ClientConnectionError
from cashews import Cache

from libs.exception_handlers import ErrorMessages, CustomException

GENERATOR_URL = os.getenv('GENERATOR_URL', 'http://0.0.0.0:8890')
MODEL_REGISTRY_PATH = os.getenv('MODEL_REGISTRY', '../../../resources/model_registry.json')
NUM_MODELS = int(os.getenv('NUM_MODELS', 5))
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost')

local_cache = Cache()
local_cache.setup("mem://", size=3, ttl=10)
redis_cache = Cache()
redis_cache.setup(REDIS_URL)

log = logging.getLogger('uvicorn.info')


def get_model_names(registry_path: str, num: int) -> list[str]:
    """
    Returns list of `num` random model names from the model registry.
    """
    try:
        with open(registry_path, 'r') as registry:
            js = json.loads(registry.read())
            model_names = [
                model['name'] for model in js['models']
            ]
            return random.sample(model_names, num)
    except FileNotFoundError as exc:
        raise CustomException(
            name=HTTPStatus.INTERNAL_SERVER_ERROR.name,
            detail=ErrorMessages.MODEL_REGISTRY_NOT_FOUND
        ) from exc


async def call_generator(url: str, model_name: str, viewer_id: str) -> Awaitable[dict]:
    """
    Calls Generator service with a given `viewer_id` and `model_name`.
    """
    async with aiohttp.ClientSession() as session:
        endpoint = urljoin(url, '/generate')
        data = {
            'rec_model_name': model_name,
            'viewer_id': viewer_id
        }
        async with session.post(endpoint, json=data) as response:
            return await response.json()


async def runcascade(viewer_id: str, model_names: list[str]) -> list[Any] | None:
    """
    Send parallel requests to the Generator service.
    """
    try:
        return [
            await call_generator(GENERATOR_URL, model, viewer_id) for model in model_names
        ]
    except ClientConnectionError as exc:
        raise CustomException(
            name=HTTPStatus.INTERNAL_SERVER_ERROR.name,
            detail=ErrorMessages.GENERATOR_SERVICE_UNAVAILABLE
        ) from exc


async def get_recommendations(viewer_id: str, model_names: list[str]) -> list[Any] | None:
    """
    For the given `viewer_id` and `model_names` fetch data either from cache or
    from Generator service.
    """
    if cached_data := await local_cache.get(viewer_id):
        log.info(f"Data loaded from local cache for viewer_id: {viewer_id}")
        return cached_data

    if cached_data := await redis_cache.get(viewer_id):
        log.info(f"Data loaded from Redis cache for viewer_id: {viewer_id}")
        return cached_data

    if data := await runcascade(viewer_id, model_names):
        await local_cache.set(viewer_id, data)
        await redis_cache.set(viewer_id, data)
        log.info(f"Data computed for viewer_id: {viewer_id}")
        return data
    return None


async def recommend(viewer_id: str) -> list[Any]:
    """
    Get random NUM_MODELS model name from teh registry and retrieve
    recommendations for the given viewer_id.
    """
    try:
        model_names = get_model_names(MODEL_REGISTRY_PATH, NUM_MODELS)
        return await get_recommendations(viewer_id, model_names)
    except CustomException:
        raise
