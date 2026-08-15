# Warehouse Service (ProjectB)

Independent Django/DRF service for bookstore stock and reservations. See the root `README.md` for architecture, Docker startup, API usage and deployment instructions.

Local development:

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
USE_REDIS=False .venv/bin/python manage.py migrate
USE_REDIS=False .venv/bin/python manage.py runserver 8001
```

Swagger: `http://127.0.0.1:8001/api/docs/`.
