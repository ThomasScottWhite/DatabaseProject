import contextlib
from typing import Final, Generator

from config import CONFIG
from sqlalchemy import Connection, Engine, create_engine
from utils import export

_ENGINE: Final[Engine] = create_engine(CONFIG.database_url)


@export
def get_engine() -> Engine:
    return _ENGINE


@contextlib.contextmanager
@export
def get_connection() -> Generator[None, None, Connection]:
    with _ENGINE.connect() as conn:
        yield conn
        yield conn
