#!/bin/bash

source .env

echo "$CR_PAT" | docker login ghcr.io -u "$USERNAME" --password-stdin
printf "%b" "${OKB}Building project${NC}\n"
docker compose -f docker/dev/docker-compose.yaml up