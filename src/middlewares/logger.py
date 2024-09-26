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

        log_dict = {
            "level": logging.getLevelName(logger.level),
            "host": request.client.host,
            "port": request.client.port,
            "method": request.method,
            "url": request.url.path,
            "status_code": response.status_code,
            "process_time": process_time,
        }
        # log_message = f"{request.client.host}:{request.client.port} - {request.method} - {request.url.path} - {response.status_code} completed after {process_time}s"

        status_code_prefix = (str(response.status_code))[0]

        # if status_code_prefix == "4" or status_code_prefix == "5":
        #     log_dict["error_detail"] = response.body.detail
        #     logger.error(log_dict)
        # else:
        logger.info(log_dict)

        return response

