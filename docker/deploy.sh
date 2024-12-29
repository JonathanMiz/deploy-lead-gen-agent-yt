#! /usr/bin/env bash

set -e

start_time=$(date +%s)

source docker/build.sh

docker push "${DOCKER_IMAGE_NAME}"

export SERVICE_NAME="lead-gen-bot-yt"
sls deploy --region ${AWS_REGION}

end_time=$(date +%s)
runtime=$((end_time - start_time))
echo "Deployment completed successfully ✅"
echo "Total deployment time: ${runtime} seconds"