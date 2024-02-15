"""
Module with tests for auth server
"""

from fastapi import status
from httpx import AsyncClient


async def test_root(ac: AsyncClient):
    expected_response = {"detail": "home"}

    response = await ac.get("/auth/")

    assert expected_response == response.json()


async def test_register_unique(ac: AsyncClient):
    expected_response_status_code = status.HTTP_201_CREATED

    response = await ac.post(
        "/auth/register/",
        json={
            "username": "unique_sloi",
            "email": "test@example.com",
            "password": "unique_user_passwd",
        },
    )

    assert response.status_code == expected_response_status_code
