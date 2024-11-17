from typing import Final

from pydantic_settings import BaseSettings


class _Config(BaseSettings):
    database_url: str = "sqlite:///./test.db"
    port: int = 6969


CONFIG: Final[_Config] = _Config()
CONFIG: Final[_Config] = _Config()
