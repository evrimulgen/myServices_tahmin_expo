#!/usr/bin/env bash

# This script starts the development environment using Docker
# Launch as: source tools/dev.sh from the project's root

DOCKER_COMPOSE_FILE="./docker-compose.yml"

docker-compose -f ${DOCKER_COMPOSE_FILE} stop
docker-compose -f ${DOCKER_COMPOSE_FILE} rm --force

docker-compose -f ${DOCKER_COMPOSE_FILE} build

docker-compose -f ${DOCKER_COMPOSE_FILE} up -d --remove-orphans

docker-compose -f ${DOCKER_COMPOSE_FILE} exec web_app bash
