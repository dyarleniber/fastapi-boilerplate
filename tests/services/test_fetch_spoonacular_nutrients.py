from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import AsyncClient, Response

from fastapi_boilerplate.services.fetch_spoonacular_nutrients import (
    FetchSpoonacularNutrients,
)
from fastapi_boilerplate.types import Config, Logger, Nutrients, NutrientSource


@pytest.fixture
def config():
    config = MagicMock(spec_set=Config)
    config.spoonacular.base_url = "https://api.spoonacular.com"
    config.spoonacular.api_key = "test_api_key"
    return config


@pytest.fixture
def logger():
    logger = MagicMock(spec_set=Logger)
    return logger


@pytest.fixture
def http_client():
    http_client_response = MagicMock(spec_set=Response)
    http_client_response.json.return_value = [
        {
            "name": "food_1",
            "amount": 1.0,
            "unit": "food_1_unit",
            "nutrition": {
                "nutrients": [
                    {
                        "name": "Calories",
                        "amount": 100.1111,
                        "unit": "kcal",
                    },
                    {
                        "name": "Protein",
                        "amount": 1,
                        "unit": "g",
                    },
                    {
                        "name": "Fat",
                        "amount": 0.2222,
                        "unit": "g",
                    },
                    {
                        "name": "Saturated Fat",
                        "amount": 0.33,
                        "unit": "g",
                    },
                    {
                        "name": "Carbohydrates",
                        "amount": 44.4,
                        "unit": "g",
                    },
                    {
                        "name": "Fiber",
                        "amount": 55,
                        "unit": "g",
                    },
                    {
                        "name": "Sugar",
                        "amount": 0.066,
                        "unit": "g",
                    },
                    {
                        "name": "Cholesterol",
                        "amount": 0.07,
                        "unit": "mg",
                    },
                    {
                        "name": "Sodium",
                        "amount": 0,
                        "unit": "mg",
                    },
                ],
                "weightPerServing": {"amount": 22.22, "unit": "g"},
            },
        },
        {
            "name": "food_2",
            "amount": 1.0,
            "unit": "food_2_unit",
            "nutrition": {
                "nutrients": [
                    {
                        "name": "Calories",
                        "amount": 200,
                        "unit": "kcal",
                    }
                ],
                "weightPerServing": {"amount": 1, "unit": "g"},
            },
        },
    ]
    http_client = AsyncMock(set_spec=AsyncClient)
    http_client.post.return_value = http_client_response
    return http_client


@pytest.fixture
def fetch_spoonacular_nutrients(config, logger, http_client):
    fetch_spoonacular_nutrients = FetchSpoonacularNutrients(config, logger, http_client)
    return fetch_spoonacular_nutrients


@pytest.mark.anyio
async def test_execute(logger, http_client, fetch_spoonacular_nutrients):
    result = await fetch_spoonacular_nutrients.execute(query="test_query")
    assert result == [
        Nutrients(
            name="food_1",
            quantity=1,
            unit="food_1_unit",
            calories_kcal=10011,
            weight_grams=2222,
            calories_kcal_per_gram=451,
            protein_grams=100,
            total_fat_grams=22,
            saturated_fat_grams=33,
            total_carbohydrates_grams=4440,
            dietary_fiber_grams=5500,
            sugars_grams=7,
            cholesterol_mg=7,
            source=NutrientSource.SPOONACULAR,
        ),
        Nutrients(
            name="food_2",
            quantity=1,
            unit="food_2_unit",
            calories_kcal=20000,
            weight_grams=100,
            calories_kcal_per_gram=20000,
            source=NutrientSource.SPOONACULAR,
        ),
    ]
    logger.error.assert_not_called()
    http_client.post.assert_called_once_with(
        "https://api.spoonacular.com/recipes/parseIngredients?apiKey=test_api_key",
        headers={
            "User-Agent": "FOOD AI API",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "ingredientList": "test_query",
            "servings": 1,
            "includeNutrition": "true",
            "language": "en",
        },
        timeout=5,
    )
    http_client.post.return_value.raise_for_status.assert_called_once()


@pytest.mark.anyio
async def test_execute_with_empty_food_name_response(
    logger, http_client, fetch_spoonacular_nutrients
):
    http_client_response = MagicMock(spec_set=Response)
    http_client_response.json.return_value = [
        {
            "amount": 1.0,
            "unit": "food_unit",
            "nutrition": {
                "nutrients": [
                    {
                        "name": "Calories",
                        "amount": 200,
                        "unit": "kcal",
                    }
                ],
                "weightPerServing": {"amount": 1, "unit": "g"},
            },
        },
    ]
    http_client.post.return_value = http_client_response
    result = await fetch_spoonacular_nutrients.execute(query="test_query")
    assert result is None
    logger.error.assert_called_once()


@pytest.mark.anyio
async def test_execute_with_empty_quantity_response(
    logger, http_client, fetch_spoonacular_nutrients
):
    http_client_response = MagicMock(spec_set=Response)
    http_client_response.json.return_value = [
        {
            "name": "food",
            "unit": "food_unit",
            "nutrition": {
                "nutrients": [
                    {
                        "name": "Calories",
                        "amount": 200,
                        "unit": "kcal",
                    }
                ],
                "weightPerServing": {"amount": 1, "unit": "g"},
            },
        },
    ]
    http_client.post.return_value = http_client_response
    result = await fetch_spoonacular_nutrients.execute(query="test_query")
    assert result is None
    logger.error.assert_called_once()


@pytest.mark.anyio
async def test_execute_with_empty_unit_response(
    logger, http_client, fetch_spoonacular_nutrients
):
    http_client_response = MagicMock(spec_set=Response)
    http_client_response.json.return_value = [
        {
            "name": "food",
            "amount": 1.0,
            "nutrition": {
                "nutrients": [
                    {
                        "name": "Calories",
                        "amount": 200,
                        "unit": "kcal",
                    }
                ],
                "weightPerServing": {"amount": 1, "unit": "g"},
            },
        },
    ]
    http_client.post.return_value = http_client_response
    result = await fetch_spoonacular_nutrients.execute(query="test_query")
    assert result is None
    logger.error.assert_called_once()


@pytest.mark.anyio
async def test_execute_with_empty_calories_response(
    logger, http_client, fetch_spoonacular_nutrients
):
    http_client_response = MagicMock(spec_set=Response)
    http_client_response.json.return_value = [
        {
            "name": "food",
            "amount": 1.0,
            "unit": "food_unit",
            "nutrition": {
                "nutrients": [],
                "weightPerServing": {"amount": 1, "unit": "g"},
            },
        },
    ]
    http_client.post.return_value = http_client_response
    result = await fetch_spoonacular_nutrients.execute(query="test_query")
    assert result is None
    logger.error.assert_called_once()


@pytest.mark.anyio
async def test_execute_with_exception(logger, http_client, fetch_spoonacular_nutrients):
    http_client.post.side_effect = Exception("test_error")
    result = await fetch_spoonacular_nutrients.execute(query="test_query")
    assert result is None
    logger.error.assert_called_once_with(
        "Failed to fetch spoonacular nutrients: test_error"
    )
