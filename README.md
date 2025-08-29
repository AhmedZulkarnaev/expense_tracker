# Трекер расходов

Простое приложение для учета расходов и доходов с backend на Django REST и статическим JavaScript frontend.

## Возможности

- Классификация расходов и доходов для каждого пользователя с сохранением суммы, даты и описания
- Аутентификация на основе JWT и кастомная модель пользователя, где в качестве имени используется e-mail
- REST API для управления категориями и расходами, генерации сводных и категориальных отчетов, а также экспорта расходов в CSV
- Интерактивная документация API, генерируемая drf-spectacular по адресу `/api/docs/`

## Начало работы

### Необходимые инструменты

- [Docker](https://www.docker.com/) и [Docker Compose](https://docs.docker.com/compose/)
- Либо Python 3.12 и pip для локального запуска backend.

### Переменные окружения

Скопируйте `.env.example` в `.env` и при необходимости измените значения:

```bash
cp .env.example .env
```

Файл `.env` содержит учетные данные базы данных и секретный ключ Django.

### Запуск в Docker

```bash
docker-compose up --build
```

- Backend будет доступен по адресу `http://localhost:8000`
- Frontend, обслуживаемый Nginx, по адресу `http://localhost:3000`

### Локальная разработка

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

API будет доступен по адресу `http://localhost:8000`.

### Запуск тестов

```bash
cd backend
python manage.py test
```

## Структура проекта

- `backend/` – Django‑проект с REST API
- `frontend/` – статический frontend на HTML/CSS/JS
- `docker-compose.yml` – конфигурация Docker, связывающая Django, PostgreSQL и Nginx
