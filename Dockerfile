FROM python:3.10-slim

WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install extra needed libs
RUN pip install pyyaml

# Set environment
ENV PYTHONPATH=/app

# Default command
CMD ["uvicorn", "app_server:app", "--host", "0.0.0.0", "--port", "7860"]