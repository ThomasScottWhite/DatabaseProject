from typing import Final

from sqlalchemy import Engine, create_engine

from api.config import CONFIG
from api.utils import export

_ENGINE: Final[Engine] = create_engine(CONFIG.database_url)

__all__ = []


@export
def get_engine() -> Engine:
    return _ENGINE


get_connection = _ENGINE.connect

begin = _ENGINE.begin

__all__.extend(["get_connection", "begin"])
