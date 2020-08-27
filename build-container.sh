#!/bin/bash
APP_NAME=personal-api
APP_VERSION=$(cat VERSION)
UID=$(id -u)
GID=$(id -g)
echo "Building image for APP_NAME=$APP_NAME, VERSION=$APP_VERSION, UID=$UID, GID=$GID..."

docker build -t $APP_NAME --pull --no-cache --build-arg UID=$UID --build-arg GID=$GID .


IMAGE_ID=$(docker images --filter reference=$APP_NAME --format "{{.ID}}")


echo "Tagging image to prepare to push..."
docker tag $IMAGE_ID "${APP_NAME}:${APP_VERSION}"
docker tag $IMAGE_ID "${APP_NAME}:latest"
echo "FINISHED! :)"
