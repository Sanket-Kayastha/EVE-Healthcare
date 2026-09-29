# EVE Healthcare Backend

Backend engineering assignment for EVE Healthcare built using Python, Flask, PostgreSQL and JWT authentication.

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-JWT-Extended
- Flask-Bcrypt
- PostgreSQL
- Pytest

## Features

- User signup and login
- JWT-based authentication
- Diagnostic centre management
- Diagnostic test management
- Centre-test pricing
- Authenticated test bookings
- Booking cancellation
- Simulated payments
- Payment success/failure handling
- Payment webhook
- Idempotent webhook processing
- Automated tests
- Database migrations

---

## Project Structure

```text
EVE_HealthCare/
│
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── centre.py
│   │   ├── diagnostic_test.py
│   │   ├── centre_test.py
│   │   ├── booking.py
│   │   └── payment.py
│   │
│   └── routes/
│       ├── auth.py
│       ├── centre.py
│       ├── test.py
│       ├── centre_test.py
│       ├── booking.py
│       └── payment.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_booking.py
│   └── test_payment.py
│
├── .env
├── .env.example
├── .gitignore
├── config.py
├── requirements.txt
├── run.py
└── README.md
```
## Run Project Locally
1. git clone <GITHUB_REPOSITORY_URL>
cd EVE_HealthCare

2. Create a virtual environment
python -m venv venv

3. Install dependencies
pip install -r requirements.txt

4. Create PostgreSQL database
CREATE DATABASE eve_healthcare;

5. Configure environment variables
DATABASE_URL=postgresql://postgres:<PASSWORD>@localhost:5432/eve_healthcare
JWT_SECRET_KEY=<LONG_RANDOM_SECRET>

6. Run database migrations
flask --app run.py db init
flask --app run.py db migrate -m "Initial database schema"
flask --app run.py db upgrade

7. Start the application
python run.py
The API will run at:
http://127.0.0.1:5000

Authentication APIs

POST /auth/signup
Example:

{
    "name": "Sanket",
    "email": "sanket@example.com",
    "password": "password123"
}

POST /auth/login
Example:

{
    "email": "sanket@example.com",
    "password": "password123"
}

Diagnostic Centre APIs
POST /centres/
Example:

{
    "name": "Apollo Diagnostic Centre",
    "location": "Lucknow"
}

Diagnostic Test APIs
Create Test
POST /tests/

Example:

{
    "name": "Complete Blood Count",
    "description": "Blood test used to evaluate overall health."
}

Centre-Test APIs
POST /centres/<centre_id>/tests

Example:

{
    "test_id": 1,
    "price": 500
}

Booking APIs
Create Booking
POST /bookings/

Example:

{
    "centre_test_id": 1,
    "appointment_datetime": "2026-10-15T10:30:00"
}

Payment APIs
POST /payments/

Example:

{
    "booking_id": 1,
    "result": "SUCCESS"
}

Database Design

The main entities are:

users
   |
   | 1:N
   v
bookings
   |
   | N:1
   v
centre_tests
   |
   +------> diagnostic_centres
   |
   +------> diagnostic_tests

bookings
   |
   | 1:1
   v
payments

Main Tables
users

Stores registered users and password hashes.

Important fields:

id
name
email
password_hash
created_at
diagnostic_centres

Stores diagnostic centre information.

Important fields:

id
name
location
created_at
diagnostic_tests

Stores available diagnostic tests.

Important fields:

id
name
description
centre_tests

Connects diagnostic centres with diagnostic tests.

Important fields:

id
centre_id
test_id
price

A unique constraint prevents the same test from being added twice to the same centre.

bookings

Stores appointments.

Important fields:

id
user_id
centre_test_id
appointment_datetime
amount
status
created_at
updated_at
payments

Stores simulated payment information.

Important fields:

id
booking_id
event_id
amount
status
created_at
updated_at

event_id is unique to support webhook idempotency.


Assumptions


Payments are simulated and do not connect to a real payment provider.
Users can access only their own bookings and payments.
Booking amount is determined from the centre-test price stored in the database.
Appointment dates must be in the future.
A booking can have at most one payment.
Payment webhook events are identified using a unique event ID.
PostgreSQL is the primary application database.
SQLite is used for automated tests.

Future Improvements

Possible improvements include:

Swagger/OpenAPI documentation
Docker and docker-compose setup
Redis caching
Rate limiting
Structured logging
Webhook retry handling
More comprehensive integration tests
Production deployment configuration
Role-based access control
