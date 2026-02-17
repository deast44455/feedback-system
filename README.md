# Информационная система для сбора и анализа отзывов ООО "Команда Ф5"

## Описание проекта

Полнофункциональная информационная система на Django для сбора и анализа отзывов от клиентов. Система включает веб-интерфейс для отправки отзывов, дашборд с аналитикой и графиками, а также REST API для интеграции с Telegram ботом.

## Технологический стек

- **Backend**: Django 5.x
- **Database**: PostgreSQL
- **Frontend**: Django Templates, Bootstrap 5
- **Графики**: Chart.js
- **API**: Django REST Framework
- **Анализ**: Rule-based sentiment analysis и автоматическая категоризация
- **Контейнеризация**: Docker и Docker Compose

## Функциональность

### 1. Система ролей пользователей

- **Администратор** - полный доступ ко всем функциям, включая Django Admin
- **Менеджер** - доступ к дашборду, просмотр и обработка отзывов
- **Клиент** - отправка отзывов через веб-форму (без авторизации)

### 2. Веб-интерфейс

- **Публичная форма отзывов** (`/`) - доступна без авторизации
- **Страница авторизации** (`/login/`) - вход в систему
- **Дашборд** (`/dashboard/`) - статистика и графики (требует авторизации)
- **Список отзывов** (`/feedbacks/`) - таблица всех отзывов с фильтрами
- **Детали отзыва** (`/feedbacks/<id>/`) - просмотр и обработка отзыва

### 3. Дашборд и аналитика

- Общая статистика (количество отзывов, средняя оценка)
- Распределение по тональности (позитивные/нейтральные/негативные)
- Динамика отзывов по датам (линейный график)
- Распределение оценок (столбчатая диаграмма)
- Распределение по категориям (круговая диаграмма)
- Распределение по тональности (круговая диаграмма)
- Распределение по источникам (веб/Telegram)
- Система фильтров (дата, категория, тональность, источник, статус)

### 4. REST API для Telegram бота

#### Отправка отзыва
```bash
POST /api/feedback/submit/
Headers: X-API-Key: your-api-key
Content-Type: application/json

{
  "client_name": "Иван Иванов",
  "client_phone": "+79001234567",
  "rating": 5,
  "category": "SERVICE",
  "text": "Отличное обслуживание!",
  "telegram_user_id": "123456789"
}
```

Ответ:
```json
{
  "success": true,
  "message": "Отзыв успешно принят",
  "feedback_id": 1
}
```

#### Получение статистики
```bash
GET /api/feedback/stats/
Headers: X-API-Key: your-api-key
```

Ответ:
```json
{
  "success": true,
  "data": {
    "total_count": 150,
    "average_rating": 4.2,
    "positive_count": 95,
    "neutral_count": 30,
    "negative_count": 25,
    "by_category": {
      "QUALITY": 50,
      "SERVICE": 60,
      "PRICE": 20,
      "DELIVERY": 15,
      "OTHER": 5
    },
    "by_source": {
      "WEB": 100,
      "TELEGRAM": 50
    }
  }
}
```

### 5. Автоматический анализ

- **Анализ тональности** - автоматическое определение настроения отзыва (позитивный/нейтральный/негативный)
- **Категоризация** - автоматическое определение категории по ключевым словам

## Требования

- Docker
- Docker Compose

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/deast44455/feedback-system.git
cd feedback-system
```

### 2. Создание файла .env

Скопируйте `.env.example` в `.env` и настройте переменные окружения:

```bash
cp .env.example .env
```

Отредактируйте `.env` файл:
```
DEBUG=True
SECRET_KEY=your-secret-key-change-this-in-production
DATABASE_NAME=feedback_db
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=db
DATABASE_PORT=5432
API_KEY=your-api-key-for-telegram-bot-change-this
ALLOWED_HOSTS=localhost,127.0.0.1
```

**ВАЖНО**: Измените `SECRET_KEY` и `API_KEY` на свои уникальные значения в production!

### 3. Запуск через Docker Compose

```bash
docker-compose up --build
```

При первом запуске автоматически:
- Создастся база данных PostgreSQL
- Применятся все миграции
- Соберутся статические файлы

### 4. Создание суперпользователя (опционально)

В отдельном терминале:

```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. Создание тестовых пользователей

```bash
docker-compose exec web python manage.py create_test_users
```

Будут созданы:
- **Администратор**: username=`admin`, password=`admin123`
- **Менеджер**: username=`manager`, password=`manager123`

## Доступ к системе

После запуска система будет доступна по адресам:

- **Главная страница (форма отзывов)**: http://localhost:8000/
- **Авторизация**: http://localhost:8000/login/
- **Дашборд**: http://localhost:8000/dashboard/
- **Список отзывов**: http://localhost:8000/feedbacks/
- **Django Admin**: http://localhost:8000/admin/
- **API отправки отзыва**: http://localhost:8000/api/feedback/submit/
- **API статистики**: http://localhost:8000/api/feedback/stats/

