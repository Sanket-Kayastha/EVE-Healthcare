from uuid import uuid4

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.booking import Booking
from app.models.payment import Payment


payment_bp = Blueprint(
    "payment",
    __name__,
    url_prefix="/payments"
)


@payment_bp.route("/", methods=["POST"])
@jwt_required()
def create_payment():
    user_id = int(get_jwt_identity())

    data = request.get_json()

    if not data:
        return {
            "error": "Request body is required"
        }, 400

    booking_id = data.get("booking_id")
    result = data.get("result")

    if booking_id is None or not result:
        return {
            "error": "booking_id and result are required"
        }, 400

    result = result.upper()

    if result not in ("SUCCESS", "FAILED"):
        return {
            "error": "result must be SUCCESS or FAILED"
        }, 400

    booking = db.session.get(
        Booking,
        booking_id
    )

    if not booking:
        return {
            "error": "Booking not found"
        }, 404

    
    if booking.user_id != user_id:
        return {
            "error": "You are not authorized to pay for this booking"
        }, 403

    
    if booking.status == "CANCELLED":
        return {
            "error": "Cancelled booking cannot be paid"
        }, 409

    
    if booking.status == "CONFIRMED":
        return {
            "error": "Booking is already confirmed"
        }, 409

    
    if booking.payment:
        return {
            "error": "Payment has already been processed for this booking"
        }, 409

    event_id = f"payment_{uuid4().hex}"

    payment = Payment(
        booking_id=booking.id,
        event_id=event_id,
        amount=booking.amount,
        status=result
    )

    if result == "SUCCESS":
        booking.status = "CONFIRMED"
    else:
        booking.status = "FAILED"

    db.session.add(payment)
    db.session.commit()

    return {
        "message": "Payment processed successfully",
        "payment": {
            "id": payment.id,
            "booking_id": payment.booking_id,
            "event_id": payment.event_id,
            "amount": float(payment.amount),
            "status": payment.status
        },
        "booking": {
            "id": booking.id,
            "status": booking.status
        }
    }, 201


@payment_bp.route(
    "/<int:payment_id>",
    methods=["GET"]
)
@jwt_required()
def get_payment(payment_id):
    user_id = int(get_jwt_identity())

    payment = db.session.get(
        Payment,
        payment_id
    )

    if not payment:
        return {
            "error": "Payment not found"
        }, 404

    if payment.booking.user_id != user_id:
        return {
            "error": "You are not authorized to view this payment"
        }, 403

    return {
        "id": payment.id,
        "booking_id": payment.booking_id,
        "event_id": payment.event_id,
        "amount": float(payment.amount),
        "status": payment.status,
        "created_at": payment.created_at.isoformat()
    }, 200

@payment_bp.route(
    "/webhook/",
    methods=["POST"]
)
def payment_webhook():
    data = request.get_json()

    if not data:
        return {
            "error": "Request body is required"
        }, 400

    event_id = data.get("event_id")
    booking_id = data.get("booking_id")
    result = data.get("result")

    if not event_id or booking_id is None or not result:
        return {
            "error": (
                "event_id, booking_id and result are required"
            )
        }, 400

    result = result.upper()

    if result not in ("SUCCESS", "FAILED"):
        return {
            "error": "result must be SUCCESS or FAILED"
        }, 400

    # ------------------------------------------------
    # IDEMPOTENCY CHECK
    # ------------------------------------------------

    existing_payment = Payment.query.filter_by(
        event_id=event_id
    ).first()

    if existing_payment:
        return {
            "message": "Webhook already processed",
            "payment": {
                "id": existing_payment.id,
                "booking_id": existing_payment.booking_id,
                "event_id": existing_payment.event_id,
                "status": existing_payment.status
            }
        }, 200

    booking = db.session.get(
        Booking,
        booking_id
    )

    if not booking:
        return {
            "error": "Booking not found"
        }, 404

    
    if booking.payment:
        return {
            "message": "Booking already has a payment",
            "payment": {
                "id": booking.payment.id,
                "booking_id": booking.payment.booking_id,
                "event_id": booking.payment.event_id,
                "status": booking.payment.status
            }
        }, 200



    payment = Payment(
        booking_id=booking.id,
        event_id=event_id,
        amount=booking.amount,
        status=result
    )

   
    if result == "SUCCESS":
        booking.status = "CONFIRMED"
    else:
        booking.status = "FAILED"

    db.session.add(payment)
    db.session.commit()

    return {
        "message": "Webhook processed successfully",
        "payment": {
            "id": payment.id,
            "booking_id": payment.booking_id,
            "event_id": payment.event_id,
            "status": payment.status
        },
        "booking": {
            "id": booking.id,
            "status": booking.status
        }
    }, 200