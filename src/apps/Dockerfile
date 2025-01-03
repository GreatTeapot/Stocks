FROM python:3.12-alpine AS builder

# Setting environment variables
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    # python
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_ROOT_USER_ACTION=ignore

# Installing system packages for dependencies compilation
#RUN apk add --no-cache \
#    gcc \
#    musl-dev \
#    libffi-dev \
#   openssl-dev \
#    postgresql-dev \
#    build-base

# Setting the working directory
WORKDIR /app
# Copying the dependency file
COPY requirements.txt .
# Installing dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copying the application code
COPY . .
# Command to start the server with Uvicorn
ENTRYPOINT ["/bin/sh", "-c", "alembic upgrade head && python main.py"]
