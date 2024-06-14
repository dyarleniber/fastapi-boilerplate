from pydantic import BaseModel
from fastapi import Response, HTTPException, Body
from ..types import (
    Logger,
    UpdateFood,
)


class Data(BaseModel):
    name: str | None

    class Config:
        schema_extra = {
            "example": {
                "name": "apple",
            }
        }


class PutFood:
    def __init__(
        self,
        logger: Logger,
        update_food: UpdateFood,
    ):
        self.logger = logger
        self.update_food = update_food

    async def execute(self, id: str, response: Response, data: Data = Body(...)):
        try:
            food_data = {k: v for k, v in data.dict().items() if v is not None}
            if len(food_data) == 0:
                response.status_code = 400
                return response
            result = self.update_food.execute(id=id, data=food_data)
            if result["modified_count"]:
                response.status_code = 204
                return response
            response.status_code = 404
            return response
        except Exception as e:
            self.logger.error(f"Failed to put food: {str(e)}")
            raise HTTPException(status_code=500)
