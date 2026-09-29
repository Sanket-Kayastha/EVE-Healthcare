from datetime import datetime, timedelta, timezone


def setup_booking(client):
    # Create user
    client.post(
        "/auth/signup",
        json={
            "name": "Payment User",
            "email": "payment@example.com",
            "password": "Password123"
        }
    )

    # Login
    login_response = client.post(
        "/auth/login",
        json={
            "email": "payment@example.com",
            "password": "Password123"
        }
    )

    token = login_response.get_json()["access_token"]

    # Create centre
    centre_response = client.post(
        "/centres/",
        json={
            "name": "Payment Centre",
            "location": "Delhi"
        }
    )

    centre_id = centre_response.get_json()["centre"]["id"]

    # Create test
    test_response = client.post(
        "/tests/",
        json={
            "name": "CBC",
            "description": "Complete blood count"
        }
    )

    test_id = test_response.get_json()["test"]["id"]

    # Connect test to centre
    centre_test_response = client.post(
        f"/centres/{centre_id}/tests",
        json={
            "test_id": test_id,
            "price": 500
        }
    )

    centre_test_id = (
        centre_test_response
        .get_json()["centre_test"]["id"]
    )

    # Create booking
    appointment = (
        datetime.now(timezone.utc)
        + timedelta(days=7)
    ).isoformat()

    booking_response = client.post(
        "/bookings/",
        json={
            "centre_test_id": centre_test_id,
            "appointment_datetime": appointment
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    booking_id = (
        booking_response
        .get_json()["booking"]["id"]
    )

    return token, booking_id


def test_successful_payment(client):
    token, booking_id = setup_booking(client)

    response = client.post(
        "/payments/",
        json={
            "booking_id": booking_id,
            "result": "SUCCESS"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["payment"]["status"] == "SUCCESS"
    assert data["booking"]["status"] == "CONFIRMED"


def test_failed_payment(client):
    token, booking_id = setup_booking(client)

    response = client.post(
        "/payments/",
        json={
            "booking_id": booking_id,
            "result": "FAILED"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["payment"]["status"] == "FAILED"
    assert data["booking"]["status"] == "FAILED"


def test_webhook_is_idempotent(client):
    _, booking_id = setup_booking(client)

    webhook = {
        "event_id": "evt_test_001",
        "booking_id": booking_id,
        "result": "SUCCESS"
    }

    first_response = client.post(
        "/payments/webhook/",
        json=webhook
    )

    assert first_response.status_code == 200

    first_data = first_response.get_json()

    assert (
        first_data["message"]
        == "Webhook processed successfully"
    )

    second_response = client.post(
        "/payments/webhook/",
        json=webhook
    )

    assert second_response.status_code == 200

    second_data = second_response.get_json()

    assert (
        second_data["message"]
        == "Webhook already processed"
    )

    assert (
        second_data["payment"]["id"]
        == first_data["payment"]["id"]
    )