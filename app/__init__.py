from flask import Flask

from config import Config
from app.extensions import db, migrate, jwt, bcrypt


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Import models so SQLAlchemy knows about them
    from app.models import (
        User,
        DiagnosticCentre,
        DiagnosticTest,
        CentreTest,
        Booking,
        Payment,
    )

    @app.route("/")
    def home():
        return {"message": "EVE Healthcare API is running"}

    from app.routes.auth import auth_bp
    from app.routes.centre import centre_bp
    from app.routes.test import test_bp
    from app.routes.payment import payment_bp
    from app.routes.booking import booking_bp
    from app.routes.centre_test import centre_test_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(centre_bp)
    app.register_blueprint(test_bp)
    app.register_blueprint(centre_test_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(payment_bp)


    return app