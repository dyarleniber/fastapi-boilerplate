from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from httpx import AsyncClient

from .config import config
from .logger import Logger
from .services.fetch_edamam_nutrients import FetchEdamamNutrients
from .services.fetch_nutritionix_nutrients import FetchNutritionixNutrients
from .services.fetch_spoonacular_nutrients import FetchSpoonacularNutrients

http_client = AsyncClient()
logger = Logger(config)
fetch_nutritionix_nutrients = FetchNutritionixNutrients(config, logger, http_client)
fetch_spoonacular_nutrients = FetchSpoonacularNutrients(config, logger, http_client)
fetch_edamam_nutrients = FetchEdamamNutrients(config, logger, http_client)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # shutdown
    await http_client.aclose()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def get_health():
    return {"message": "OK"}


@app.get("/nutrients/{query}")
async def get_nutrients(query: str):
    try:
        language = "en_US"
        nutritionix_nutrients = await fetch_nutritionix_nutrients.execute(
            query=query, language=language
        )
        if nutritionix_nutrients:
            return nutritionix_nutrients
        spoonacular_nutrients = await fetch_spoonacular_nutrients.execute(query=query)
        if spoonacular_nutrients:
            return spoonacular_nutrients
        edamam_nutrients = await fetch_edamam_nutrients.execute(query=query)
        if edamam_nutrients:
            return edamam_nutrients
    except Exception as e:
        logger.error(f"Failed to get nutrients: {str(e)}")
        raise HTTPException(status_code=500)
    raise HTTPException(status_code=404)
