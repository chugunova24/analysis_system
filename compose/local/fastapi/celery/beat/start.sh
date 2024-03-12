#!/bin/bash

set -o errexit

rm -f './celerybeat.pid'
poetry run celery -A src.worker beat -l info