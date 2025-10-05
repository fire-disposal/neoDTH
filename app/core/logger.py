import logging
from typing import Optional

try:
    from .settings import settings
except ImportError:
    settings = None

class EventTypeFilter(logging.Filter):
    def filter(self, record):
        # 保证 event_type 字段存在
        if not hasattr(record, "event_type"):
            record.event_type = "-"
        return True

def get_logger(name: str, event_type: Optional[str] = None) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s [%(name)s][%(event_type)s] %(message)s"
        )
        handler.setFormatter(formatter)
        handler.addFilter(EventTypeFilter())
        logger.addHandler(handler)
    # 日志等级由 settings 控制
    level = getattr(settings, "log_level", "INFO") if settings else "INFO"
    logger.setLevel(level)
    # 支持事件类型标记
    if event_type:
        logger = logging.LoggerAdapter(logger, {"event_type": event_type})
    return logger

logger = get_logger("neoDTH")