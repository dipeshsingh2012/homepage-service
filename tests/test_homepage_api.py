import pytest
from httpx import ASGITransport, AsyncClient
from src.main import app


@pytest.fixture
async def test_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_health_endpoint(test_client: AsyncClient):
    response = await test_client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "homepage-service"


@pytest.mark.asyncio
async def test_homepage_endpoint(test_client: AsyncClient):
    response = await test_client.get("/api/v1/homepage")
    assert response.status_code == 200
    data = response.json()
    assert "hero" in data
    assert "featuredCategories" in data
    assert "howItWorks" in data
    assert len(data["featuredCategories"]) > 0
