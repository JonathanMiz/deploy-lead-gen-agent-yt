#!/bin/bash

set -e

source docker/build.sh

source .env

docker run --rm -p ${PORT}:${PORT} \
    --entrypoint python \
    --env-file .env \
    ${DOCKER_IMAGE_NAME} app/api.py