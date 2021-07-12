SHELL:=/bin/bash

RED=\033[0;31m
GREEN=\033[0;32m
NC=\033[0m

NETWORK?=load_testing
export NETWORK_NAME=$(NETWORK)

COMPOSE_FILE=docker/docker-compose.yml
PROD_FILE=docker/docker-compose-prod.yml
DEV_FILE=docker/docker-compose-dev.yml

# Check for NETWORK_NAME network and create it
NETWORKS=$(shell docker network ls --filter name=^${NETWORK_NAME} --format="{{ .Name }}")
PROD_COMPOSE_CMD=docker-compose -f $(CURDIR)/$(COMPOSE_FILE) -f $(CURDIR)/$(PROD_FILE)
DEV_COMPOSE_CMD=docker-compose -f $(CURDIR)/$(COMPOSE_FILE) -f $(CURDIR)/$(DEV_FILE)

create_network:
	@if [ -z $(NETWORKS) ]; then \
		printf "${GREEN}Creating network '$(NETWORK_NAME)'${NC}"; \
		docker network create $(NETWORK_NAME); \
	fi;

build:
	$(PROD_COMPOSE_CMD) build

stop:
	$(PROD_COMPOSE_CMD) down

run:
	$(PROD_COMPOSE_CMD) up -d

build_dev: create_network
	$(DEV_COMPOSE_CMD) build

run_dev:
	$(DEV_COMPOSE_CMD) up -d

#run_locust:
#	locust -f src/locust_files/load_test.py

create_topics:
	docker-compose -f $(COMPOSE_FILE) exec message-broker \
		bash -c " \
		cub kafka-ready -b message-broker:9092 1 60 && \
		kafka-topics --zookeeper zookeeper-dv:2182 --if-exists --delete --topic read.events && \
		kafka-topics --zookeeper zookeeper-dv:2182 --if-exists --delete --topic write.events && \
		kafka-topics --zookeeper zookeeper-dv:2182 --create --replication-factor 1 --partitions 1 --if-not-exists --topic read.events && \
		kafka-topics --zookeeper zookeeper-dv:2182 --create --replication-factor 1 --partitions 1 --if-not-exists --topic write.events"

start_project:
	@printf '${GREEN} Installing and creating virtualenv... ${NC}\n';
	@python3 -m venv .venv

	@printf '${GREEN} Installing project dependencies... ${NC}\n';
	@source .venv/bin/activate && pip3 install -r requirements/requirements.txt;
	@source .venv/bin/activate && pip3 install -r requirements/test_requirements.txt;
	@printf '${GREEN} Configuring pre-commit hooks... ${NC}\n';
	source .venv/bin/activate && pre-commit install
	source .venv/bin/activate && pre-commit install --install-hooks

