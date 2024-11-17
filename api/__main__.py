import logging
from contextlib import asynccontextmanager

from config import CONFIG
from fastapi import FastAPI
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup

    yield

    # shutdown


app = FastAPI(lifespan=lifespan)


@app.get("/shart")
def test():
    return "hello, world!"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=CONFIG.port)
