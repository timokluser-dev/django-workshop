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
		npm install hostile -g
		sudo hostile set 127.0.0.1 django.what-ever.lo
		cp -n .env.sample .env