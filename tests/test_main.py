"""
Test suite for the FastAPI boilerplate application.
"""

import pytest
from fastapi.testclient import TestClient
from main import app, items_db, next_id

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_database():
    """Reset the database before each test."""
    global items_db, next_id
    items_db.clear()
    next_id = 1
    yield
    # Clean up after test if needed
    items_db.clear()
    next_id = 1


def test_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FastAPI Boilerplate API", "docs": "/docs"}


def test_health():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_item():
    """Test creating an item."""
    response = client.post(
        "/items",
        json={"name": "Test Item", "description": "A test item", "price": 10.0, "tax": 1.0},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["description"] == "A test item"
    assert data["price"] == 10.0
    assert data["tax"] == 1.0
    assert "id" in data


def test_get_items():
    """Test retrieving all items."""
    response = client.get("/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_item_not_found():
    """Test retrieving a non-existent item."""
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_update_item():
    """Test updating an item."""
    # First create an item
    create_response = client.post(
        "/items",
        json={"name": "Original Item", "price": 5.0},
    )
    assert create_response.status_code == 201
    item_id = create_response.json()["id"]

    # Update the item
    update_response = client.put(
        f"/items/{item_id}",
        json={"name": "Updated Item", "price": 15.0},
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["name"] == "Updated Item"
    assert data["price"] == 15.0
    assert data["id"] == item_id


def test_delete_item():
    """Test deleting an item."""
    # Create an item
    create_response = client.post(
        "/items",
        json={"name": "To Delete", "price": 20.0},
    )
    assert create_response.status_code == 201
    item_id = create_response.json()["id"]

    # Delete the item
    delete_response = client.delete(f"/items/{item_id}")
    assert delete_response.status_code == 204

    # Verify it's gone
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404


def test_search_items():
    """Test searching items."""
    # Create a couple of items
    client.post("/items", json={"name": "Apple", "price": 1.0})
    client.post("/items", json={"name": "Banana", "price": 2.0})

    # Search by query
    response = client.get("/items/search/?q=Apple")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Apple"

    # Search by min price
    response = client.get("/items/search/?min_price=1.5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Banana"

    # Combined search
    response = client.get("/items/search/?q=Banana&min_price=1.0")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Banana"