## Структура проекта

```
feedback-system/
├── docker-compose.yml          # Конфигурация Docker Compose
├── Dockerfile                  # Dockerfile для Django приложения
├── entrypoint.sh              # Скрипт инициализации при запуске
├── requirements.txt           # Python зависимости
├── .env.example              # Пример файла переменных окружения
├── .gitignore                # Git ignore правила
├── README.md                 # Документация
├── manage.py                 # Django management скрипт
├── feedback_project/         # Основной проект Django
│   ├── settings.py          # Настройки проекта
│   ├── urls.py              # Главные URL маршруты
│   └── wsgi.py              # WSGI конфигурация
└── feedback/                # Приложение для отзывов
    ├── models.py            # Модели данных (User, Feedback)
    ├── views.py             # Views для веб-интерфейса и API
    ├── forms.py             # Формы Django
    ├── urls.py              # URL маршруты приложения
    ├── admin.py             # Настройка Django Admin
    ├── serializers.py       # DRF сериализаторы для API
    ├── permissions.py       # Права доступа и API ключи
    ├── utils/              # Утилиты
    │   ├── sentiment_analysis.py    # Анализ тональности
    │   └── category_detection.py    # Автокатегоризация
    ├── management/         # Management команды
    │   └── commands/
    │       └── create_test_users.py
    ├── templates/          # HTML шаблоны
    │   ├── base.html
    │   └── feedback/
    │       ├── submit.html
    │       ├── login.html
    │       ├── dashboard.html
    │       ├── feedback_list.html
    │       └── feedback_detail.html
    └── static/             # Статические файлы
        └── feedback/
            ├── css/
            │   └── styles.css
            └── js/
                └── charts.js
```

## Примеры использования API

### Отправка отзыва через curl

```bash
curl -X POST http://localhost:8000/api/feedback/submit/ \
  -H "X-API-Key: your-api-key-for-telegram-bot-change-this" \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "Иван Иванов",
    "client_phone": "+79001234567",
    "rating": 5,
    "category": "SERVICE",
    "text": "Отличное обслуживание! Очень доволен работой менеджеров.",
    "telegram_user_id": "123456789"
  }'
```

### Получение статистики через curl

```bash
curl http://localhost:8000/api/feedback/stats/ \
  -H "X-API-Key: your-api-key-for-telegram-bot-change-this"
```

## Модели данных

### User (Пользователь)

Расширение стандартной модели Django с ролями:
- `username` - имя пользователя
- `email` - email
- `role` - роль (ADMINISTRATOR, MANAGER, CLIENT)
- `is_active` - активен ли пользователь

### Feedback (Отзыв)

Основная модель отзыва:
- `client_name` - имя клиента
- `client_email` - email клиента (опционально)
- `client_phone` - телефон клиента (опционально)
- `telegram_user_id` - ID пользователя Telegram (опционально)
- `source` - источник (WEB, TELEGRAM)
- `rating` - оценка (1-5)
- `category` - категория (QUALITY, SERVICE, PRICE, DELIVERY, OTHER)
- `text` - текст отзыва
- `sentiment` - тональность (POSITIVE, NEUTRAL, NEGATIVE)
- `created_at` - дата создания
- `updated_at` - дата обновления
- `is_processed` - обработан ли отзыв
- `processed_by` - кто обработал
- `response` - ответ на отзыв

## Управление проектом

### Остановка контейнеров

```bash
docker-compose down
```

### Просмотр логов

```bash
docker-compose logs -f web
```

### Выполнение команд Django

```bash
docker-compose exec web python manage.py <command>
```

### Применение миграций

```bash
docker-compose exec web python manage.py migrate
```

### Создание миграций

```bash
docker-compose exec web python manage.py makemigrations
```

### Сбор статических файлов

```bash
docker-compose exec web python manage.py collectstatic
```

## Безопасность

- CSRF защита на всех формах
- SQL injection защита через Django ORM
- XSS защита через Django templating
- API ключ для аутентификации Telegram бота
- Система ролей и прав доступа
- Переменные окружения для конфиденциальных данных

## Скриншоты

_Скриншоты будут добавлены после развертывания системы_

## Технологии

- **Django 5.x** - веб-фреймворк
- **PostgreSQL** - база данных
- **Django REST Framework** - REST API
- **Bootstrap 5** - CSS фреймворк
- **Chart.js** - библиотека для графиков
- **Docker & Docker Compose** - контейнеризация
- **Gunicorn** - WSGI сервер

## Лицензия

MIT License

---

© 2024 ООО "Команда Ф5"

