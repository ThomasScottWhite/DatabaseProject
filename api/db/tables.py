from typing import Any, Final

from sqlalchemy import MetaData, Table, text

from . import engine

_META = MetaData()

_TABLES_QUERY = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'"


class _TableManager:

    def __init__(self):
        self.meta = MetaData()
        self.load_tables()

    def load_tables(self):
        self.meta.reflect(bind=engine.get_engine())

    def __getattr__(self, name) -> Table | Any:
        if name in self.meta.tables:
            return self.meta.tables[name]
        else:
            return super().__getattribute__(name)


tables: Final[_TableManager] = _TableManager()
