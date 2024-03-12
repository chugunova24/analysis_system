 
compose:
	docker-compose up

flake8:
	flake8  # запускайте из директории ./services/backend

alembic-revision:
	poetry run alembic revision --autogenerate # введите сообщение: -m "Example"

alembic-upgrade:
	poetry run alembic upgrade # введите id ревизии: "fb16c061d81c"

alembic-downgrade:
	alembic downgrade -1

install-dep:
	poetry install

allure:
	allure serve ./testing/allureress

pytest-allure:
	poetry run python -m pytest -s -v --alluredir=./testing/allureress

pytest:
	poetry run python -m pytest -s -v

start-celery:
	poetry run celery -A src.worker worker --loglevel=DEBUG

start-celery-beat:
	poetry run celery -A src.worker beat

start-flower:
	poetry run celery -A src.worker flower --port=5555

start-server:
	poetry run uvicorn src.main:app --reload

