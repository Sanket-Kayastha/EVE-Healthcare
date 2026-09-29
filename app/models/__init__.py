from app.models.user import User
from app.models.centre import DiagnosticCentre
from app.models.diagnostic_test import DiagnosticTest
from app.models.centre_test import CentreTest
from app.models.booking import Booking
from app.models.payment import Payment

__all__ = [
    "User",
    "DiagnosticCentre",
    "DiagnosticTest",
    "CentreTest",
    "Booking",
    "Payment",
]