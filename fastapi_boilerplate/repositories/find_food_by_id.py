from bson.objectid import ObjectId
from ..types import Config, Collection, Db


class FindFoodById:
    def __init__(self, config: Config, db: Db):
        self.config = config
        self.db = db

    def execute(self, *, id: str):
        foods_collection = self.db.get_collection(Collection.FOODS)
        food = foods_collection.find_one({"_id": ObjectId(id)})
        if food:
            return {"id": str(food["_id"]), "name": food["name"]}
