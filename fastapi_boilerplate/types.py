from dataclasses import dataclass
from enum import Enum
from typing import List, Protocol
from pymongo.database import Database


class Language(str, Enum):
    EN_US = "en_US"
    PT_BR = "pt_BR"
    IT_IT = "it_IT"


class Collection(str, Enum):
    FOODS = "foods"


# Config


@dataclass(kw_only=True, slots=True)
class DatabaseConfig:
    url: str
    name: str


@dataclass(kw_only=True, slots=True)
class NutritionixConfig:
    base_url: str
    app_id: str
    app_key: str


@dataclass(kw_only=True, slots=True)
class SpoonacularConfig:
    base_url: str
    api_key: str


@dataclass(kw_only=True, slots=True)
class EdamamConfig:
    base_url: str
    app_id: str
    app_key: str


@dataclass(kw_only=True, slots=True)
class Config:
    log_level: int
    db: DatabaseConfig
    nutritionix: NutritionixConfig
    spoonacular: SpoonacularConfig
    edamam: EdamamConfig


# Logger


class Logger(Protocol):
    def debug(self, message: str) -> None:
        ...

    def info(self, message: str) -> None:
        ...

    def warning(self, message: str) -> None:
        ...

    def error(self, message: str) -> None:
        ...

    def critical(self, message: str) -> None:
        ...


# Database


class Db(Protocol):
    def connect(self) -> None:
        ...

    def disconnect(self) -> None:
        ...

    def get_collection(self, collection: Collection) -> Database:
        ...


# Services


class NutrientSource(str, Enum):
    NUTRITIONIX = "nutritionix"
    SPOONACULAR = "spoonacular"
    EDAMAM = "edamam"


@dataclass(kw_only=True, slots=True)
class Nutrients:
    name: str
    brand_name: str | None = None
    quantity: int
    unit: str
    calories_kcal: int
    weight_grams: int | None = None
    calories_kcal_per_gram: int | None = None
    protein_grams: int | None = None
    total_fat_grams: int | None = None
    saturated_fat_grams: int | None = None
    total_carbohydrates_grams: int | None = None
    dietary_fiber_grams: int | None = None
    sugars_grams: int | None = None
    cholesterol_mg: int | None = None
    sodium_mg: int | None = None
    source: NutrientSource


class FetchNutritionixNutrients(Protocol):
    def execute(
        self, *, query: str, language: Language | None
    ) -> List[Nutrients] | None:
        ...


class FetchSpoonacularNutrients(Protocol):
    def execute(self, *, query: str) -> List[Nutrients] | None:
        ...


class FetchEdamamNutrients(Protocol):
    def execute(self, *, query: str) -> List[Nutrients] | None:
        ...


# Repositories


class InsertFood(Protocol):
    def execute(self) -> None:
        ...


class FindFoodById(Protocol):
    def execute(self) -> None:
        ...


class FindFoods(Protocol):
    def execute(self) -> None:
        ...


class UpdateFood(Protocol):
    def execute(self) -> None:
        ...


class RemoveFood(Protocol):
    def execute(self) -> None:
        ...
