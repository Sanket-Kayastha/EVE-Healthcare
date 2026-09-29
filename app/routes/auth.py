from flask import Blueprint, request
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from app.extensions import db
from app.models.user import User


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    if not data:
        return {"error": "Request body is required"}, 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return {
            "error": "name, email and password are required"
        }, 400

    if len(password) < 6:
        return {
            "error": "Password must be at least 6 characters"
        }, 400

    email = email.strip().lower()

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return {
            "error": "User with this email already exists"
        }, 409

    password_hash = generate_password_hash(password).decode("utf-8")

    user = User(
        name=name.strip(),
        email=email,
        password_hash=password_hash,
    )

    db.session.add(user)
    db.session.commit()

    return {
        "message": "User registered successfully",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        },
    }, 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return {"error": "Request body is required"}, 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {
            "error": "email and password are required"
        }, 400

    email = email.strip().lower()

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(
        user.password_hash,
        password
    ):
        return {
            "error": "Invalid email or password"
        }, 401

    access_token = create_access_token(identity=str(user.id))

    return {
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        },
    }, 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()

    user = db.session.get(User, int(user_id))

    if not user:
        return {"error": "User not found"}, 404

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
    }, 200