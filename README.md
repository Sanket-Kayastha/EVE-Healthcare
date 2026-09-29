# EVE Healthcare – Backend Engineering Assignment

A backend API for **diagnostic test bookings and simulated payments**, built using Flask and PostgreSQL.

## Tech Stack

* Python
* Flask
* PostgreSQL
* SQLAlchemy
* Flask-JWT-Extended
* Flask-Migrate
* Flask-Bcrypt
* Pytest

## Features

* User signup and login with JWT authentication
* Diagnostic centre management
* Diagnostic test management
* Centre-specific test pricing
* Authenticated test bookings
* Simulated payment processing
* Payment webhook
* Idempotent webhook handling
* Booking and payment status management
* Input validation and authorization
* Automated tests

## Project Structure

```text
eve-healthcare/
├── app/
│   ├── models/
│   └── routes/
├── tests/
├── migrations/
├── config.py
├── run.py
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Sanket-Kayastha/EVE-Healthcare.git
cd EVE-Healthcare
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://postgres:<password>@localhost:5432/eve_healthcare
JWT_SECRET_KEY=<your-secret-key>
```

### 5. Create database

```sql
CREATE DATABASE eve_healthcare;
```

Run migrations:

```bash
flask --app run.py db upgrade
```

### 6. Start the server

```bash
python run.py
```

API will run at:

```text
http://127.0.0.1:5000
```

## Main API Endpoints

| Method | Endpoint              | Purpose                      |
| ------ | --------------------- | ---------------------------- |
| POST   | `/auth/signup`        | Register user                |
| POST   | `/auth/login`         | Login and receive JWT        |
| GET    | `/auth/me`            | Get current user             |
| POST   | `/centres/`           | Create diagnostic centre     |
| GET    | `/centres/`           | List centres                 |
| POST   | `/tests/`             | Create diagnostic test       |
| GET    | `/tests/`             | List tests                   |
| POST   | `/centres/<id>/tests` | Add test and price to centre |
| POST   | `/bookings/`          | Create booking               |
| GET    | `/bookings/`          | View user's bookings         |
| GET    | `/bookings/<id>`      | View booking                 |
| DELETE | `/bookings/<id>`      | Cancel booking               |
| POST   | `/payments/`          | Simulate payment             |
| GET    | `/payments/<id>`      | View payment                 |
| POST   | `/payments/webhook/`  | Process payment webhook      |

## Booking & Payment Flow

```text
User Login
    ↓
Select Diagnostic Test
    ↓
Create Booking
    ↓
Payment
    ↓
SUCCESS → Booking CONFIRMED
FAILED  → Booking FAILED
```

Payment webhooks use an `event_id` to ensure **idempotency**, preventing duplicate payment records when the same event is received multiple times.

## Database Design

Main entities:

* `User`
* `Centre`
* `DiagnosticTest`
* `CentreTest`
* `Booking`
* `Payment`

`CentreTest` stores the price because the same diagnostic test can have different prices at different centres.

## Validation & Security

* JWT authentication
* Password hashing with bcrypt
* User ownership checks
* Invalid ID handling
* Future appointment validation
* Duplicate payment prevention
* Idempotent payment webhooks
* Booking status validation

## Testing

Run:

```bash
python -m pytest
```

The project includes authentication, booking, payment, and webhook tests.

## Assumptions

* Payments are simulated; no real payment gateway is integrated.
* Only authenticated users can create and manage their own bookings.
* A booking has a single associated payment.
* Payment webhook events are uniquely identified by `event_id`.

## Future Improvements

* Redis caching
* Celery background jobs
* Docker/Docker Compose
* Swagger/OpenAPI documentation
* Pagination
* Rate limiting
* Structured logging
* Advanced webhook retry handling
