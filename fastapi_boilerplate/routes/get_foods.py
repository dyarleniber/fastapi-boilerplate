from fastapi import HTTPException
from ..types import (
    Logger,
    FindFoods,
)


class GetFoods:
    def __init__(
        self,
        logger: Logger,
        find_foods: FindFoods,
    ):
        self.logger = logger
        self.find_foods = find_foods

    async def execute(self):
        try:
            foods = self.find_foods.execute()
            if foods:
                return foods
            return []
        except Exception as e:
            self.logger.error(f"Failed to get foods: {str(e)}")
            raise HTTPException(status_code=500)
