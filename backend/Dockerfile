# Use lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Pre-install system dependencies
RUN apt-get update && apt-get install -y \
    gcc g++ libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Now copy the rest of the code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI backend
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

