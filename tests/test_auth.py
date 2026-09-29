def test_signup(client):
    response = client.post(
        "/auth/signup",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "Password123"
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["message"] == "User registered successfully"
    assert data["user"]["email"] == "test@example.com"


def test_duplicate_signup(client):
    user = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "Password123"
    }

    first = client.post(
        "/auth/signup",
        json=user
    )

    assert first.status_code == 201

    second = client.post(
        "/auth/signup",
        json=user
    )

    assert second.status_code == 409


def test_login(client):
    client.post(
        "/auth/signup",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "Password123"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "Password123"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "access_token" in data


def test_invalid_login(client):
    client.post(
        "/auth/signup",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "Password123"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "WrongPassword"
        }
    )

    assert response.status_code == 401