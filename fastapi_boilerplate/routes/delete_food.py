from fastapi import Response, HTTPException
from ..types import (
    Logger,
    RemoveFood,
)


class DeleteFood:
    def __init__(
        self,
        logger: Logger,
        remove_food: RemoveFood,
    ):
        self.logger = logger
        self.remove_food = remove_food

    async def execute(self, id: str, response: Response):
        try:
            result = self.remove_food.execute(id=id)
            if result["deleted_count"]:
                response.status_code = 204
                return response
            response.status_code = 404
            return response
        except Exception as e:
            self.logger.error(f"Failed to delete food: {str(e)}")
            raise HTTPException(status_code=500)
