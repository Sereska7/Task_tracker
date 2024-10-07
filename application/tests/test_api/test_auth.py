from unittest.mock import patch, ANY

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_check_user_exists(ac: AsyncClient, prepare_base):
    user_data = {
        "name": "Existing_User",
        "email": "existing@example.com",
        "password": "password",
        "position": "Developer",
    }

    with patch("application.api.view_auth.get_user") as mock_get_user:
        mock_get_user.return_value = (
            user_data  # Мокируем, что пользователь уже существует
        )
        response = await ac.post("/auth/register", data=user_data)

        # Проверяем, что сервер вернул статус 200 с сообщением о существующем пользователе
        assert response.status_code == 200
        assert response.json() == {
            "status": "Пользователь с таким e-mail уже существует"
        }


@pytest.mark.asyncio
async def test_generate_and_send_verification_code(ac: AsyncClient, prepare_base):
    user_data = {
        "name": "New_User",
        "email": "newuser@example.com",
        "password": "password",
        "position": "Developer",
    }

    with patch(
        "application.api.view_auth.send_email_confirmation_code"
    ) as mock_send_email:
        response = await ac.post("/auth/register", data=user_data)

        # Проверяем, что email отправлен
        mock_send_email.assert_called_once_with(user_data["email"], ANY)

        # Проверяем, что статус ответа успешный
        assert response.status_code == 303
        assert response.headers["location"] == "/pages/verify"
