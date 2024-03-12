#!/bin/bash

set -o errexit
set -o nounset

poetry run celery -A src.worker flower --port=${FLOWER_PORT}
command: tail -f /dev/null