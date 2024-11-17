import contextlib
from typing import Final, Generator

from sqlalchemy import Connection, Engine, create_engine

from api.config import CONFIG
from api.utils import export

_ENGINE: Final[Engine] = create_engine(CONFIG.database_url)


@export
def get_engine() -> Engine:
    return _ENGINE


@contextlib.contextmanager
@export
def get_connection() -> Generator[Connection, None, None]:
    with _ENGINE.connect() as conn:
        yield conn
