RUN = docker-compose run django

.PHONY: bash
bash::
		docker-compose exec django bash

.PHONY: up
up::
		docker-compose up --build

.PHONY: down
down::
		docker-compose down

.PHONY: init
init::
		cp -n .env.sample .env