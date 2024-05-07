# Stage 1: Build
# FROM python:3.11-slim-buster AS builder

# WORKDIR /app

# ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
#     PYTHONUNBUFFERED=1 \
#     PYTHONDONTWRITEBYTECODE=1

# COPY requirements.txt .

# RUN pip install --user -r requirements.txt

# # Stage 2: Runtime
# FROM python:3.11-slim-buster

# WORKDIR /app

# # Install Tesseract in the final stage
# RUN apt-get update && apt-get install -y \
#     tesseract-ocr \
#     libtesseract-dev \
#     && rm -rf /var/lib/apt/lists/*


# COPY --from=builder /root/.local /root/.local
# COPY . .

# # Make sure scripts in .local are usable:
# ENV PATH=/root/.local/bin:$PATH

# CMD gunicorn --bind 0.0.0.0:80 ticket_management.wsgi


# An updated code suggested to reduce image size
# # Stage 1: Build
# FROM python:3.11-slim-buster AS builder

# WORKDIR /app

# ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
#     PYTHONUNBUFFERED=1 \
#     PYTHONDONTWRITEBYTECODE=1

# # Install build dependencies
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends \
#         build-essential \
#         libtesseract-dev \
#         && rm -rf /var/lib/apt/lists/*

# COPY requirements.txt .

# # Install Python dependencies
# RUN pip install --user -r requirements.txt

# # Stage 2: Runtime
# FROM python:3.11-slim-buster

# WORKDIR /app

# # Copy Python dependencies from the builder stage
# COPY --from=builder /root/.local /root/.local

# # Install Tesseract OCR runtime dependencies
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends \
#         tesseract-ocr \
#         && rm -rf /var/lib/apt/lists/*

# # Copy the rest of the application code
# COPY . .

# # Make sure scripts in .local are usable:
# ENV PATH=/root/.local/bin:$PATH

# CMD ["gunicorn", "--bind", "0.0.0.0:80", "ticket_management.wsgi"]

# Multisage build of above suggestion


# Stage 1: Build
# FROM python:3.11-slim-buster AS builder

# WORKDIR /app

# ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
#     PYTHONUNBUFFERED=1 \
#     PYTHONDONTWRITEBYTECODE=1

# # Install build dependencies
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends \
#         build-essential \
#         libtesseract-dev \
#         && rm -rf /var/lib/apt/lists/*

# COPY requirements.txt .

# # Install Python dependencies
# RUN pip install --user  -r requirements.txt

# # Stage 2: Runtime
# FROM python:3.11-slim-buster

# WORKDIR /app


# # Install Tesseract OCR and English language data files
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends \
#         tesseract-ocr \
#     && rm -rf /var/lib/apt/lists/*

# # Copy Python dependencies from the builder stage
# COPY --from=builder /root/.local /root/.local

# # Copy the rest of the application code
# COPY . .

# # Make sure scripts in .local are usable:
# ENV PATH=/root/.local/bin:$PATH

# CMD ["gunicorn", "--bind", "0.0.0.0:80", "ticket_management.wsgi"]


# Now with alpine instead of slim buster


# Stage 1: Build
# FROM python:3.11-alpine AS builder

# WORKDIR /app

# ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
#     PYTHONUNBUFFERED=1 \
#     PYTHONDONTWRITEBYTECODE=1

# # Install build dependencies
# RUN apk update && \
#     apk add --no-cache \
#         gcc \
#         musl-dev \
#         linux-headers \
#         python3-dev \
#     && rm -rf /var/cache/apk/*
# COPY requirements.txt .

# # Install Python dependencies
# RUN pip install --user -r requirements.txt

# # Stage 2: Runtime
# FROM python:3.11-alpine

# WORKDIR /app

# # Install Tesseract OCR runtime dependencies
# RUN apk update && \
#     apk add --no-cache \
#         tesseract-ocr \
#     && rm -rf /var/cache/apk/*

# # Copy Python dependencies from the builder stage
# COPY --from=builder /root/.local /root/.local

# # Copy the rest of the application code
# COPY . .

# # Make sure scripts in .local are usable:
# ENV PATH=/root/.local/bin:$PATH

# CMD ["gunicorn", "--bind", "0.0.0.0:80", "ticket_management.wsgi"]


# syntax=docker/dockerfile:1.0.0-experimental

# Stage 1: Build
FROM python:3.11-slim-buster AS builder

WORKDIR /app

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libtesseract-dev \
        tesseract-ocr-eng \ 
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt separately to leverage caching
COPY requirements.txt .

# Install Python dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim-buster

WORKDIR /app

# Install Tesseract OCR and English language data files
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from the builder stage
COPY --from=builder /root/.local /root/.local

# Copy the rest of the application code
COPY . .

# Make sure scripts in .local are usable:
ENV PATH=/root/.local/bin:$PATH

# Remove package cache files and other build artifacts
RUN apt-get clean && \
    rm -rf /var/cache/apt/* /var/cache/debconf/*-old /var/lib/apt/lists/* /tmp/* /var/tmp/*

CMD ["gunicorn", "--bind", "0.0.0.0:80", "ticket_management.wsgi"]
