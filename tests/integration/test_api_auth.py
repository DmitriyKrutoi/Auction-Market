import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


class TestAuthAPI:
    async def test_register_success(self, client):
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password123",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "testuser"
        assert "user_id" in data

    async def test_register_duplicate(self, client):
        # Первая регистрация
        await client.post(
            "/api/v1/auth/register",
            json={
                "username": "duplicate",
                "email": "dup@example.com",
                "password": "password123",
            },
        )
        # Вторая с тем же username
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "username": "duplicate",
                "email": "another@example.com",
                "password": "password123",
            },
        )
        assert response.status_code == 400
        assert "уже существует" in response.json()["detail"]

    async def test_login_success(self, client):
        # Сначала регистрируем
        await client.post(
            "/api/v1/auth/register",
            json={
                "username": "loginuser",
                "email": "login@example.com",
                "password": "password123",
            },
        )
        # Логинимся
        response = await client.post(
            "/api/v1/auth/login",
            json={"username": "loginuser", "password": "password123"},
        )
        assert response.status_code == 200
        assert "access_token" in response.json()

    async def test_login_wrong_password(self, client):
        response = await client.post(
            "/api/v1/auth/login", json={"username": "nonexistent", "password": "wrong"}
        )
        assert response.status_code == 401
