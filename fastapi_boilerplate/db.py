from pymongo import MongoClient
from pymongo.database import Database
from .types import Config, Collection


class Db:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.client: MongoClient | None = None

    def connect(self) -> None:
        self.client = MongoClient(self.config.db.url)

    def disconnect(self) -> None:
        self.client.close()

    def get_collection(self, collection: Collection) -> Database:
        if self.client is None:
            self.connect()
        db = self.client[self.config.db.name]
        return db[collection]
