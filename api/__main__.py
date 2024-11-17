import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

logger = logging.getLogger(__name__)

from api.config import CONFIG


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup

    yield

    # shutdown


app = FastAPI(lifespan=lifespan)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=CONFIG.port)
