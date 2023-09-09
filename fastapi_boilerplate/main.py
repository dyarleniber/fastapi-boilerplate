from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter


from .dependencies import (
    get_nutrients,
    startup,
    shutdown,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup()
    yield
    await shutdown()


app = FastAPI(lifespan=lifespan)


@app.get("/", include_in_schema=False)
async def get_health():
    return {"message": "OK"}


nutrients_router = APIRouter(prefix="/nutrients", tags=["nutrients"])
nutrients_router.add_api_route(
    "/{query}", endpoint=get_nutrients.execute, methods=["GET"]
)


app.include_router(nutrients_router)
