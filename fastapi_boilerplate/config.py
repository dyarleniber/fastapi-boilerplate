import logging
import os

from dotenv import load_dotenv

from .types import Config, EdamamConfig, NutritionixConfig, SpoonacularConfig

load_dotenv()


config = Config(
    log_level=logging.WARNING,
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
