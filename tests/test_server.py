"""
API Integration tests for FastAPI server endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from server import app

client = TestClient(app)


def test_api_index_endpoint():
    response = client.get("/")
    assert response.status_code == 200


def test_api_choices_endpoint():
    response = client.get("/api/choices")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    intent_names = {c["name"] for c in data}
    assert intent_names == {"analytics", "products", "customers", "inventory", "support"}


def test_api_mock_data_endpoint():
    response = client.get("/api/mock-data")
    assert response.status_code == 200
    data = response.json()
    assert "products" in data
    assert "customers" in data
    assert "daily_sales" in data
    assert "inventory" in data


def test_api_query_analytics():
    response = client.post("/api/query", json={"message": "Why were my sales low yesterday?"})
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "analytics"
    assert data["confidence"] >= 0.70
    assert data["passes_threshold"] is True
    assert data["routed_node"] == "analytics"
    assert "Sales Analytics" in data["reply"] or "revenue" in data["reply"].lower()


def test_api_query_low_confidence_diverts():
    response = client.post("/api/query", json={"message": "tell me about my business"})
    assert response.status_code == 200
    data = response.json()
    assert data["confidence"] < 0.70
    assert data["passes_threshold"] is False
    assert data["routed_node"] == "support"


def test_api_query_empty_bad_request():
    response = client.post("/api/query", json={"message": "   "})
    assert response.status_code == 400


def test_api_classify_explain():
    response = client.post("/api/classify", json={"message": "show my products"})
    assert response.status_code == 200
    data = response.json()
    assert "intent_scores" in data
    assert "selected_intent" in data
    assert data["selected_intent"] == "products"
