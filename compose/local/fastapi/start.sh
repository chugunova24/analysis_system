#!/bin/bash

set -o errexit

echo $PWD
poetry run alembic upgrade head
poetry run uvicorn src.main:app --reload --host ${FASTAPI_HOST} --port ${FASTAPI_PORT}