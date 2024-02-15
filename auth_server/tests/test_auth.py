"""
Module with tests for auth server
"""

from fastapi import status
from httpx import AsyncClient

from auth.utils import encode_jwt


async def test_root(ac: AsyncClient):
    expected_response = {"detail": "home"}

    response = await ac.get("/auth/")

    assert expected_response == response.json()


async def test_register_unique(ac: AsyncClient):
    expected_response_status_code = status.HTTP_201_CREATED

    response = await ac.post(
        "/auth/register/",
        json={
            "username": "unique_nickname",
            "email": "test@example.com",
            "password": "unique_user_passwd",
        },
    )

    assert response.status_code == expected_response_status_code
    assert (
        response.json()["username"] == "unique_nickname"
        and response.json()["email"] == "test@example.com"
    )


async def test_register_user_exists(ac: AsyncClient):
    expected_response_status_code = status.HTTP_403_FORBIDDEN

    response = await ac.post(
        "/auth/register/",
        json={
            "username": "unique_nickname",
            "email": "test@example.com",
            "password": "unique_user_passwd",
        },
    )

    assert response.status_code == expected_response_status_code


async def test_register_cookie_deleted(ac: AsyncClient):
    expected_response_status_code = status.HTTP_201_CREATED

    response = await ac.post(
        "/auth/register/",
        json={
            "username": "cookie",
            "email": "test@example.com",
            "password": "cookie",
        },
        cookies={"access_token": "some_token"},
    )

    assert not response.cookies.get("access_token")
    assert response.status_code == expected_response_status_code


async def test_login_valid_credentials(ac: AsyncClient):
    expected_response_status_code = status.HTTP_200_OK

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = await ac.post(
        "/auth/login/",
        data={"username": "unique_nickname", "password": "unique_user_passwd"},
        headers=headers,
    )

    assert response.status_code == expected_response_status_code
    assert response.cookies.get("access_token")
    assert (
        response.json().get("access_token") == response.cookies.get("access_token")
        and response.json().get("token_type") == "Bearer"
    )


async def test_login_invalid_passwd(ac: AsyncClient):
    expected_response_status_code = status.HTTP_401_UNAUTHORIZED

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = await ac.post(
        "/auth/login/",
        data={"username": "unique_nickname", "password": "unique_user_wrong_passwd"},
        headers=headers,
    )
    assert response.status_code == expected_response_status_code


async def test_login_invalid_login(ac: AsyncClient):
    expected_response_status_code = status.HTTP_401_UNAUTHORIZED

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = await ac.post(
        "/auth/login/",
        data={"username": "unique_nickname_wrong", "password": "unique_user_passwd"},
        headers=headers,
    )
    assert response.status_code == expected_response_status_code


async def test_login_cookie_deleted(ac: AsyncClient):
    expected_response_status_code = status.HTTP_200_OK

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    cookies = {"access_token": "some_token"}
    response = await ac.post(
        "/auth/login/",
        data={"username": "unique_nickname", "password": "unique_user_passwd"},
        headers=headers,
        cookies=cookies,
    )

    assert response.status_code == expected_response_status_code
    assert response.cookies.get("access_token") != cookies["access_token"]


async def test_logout_token_is_set(ac: AsyncClient):
    expected_response_status_code = status.HTTP_200_OK

    cookies = {"access_token": "some_token"}
    response = await ac.post("/auth/logout/", cookies=cookies)

    assert response.status_code == expected_response_status_code
    assert not response.cookies.get("access_token")


async def test_logout_no_token(ac: AsyncClient):
    expected_response_status_code = status.HTTP_403_FORBIDDEN

    response = await ac.post("/auth/logout/")

    assert response.status_code == expected_response_status_code


async def test_validate_valid_jwt(ac: AsyncClient):
    expected_response_status_code = status.HTTP_200_OK

    token = encode_jwt({"sub": 1})
    cookies = {"access_token": token}
    response = await ac.get("/auth/validate/", cookies=cookies)

    assert response.status_code == expected_response_status_code
    assert response.json().get("username") == "unique_nickname"


async def test_validate_no_token(ac: AsyncClient):
    expected_response_status_code = status.HTTP_401_UNAUTHORIZED

    response = await ac.get("/auth/validate/")

    assert response.status_code == expected_response_status_code


async def test_validate_invalid_token(ac: AsyncClient):
    expected_response_status_code = status.HTTP_401_UNAUTHORIZED

    cookies = {"access_token": "not_a_valid_jwt_token"}
    response = await ac.get("/auth/validate/", cookies=cookies)

    assert response.status_code == expected_response_status_code


async def test_validate_user_doesnt_exist(ac: AsyncClient):
    expected_response_status_code = status.HTTP_401_UNAUTHORIZED

    token = encode_jwt({"sub": 9999})
    cookies = {"access_token": token}
    response = await ac.get("/auth/validate/", cookies=cookies)

    assert response.status_code == expected_response_status_code
