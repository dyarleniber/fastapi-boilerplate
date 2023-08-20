from typing import List

from httpx import AsyncClient
from pydantic import BaseModel

from ..types import Config, Logger, Nutrients, NutrientSource
from ..utils.micrograms_to_grams import micrograms_to_grams
from ..utils.milligrams_to_grams import milligrams_to_grams
from ..utils.nutrient_to_int import nutrient_to_int


class EdamamNutrient(BaseModel):
    label: str
    quantity: float
    unit: str


class EdamamNutrients(BaseModel):
    ENERC_KCAL: EdamamNutrient
    PROCNT: EdamamNutrient | None = None
    FAT: EdamamNutrient | None = None
    FASAT: EdamamNutrient | None = None
    CHOCDF: EdamamNutrient | None = None
    FIBTG: EdamamNutrient | None = None
    SUGAR: EdamamNutrient | None = None
    CHOLE: EdamamNutrient | None = None
    NA: EdamamNutrient | None = None


class EdamamParsedIngredient(BaseModel):
    quantity: float
    measure: str
    food: str
    weight: float
    nutrients: EdamamNutrients
    status: str


class EdamamIngredient(BaseModel):
    parsed: List[EdamamParsedIngredient]


class EdamamResponse(BaseModel):
    ingredients: List[EdamamIngredient]


class FetchEdamamNutrients:
    def __init__(self, config: Config, logger: Logger, http_client: AsyncClient):
        self.config = config
        self.logger = logger
        self.http_client = http_client

    def get_nutrient_milligrams(
        self, *, nutrient: EdamamNutrient | None
    ) -> float | None:
        if nutrient:
            match nutrient.unit:
                case "mg":
                    return nutrient.quantity
                case _:
                    return None
        return None

    def get_nutrient_grams(self, *, nutrient: EdamamNutrient | None) -> float | None:
        if nutrient:
            match nutrient.unit:
                case "µg":
                    return micrograms_to_grams(nutrient.quantity)
                case "mg":
                    return milligrams_to_grams(nutrient.quantity)
                case "g":
                    return nutrient.quantity
                case _:
                    return None
        return None

    async def execute(self, *, query: str) -> List[Nutrients] | None:
        try:
            url = f"{self.config.edamam.base_url}/api/nutrition-data"
            headers = {
                "Content-Type": "application/json",
            }
            params = {
                "ingr": query.replace(",", " AND "),
                "app_id": self.config.edamam.app_id,
                "app_key": self.config.edamam.app_key,
                "nutrition-type": "cooking",
            }
            response = await self.http_client.get(
                url, headers=headers, params=params, timeout=5
            )
            response.raise_for_status()
            response_data = response.json()
            edamam_response = EdamamResponse(**response_data)
            nutrients: List[Nutrients] = []
            for edamam_ingredient in edamam_response.ingredients:
                for edamam_parsed_ingredient in edamam_ingredient.parsed:
                    nutrients.append(
                        Nutrients(
                            name=edamam_parsed_ingredient.food,
                            quantity=int(edamam_parsed_ingredient.quantity),
                            unit=edamam_parsed_ingredient.measure,
                            calories_kcal=nutrient_to_int(
                                edamam_parsed_ingredient.nutrients.ENERC_KCAL.quantity
                            ),
                            weight_grams=nutrient_to_int(
                                edamam_parsed_ingredient.weight
                            ),
                            calories_kcal_per_gram=nutrient_to_int(
                                edamam_parsed_ingredient.nutrients.ENERC_KCAL.quantity
                                / edamam_parsed_ingredient.weight
                            )
                            if edamam_parsed_ingredient.nutrients.ENERC_KCAL.quantity
                            and edamam_parsed_ingredient.weight
                            else None,
                            protein_grams=nutrient_to_int(
                                self.get_nutrient_grams(
                                    nutrient=edamam_parsed_ingredient.nutrients.PROCNT
                                )
                            ),
                            total_fat_grams=nutrient_to_int(
                                self.get_nutrient_grams(
                                    nutrient=edamam_parsed_ingredient.nutrients.FAT
                                )
                            ),
                            saturated_fat_grams=nutrient_to_int(
                                self.get_nutrient_grams(
                                    nutrient=edamam_parsed_ingredient.nutrients.FASAT
                                )
                            ),
                            total_carbohydrates_grams=nutrient_to_int(
                                self.get_nutrient_grams(
                                    nutrient=edamam_parsed_ingredient.nutrients.CHOCDF
                                )
                            ),
                            dietary_fiber_grams=nutrient_to_int(
                                self.get_nutrient_grams(
                                    nutrient=edamam_parsed_ingredient.nutrients.FIBTG
                                )
                            ),
                            sugars_grams=nutrient_to_int(
                                self.get_nutrient_grams(
                                    nutrient=edamam_parsed_ingredient.nutrients.SUGAR
                                )
                            ),
                            cholesterol_mg=nutrient_to_int(
                                self.get_nutrient_milligrams(
                                    nutrient=edamam_parsed_ingredient.nutrients.CHOLE
                                )
                            ),
                            sodium_mg=nutrient_to_int(
                                self.get_nutrient_milligrams(
                                    nutrient=edamam_parsed_ingredient.nutrients.NA
                                )
                            ),
                            source=NutrientSource.EDAMAM,
                        )
                    )
            return nutrients
        except Exception as e:
            self.logger.error(f"Failed to fetch edamam nutrients: {str(e)}")
            return None
