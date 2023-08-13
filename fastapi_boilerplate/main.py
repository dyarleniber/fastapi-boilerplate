from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from httpx import AsyncClient

from .config import config
from .logger import Logger
from .services.fetch_nutritionix_nutrients import FetchNutritionixNutrients
from .types import NutritionixParams

http_client = AsyncClient()
logger = Logger(config)
fetch_nutritionix_nutrients = FetchNutritionixNutrients(config, logger, http_client)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # shutdown
    await http_client.aclose()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    return {"message": "OK"}


@app.get("/nutrients/{query}")
async def read_nutrients(query: str):
    try:
        params = NutritionixParams(query=query)
        nutrients = await fetch_nutritionix_nutrients.execute(params=params)
        return nutrients
    except Exception as e:
        logger.error(f"Failed to get nutrients: {str(e)}")
        raise HTTPException(status_code=500)
