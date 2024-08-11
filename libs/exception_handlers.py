from enum import StrEnum
from http import HTTPStatus

from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class CustomException(Exception):
    def __init__(self, name: str, detail: str):
        self.name = name
        self.detail = detail


class HttpErrorResponse(BaseModel):
    detail: str
    status_code: int


class ErrorMessages(StrEnum):
    GENERATOR_SERVICE_UNAVAILABLE = 'GENERATOR_SERVICE_UNAVAILABLE'
    MODEL_REGISTRY_NOT_FOUND = 'MODEL_REGISTRY_NOT_FOUND'


async def general_exception_handler(request: Request, exc: CustomException) -> JSONResponse:
    response = JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content=HttpErrorResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=exc.detail
        ).dict()
    )
    return response
