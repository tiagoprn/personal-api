SHELL := /bin/bash  # necessary to use the source command, which is not on sh, Makefile's default shell ;)
help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

bash:  ## Run a bash session
	docker exec -it $$(docker ps | grep postgres-personal_api | awk '{print $$1}') bash

psql:  ## Enter the docker container on psql."
	set -a && source postgres.env && set +a && docker exec -it $$(docker ps | grep postgres-personal_api | awk '{print $$1}') psql -U postgres personal_api

backup:  ## Make a backup of postgresql data.
	set -a && source postgres.env && set +a && docker exec -i $$(docker ps | grep postgres-personal_api | awk '{print $$1}') /utils/dump.sh

restore:  ## Restore to the most recent database backup."
	set -a && source postgres.env && set +a && docker exec -i $$(docker ps | grep postgres-personal_api | awk '{print $$1}') /utils/restore.sh

stop:  ## Stop the container."
	docker-compose stop

remove: stop  ## Remove (delete) the container."
	docker-compose rm -f

start: remove  ## Start the container. If there is another instance of it running, it will be killed and removed first."
	docker-compose up -d
	@echo -e "IMPORTANT: If this is the first time you start this container, run: \n    $ make setupdb"

setupdb: start  ## Setup database credentials and default encoding to be ready for a django app."
	set -a && source postgres.env && set +a && docker exec -i $$(docker ps | grep postgres-personal_api | awk '{print $$1}') /utils/setup.sh
