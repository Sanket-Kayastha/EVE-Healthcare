from app.extensions import db


class DiagnosticTest(db.Model):
    __tablename__ = "diagnostic_tests"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    # Relationship with CentreTest
    centre_tests = db.relationship(
        "CentreTest",
        back_populates="test",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<DiagnosticTest {self.name}>"