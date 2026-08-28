FROM python:3.11-slim

WORKDIR /app

# System deps for bcrypt/cryptography wheels on slim images.
RUN apt-get update && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# MONGO_URL, DB_NAME, JWT_SECRET, ANTHROPIC_API_KEY are required at runtime —
# set them via your host's environment/secrets UI, never baked into the image.
ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn server:app --host 0.0.0.0 --port ${PORT}"]
