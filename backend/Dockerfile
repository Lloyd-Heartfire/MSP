# Use Python 3.11 slim better for psycopg2
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Install for PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# copy requirements file
COPY requirements.txt .

# pip and install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# copy all project code
COPY . .

#port 8000
EXPOSE 8000

# start Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]