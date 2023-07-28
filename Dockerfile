# Use slim-buster base image for Python
FROM python:3.9-slim-buster

# Install PostgreSQL client for psycopg2 (required for testing)
RUN apt-get update \
    && apt-get install -y libpq-dev gcc

# Set the working directory inside the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app files into the container
COPY app /app

# Set the command to run the FastAPI server with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]