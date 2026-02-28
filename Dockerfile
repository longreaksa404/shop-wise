# 1. Use an official Python runtime (slim version keeps the image small)
FROM python:3.11-slim

# 2. Set environment variables to prevent Python from writing .pyc files
# and to ensure output is sent straight to terminal (useful for logs)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Install system dependencies for PostgreSQL (psycopg2 needs these)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# 5. Install Python dependencies
# Make sure you have a requirements.txt file in your root folder!
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 6. Copy the rest of your project code into the container
COPY . /app/

# 7. Expose the port Django runs on
EXPOSE 8000

# 8. Command to run the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]