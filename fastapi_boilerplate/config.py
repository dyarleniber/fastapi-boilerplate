import logging
import os

from dotenv import load_dotenv

from .types import (
    Config,
    DatabaseConfig,
    EdamamConfig,
    NutritionixConfig,
    SpoonacularConfig,
)


load_dotenv()


config = Config(
    log_level=logging.WARNING,
    db=DatabaseConfig(
        url=f"mongodb+srv://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@{os.environ.get('DB_NAME')}.5j7qvjf.mongodb.net/?retryWrites=true&w=majority",
        name=os.environ.get("DB_NAME") or "",
    ),
    nutritionix=NutritionixConfig(
        base_url=os.environ.get("NUTRITIONIX_BASE_URL") or "",
        app_id=os.environ.get("NUTRITIONIX_APP_ID") or "",
        app_key=os.environ.get("NUTRITIONIX_APP_KEY") or "",
    ),
    spoonacular=SpoonacularConfig(
        base_url=os.environ.get("SPOONACULAR_BASE_URL") or "",
        api_key=os.environ.get("SPOONACULAR_API_KEY") or "",
    ),
    edamam=EdamamConfig(
        base_url=os.environ.get("EDAMAM_BASE_URL") or "",
        app_id=os.environ.get("EDAMAM_APP_ID") or "",
        app_key=os.environ.get("EDAMAM_APP_KEY") or "",
    ),
)
