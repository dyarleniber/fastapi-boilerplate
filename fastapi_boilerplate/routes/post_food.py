from pydantic import BaseModel, Field
from fastapi import HTTPException, Body
from ..types import (
    Logger,
    InsertFood,
)
from fastapi.encoders import jsonable_encoder


class Data(BaseModel):
    name: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "apple",
            }
        }


class PostFood:
    def __init__(
        self,
        logger: Logger,
        insert_food: InsertFood,
    ):
        self.logger = logger
        self.insert_food = insert_food

    async def execute(self, data: Data = Body(...)):
        try:
            food_data = jsonable_encoder(data)
            result = self.insert_food.execute(data=food_data)
            return {"id": result["inserted_id"]}
        except Exception as e:
            self.logger.error(f"Failed to post food: {str(e)}")
            raise HTTPException(status_code=500)
