from decimal import Decimal

from app.extensions import db


class CentreTest(db.Model):
    __tablename__ = "centre_tests"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    centre_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "diagnostic_centres.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    test_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "diagnostic_tests.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    price = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    # Relationships
    centre = db.relationship(
        "DiagnosticCentre",
        back_populates="centre_tests"
    )

    test = db.relationship(
        "DiagnosticTest",
        back_populates="centre_tests"
    )

    bookings = db.relationship(
    "Booking",
    back_populates="centre_test"
    )

    
    __table_args__ = (
        db.UniqueConstraint(
            "centre_id",
            "test_id",
            name="uq_centre_test"
        ),
    )

    def __repr__(self):
        return f"<CentreTest centre={self.centre_id} test={self.test_id}>"