from datetime import datetime, timezone

from app.extensions import db


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    centre_test_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "centre_tests.id",
            ondelete="RESTRICT"
        ),
        nullable=False
    )

    appointment_datetime = db.Column(
        db.DateTime(timezone=True),
        nullable=False
    )

    amount = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="PENDING"
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    user = db.relationship(
        "User",
        back_populates="bookings"
    )

    centre_test = db.relationship(
        "CentreTest"
    )

    payment = db.relationship(
        "Payment",
        back_populates="booking",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Booking {self.id} status={self.status}>"