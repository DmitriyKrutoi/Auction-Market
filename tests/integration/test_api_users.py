import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


class TestUsersAPI:
    async def test_me_after_registration(self, client):
        # Регистрируем пользователя
        register_response = await client.post(
            "/api/v1/auth/register",
            json={
                "username": "newuser",
                "email": "new@example.com",
                "password": "password123",
            },
        )
        assert register_response.status_code == 201

        # Логинимся
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"username": "newuser", "password": "password123"},
        )
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # Запрашиваем /users/me
        response = await client.get(
            "/api/v1/users/me", headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "new@example.com"
