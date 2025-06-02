.PHONY: build
build:
	docker build \
		-t stac_check .

run_docker = docker run -it --rm \
		stac_check

.PHONY: shell
shell: 
	$(run_docker) /bin/bash

.PHONY: docs
docs:           ## Build documentation locally
	pip install -e ".[docs]"
	sphinx-build -b html -E docs/ docs/_build/html
	@echo "Documentation built in docs/_build/html"

.PHONY: docker-docs
docker-docs:    ## Build documentation inside Docker container
	docker build -t stac_check .
	docker run --rm -v $(PWD)/docs/_build:/app/docs/_build stac_check sphinx-build -b html -E docs/ docs/_build/html
	@echo "Documentation built in docs/_build/html"
	@echo "Docker documentation build complete."