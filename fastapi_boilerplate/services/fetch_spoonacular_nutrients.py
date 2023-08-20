from typing import List

from httpx import AsyncClient
from pydantic import BaseModel

from ..types import Config, Logger, Nutrients, NutrientSource
from ..utils.micrograms_to_grams import micrograms_to_grams
from ..utils.milligrams_to_grams import milligrams_to_grams
from ..utils.nutrient_to_int import nutrient_to_int


class SpoonacularNutrient(BaseModel):
    name: str
    amount: float
    unit: str


class SpoonacularWeightPerServing(BaseModel):
    amount: float
    unit: str


class SpoonacularNutrition(BaseModel):
    nutrients: List[SpoonacularNutrient]
    weightPerServing: SpoonacularWeightPerServing


class SpoonacularIngredient(BaseModel):
    name: str
    amount: float
    unit: str
    nutrition: SpoonacularNutrition


class FetchSpoonacularNutrients:
    def __init__(self, config: Config, logger: Logger, http_client: AsyncClient):
        self.config = config
        self.logger = logger
        self.http_client = http_client

    def find_nutrient(
        self, *, name: str, nutrients: List[SpoonacularNutrient]
    ) -> SpoonacularNutrient | None:
        return next(filter(lambda nutrient: nutrient.name == name, nutrients), None)

    def get_nutrient_milligrams(
        self, *, name: str, nutrients: List[SpoonacularNutrient]
    ) -> float | None:
        nutrient = self.find_nutrient(name=name, nutrients=nutrients)
        if nutrient:
            match nutrient.unit:
                case "mg":
                    return nutrient.amount
                case _:
                    return None
        return None

    def get_nutrient_grams(
        self, *, name: str, nutrients: List[SpoonacularNutrient]
    ) -> float | None:
        nutrient = self.find_nutrient(name=name, nutrients=nutrients)
        if nutrient:
            match nutrient.unit:
                case "µg":
                    return micrograms_to_grams(nutrient.amount)
                case "mg":
                    return milligrams_to_grams(nutrient.amount)
                case "g":
                    return nutrient.amount
                case _:
                    return None
        return None

    async def execute(self, *, query: str) -> List[Nutrients] | None:
        try:
            url = f"{self.config.spoonacular.base_url}/recipes/parseIngredients?apiKey={self.config.spoonacular.api_key}"
            headers = {
                "User-Agent": "FOOD AI API",
                "Content-Type": "application/x-www-form-urlencoded",
            }
            data = {
                "ingredientList": query.replace(",", "\n"),
                "servings": 1,
                "includeNutrition": "true",
                "language": "en",
            }
            response = await self.http_client.post(
                url, headers=headers, data=data, timeout=5
            )
            response.raise_for_status()
            response_data = response.json()
            nutrients: List[Nutrients] = []
            for response_item in response_data:
                spoonacular_ingredient = SpoonacularIngredient.model_validate(
                    response_item
                )
                spoonacular_nutrients = spoonacular_ingredient.nutrition.nutrients
                spoonacular_weight_per_serving = (
                    spoonacular_ingredient.nutrition.weightPerServing
                )
                if spoonacular_weight_per_serving.unit != "g":
                    self.logger.error(
                        f"Failed to fetch Spoonacular nutrients: {spoonacular_ingredient.name} does not have weight in grams"
                    )
                    return None
                calories = self.find_nutrient(
                    name="Calories", nutrients=spoonacular_nutrients
                )
                if not calories or calories.unit != "kcal":
                    self.logger.error(
                        f"Failed to fetch Spoonacular nutrients: {spoonacular_ingredient.name} does not have calories"
                    )
                    return None
                calories_kcal = calories.amount
                quantity = int(spoonacular_ingredient.amount)
                weight_grams = spoonacular_weight_per_serving.amount * quantity
                nutrients.append(
                    Nutrients(
                        name=spoonacular_ingredient.name,
                        quantity=quantity,
                        unit=spoonacular_ingredient.unit,
                        calories_kcal=nutrient_to_int(calories_kcal),
                        weight_grams=nutrient_to_int(weight_grams),
                        calories_kcal_per_gram=nutrient_to_int(
                            calories_kcal / weight_grams
                        )
                        if calories_kcal and weight_grams
                        else None,
                        protein_grams=nutrient_to_int(
                            self.get_nutrient_grams(
                                name="Protein", nutrients=spoonacular_nutrients
                            )
                        ),
                        total_fat_grams=nutrient_to_int(
                            self.get_nutrient_grams(
                                name="Fat", nutrients=spoonacular_nutrients
                            )
                        ),
                        saturated_fat_grams=nutrient_to_int(
                            self.get_nutrient_grams(
                                name="Saturated Fat", nutrients=spoonacular_nutrients
                            )
                        ),
                        total_carbohydrates_grams=nutrient_to_int(
                            self.get_nutrient_grams(
                                name="Carbohydrates", nutrients=spoonacular_nutrients
                            )
                        ),
                        dietary_fiber_grams=nutrient_to_int(
                            self.get_nutrient_grams(
                                name="Fiber", nutrients=spoonacular_nutrients
                            )
                        ),
                        sugars_grams=nutrient_to_int(
                            self.get_nutrient_grams(
                                name="Sugar", nutrients=spoonacular_nutrients
                            )
                        ),
                        cholesterol_mg=nutrient_to_int(
                            self.get_nutrient_milligrams(
                                name="Cholesterol", nutrients=spoonacular_nutrients
                            )
                        ),
                        sodium_mg=nutrient_to_int(
                            self.get_nutrient_milligrams(
                                name="Sodium", nutrients=spoonacular_nutrients
                            )
                        ),
                        source=NutrientSource.SPOONACULAR,
                    )
                )
            return nutrients
        except Exception as e:
            self.logger.error(f"Failed to fetch spoonacular nutrients: {str(e)}")
            return None
