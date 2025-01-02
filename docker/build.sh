#!/bin/bash

set -e

source .env

echo "-> build vector db"
python3 app/vector_db/build.py

export DOCKER_IMAGE_NAME="${AWS_DOCKER_REGISTRY_URL}/lead-gen-bot-yt:latest"

echo "-> Logging into AWS ECR"
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_DOCKER_REGISTRY_URL}

echo "-> Building Docker image: ${DOCKER_IMAGE_NAME}"
docker build -t "${DOCKER_IMAGE_NAME}" --platform linux/amd64 -f docker/Dockerfile .

echo "-> Build completed successfully ✅"