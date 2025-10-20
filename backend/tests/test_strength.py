import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_currency_strength():
    """Test currency strength endpoint"""
    response = client.get("/api/strength/")
    assert response.status_code == 200
    data = response.json()
    assert "strengths" in data
    assert "updated_at" in data
    assert len(data["strengths"]) > 0

def test_get_single_currency():
    """Test single currency strength endpoint"""
    response = client.get("/api/strength/currency/USD")
    assert response.status_code == 200
    data = response.json()
    assert data["currency"] == "USD"
    assert "data" in data
    assert "strength_score" in data["data"]

def test_invalid_currency():
    """Test invalid currency code"""
    response = client.get("/api/strength/currency/XXX")
    assert response.status_code == 404
