# syntax=docker/dockerfile:1

FROM python:3.12-slim

# Не пишем .pyc, не буферизуем stdout — логи сразу видно в kubectl logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Сначала только requirements.txt — так слой с зависимостями кэшируется
# и не пересобирается при каждом изменении кода бота
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Теперь копируем весь код проекта
COPY . .

# Alem Plus проверяет живость пода по 80 порту (HTTP) —
# см. правки в main.py: рядом с polling поднят aiohttp healthcheck-сервер
EXPOSE 80

CMD ["python", "main.py"]
