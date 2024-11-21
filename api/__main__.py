import logging

from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

logger = logging.getLogger(__name__)

from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.config import CONFIG
from api.routes import ROUTERS


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup

    yield

    # shutdown


app = FastAPI(lifespan=lifespan)

for router in ROUTERS:
    app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=CONFIG.port)
