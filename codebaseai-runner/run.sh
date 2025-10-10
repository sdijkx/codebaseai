#!/bin/bash

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
echo "Script directory: $SCRIPT_DIR"
export CODEBASEAI_DIR=$(realpath ..)
export PROJECT_DIR=$SCRIPT_DIR/example_projects/hello-world-python
export JAVA_PROJECT_DIR=$SCRIPT_DIR/example_projects/hello-world-java
export UID=$(id -u)
export GID=$(id -g)

echo "CODEBASEAI_DIR: $CODEBASEAI_DIR"
echo "PROJECT_DIR: $PROJECT_DIR"
echo "JAVA_PROJECT_DIR: $JAVA_PROJECT_DIR"


cd docker
docker-compose build
# docker-compose exec python-app bash
docker-compose run python-app bash
