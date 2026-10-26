FROM python:3.12-slim

WORKDIR /app

# Install uv
RUN pip install uv

# 1. Copy ONLY the pyproject.toml
COPY pyproject.toml .

# 2. Compile pyproject.toml into requirements.txt and install ONLY dependencies
RUN uv pip compile pyproject.toml -o requirements.txt && \
    uv pip install --system -r requirements.txt

# 3. NOW copy the rest of your source code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]