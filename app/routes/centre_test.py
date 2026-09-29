from flask import Blueprint, request

from app.extensions import db
from app.models.centre import DiagnosticCentre
from app.models.diagnostic_test import DiagnosticTest
from app.models.centre_test import CentreTest


centre_test_bp = Blueprint(
    "centre_test",
    __name__,
    url_prefix="/centres"
)


@centre_test_bp.route(
    "/<int:centre_id>/tests",
    methods=["POST"]
)
def add_test_to_centre(centre_id):
    data = request.get_json()

    if not data:
        return {
            "error": "Request body is required"
        }, 400

    test_id = data.get("test_id")
    price = data.get("price")

    if test_id is None or price is None:
        return {
            "error": "test_id and price are required"
        }, 400

    centre = db.session.get(
        DiagnosticCentre,
        centre_id
    )

    if not centre:
        return {
            "error": "Diagnostic centre not found"
        }, 404

    test = db.session.get(
        DiagnosticTest,
        test_id
    )

    if not test:
        return {
            "error": "Diagnostic test not found"
        }, 404

    try:
        price = float(price)
    except (TypeError, ValueError):
        return {
            "error": "price must be a valid number"
        }, 400

    if price <= 0:
        return {
            "error": "price must be greater than 0"
        }, 400

    existing = CentreTest.query.filter_by(
        centre_id=centre_id,
        test_id=test_id
    ).first()

    if existing:
        return {
            "error": "Test is already available at this centre"
        }, 409

    centre_test = CentreTest(
        centre_id=centre_id,
        test_id=test_id,
        price=price
    )

    db.session.add(centre_test)
    db.session.commit()

    return {
        "message": "Test added to centre successfully",
        "centre_test": {
            "id": centre_test.id,
            "centre_id": centre_id,
            "test_id": test_id,
            "price": float(centre_test.price)
        }
    }, 201