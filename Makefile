.PHONY: help requirements
SHELL := /bin/bash

DJANGO_CMD = python personal_api/manage.py

SETTINGS = personal_api.settings

help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

clean:  ## Clean python bytecodes, cache...
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@find . -name ".cache" -type d | xargs rm -rf
	@find . -name ".coverage" -type f | xargs rm -rf

env-file:  ## Generate the .env file for local development
	@cp -farv contrib/localenv .env
	@echo 'Please configure params from .env file before starting. Ask for one from your peers (may be easier ;)'

migrations:  ## Create migrations
	$(DJANGO_CMD) makemigrations core

migrate: ## Execute the migrations
	$(DJANGO_CMD) migrate

requirements:  ## Install the app requirements
	@pip install --upgrade pip
	@pip install -r requirements.txt

createsuperuser:  ## Create the django admin superuser
	$(DJANGO_CMD) createsuperuser

create-admin-superuser-without-input:  ## Create a django admin superuser non-interactively. E.g.: make create-admin-superuser-without-input username=admin1 password=12345678 email=admin1@gmail.com
	$(DJANGO_CMD) create_admin_superuser_without_input --username $(username) --password $(password) --noinput --email '$(email)'

test: clean  ## Run the test suite
	py.test personal_api/ --ds=$(SETTINGS) -s

test-matching: clean  ## Run only tests matching pattern. e.g. make test-matching test=test_healthcheck_liveness
	py.test personal_api/ -k $(test) --ds=$(SETTINGS) -s

coverage: clean  ## Run the test coverage report
	@mkdir -p logs
	py.test --cov-config .coveragerc --cov personal_api personal_api --ds=$(SETTINGS) --cov-report term-missing

lint: clean  ## Run the pylint test
	@pylint --rcfile=.pylintrc  personal_api/*

style:	## Run isort and black auto formatting code style in the project
	@isort -m 3 -tc -y
	@black -S -l 79 personal_api/.

style-check:	## Run black check code style
	@black -S -t py37 -l 79 --check personal_api/.

shell: clean  ## Run a django shell
	$(DJANGO_CMD) shell_plus

runserver: clean migrate  ## Run production (gunicorn) web server
	@cd personal_api && gunicorn --worker-tmp-dir /dev/shm --log-level INFO --workers=1 --threads=2 --worker-class=gthread --bind 0.0.0.0:8000 personal_api.wsgi:application

runserver-dev: clean migrate  ## Run development web server
	set -a && source .env && set +a && $(DJANGO_CMD) runserver 0.0.0.0:8000

runworker: clean migrate  ## Run production celery worker
	@cd personal_api && celery -A personal_api worker --loglevel=$$CELERY_LOG_LEVEL --pool=solo --concurrency=1 --autoscale=1,1 --max-tasks-per-child=10000 --without-heartbeat --without-gossip --without-mingle --queues=$$WORKER_QUEUES

runworker-dev: clean migrate  ## Run development celery worker
	@set -a && source .env && set +a && cd personal_api && celery -A personal_api worker --loglevel=$$CELERY_LOG_LEVEL --pool=solo --concurrency=1 --autoscale=1,1 --max-tasks-per-child=10000 --without-heartbeat --without-gossip --without-mingle --queues=$$WORKER_QUEUES

container-build: clean  ## create the docker image
	@./build-container.sh

container-upload:  ## upload the docker image to its docker registry
	@echo 'TODO'

container-run: env-file  ## run the app docker container through docker-compose
	@docker-compose up -d

container-clean: ## stop and delete the app docker container through docker-compose
	@docker-compose stop && docker-compose rm -f
