from httpx import AsyncClient


from .config import config
from .logger import Logger
from .services.fetch_edamam_nutrients import FetchEdamamNutrients
from .services.fetch_nutritionix_nutrients import FetchNutritionixNutrients
from .services.fetch_spoonacular_nutrients import FetchSpoonacularNutrients
from .routes.get_nutrients import GetNutrients


http_client = AsyncClient()


logger = Logger(config)


# Services


fetch_nutritionix_nutrients = FetchNutritionixNutrients(config, logger, http_client)
fetch_spoonacular_nutrients = FetchSpoonacularNutrients(config, logger, http_client)
fetch_edamam_nutrients = FetchEdamamNutrients(config, logger, http_client)


# Routes


get_nutrients = GetNutrients(
    logger,
    fetch_nutritionix_nutrients,
    fetch_spoonacular_nutrients,
    fetch_edamam_nutrients,
)


async def startup() -> None:
    print("Starting up...")


async def shutdown() -> None:
    await http_client.aclose()
