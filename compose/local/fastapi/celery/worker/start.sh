#!/bin/bash

set -o errexit


poetry run celery -A src.worker worker --loglevel=DEBUG