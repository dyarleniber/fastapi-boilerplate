from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter

from .dependencies import (
    get_nutrients,
    post_food,
    get_foods,
    get_food_by_id,
    put_food,
    delete_food,
    shutdown,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
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

# todo: add response model
# @router.get("/", response_description="List all books", response_model=List[Book])
# todo: add response status code
foods_router = APIRouter(prefix="/foods", tags=["foods"])
foods_router.add_api_route("/", endpoint=post_food.execute, methods=["POST"])
foods_router.add_api_route("/", endpoint=get_foods.execute, methods=["GET"])
foods_router.add_api_route("/{id}", endpoint=get_food_by_id.execute, methods=["GET"])
foods_router.add_api_route("/{id}", endpoint=put_food.execute, methods=["PUT"])
foods_router.add_api_route("/{id}", endpoint=delete_food.execute, methods=["DELETE"])


app.include_router(nutrients_router)
app.include_router(foods_router)
