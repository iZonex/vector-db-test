# Use the official Python image as the base
FROM python:3.11-slim

# Set environment variables used in Python:
# - PYTHONUNBUFFERED: do not buffer stdout and stderr
# - PYTHONDONTWRITEBYTECODE: do not write .pyc files
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.7.1

# Install the necessary tools for dependency building
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Set the working directory for the application
WORKDIR /app

# Copy Poetry dependency files
COPY pyproject.toml poetry.lock* /app/

# Install project dependencies using Poetry
# Set the POETRY_VIRTUALENVS_CREATE environment variable to false to avoid creating a virtual environment
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the rest of the project files to the working directory
COPY vector /app
COPY data /app/data
COPY appmap.yml /app

# Expose the port that will be used by FastAPI
EXPOSE 8000

# Command to run the application
CMD ["python", "run.py"]
