from flask import Blueprint, request

from app.extensions import db
from app.models.centre import DiagnosticCentre
from app.models.diagnostic_test import DiagnosticTest
from app.models.centre_test import CentreTest


centre_bp = Blueprint(
    "centre",
    __name__,
    url_prefix="/centres"
)


@centre_bp.route("/", methods=["POST"])
def create_centre():
    data = request.get_json()

    if not data:
        return {"error": "Request body is required"}, 400

    name = data.get("name")
    location = data.get("location")

    if not name or not location:
        return {
            "error": "name and location are required"
        }, 400

    centre = DiagnosticCentre(
        name=name.strip(),
        location=location.strip()
    )

    db.session.add(centre)
    db.session.commit()

    return {
        "message": "Diagnostic centre created successfully",
        "centre": {
            "id": centre.id,
            "name": centre.name,
            "location": centre.location
        }
    }, 201


@centre_bp.route("/", methods=["GET"])
def get_centres():
    centres = DiagnosticCentre.query.order_by(
        DiagnosticCentre.id
    ).all()

    result = []

    for centre in centres:
        result.append({
            "id": centre.id,
            "name": centre.name,
            "location": centre.location
        })

    return {
        "centres": result
    }, 200


@centre_bp.route("/<int:centre_id>", methods=["GET"])
def get_centre(centre_id):
    centre = db.session.get(
        DiagnosticCentre,
        centre_id
    )

    if not centre:
        return {
            "error": "Diagnostic centre not found"
        }, 404

    tests = []

    for centre_test in centre.centre_tests:
        tests.append({
            "test_id": centre_test.test.id,
            "test_name": centre_test.test.name,
            "price": float(centre_test.price)
        })

    return {
        "id": centre.id,
        "name": centre.name,
        "location": centre.location,
        "tests": tests
    }, 200