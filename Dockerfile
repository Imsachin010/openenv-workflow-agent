FROM public.ecr.aws/docker/library/python:3.10-slim

WORKDIR /app

# Prevent interactive issues
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Install system deps (safe minimal)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (cache optimization)
COPY requirements.txt .

# Install python deps
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy rest of code
COPY . .

# Expose port
EXPOSE 7860

# Start server
CMD ["uvicorn", "app_server:app", "--host", "0.0.0.0", "--port", "7860"]