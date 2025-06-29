import json
from app.cache import redis_client
import pytest
from httpx import AsyncClient
from app.main import app
import redis.asyncio as redis
from httpx import ASGITransport

def test_add_book(client):
    response = client.post("/books", json={"title": "Atomic Habits", "author": "James Clear"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Atomic Habits"
    assert data["author"] == "James Clear"
    assert "id" in data

def test_get_books(client):
    response = client.get("/books")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1





import pytest
import json
from httpx import AsyncClient
from httpx import ASGITransport
from app.main import app
import redis.asyncio as redis

@pytest.mark.asyncio
async def test_cache_miss():
    # Redis client tied to this loop
    test_redis = redis.Redis(host="localhost", port=6379, decode_responses=True)
    await test_redis.flushall()

    # ASGITransport (remove lifespan)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/books", json={"title": "The Alchemist", "author": "Paulo Coelho"})
        assert response.status_code == 200

        response = await ac.get("/books")
        assert response.status_code == 200
        data = response.json()
        assert any(book["title"] == "The Alchemist" for book in data)

    # Check Redis now contains the book
    cached_data = await test_redis.get("all_books")
    assert cached_data is not None
    cached_books = json.loads(cached_data)
    assert any(book["title"] == "The Alchemist" for book in cached_books)
