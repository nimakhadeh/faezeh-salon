# Faezeh Salon

## Salon Management & Booking Platform

Faezeh Salon is a full-stack business platform built to digitize appointment booking, customer management, payments, notifications and real-time communication for a hair-braiding and extension business.

## What the System Does

- Customer registration and authentication
- JWT-based API authentication
- OTP password recovery
- Specialist management
- Service and pricing management
- Appointment booking and availability checks
- Deposit-based reservation flow
- Zarinpal payment integration
- Wallet and transaction management
- Loyalty and CRM features
- SMS and Telegram notifications
- Real-time customer/specialist chat
- Background jobs with Celery
- PostgreSQL and Redis
- Docker-based deployment

## Architecture

```text
Next.js 14
    │
    ▼
Django REST Framework
    │
    ├── PostgreSQL
    ├── Redis
    ├── Django Channels
    └── Celery
          │
          ├── Kavenegar
          ├── Telegram
          └── Zarinpal
```

## Tech Stack

### Backend
- Python
- Django
- Django REST Framework
- Django Channels
- Simple JWT
- Celery
- Redis
- PostgreSQL

### Frontend
- Next.js 14
- React
- TypeScript
- Tailwind CSS

### Infrastructure
- Docker / Docker Compose
- Nginx
- Daphne / ASGI

### Integrations
- Zarinpal
- Kavenegar
- Telegram Bot API
- Cloudinary

## Backend Engineering Highlights

### Authentication
- JWT access/refresh authentication
- Refresh-token rotation and blacklist support
- Password validation
- OTP password reset
- Rate limiting for sensitive authentication endpoints
- Role-based access control
- Protection against public role escalation

### Appointment Workflow
Appointment state transitions are controlled by user role and current appointment state.

The booking layer checks specialist availability and prevents overlapping confirmed or deposit-paid appointments at the application level.

### Payment Handling
Payment callbacks use transactional locking and idempotent success handling so repeated callbacks do not repeat business side effects.

### Asynchronous Processing
Celery handles operations such as SMS delivery, scheduled jobs and notification workflows.

## Project Structure

```text
backend/
├── apps/
│   ├── accounts/
│   ├── appointments/
│   ├── services/
│   ├── payments/
│   ├── wallet/
│   ├── loyalty/
│   ├── gallery/
│   ├── chat/
│   ├── survey/
│   └── crm/
├── config/
└── manage.py

frontend/
└── Next.js application
```

## Local Development

Backend dependencies are defined in `backend/requirements.txt`.

Typical Django commands:

```bash
python manage.py migrate
python manage.py test
python manage.py runserver
```

For the full stack, use the project's Docker Compose configuration.

## Portfolio Focus

This project demonstrates practical experience with:

- REST API design
- Django application architecture
- authentication and authorization
- database-backed business workflows
- payment gateway integration
- WebSocket communication
- asynchronous task processing
- Dockerized deployment
- security hardening and regression testing

## Developer

**Nima Khadeh**

Backend-focused Software Developer

**Python · Django · DRF · PostgreSQL · Redis · Celery · Docker · REST APIs**
