# 🧾 Subscription Management System with Currency Exchange Tracker

A Django-based system to manage user subscriptions and monitor real-time currency exchange rates.

---

## 🚀 Features

- User subscriptions to plans (duration-based)
- JWT-authenticated REST APIs
- Exchange rate integration via public API
- Background exchange rate fetcher via Celery + Redis
- Admin interface for plans, subscriptions, and exchange logs
- Bootstrap-powered frontend `/subscriptions/` view (public)
- Optional Docker support (if needed)

---

## 🛠 Tech Stack

- Django + DRF
- SQLite
- Celery + Redis
- Bootstrap (HTML frontend)
- JWT Authentication

---

## 🧩 Installation & Local Setup

```bash
git clone https://github.com/muhayminul96/SubscriptionManagementSystem.git
cd subscription-system
```
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```
```bash
pip install -r requirements.txt
```
```bash
python manage.py migrate
```
```bash
python manage.py createsuperuser
```
```bash
python manage.py runserver
```

## 🔗 API Endpoints

All endpoints are under the `/api/` namespace and require **JWT authentication** unless otherwise noted.

---

### 🔐 Authentication

#### POST `/api/token/`
Obtain JWT access and refresh tokens.
```json
Request:
{
  "username": "yourusername",
  "password": "yourpassword"
}

Response:
{
  "access": "<access_token>",
  "refresh": "<refresh_token>"
}
```
POST /api/token/refresh/

```json 
Request:
{
  "refresh": "<your_refresh_token>"
}

Response:
{
  "access": "<new_access_token>"
}
```
#### GET /api/plans/
Returns a list of all available subscription plans.

#### GET /api/subscriptions/
List all subscriptions for the currently authenticated user.

#### POST /api/subscriptions/
Subscribe to a plan.
```json
Request:
{
  "plan_id": 1
}

Response:
{
  "message": "Subscription created successfully",
  "subscription": {
    "id": 6,
    "user": {...},
    "plan": {...},
    "start_date": "...",
    "end_date": "...",
    "status": "active"
  }
}
```
#### POST /api/cancel/
Cancel a subscription.

```json 
Request:
{
  "plan_id": 1
}


Response:
{
  "message": "Subscription cancelled successfully",
  "subscription": {
    "id": 6,
    "status": "cancelled"
    ...
  }
}
```

#### GET /api/exchange-rate/?base=USD&target=BDT

Fetch and return the latest exchange rate between currencies.

```json
Response:
{
  "base_currency": "USD",
  "target_currency": "BDT",
  "rate": 109.76,
  "fetched_at": "2025-07-31T11:00:00Z"
}
```




