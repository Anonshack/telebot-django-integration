# Telebot-Django-Integration

A full-stack Django project integrated with an **Aiogram Telegram Bot** for collecting, managing, and interacting with user feedbacks.

---

## Features

### Django Backend

* **Models**:

  * `BotUsers`: stores Telegram user information
  * `FeedbackForAdmin`: stores feedback messages linked to users
* **REST API**:

  * `GET /api/feedbacks/` - list all feedbacks
  * `POST /api/feedbacks/` - create new feedback
  * Supports filtering feedbacks by user
* **Admin Panel**:

  * Manage users and feedbacks
  * Optional import/export functionality
* **Serializers** for API communication
* Swagger/OpenAPI documentation included

### Telegram Bot

* Integrated with **Aiogram v3**.
* **Commands**:

  * `/start` → greets user and shows main feedback buttons
  * Inline buttons:

    * Show last 5 feedbacks (only user’s own)
    * Send new feedback
* **Feedback Interactions**:

  * Send, delete, update feedback
  * Inline buttons for per-feedback actions
  * FSM (Finite State Machine) for feedback creation & update
* Handles **async-safe Django ORM operations** via `sync_to_async`.
* Auto-restart on errors.

---

## Setup

### Requirements

* Python 3.10+
* Django 4.x
* djangorestframework
* aiogram
* requests
* python-dotenv

### Installation

```bash
git clone https://github.com/Anonshack/telebot-django-integration.git
cd telebot-django-integration
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```
SECRET_KEY=your_django_secret_key
DEBUG=True
TOKEN=your_telegram_bot_token
```

### Database

```bash
python manage.py makemigrations
python manage.py migrate
```

### Run Django Server

```bash
python manage.py runserver
```

### Run Telegram Bot

```bash
python bot/main.py
```

---

## Usage

1. Start bot via `/start` → shows buttons for sending or viewing feedbacks.
2. Send a feedback → stored in the database.
3. Show last 5 feedbacks → only your own messages displayed.
4. Delete or update feedback → interact with inline buttons.

---

## Folder Structure

```
telebot-django-integration/
│
├─ bot/               # Aiogram bot scripts
├─ main_tg_api/       # Django app
│   ├─ models.py      # BotUsers & Feedback models
│   ├─ serializers.py
│   ├─ views.py
│   └─ urls.py
├─ templates/
├─ static/
├─ manage.py
└─ .env
```

---

## Notes

* Make sure `SECRET_KEY` and `TOKEN` are set in `.env`.
* Bot uses `sync_to_async` for Django ORM compatibility in async context.
* Users can only view, delete, or update their own feedbacks.
* Inline buttons are dynamically generated per feedback.

---

# Qudratbekh -> Anonshack
* anonshak48@gmail.com