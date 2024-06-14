from fastapi import Response, HTTPException
from ..types import (
    Logger,
    FindFoodById,
)


class GetFoodById:
    def __init__(
        self,
        logger: Logger,
        find_food_by_id: FindFoodById,
    ):
        self.logger = logger
        self.find_food_by_id = find_food_by_id

    async def execute(self, id: str, response: Response):
        try:
            food = self.find_food_by_id.execute(id=id)
            if food:
                return food
            response.status_code = 404
            return response
        except Exception as e:
            self.logger.error(f"Failed to get food by id: {str(e)}")
            raise HTTPException(status_code=500)
