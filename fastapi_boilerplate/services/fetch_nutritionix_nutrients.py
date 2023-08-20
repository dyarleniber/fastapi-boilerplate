from typing import List

from httpx import AsyncClient
from pydantic import BaseModel

from ..types import Config, Language, Logger, Nutrients, NutrientSource
from ..utils.nutrient_to_int import nutrient_to_int


class NutritionixNutrients(BaseModel):
    food_name: str
    brand_name: str | None = None
    serving_qty: int
    serving_unit: str
    nf_calories: float
    serving_weight_grams: float | None = None
    nf_protein: float | None = None
    nf_total_fat: float | None = None
    nf_saturated_fat: float | None = None
    nf_total_carbohydrate: float | None = None
    nf_dietary_fiber: float | None = None
    nf_sugars: float | None = None
    nf_cholesterol: float | None = None
    nf_sodium: float | None = None


class NutritionixResponse(BaseModel):
    foods: List[NutritionixNutrients]


class FetchNutritionixNutrients:
    def __init__(self, config: Config, logger: Logger, http_client: AsyncClient):
        self.config = config
        self.logger = logger
        self.http_client = http_client

    async def execute(
        self, *, query: str, language: Language = Language.EN_US
    ) -> List[Nutrients] | None:
        try:
            url = f"{self.config.nutritionix.base_url}/v2/natural/nutrients"
            headers = {
                "Content-Type": "application/json",
                "x-app-id": self.config.nutritionix.app_id,
                "x-app-key": self.config.nutritionix.app_key,
                "x-remote-user-id": "0",
            }
            body = {
                "query": query.replace(",", " , "),
                "locale": language,
                "num_servings": 1,
                "line_delimited": False,
                "use_raw_foods": False,
                "use_branded_foods": False,
            }
            response = await self.http_client.post(
                url, headers=headers, json=body, timeout=5
            )
            response.raise_for_status()
            response_data = response.json()
            nutritionix_response = NutritionixResponse.model_validate(response_data)
            nutrients: List[Nutrients] = []
            for nutritionix_nutrients in nutritionix_response.foods:
                nutrients.append(
                    Nutrients(
                        name=nutritionix_nutrients.food_name,
                        brand_name=nutritionix_nutrients.brand_name,
                        quantity=nutritionix_nutrients.serving_qty,
                        unit=nutritionix_nutrients.serving_unit,
                        calories_kcal=nutrient_to_int(
                            nutritionix_nutrients.nf_calories
                        ),
                        weight_grams=nutrient_to_int(
                            nutritionix_nutrients.serving_weight_grams
                        ),
                        calories_kcal_per_gram=nutrient_to_int(
                            nutritionix_nutrients.nf_calories
                            / nutritionix_nutrients.serving_weight_grams
                        )
                        if nutritionix_nutrients.nf_calories
                        and nutritionix_nutrients.serving_weight_grams
                        else None,
                        protein_grams=nutrient_to_int(nutritionix_nutrients.nf_protein),
                        total_fat_grams=nutrient_to_int(
                            nutritionix_nutrients.nf_total_fat
                        ),
                        saturated_fat_grams=nutrient_to_int(
                            nutritionix_nutrients.nf_saturated_fat
                        ),
                        total_carbohydrates_grams=nutrient_to_int(
                            nutritionix_nutrients.nf_total_carbohydrate
                        ),
                        dietary_fiber_grams=nutrient_to_int(
                            nutritionix_nutrients.nf_dietary_fiber
                        ),
                        sugars_grams=nutrient_to_int(nutritionix_nutrients.nf_sugars),
                        cholesterol_mg=nutrient_to_int(
                            nutritionix_nutrients.nf_cholesterol
                        ),
                        sodium_mg=nutrient_to_int(nutritionix_nutrients.nf_sodium),
                        source=NutrientSource.NUTRITIONIX,
                    )
                )
            return nutrients
        except Exception as e:
            self.logger.error(f"Failed to fetch nutritionix nutrients: {str(e)}")
            return None
