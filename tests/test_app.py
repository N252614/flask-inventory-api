# Tests for the Flask Inventory API and external API helper

import os
import sys
import pytest
from unittest.mock import patch

# Add project root to import path so "app" is visible
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app
from inventory_data import inventory
from external_api import fetch_product_by_barcode


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_route(client):
    """Root route should return a simple status message."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Inventory API is running!"


def test_get_inventory_returns_list(client):
    """GET /inventory should return a list of items."""
    response = client.get("/inventory")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1  # we have some initial data


def test_get_single_item_success(client):
    """GET /inventory/<id> should return one item when it exists."""
    item_id = inventory[0]["id"]  # take id of first item
    response = client.get(f"/inventory/{item_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == item_id


def test_get_single_item_not_found(client):
    """GET /inventory/<id> should return 404 for unknown id."""
    response = client.get("/inventory/999999")
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Item not found"


def test_add_item_via_post(client):
    """POST /inventory should create a new item and return it."""
    payload = {
        "barcode": "111111",
        "name": "Test Product",
        "brand": "Test Brand",
        "price": 5.99,
        "stock": 10,
    }
    response = client.post("/inventory", json=payload)
    assert response.status_code == 201

    data = response.get_json()
    assert data["name"] == "Test Product"
    assert "id" in data  # new id was assigned


def test_update_item_with_patch(client):
    """PATCH /inventory/<id> should update fields of an existing item."""
    item_id = inventory[0]["id"]
    response = client.patch(f"/inventory/{item_id}", json={"price": 9.99})
    assert response.status_code == 200

    data = response.get_json()
    assert data["price"] == 9.99


def test_delete_item(client):
    """
    DELETE /inventory/<id> should remove an item.
    We first create a temporary item, then delete it.
    """
    # create temp item
    create_response = client.post(
        "/inventory",
        json={
            "barcode": "222222",
            "name": "To Delete",
            "brand": "Temp",
            "price": 1.0,
            "stock": 1,
        },
    )
    new_id = create_response.get_json()["id"]

    # now delete it
    delete_response = client.delete(f"/inventory/{new_id}")
    assert delete_response.status_code == 200
    data = delete_response.get_json()
    assert data["message"] == "Item deleted"


def test_fetch_product_by_barcode_uses_external_api():
    """external_api.fetch_product_by_barcode should parse external JSON correctly."""
    fake_json = {
        "status": 1,
        "product": {
            "product_name": "Mock Product",
            "brands": "MockBrand",
            "ingredients_text": "Sugar",
            "categories": "Snacks",
        },
    }

    # Patch requests.get inside external_api module
    with patch("external_api.requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = fake_json

        result = fetch_product_by_barcode("123456")

        assert result is not None
        assert result["barcode"] == "123456"
        assert result["name"] == "Mock Product"
        assert result["brand"] == "MockBrand"