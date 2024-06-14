from httpx import AsyncClient

from .config import config
from .logger import Logger
from .db import Db
from .services.fetch_edamam_nutrients import FetchEdamamNutrients
from .services.fetch_nutritionix_nutrients import FetchNutritionixNutrients
from .services.fetch_spoonacular_nutrients import FetchSpoonacularNutrients
from .repositories.insert_food import InsertFood
from .repositories.find_foods import FindFoods
from .repositories.find_food_by_id import FindFoodById
from .repositories.update_food import UpdateFood
from .repositories.remove_food import RemoveFood
from .routes.get_nutrients import GetNutrients
from .routes.post_food import PostFood
from .routes.get_foods import GetFoods
from .routes.get_food_by_id import GetFoodById
from .routes.put_food import PutFood
from .routes.delete_food import DeleteFood


http_client = AsyncClient()
logger = Logger(config)
db = Db(config)


# Services


fetch_nutritionix_nutrients = FetchNutritionixNutrients(config, logger, http_client)
fetch_spoonacular_nutrients = FetchSpoonacularNutrients(config, logger, http_client)
fetch_edamam_nutrients = FetchEdamamNutrients(config, logger, http_client)


# Repositories


insert_food = InsertFood(config, db)
find_foods = FindFoods(config, db)
find_food_by_id = FindFoodById(config, db)
update_food = UpdateFood(config, db)
remove_food = RemoveFood(config, db)


# Routes


get_nutrients = GetNutrients(
    logger,
    fetch_nutritionix_nutrients,
    fetch_spoonacular_nutrients,
    fetch_edamam_nutrients,
)
post_food = PostFood(logger, insert_food)
get_foods = GetFoods(logger, find_foods)
get_food_by_id = GetFoodById(logger, find_food_by_id)
put_food = PutFood(logger, update_food)
delete_food = DeleteFood(logger, remove_food)


async def startup() -> None:
    db.connect()


async def shutdown() -> None:
    db.disconnect()
    await http_client.aclose()
