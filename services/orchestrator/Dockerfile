FROM python:3.11-slim

WORKDIR /app

# Install system build dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy consolidated orchestrator requirements and install
COPY services/orchestrator/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared modules and services
COPY shared/ /app/shared/
RUN pip install -e /app/shared/

COPY services/ /app/services/
COPY database/ /app/database/
COPY evaluation/ /app/evaluation/

# Set Python path to /app for in-process monolithic imports
ENV PYTHONPATH="/app:/app/services/orchestrator"

EXPOSE 8000

CMD ["uvicorn", "services.orchestrator.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
