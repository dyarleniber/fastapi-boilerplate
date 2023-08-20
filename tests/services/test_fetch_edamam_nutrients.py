from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import AsyncClient, Response

from fastapi_boilerplate.services.fetch_edamam_nutrients import FetchEdamamNutrients
from fastapi_boilerplate.types import Config, Logger, Nutrients, NutrientSource


@pytest.fixture
def config():
    config = MagicMock(spec_set=Config)
    config.edamam.base_url = "https://api.edamam.com"
    config.edamam.app_id = "test_app_id"
    config.edamam.app_key = "test_app_key"
    return config


@pytest.fixture
def logger():
    logger = MagicMock(spec_set=Logger)
    return logger


@pytest.fixture
def http_client():
    http_client_response = MagicMock(spec_set=Response)
    http_client_response.json.return_value = {
        "ingredients": [
            {
                "parsed": [
                    {
                        "quantity": 1.0,
                        "measure": "food_1_unit",
                        "food": "food_1",
                        "weight": 22.22,
                        "nutrients": {
                            "ENERC_KCAL": {
                                "label": "Calories",
                                "quantity": 100.1111,
                                "unit": "kcal",
                            },
                            "PROCNT": {
                                "label": "Protein",
                                "quantity": 1,
                                "unit": "g",
                            },
                            "FAT": {
                                "label": "Fat",
                                "quantity": 0.2222,
                                "unit": "g",
                            },
                            "FASAT": {
                                "label": "Saturated Fat",
                                "quantity": 0.33,
                                "unit": "g",
                            },
                            "CHOCDF": {
                                "label": "Carbohydrates",
                                "quantity": 44.4,
                                "unit": "g",
                            },
                            "FIBTG": {
                                "label": "Fiber",
                                "quantity": 55,
                                "unit": "g",
                            },
                            "SUGAR": {
                                "label": "Sugar",
                                "quantity": 0.066,
                                "unit": "g",
                            },
                            "CHOLE": {
                                "label": "Cholesterol",
                                "quantity": 0.07,
                                "unit": "mg",
                            },
                            "NA": {
                                "label": "Sodium",
                                "quantity": 0,
                                "unit": "mg",
                            },
                        },
                        "status": "OK",
                    },
                    {
                        "quantity": 1.0,
                        "measure": "food_2_unit",
                        "food": "food_2",
                        "weight": 1,
                        "nutrients": {
                            "ENERC_KCAL": {
                                "label": "Calories",
                                "quantity": 200,
                                "unit": "kcal",
                            }
                        },
                        "status": "OK",
                    },
                ]
            }
        ]
    }
    http_client = AsyncMock(set_spec=AsyncClient)
    http_client.get.return_value = http_client_response
    return http_client


@pytest.fixture
def fetch_edamam_nutrients(config, logger, http_client):
    fetch_edamam_nutrients = FetchEdamamNutrients(config, logger, http_client)
    return fetch_edamam_nutrients


@pytest.mark.anyio
async def test_execute(logger, http_client, fetch_edamam_nutrients):
    result = await fetch_edamam_nutrients.execute(query="test_query")
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
            source=NutrientSource.EDAMAM,
        ),
        Nutrients(
            name="food_2",
            quantity=1,
            unit="food_2_unit",
            calories_kcal=20000,
            weight_grams=100,
            calories_kcal_per_gram=20000,
            source=NutrientSource.EDAMAM,
        ),
    ]
    logger.error.assert_not_called()
    http_client.get.assert_called_once_with(
        "https://api.edamam.com/api/nutrition-data",
        headers={
            "Content-Type": "application/json",
        },
        params={
            "ingr": "test_query",
            "app_id": "test_app_id",
            "app_key": "test_app_key",
            "nutrition-type": "cooking",
        },
        timeout=5,
    )
    http_client.get.return_value.raise_for_status.assert_called_once()


@pytest.mark.anyio
async def test_execute_with_empty_food_name_response(
    logger, http_client, fetch_edamam_nutrients
):
    http_client_response = MagicMock(spec_set=Response)
    http_client_response.json.return_value = {
        "ingredients": [
            {
                "parsed": [
                    {
                        "quantity": 1.0,
                        "measure": "food_unit",
                        "weight": 1,
                        "nutrients": {
                            "ENERC_KCAL": {
                                "label": "Calories",
                                "quantity": 200,
                                "unit": "kcal",
                            }
                        },
                        "status": "OK",
                    },
                ]
            }
        ]
    }
    http_client.get.return_value = http_client_response
    result = await fetch_edamam_nutrients.execute(query="test_query")
    assert result is None
    logger.error.assert_called_once()


@pytest.mark.anyio
async def test_execute_with_empty_quantity_response(
    logger, http_client, fetch_edamam_nutrients
):
    http_client_response = MagicMock(spec_set=Response)
    http_client_response.json.return_value = {
        "ingredients": [
            {
                "parsed": [
                    {
                        "measure": "food_unit",
                        "food": "food",
                        "weight": 1,
                        "nutrients": {
                            "ENERC_KCAL": {
                                "label": "Calories",
                                "quantity": 200,
                                "unit": "kcal",
                            }
                        },
                        "status": "OK",
                    },
                ]
            }
        ]
    }
    http_client.get.return_value = http_client_response
    result = await fetch_edamam_nutrients.execute(query="test_query")
    assert result is None
    logger.error.assert_called_once()


@pytest.mark.anyio
async def test_execute_with_empty_unit_response(
    logger, http_client, fetch_edamam_nutrients
):
    http_client_response = MagicMock(spec_set=Response)
    http_client_response.json.return_value = {
        "ingredients": [
            {
                "parsed": [
                    {
                        "quantity": 1.0,
                        "food": "food",
                        "weight": 1,
                        "nutrients": {
                            "ENERC_KCAL": {
                                "label": "Calories",
                                "quantity": 200,
                                "unit": "kcal",
                            }
                        },
                        "status": "OK",
                    },
                ]
            }
        ]
    }
    http_client.get.return_value = http_client_response
    result = await fetch_edamam_nutrients.execute(query="test_query")
    assert result is None
    logger.error.assert_called_once()


@pytest.mark.anyio
async def test_execute_with_empty_calories_response(
    logger, http_client, fetch_edamam_nutrients
):
    http_client_response = MagicMock(spec_set=Response)
    http_client_response.json.return_value = {
        "ingredients": [
            {
                "parsed": [
                    {
                        "quantity": 1.0,
                        "measure": "food_unit",
                        "food": "food",
                        "weight": 1,
                        "nutrients": {},
                        "status": "OK",
                    },
                ]
            }
        ]
    }
    http_client.get.return_value = http_client_response
    result = await fetch_edamam_nutrients.execute(query="test_query")
    assert result is None
    logger.error.assert_called_once()


@pytest.mark.anyio
async def test_execute_with_exception(logger, http_client, fetch_edamam_nutrients):
    http_client.get.side_effect = Exception("test_error")
    result = await fetch_edamam_nutrients.execute(query="test_query")
    assert result is None
    logger.error.assert_called_once_with("Failed to fetch edamam nutrients: test_error")
