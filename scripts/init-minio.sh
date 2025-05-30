#!/bin/bash

# MinIO bucket initialization script
# This script creates the required bucket if it doesn't exist

set -e

# MinIO configuration
MINIO_ENDPOINT="${MINIO_ENDPOINT:-minio:9000}"
BUCKET_NAME="${MINIO_BUCKET_NAME:-flashcards-media}"
ACCESS_KEY="${MINIO_ACCESS_KEY:-minioadmin}"
SECRET_KEY="${MINIO_SECRET_KEY:-minioadmin}"

echo "Waiting for MinIO to be ready..."
until curl -sf http://${MINIO_ENDPOINT}/minio/health/live; do
    echo "MinIO is not ready yet, waiting..."
    sleep 2
done

echo "MinIO is ready! Configuring mc client..."

# Configure mc client
mc alias set myminio http://${MINIO_ENDPOINT} ${ACCESS_KEY} ${SECRET_KEY}

# Create bucket if it doesn't exist
if ! mc ls myminio/${BUCKET_NAME} >/dev/null 2>&1; then
    echo "Creating bucket: ${BUCKET_NAME}"
    mc mb myminio/${BUCKET_NAME}
    echo "Setting public read policy for bucket: ${BUCKET_NAME}"
    mc anonymous set public myminio/${BUCKET_NAME}
else
    echo "Bucket ${BUCKET_NAME} already exists"
fi

echo "MinIO setup completed successfully!"