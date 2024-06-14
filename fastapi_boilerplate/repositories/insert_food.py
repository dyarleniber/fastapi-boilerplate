from ..types import Config, Collection, Db
from typing import TypedDict


class Response(TypedDict):
    inserted_id: str


class InsertFood:
    def __init__(self, config: Config, db: Db):
        self.config = config
        self.db = db

    def execute(self, *, data) -> Response:
        foods_collection = self.db.get_collection(Collection.FOODS)
        result = foods_collection.insert_one(data)
        return {"inserted_id": str(result.inserted_id)}
