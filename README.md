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
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser

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
json```
POST /api/token/refresh/


