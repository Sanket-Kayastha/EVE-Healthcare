from datetime import datetime, timedelta, timezone


def create_user_and_login(client):
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

    return response.get_json()["access_token"]


def create_centre_test(client):
    centre_response = client.post(
        "/centres/",
        json={
            "name": "Test Centre",
            "location": "Lucknow"
        }
    )

    centre_id = centre_response.get_json()["centre"]["id"]

    test_response = client.post(
        "/tests/",
        json={
            "name": "Blood Test",
            "description": "Basic blood test"
        }
    )

    test_id = test_response.get_json()["test"]["id"]

    response = client.post(
        f"/centres/{centre_id}/tests",
        json={
            "test_id": test_id,
            "price": 500
        }
    )

    return response.get_json()["centre_test"]["id"]


def future_appointment():
    return (
        datetime.now(timezone.utc)
        + timedelta(days=7)
    ).isoformat()


def test_create_booking(client):
    token = create_user_and_login(client)
    centre_test_id = create_centre_test(client)

    response = client.post(
        "/bookings/",
        json={
            "centre_test_id": centre_test_id,
            "appointment_datetime": future_appointment()
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["booking"]["status"] == "PENDING"
    assert data["booking"]["amount"] == 500.0


def test_booking_requires_authentication(client):
    response = client.post(
        "/bookings/",
        json={
            "centre_test_id": 1,
            "appointment_datetime": future_appointment()
        }
    )

    assert response.status_code == 401


def test_invalid_booking_centre_test(client):
    token = create_user_and_login(client)

    response = client.post(
        "/bookings/",
        json={
            "centre_test_id": 9999,
            "appointment_datetime": future_appointment()
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 404


def test_past_appointment_rejected(client):
    token = create_user_and_login(client)
    centre_test_id = create_centre_test(client)

    response = client.post(
        "/bookings/",
        json={
            "centre_test_id": centre_test_id,
            "appointment_datetime": "2020-01-01T10:00:00+00:00"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 400