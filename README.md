<div align="center">

# FAEZEH SALON

### Enterprise Salon Management Platform

<p align="center">
A Modern Full-Stack Platform for Hair Braiding & Extension Businesses
</p>

<br>

<img src="https://img.shields.io/badge/Django-5.0-092E20?style=for-the-badge&logo=django&logoColor=white"/>
<img src="https://img.shields.io/badge/Next.js-14-000000?style=for-the-badge&logo=nextdotjs&logoColor=white"/>
<img src="https://img.shields.io/badge/PostgreSQL-16-316192?style=for-the-badge&logo=postgresql&logoColor=white"/>
<img src="https://img.shields.io/badge/Redis-7-DC382D?style=for-the-badge&logo=redis&logoColor=white"/>
<img src="https://img.shields.io/badge/Celery-5-37814A?style=for-the-badge&logo=celery&logoColor=white"/>
<img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>

<br><br>

### Designed & Engineered by

# NIEMA KHADEH

*Full Stack Software Engineer*

</div>

---

## Executive Summary

FAEZEH SALON is a production-ready enterprise platform developed to digitize and automate salon operations.

The platform combines appointment scheduling, online payments, customer relationship management, loyalty programs, SMS automation, real-time communication, business intelligence, and customer engagement tools into a unified ecosystem.

Built with scalability, maintainability, and modern software architecture principles in mind, the system demonstrates advanced backend engineering, real-time communication, distributed task processing, and containerized deployment.

---

## Core Business Capabilities

### Appointment Management

* Dynamic scheduling engine
* Real-time availability calculation
* Specialist calendar management
* Deposit-based reservation workflow
* Automated reminders and follow-ups

### Customer Relationship Management

* Centralized customer profiles
* Customer lifecycle tracking
* Interaction history
* Targeted communication campaigns
* Retention management

### Payment Infrastructure

* Zarinpal payment gateway integration
* Wallet-based transactions
* Deposit payments
* Purchase payments
* Transaction auditing

### Loyalty & Rewards

* Point accumulation system
* Reward conversion engine
* Custom loyalty rules
* Customer engagement metrics

### Communication Layer

* Real-time WebSocket messaging
* Telegram bot integration
* SMS automation
* Event-driven notifications

### Administrative Operations

* Business analytics dashboard
* Customer management
* Service management
* Transaction monitoring
* Content moderation

---

## System Architecture

```text
┌──────────────────────────────────────┐
│              Next.js 14              │
│         Frontend Application         │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│          Django REST Framework       │
│             API Layer                │
└───────┬──────────┬───────────┬────────┘
        │          │           │
        ▼          ▼           ▼

 PostgreSQL      Redis     Channels
 Database        Cache     WebSocket

                    │
                    ▼

                 Celery
           Async Task Queue

                    │
                    ▼

       SMS • Telegram • Payments
```

---

## Technology Stack

### Backend

* Django 5
* Django REST Framework
* Django Channels
* Celery
* Redis
* PostgreSQL

### Frontend

* Next.js 14
* TypeScript
* React
* Tailwind CSS

### Infrastructure

* Docker
* Docker Compose
* Nginx
* Daphne ASGI

### Integrations

* Zarinpal
* Kavenegar
* Telegram Bot API

---

## Engineering Highlights

### Authentication & Authorization

* JWT Authentication
* Refresh Token Rotation
* OTP Password Recovery
* Role-Based Access Control

### Real-Time Systems

* WebSocket Architecture
* Live Chat Messaging
* Instant Notifications

### Distributed Processing

* Celery Workers
* Scheduled Tasks
* Background Processing
* Queue Management

### Scalability

* Service-Oriented Structure
* Modular Django Apps
* Containerized Deployment
* Redis-Based Caching

---

## Project Structure

```text
backend/
 ├── accounts
 ├── services
 ├── appointments
 ├── payments
 ├── wallet
 ├── loyalty
 ├── gallery
 ├── chat
 ├── survey
 ├── crm
 └── telegram_bot

frontend/
 ├── app
 ├── components
 ├── lib
 └── public

docker/
 └── nginx
```

---

## Deployment

```bash
git clone https://github.com/your-username/faezeh-salon

cd faezeh-salon

cp .env.example .env

docker compose up -d --build
```

---

## Production Features

✔ JWT Authentication

✔ Appointment Scheduling Engine

✔ Online Payments

✔ Wallet System

✔ Loyalty Program

✔ CRM

✔ Real-Time Chat

✔ SMS Automation

✔ Telegram Integration

✔ Customer Surveys

✔ Dockerized Infrastructure

✔ PostgreSQL Persistence

✔ Redis Caching

✔ Celery Background Tasks

---

## Software Engineering Goals

This project was built to demonstrate:

* Enterprise Software Architecture
* Backend System Design
* API Development
* Real-Time Communication
* Payment Gateway Integration
* Asynchronous Processing
* Docker-Based Deployment
* Modern Full Stack Development

---

## Developer

### NIEMA KHADEH

Full Stack Software Engineer

Specializing in:

* Python & Django
* Next.js & React
* PostgreSQL
* Redis
* Docker
* System Design
* API Architecture
* Real-Time Applications

---

<div align="center">

### "Building scalable software that solves real business problems."

<br>

© 2026 NIEMA KHADEH

</div>

