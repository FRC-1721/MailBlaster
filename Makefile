.PHONY: help clean clean-pyc clean-build list test coverage release

# Help
help:
	@echo "  clean-build -          Remove build artifacts"
	@echo "  clean-pyc -            Remove Python file artifacts"
	@echo "  lint -                 Check style with flake8"
	@echo "  test -                 Run tests quickly with the default Python"
	@echo "  install-requirements - install the requirements for development"
	@echo "  build                  Builds the docker images for the docker-compose setup"
	@echo "  docker-rm              Stops and removes all docker containers"
	@echo "  run                    Run a command. Can run scripts, e.g. make run COMMAND=\"./scripts/schema_generator.sh\""
	@echo "  shell                  Opens a Bash shell"
	@echo "  prod					Is meant for running on the production env"

# Clean everything
clean: clean-build clean-pyc docker-rm

# Clean build data
clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

# Clean python cache
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

# Delint the code
lint:
	flake8 .

# Run the tests
test:
	docker-compose run email_blaster test

# Install requirements (locally)
install-requirements:
	pip install -r requirements/requirements.txt
	pip install -r requirements/test_requirements.txt

# Build container (similar to prod)
build:
	docker-compose build

# Delete container
docker-rm: stop
	docker-compose rm -f

# Get container shell
shell:
	docker-compose run --entrypoint "/bin/bash" email_blaster

# Run command in container
run:
	docker-compose run -e GCLOUD_SERVICE_KEY email_blaster $(COMMAND)

# Stop container
stop:
	docker-compose down
	docker-compose stop

# "production"
prod:
	docker-compose build --build-arg GIT_COMMIT=$(shell git rev-parse HEAD)
