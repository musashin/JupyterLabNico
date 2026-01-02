#!/bin/bash
DOCKERPATH="docker"

# forbiden character : "_", "-", " ", and uppercase
NAME="dockerjupyter"
VERSION='1.1'

# continue docker image existance check
DOCKERFILE=$DOCKERPATH//"Dockerfile"

docker build --no-cache -t ${NAME}:${VERSION} -f ${DOCKERFILE} .

