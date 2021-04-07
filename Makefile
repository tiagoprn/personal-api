.PHONY: help requirements

SHELL := /bin/bash
PROJECT_ROOT=$(shell pwd)
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
	@cp -farv vars/localenv .env
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

create-test-admin-superuser:  ## Create a test django admin superuser, named admin1
	@$(DJANGO_CMD) create_admin_superuser_without_input --username admin1 --password 12345678 --noinput --email 'admin1@gmail.com' || true

test: clean  ## Run the test suite
	py.test personal_api/ --ds=$(SETTINGS) -s -vvv

test-matching: clean  ## Run only tests matching pattern. e.g. make test-matching test=test_healthcheck_liveness
	py.test personal_api/ -k $(test) --ds=$(SETTINGS) -s -vvv

coverage: clean  ## Run the test coverage report
	@mkdir -p logs
	py.test --cov-config .coveragerc --cov personal_api personal_api --ds=$(SETTINGS) --cov-report term-missing

lint: clean  ## Run the pylint test
	@pylint --rcfile=.pylintrc  personal_api/*

style:	## Run isort and black auto formatting code style in the project
	@isort -m 3 --trailing-comma --use-parentheses --honor-noqa .
	@black -S -l 79 personal_api/.

style-check:	## Run black check code style
	@isort -v --check -m 3 --trailing-comma --use-parentheses --honor-noqa --color .
	@echo '-----'
	@echo 'black' | figlet
	@black -S -t py37 -l 79 --check personal_api/.

shell: clean  ## Run a django shell
	$(DJANGO_CMD) shell_plus

runserver: clean migrate  ## Run production (gunicorn) web server
	@cd personal_api && gunicorn --worker-tmp-dir /dev/shm --log-level INFO --workers=1 --threads=2 --worker-class=gthread --bind 0.0.0.0:8000 personal_api.wsgi:application

runserver-dev: clean runstatic-dev migrate   ## Run development web server
	set -a && source .env && set +a && $(DJANGO_CMD) runserver 0.0.0.0:8000

runworker: clean migrate  ## Run production celery worker
	@cd personal_api && celery -A personal_api worker --loglevel=$$CELERY_LOG_LEVEL --pool=solo --concurrency=1 --autoscale=1,1 --max-tasks-per-child=10000 --without-heartbeat --without-gossip --without-mingle --queues=$$WORKER_QUEUES

runworker-dev: clean migrate  ## Run development celery worker
	@set -a && source .env && set +a && cd personal_api && celery -A personal_api worker --loglevel=$$CELERY_LOG_LEVEL --pool=solo --concurrency=1 --autoscale=1,1 --max-tasks-per-child=10000 --without-heartbeat --without-gossip --without-mingle --queues=$$WORKER_QUEUES

static: clean  ## Create frontend (Django Admin, Swagger, etc...) static files
	@rm -fr static || true && mkdir static && $(DJANGO_CMD) collectstatic

runstatic-dev: clean static  ## Run local server to serve frontend (Django Admin, Swagger, etc...) static files
	@docker-compose up -d nginx

container-build: clean  ## create the docker image
	@./build-container.sh

container-upload:  ## upload the docker image to its docker registry
	@echo 'TODO'

container-run: env-file  ## run the app docker container through docker-compose
	@docker-compose up -d

container-clean: ## stop and delete the app docker container through docker-compose
	@docker-compose stop && docker-compose rm -f

show-urls: clean  ## Show all urls available on the app
	$(DJANGO_CMD) show_urls

local-healthcheck-readiness:  ## Run curl to make sure the app/worker/scheduler is ready
	@curl http://localhost:8000/health-check/readiness -L -s | jq

local-healthcheck-liveness:  ## Run curl to make sure the app/worker/scheduler is live
	@curl http://localhost:8000/health-check/liveness -L -s | jq

local-get-access-token:  ## Get the token for the endpoints that require authentication. E.g.: make local-get-access-token username=tiago password=12345678
	@curl -s -X POST http://localhost:8000/api/token/ -d "username=$(username)" -d "password=$(password)" | jq

local-refresh-access-token:  ## Refresh the authentication token for the endpoints that require authentication, generating a new one. E.g.: make local-refresh-access-token refresh_token=XXXXXX
	@curl -s -X POST http://localhost:8000/api/token/refresh/ -d "refresh=$(refresh_token)" | jq

local-test-user-token:  ## Use greetings' protected endpoint to test the authentication token. E.g.: make local-test-user-token token=XXXXXX
	@curl http://localhost:8000/core/greetings/ -H "Authorization: Bearer $(token)"

local-links-csv-import-test: create-test-admin-superuser  ## Imports the sample csv into the local database
	@$(DJANGO_CMD) import_links_from_csv --username=admin1 --csv-file-path=$(PROJECT_ROOT)/personal_api/core/tests/assets/links.csv

local-test-get-links:  ## Get all links. E.g.: make local-test-get-links token=XXXXXX
	@curl http://localhost:8000/core/api/links -H "Content-Type: application/json;charset=utf-8" -H "Authorization: Bearer $(token)" -L -s | jq

