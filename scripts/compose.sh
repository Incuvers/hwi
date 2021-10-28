#!/bin/bash

source .env

# handle all non-zero exit status codes with a slack notification
trap 'handler $? $LINENO' ERR

handler () {
    printf "%b" "${FAIL} ✗ ${NC} ${0##*/} failed on line $2 with exit status $1\n"
}

echo "$CR_PAT" | docker login ghcr.io -u "$USERNAME" --password-stdin

printf "%b" "${OKB}Building project${NC}\n"
docker compose -f "$DOCKER_ROOT"/docker-compose.yaml up
printf "%b" "${OKG} ✓ ${NC}containers active\n"