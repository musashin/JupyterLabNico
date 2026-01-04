#!/bin/bash
DOCKERPATH="docker"

# forbiden character : "_", "-", " ", and uppercase
NAME="jupyter"
# continue docker image existance check
DOCKERFILE=$DOCKERPATH//"Dockerfile"

docker build --no-cache -t ${NAME} -f ${DOCKERFILE} .

