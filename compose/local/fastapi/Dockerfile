FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Configure Poetry
ENV POETRY_VERSION=1.7.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  && apt-get install -y libpq-dev

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV
RUN $POETRY_VENV/bin/pip install -U pip setuptools
RUN $POETRY_VENV/bin/pip install -U pip setuptools
RUN $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Requirements are installed here to ensure they will be cached.


COPY ./compose/local/fastapi/entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh

COPY ./compose/local/fastapi/start.sh /start.sh
RUN chmod a+x /start.sh

COPY ./compose/local/fastapi/celery/worker/start.sh /start-celeryworker.sh
RUN chmod a+x /start-celeryworker.sh

COPY ./compose/local/fastapi/celery/beat/start.sh /start-celerybeat.sh
RUN chmod a+x /start-celerybeat.sh

COPY ./compose/local/fastapi/celery/flower/start.sh /start-flower.sh
RUN chmod a+x /start-flower.sh


# Install dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry install


WORKDIR /app
#RUN chown USER nobody:nogroup -R /app

ENTRYPOINT ["/entrypoint.sh"]