"""Central logging bootstrap with no sensitive request/body logging."""
from __future__ import annotations

import logging


def configure_logging(level: str) -> logging.Logger:
    logger = logging.getLogger("shared_work_calendar")
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
        logger.addHandler(handler)
        logger.propagate = False
    logger.setLevel(level)
    return logger
