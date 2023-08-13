from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import AsyncClient, Response

from fastapi_boilerplate.services.fetch_nutritionix_nutrients import (
    FetchNutritionixNutrients,
)
from fastapi_boilerplate.types import (
    Config,
    Language,
    Logger,
    Nutrients,
    NutritionixParams,
)


@pytest.fixture
def config():
    config = MagicMock(spec_set=Config)
    config.nutritionix.base_url = "https://api.nutritionix.com"
    config.nutritionix.app_id = "test_app_id"
    config.nutritionix.app_key = "test_app_key"
    return config


@pytest.fixture
def logger():
    logger = MagicMock(spec_set=Logger)
    return logger


@pytest.fixture
def http_client():
    http_client_response = MagicMock(spec_set=Response)
    http_client_response.json.return_value = {
        "foods": [
            {
                "food_name": "food_1",
                "brand_name": None,
                "serving_qty": 1,
                "serving_unit": "food_1_unit",
                "nf_calories": 100.1111,
                "serving_weight_grams": 22.22,
                "nf_protein": 1,
                "nf_total_fat": 0.2222,
                "nf_saturated_fat": 0.33,
                "nf_total_carbohydrate": 44.4,
                "nf_dietary_fiber": 55,
                "nf_sugars": 0.066,
                "nf_cholesterol": 0.07,
                "nf_sodium": 0,
            },
            {
                "food_name": "food_2",
                "brand_name": "food_2_brand",
                "serving_qty": 1,
                "serving_unit": "food_2_unit",
                "nf_calories": 200,
            },
        ]
    }
    http_client = AsyncMock(set_spec=AsyncClient)
    http_client.post.return_value = http_client_response
    return http_client


@pytest.fixture
def fetch_nutritionix_nutrients(config, logger, http_client):
    fetch_nutritionix_nutrients = FetchNutritionixNutrients(config, logger, http_client)
    return fetch_nutritionix_nutrients


@pytest.mark.anyio
async def test_execute(logger, http_client, fetch_nutritionix_nutrients):
    params = NutritionixParams(query="test_query")
    result = await fetch_nutritionix_nutrients.execute(params=params)
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
        ),
        Nutrients(
            name="food_2",
            brand_name="food_2_brand",
            quantity=1,
            unit="food_2_unit",
            calories_kcal=20000,
        ),
    ]
    logger.error.assert_not_called()
    http_client.post.assert_called_once_with(
        "https://api.nutritionix.com/v2/natural/nutrients",
        headers={
            "Content-Type": "application/json",
            "x-app-id": "test_app_id",
            "x-app-key": "test_app_key",
            "x-remote-user-id": "0",
        },
        json={
            "query": "test_query",
            "num_servings": 1,
            "line_delimited": False,
            "use_raw_foods": False,
            "use_branded_foods": False,
            "locale": "en_US",
        },
        timeout=5,
    )
    http_client.post.return_value.raise_for_status.assert_called_once()


@pytest.mark.anyio
async def test_execute_with_custom_params(http_client, fetch_nutritionix_nutrients):
    params = NutritionixParams(
        query="test_query_with_custom_params",
        num_servings=2,
        line_delimited=True,
        use_raw_foods=True,
        use_branded_foods=True,
        locale=Language.PT_BR,
    )
    result = await fetch_nutritionix_nutrients.execute(params=params)
    assert result is not None
    http_client.post.assert_called_once_with(
        "https://api.nutritionix.com/v2/natural/nutrients",
        headers={
            "Content-Type": "application/json",
            "x-app-id": "test_app_id",
            "x-app-key": "test_app_key",
            "x-remote-user-id": "0",
        },
        json={
            "query": "test_query_with_custom_params",
            "num_servings": 2,
            "line_delimited": True,
            "use_raw_foods": True,
            "use_branded_foods": True,
            "locale": "pt_BR",
        },
        timeout=5,
    )


@pytest.mark.anyio
async def test_execute_with_empty_food_name_response(
    logger, http_client, fetch_nutritionix_nutrients
):
    http_client_response = MagicMock(spec_set=Response)
    http_client_response.json.return_value = {
        "foods": [
            {
                "food_name": None,
                "brand_name": "food_brand",
                "serving_qty": 1,
                "serving_unit": "food_unit",
                "nf_calories": 100,
            },
        ]
    }
    http_client.post.return_value = http_client_response
    params = NutritionixParams(query="test_query")
    result = await fetch_nutritionix_nutrients.execute(params=params)
    assert result is None
    logger.error.assert_called_once()


@pytest.mark.anyio
async def test_execute_with_empty_quantity_response(
    logger, http_client, fetch_nutritionix_nutrients
):
    http_client_response = MagicMock(spec_set=Response)
    http_client_response.json.return_value = {
        "foods": [
            {
                "food_name": "food_name",
                "brand_name": "food_brand",
                "serving_qty": None,
                "serving_unit": "food_unit",
                "nf_calories": 100,
            },
        ]
    }
    http_client.post.return_value = http_client_response
    params = NutritionixParams(query="test_query")
    result = await fetch_nutritionix_nutrients.execute(params=params)
    assert result is None
    logger.error.assert_called_once()


@pytest.mark.anyio
async def test_execute_with_empty_unit_response(
    logger, http_client, fetch_nutritionix_nutrients
):
    http_client_response = MagicMock(spec_set=Response)
    http_client_response.json.return_value = {
        "foods": [
            {
                "food_name": "food_name",
                "brand_name": "food_brand",
                "serving_qty": 1,
                "serving_unit": None,
                "nf_calories": 100,
            },
        ]
    }
    http_client.post.return_value = http_client_response
    params = NutritionixParams(query="test_query")
    result = await fetch_nutritionix_nutrients.execute(params=params)
    assert result is None
    logger.error.assert_called_once()


@pytest.mark.anyio
async def test_execute_with_empty_calories_response(
    logger, http_client, fetch_nutritionix_nutrients
):
    http_client_response = MagicMock(spec_set=Response)
    http_client_response.json.return_value = {
        "foods": [
            {
                "food_name": "food_name",
                "brand_name": "food_brand",
                "serving_qty": 1,
                "serving_unit": "food_unit",
                "nf_calories": None,
            },
        ]
    }
    http_client.post.return_value = http_client_response
    params = NutritionixParams(query="test_query")
    result = await fetch_nutritionix_nutrients.execute(params=params)
    assert result is None
    logger.error.assert_called_once()


@pytest.mark.anyio
async def test_execute_with_exception(logger, http_client, fetch_nutritionix_nutrients):
    http_client.post.side_effect = Exception("test_error")
    params = NutritionixParams(query="test_query")
    result = await fetch_nutritionix_nutrients.execute(params=params)
    assert result is None
    logger.error.assert_called_once_with(
        "Failed to fetch nutritionix nutrients: test_error"
    )
