FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    libjpeg-dev \
    zlib1g-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN python -m venv /opt/venv

RUN . /opt/venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

COPY . .

ENV PATH="/opt/venv/bin:$PATH"

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "wsgi:app"]