from typing import Any, Final

from sqlalchemy import MetaData, Table, text

from . import engine

_META = MetaData()

_TABLES_QUERY = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'"


class _TableManager:

    def __init__(self):
        self.tables: dict[str, Table] = dict()
        self.load_tables()

    def load_tables(self):
        eng = engine.get_engine()
        with eng.connect() as conn:
            for (table_name,) in conn.execute(text(_TABLES_QUERY)).all():
                self.tables[table_name] = Table(table_name, _META, autoload_with=eng)

    def __getattr__(self, name) -> Table | Any:
        if name in self.tables:
            return self.tables[name]
        else:
            return super().__getattribute__(name)


tables: Final[_TableManager] = _TableManager()
