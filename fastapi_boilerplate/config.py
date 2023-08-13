import logging
import os

from dotenv import load_dotenv

from .types import Config, NutritionixConfig

load_dotenv()


config = Config(
    log_level=logging.WARNING,
    nutritionix=NutritionixConfig(
        base_url=os.environ.get("NUTRITIONIX_BASE_URL") or "",
        app_id=os.environ.get("NUTRITIONIX_APP_ID") or "",
        app_key=os.environ.get("NUTRITIONIX_APP_KEY") or "",
    ),
)
