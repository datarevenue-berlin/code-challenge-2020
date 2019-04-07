#!/usr/bin/env bash
set -e
docker-compose build
docker-compose up \
    --scale dask-worker=4 \
    --abort-on-container-exit \
    --exit-code-from worker