from fastapi import HTTPException
from ..types import (
    Logger,
    FetchNutritionixNutrients,
    FetchSpoonacularNutrients,
    FetchEdamamNutrients,
)


class GetNutrients:
    def __init__(
        self,
        logger: Logger,
        fetch_nutritionix_nutrients: FetchNutritionixNutrients,
        fetch_spoonacular_nutrients: FetchSpoonacularNutrients,
        fetch_edamam_nutrients: FetchEdamamNutrients,
    ):
        self.logger = logger
        self.fetch_nutritionix_nutrients = fetch_nutritionix_nutrients
        self.fetch_spoonacular_nutrients = fetch_spoonacular_nutrients
        self.fetch_edamam_nutrients = fetch_edamam_nutrients

    async def execute(self, query: str):
        try:
            language = "en_US"
            nutritionix_nutrients = await self.fetch_nutritionix_nutrients.execute(
                query=query, language=language
            )
            if nutritionix_nutrients:
                return nutritionix_nutrients
            spoonacular_nutrients = await self.fetch_spoonacular_nutrients.execute(
                query=query
            )
            if spoonacular_nutrients:
                return spoonacular_nutrients
            edamam_nutrients = await self.fetch_edamam_nutrients.execute(query=query)
            if edamam_nutrients:
                return edamam_nutrients
        except Exception as e:
            self.logger.error(f"Failed to get nutrients: {str(e)}")
            raise HTTPException(status_code=500)
        raise HTTPException(status_code=404)
