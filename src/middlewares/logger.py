import time
from fastapi import FastAPI
from fastapi.requests import Request
from starlette.middleware.base import _StreamingResponse

from src.utils.logger import logger
import logging


def register_logger(app: FastAPI):
    @app.middleware("http")
    async def log_request(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        end_time = time.time()
        process_time = end_time - start_time

        log_message = f"{logging.getLevelName(logger.level)} - {request.client.host}:{request.client.port} - {request.method} - {request.url.path} - {response.status_code} completed after {process_time}s"
        logger.info(log_message)

        return response

