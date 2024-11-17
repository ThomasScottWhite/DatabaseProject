import importlib
import logging
from pathlib import Path
from typing import Final

from fastapi import APIRouter

ROUTERS: Final[list[APIRouter]] = []

logger = logging.getLogger(__name__)

logger.debug("Loading routes...")
for path in Path(__file__).parent.iterdir():
    if not path.is_file() or path.stem.startswith("__"):
        continue

    logger.debug(f"Loading module api.routes.{path.stem}")
    mod = importlib.import_module(f".{path.stem}", package="api.routes")

    if "router" in dir(mod):
        ROUTERS.append(mod.router)
    else:
        logger.debug(f"Loading module api.routes.{path.stem}")
