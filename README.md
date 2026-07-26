# Книжковий магазин

Навчальний Django-проєкт онлайн-магазину книг, створений у рамках курсу Python.

Проєкт дозволяє користувачам переглядати книги, виконувати пошук та фільтрацію, додавати товари до кошика, створювати замовлення та переходити до оплати через Stripe.

---

## Основні можливості

- Перегляд списку книг
- Перегляд детальної інформації про книгу
- Пошук книг за назвою, автором та описом
- Фільтрація книг за категорією
- Фільтрація книг за наявністю
- Пагінація списку книг
- Реєстрація користувачів
- Авторизація та вихід з облікового запису
- Створення, редагування та видалення книг з перевіркою permissions
- Кошик на основі Django sessions
- Додавання та видалення книг з кошика
- Створення замовлення
- Інтеграція зі Stripe Checkout
- Відправлення email після створення замовлення
- Async views з використанням Django async ORM
- Інтернаціоналізація українською та англійською мовами
- Автоматичні тести з pytest-django
- Factory Boy для створення тестових даних
- Mock зовнішніх сервісів Stripe та email

---

## Технології

Проєкт використовує:

- Python
- Django
- PostgreSQL
- Docker / Docker Compose
- Stripe
- pytest
- pytest-django
- pytest-cov
- pytest-mock
- Factory Boy
- HTML
- CSS
- Bootstrap
- Git / GitHub

---

## Структура проєкту

```text
python_homework-main/
│
├── accounts/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── urls.py
│
├── bookstore/
│   ├── settings.py
│   ├── test_settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── catalog/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── cart.py
│   ├── middleware.py
│   ├── templates/
│   └── static/
│
├── locale/
│   ├── en/
│   └── uk/
│
├── tests/
│   ├── factories.py
│   ├── test_forms.py
│   ├── test_models.py
│   ├── test_user_flows.py
│   └── test_views.py
│
├── AI_REVIEW.md
├── AI_PROMPTS.md
├── README.md
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── requirements.txt
└── manage.py
```

---

## Встановлення

### 1. Клонування репозиторію

```bash
git clone https://github.com/OleksandrByhkov/python_homework.git
cd python_homework
```

### 2. Створення virtual environment

Windows:

```bash
python -m venv .venv
```

Активація:

```bash
.venv\Scripts\activate
```

### 3. Встановлення залежностей

```bash
pip install -r requirements.txt
```

### 4. Міграції

```bash
python manage.py migrate
```

### 5. Запуск сервера

```bash
python manage.py runserver
```

Після запуску сайт буде доступний через локальний Django development server.

---

## Інтернаціоналізація

Проєкт підтримує дві мови:

- українську;
- англійську.

Переклади зберігаються у директорії:

```text
locale/
```

Проєкт використовує Django internationalization та файли `.po` і `.mo`.

Для компіляції перекладів:

```bash
python manage.py compilemessages
```

---

## Async Views

У проєкті реалізовані асинхронні views з використанням Django async ORM:

```text
AsyncBookListView
AsyncBookDetailView
AsyncBookStatsView
```

Використовуються асинхронні ORM-операції, зокрема:

```python
aget()
acount()
```

та асинхронна ітерація QuerySet.

---

## Тестування

Для тестування використовується `pytest` та `pytest-django`.

Запуск усіх тестів:

```bash
pytest
```

На поточному етапі проєкт містить:

```text
43 passed
```

Тести охоплюють:

- models;
- forms;
- views;
- user flows;
- shopping cart;
- orders;
- Stripe integration;
- email.

Для тестових даних використовується Factory Boy.

Stripe та email тестуються з використанням mock, тому реальні зовнішні запити під час тестів не виконуються.

---

## Coverage

Для перевірки coverage:

```bash
pytest --cov
```

Coverage моделей:

```text
catalog/models.py    100%
```

Загальний coverage проєкту:

```text
TOTAL    92%
```

Таким чином, вимога coverage ≥ 60% виконана.

---

## AI Usage

Під час розробки проєкту використовувався ChatGPT як допоміжний AI-інструмент.

AI використовувався для:

- code review складних Django views;
- пошуку можливих оптимізацій коду;
- аналізу роботи з Django ORM;
- аналізу використання database transactions;
- генерації додаткових тестів для моделей;
- створення docstrings;
- покращення документації проєкту.

Для code review були обрані:

1. `BookListView`
2. `order_create`
3. `AsyncBookDetailView`

AI запропонував оптимізації, серед яких:

- оптимізація QuerySet;
- покращення обробки пошукових параметрів;
- оптимізація створення `OrderItem`;
- винесення зовнішніх Stripe та email операцій за межі database transaction;
- покращення обробки HTTP 404 в async view;
- додавання docstrings.

Усі AI-рекомендації були перевірені вручну перед застосуванням.

Повний процес code review знаходиться у:

```text
AI_REVIEW.md
```

Промпти, які використовувалися під час роботи з AI, знаходяться у:

```text
AI_PROMPTS.md
```

---

## Автор

Oleksandr Byhkov

Навчальний проєкт "Книжковий магазин".