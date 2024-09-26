import logging
import sys
from src.core.config import config
from logging.handlers import SysLogHandler

log_format = logging.Formatter(
    fmt='%(asctime)s - %(levelname)s - %(message)s'
)
log_level = logging.DEBUG if config.ENV == "development" else logging.INFO

stream_handler = logging.StreamHandler(stream=sys.stdout)
file_handler = logging.FileHandler(config.LOG_PATH)
papertrail_handler = SysLogHandler(address=(config.PAPERTRAIL_HOST, config.PAPERTRAIL_PORT))

stream_handler.setFormatter(log_format)
file_handler.setFormatter(log_format)

logger = logging.getLogger("fast-crud-api")
logger.setLevel(log_level)
logger.handlers = [stream_handler, file_handler, papertrail_handler]
