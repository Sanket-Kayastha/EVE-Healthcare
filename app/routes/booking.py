from datetime import datetime, timezone

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.booking import Booking
from app.models.centre_test import CentreTest


booking_bp = Blueprint(
    "booking",
    __name__,
    url_prefix="/bookings"
)


@booking_bp.route("/", methods=["POST"])
@jwt_required()
def create_booking():
    user_id = int(get_jwt_identity())

    data = request.get_json()

    if not data:
        return {
            "error": "Request body is required"
        }, 400

    centre_test_id = data.get("centre_test_id")
    appointment_datetime = data.get(
        "appointment_datetime"
    )

    if centre_test_id is None:
        return {
            "error": "centre_test_id is required"
        }, 400

    if not appointment_datetime:
        return {
            "error": "appointment_datetime is required"
        }, 400

    
    centre_test = db.session.get(
        CentreTest,
        centre_test_id
    )

    if not centre_test:
        return {
            "error": "Centre-test combination not found"
        }, 404

    
    try:
        appointment = datetime.fromisoformat(
            appointment_datetime.replace("Z", "+00:00")
        )
    except ValueError:
        return {
            "error": (
                "Invalid appointment_datetime. "
                "Use ISO 8601 format, for example "
                "2026-10-15T10:30:00+00:00"
            )
        }, 400

    
    if appointment.tzinfo is None:
        appointment = appointment.replace(
            tzinfo=timezone.utc
        )

    
    if appointment <= datetime.now(timezone.utc):
        return {
            "error": "Appointment must be in the future"
        }, 400

    booking = Booking(
        user_id=user_id,
        centre_test_id=centre_test.id,
        appointment_datetime=appointment,
        amount=centre_test.price,
        status="PENDING"
    )

    db.session.add(booking)
    db.session.commit()

    return {
        "message": "Booking created successfully",
        "booking": {
            "id": booking.id,
            "user_id": booking.user_id,
            "centre_id": centre_test.centre_id,
            "test_id": centre_test.test_id,
            "appointment_datetime": (
                booking.appointment_datetime.isoformat()
            ),
            "amount": float(booking.amount),
            "status": booking.status
        }
    }, 201


@booking_bp.route("/", methods=["GET"])
@jwt_required()
def get_my_bookings():
    user_id = int(get_jwt_identity())

    bookings = Booking.query.filter_by(
        user_id=user_id
    ).order_by(
        Booking.created_at.desc()
    ).all()

    result = []

    for booking in bookings:
        result.append({
            "id": booking.id,
            "centre_id": booking.centre_test.centre_id,
            "centre_name": booking.centre_test.centre.name,
            "test_id": booking.centre_test.test_id,
            "test_name": booking.centre_test.test.name,
            "appointment_datetime": (
                booking.appointment_datetime.isoformat()
            ),
            "amount": float(booking.amount),
            "status": booking.status
        })

    return {
        "bookings": result
    }, 200


@booking_bp.route(
    "/<int:booking_id>",
    methods=["GET"]
)
@jwt_required()
def get_booking(booking_id):
    user_id = int(get_jwt_identity())

    booking = db.session.get(
        Booking,
        booking_id
    )

    if not booking:
        return {
            "error": "Booking not found"
        }, 404

    # Prevent users from viewing another user's booking
    if booking.user_id != user_id:
        return {
            "error": "You are not authorized to view this booking"
        }, 403

    return {
        "id": booking.id,
        "centre": {
            "id": booking.centre_test.centre_id,
            "name": booking.centre_test.centre.name
        },
        "test": {
            "id": booking.centre_test.test_id,
            "name": booking.centre_test.test.name
        },
        "appointment_datetime": (
            booking.appointment_datetime.isoformat()
        ),
        "amount": float(booking.amount),
        "status": booking.status
    }, 200


@booking_bp.route(
    "/<int:booking_id>",
    methods=["DELETE"]
)
@jwt_required()
def cancel_booking(booking_id):
    user_id = int(get_jwt_identity())

    booking = db.session.get(
        Booking,
        booking_id
    )

    if not booking:
        return {
            "error": "Booking not found"
        }, 404

    # Prevent users from modifying another user's booking
    if booking.user_id != user_id:
        return {
            "error": (
                "You are not authorized to cancel this booking"
            )
        }, 403

    if booking.status == "CANCELLED":
        return {
            "error": "Booking is already cancelled"
        }, 409

    if booking.status == "CONFIRMED":
        return {
            "error": (
                "Confirmed bookings cannot be cancelled "
                "through this endpoint"
            )
        }, 409

    booking.status = "CANCELLED"

    db.session.commit()

    return {
        "message": "Booking cancelled successfully",
        "booking_id": booking.id,
        "status": booking.status
    }, 200