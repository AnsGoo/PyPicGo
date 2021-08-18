import time
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
from pypicgo import BASE_DIR

LOG_PATH = BASE_DIR.joinpath('logs')
if not LOG_PATH.exists():
    LOG_PATH.mkdir(parents=True, exist_ok=True)

log_path_info = LOG_PATH.joinpath(f'{time.strftime("%Y-%m-%d")}_info.log')
log_path_error = LOG_PATH.joinpath(f'{time.strftime("%Y-%m-%d")}_info.log')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('pypicgo')
logger.setLevel(logging.DEBUG)
info_handler = TimedRotatingFileHandler(log_path_info.resolve(), when='midnight', interval=1, backupCount=7, atTime=datetime.time(0, 0, 0, 0))
info_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

error_handler = TimedRotatingFileHandler(log_path_error, when='midnight', interval=1, backupCount=7, atTime=datetime.time(0, 0, 0, 0))
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

logger.addHandler(info_handler)
logger.addHandler(error_handler)
__all__ = ["logger"]
