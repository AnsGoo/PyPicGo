import time
from loguru import logger
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_PATH = BASE_DIR.joinpath('logs')
if not LOG_PATH.exists():
    LOG_PATH.mkdir(parents=True, exist_ok=True)

log_path_info = LOG_PATH.joinpath(f'{time.strftime("%Y-%m-%d")}_info.log')
log_path_warning = LOG_PATH.joinpath(f'{time.strftime("%Y-%m-%d")}_warning.log')
log_path_error = LOG_PATH.joinpath(f'{time.strftime("%Y-%m-%d")}_error.log')

# 日志简单配置 文件区分不同级别的日志
logger.add(log_path_info,
           rotation="10 MB",
           encoding='utf-8',
           enqueue=True,
           level='INFO',
           compression='zip',
           retention=5)

logger.add(log_path_warning,
           rotation="10 MB",
           encoding='utf-8',
           enqueue=True,
           level='WARNING',
           compression='zip',
           retention=5)

logger.add(log_path_error,
           rotation="10 MB",
           encoding='utf-8',
           enqueue=True,
           level='ERROR',
           compression='zip',
           retention=5)

__all__ = ["logger"]
