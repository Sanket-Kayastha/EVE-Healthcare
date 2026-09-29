from flask import Blueprint, request

from app.extensions import db
from app.models.diagnostic_test import DiagnosticTest
from app.models.centre import DiagnosticCentre
from app.models.centre_test import CentreTest


test_bp = Blueprint(
    "test",
    __name__,
    url_prefix="/tests"
)


@test_bp.route("/", methods=["POST"])
def create_test():
    data = request.get_json()

    if not data:
        return {"error": "Request body is required"}, 400

    name = data.get("name")
    description = data.get("description")

    if not name:
        return {
            "error": "name is required"
        }, 400

    test = DiagnosticTest(
        name=name.strip(),
        description=description.strip() if description else None
    )

    db.session.add(test)
    db.session.commit()

    return {
        "message": "Diagnostic test created successfully",
        "test": {
            "id": test.id,
            "name": test.name,
            "description": test.description
        }
    }, 201


@test_bp.route("/", methods=["GET"])
def get_tests():
    tests = DiagnosticTest.query.order_by(
        DiagnosticTest.id
    ).all()

    result = []

    for test in tests:
        result.append({
            "id": test.id,
            "name": test.name,
            "description": test.description
        })

    return {
        "tests": result
    }, 200


@test_bp.route(
    "/<int:test_id>",
    methods=["GET"]
)
def get_test(test_id):
    test = db.session.get(
        DiagnosticTest,
        test_id
    )

    if not test:
        return {
            "error": "Diagnostic test not found"
        }, 404

    centres = []

    for centre_test in test.centre_tests:
        centres.append({
            "centre_id": centre_test.centre.id,
            "centre_name": centre_test.centre.name,
            "price": float(centre_test.price)
        })

    return {
        "id": test.id,
        "name": test.name,
        "description": test.description,
        "centres": centres
    }, 200