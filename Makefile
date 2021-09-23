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
test: build
	docker-compose run email_blaster test

# Install requirements (locally)
install-requirements:
	pip install -r requirements/requirements.txt
	pip install -r requirements/test_requirements.txt

# Build container locally
build:
	# Setup volumes
	mkdir -p ~/MailBlaster-config
	sudo chown -R 1000:1000 ~/MailBlaster-config
	sudo chmod 755 -R ~/MailBlaster-config
	# Build
	docker-compose build --build-arg GIT_COMMIT=$(shell git describe --abbrev=2 --always --tags --dirty) --build-arg DEBUG=True

# Delete container
docker-rm: stop
	docker-compose rm -f

# Get container shell
shell:
	docker-compose run --entrypoint "/bin/bash" email_blaster

# Run command in container
run: build
	docker-compose run email_blaster $(COMMAND)

# Stop container
stop:
	docker-compose down
	docker-compose stop

# "production"
prod:
	mkdir -p ~/MailBlaster-config
	sudo chown -R 1000:1000 ~/MailBlaster-config
	sudo chmod 755 -R ~/MailBlaster-config
	docker-compose -f docker-compose-prod.yml up -d
