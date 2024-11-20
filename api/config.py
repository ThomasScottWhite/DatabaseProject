from typing import Final

from pydantic_settings import BaseSettings


class _Config(BaseSettings):
    database_url: str = (
        "postgresql://admin:admin@localhost:5432/greek_management_studio"
    )
    port: int = 6969


CONFIG: Final[_Config] = _Config()
