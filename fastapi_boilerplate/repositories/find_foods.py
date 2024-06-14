from ..types import Config, Collection, Db


class FindFoods:
    def __init__(self, config: Config, db: Db):
        self.config = config
        self.db = db

    def execute(self):
        foods_collection = self.db.get_collection(Collection.FOODS)
        foods = []
        for food in foods_collection.find(limit=100):
            foods.append(
                {
                    "id": str(food["_id"]),
                    "name": food["name"],
                }
            )
        return foods
