from bson.objectid import ObjectId
from ..types import Config, Collection, Db


class UpdateFood:
    def __init__(self, config: Config, db: Db):
        self.config = config
        self.db = db

    def execute(self, *, id: str, data):
        foods_collection = self.db.get_collection(Collection.FOODS)
        result = foods_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        return {"modified_count": result.modified_count}
