from datetime import datetime, timezone

from app.extensions import db


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    booking_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "bookings.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        unique=True
    )

    
    event_id = db.Column(
        db.String(100),
        unique=True,
        nullable=False,
        index=True
    )

    amount = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False
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

    # Relationship
    booking = db.relationship(
        "Booking",
        back_populates="payment"
    )

    def __repr__(self):
        return f"<Payment {self.id} status={self.status}>"