import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.data_collection.cdc_fluview import CDCFluViewClient

@pytest.fixture
def client():
    return CDCFluViewClient()

@patch('src.data_collection.cdc_fluview.requests.get')
def test_fetch_ili_data_success(mock_get, client):
    # Mock successful API response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "result": 1,
        "message": "success",
        "epidata": [
            {"region": "nat", "epiweek": 202340, "wili": 2.5, "ili": 2.4},
            {"region": "nat", "epiweek": 202341, "wili": 2.6, "ili": 2.5}
        ]
    }
    mock_get.return_value = mock_response

    df = client.fetch_ili_data("nat", "202340-202341")

    assert not df.empty
    assert len(df) == 2
    assert "wili" in df.columns
    assert df.iloc[0]["epiweek"] == 202340

@patch('src.data_collection.cdc_fluview.requests.get')
def test_fetch_ili_data_no_results(mock_get, client):
    # Mock no results (result code -2)
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "result": -2,
        "message": "no results",
        "epidata": []
    }
    mock_get.return_value = mock_response

    df = client.fetch_ili_data("nat", "202340")

    assert df.empty

@patch('src.data_collection.cdc_fluview.requests.get')
def test_fetch_ili_data_api_error(mock_get, client):
    # Mock API error
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "result": 0,
        "message": "some error"
    }
    mock_get.return_value = mock_response

    with pytest.raises(ValueError, match="API Error"):
        client.fetch_ili_data("nat", "202340")
