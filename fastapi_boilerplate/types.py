from dataclasses import dataclass
from enum import Enum
from typing import List, Protocol


class Language(str, Enum):
    EN_US = "en_US"
    PT_BR = "pt_BR"
    IT_IT = "it_IT"


@dataclass(kw_only=True, slots=True)
class NutritionixConfig:
    base_url: str
    app_id: str
    app_key: str


@dataclass(kw_only=True, slots=True)
class Config:
    log_level: int
    nutritionix: NutritionixConfig


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


@dataclass(kw_only=True, slots=True)
class NutritionixParams:
    query: str
    num_servings: int = 1
    line_delimited: bool = False
    use_raw_foods: bool = False
    use_branded_foods: bool = False
    locale: Language = Language.EN_US


class FetchNutritionixNutrients(Protocol):
    def execute(self, *, params: NutritionixParams) -> List[Nutrients] | None:
        ...
