from datetime import datetime, timezone

from app.extensions import db


class DiagnosticCentre(db.Model):
    __tablename__ = "diagnostic_centres"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(150),
        nullable=False
    )

    location = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationship with CentreTest
    centre_tests = db.relationship(
        "CentreTest",
        back_populates="centre",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<DiagnosticCentre {self.name}>"