# Task Tracker Project

Task Tracker - это веб-приложение для управления задачами и проектами, построенное на основе FastAPI и PostgreSQL. Приложение поддерживает управление пользователями, проектами и задачами с использованием современных технологий, таких как Docker, Celery, Redis и SMTP для отправки электронной почты.

## Функциональные возможности

- **Управление пользователями**: регистрация, авторизация, управление профилем.
- **Управление проектами**: создание, редактирование и просмотр проектов.
- **Управление задачами**: создание, назначение и отслеживание задач.
- **Администрирование**: интерфейсы для администраторов и обычных пользователей.
- **Отправка уведомлений по электронной почте**: для подтверждения регистрации и уведомлений о задачах.

## Технологии

- **FastAPI**: основной фреймворк для создания веб-приложения.
- **PostgreSQL**: база данных для хранения информации о пользователях, проектах и задачах.
- **Docker**: контейнеризация приложения и зависимостей.
- **Celery и Redis**: для выполнения фоновых задач, таких как отправка уведомлений.
- **SMTP**: отправка писем с подтверждением регистрации и уведомлениями.
- **SQLAlchemy**: ORM для работы с базой данных.

## Установка

### Шаг 1: Клонируйте репозиторий

```bash
git clone https://github.com/yourusername/task-tracker.git
cd task-tracker
```

### Шаг 2: Настройте переменные окружения

- Создайте файл .env в корневой директории проекта на основе предоставленного шаблона:

```
MODE="DEV"
DB_URL='postgresql+asyncpg://postgres:password@postgres_db:5432/postgres'
TEST_DB_URL='postgresql+asyncpg://postgres:password@postgres_db:5432/test_postgres'
POSTGRES_USER='postgres'
POSTGRES_PASSWORD='password'
POSTGRES_DB='postgres'
REDIS_URL='redis://redis:6379/0'
ADMIN_EMAIL='admin@admin.com'
SECRET_KEY='your_secret_key'
ALGORITHM='HS256'
SMTP_HOST='smtp.gmail.com'
SMTP_PORT='465'
SMTP_USERNAME='your_email@gmail.com'
SMTP_PASSWORD='your_email_password'
```

## Запуск

```bash
docker-compose up --build
```

Приложение будет доступно по адресу http://localhost:8000. Документация API доступна по адресу http://localhost:8000/docs.

