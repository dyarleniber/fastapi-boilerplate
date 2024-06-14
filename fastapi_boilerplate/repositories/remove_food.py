from bson.objectid import ObjectId
from ..types import Config, Collection, Db


class RemoveFood:
    def __init__(self, config: Config, db: Db):
        self.config = config
        self.db = db

    def execute(self, *, id: str):
        foods_collection = self.db.get_collection(Collection.FOODS)
        result = foods_collection.delete_one({"_id": ObjectId(id)})
        return {"deleted_count": result.deleted_count}
