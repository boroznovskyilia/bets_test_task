FROM python:3.10-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry --no-cache-dir && \
    poetry config virtualenvs.create false && \
    poetry install --only main

COPY . .

RUN chmod +x start.sh

ENV APP__HOST=0.0.0.0
ENV APP__PORT=8080

CMD ["./start.sh"]
