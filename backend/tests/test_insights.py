import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_insights():
    """Test insights endpoint"""
    response = client.get("/api/insights/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 10  # Default limit

def test_insights_with_limit():
    """Test insights with custom limit"""
    response = client.get("/api/insights/?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 5

def test_pair_insights():
    """Test pair-specific insights"""
    response = client.get("/api/insights/pair/EUR/USD")
    assert response.status_code in [200, 404]  # May or may not have insights
