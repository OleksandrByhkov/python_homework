FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN sed -i 's/\r$//' docker-entrypoint.sh && chmod +x docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]

CMD ["sh", "-c", "gunicorn bookstore.wsgi:application --bind 0.0.0.0:${PORT:-10000} --workers 2 --access-logfile - --error-logfile -"]