.PHONY: build
build:
	docker build \
		-t stac_check .

run_docker = docker run -it --rm \
		stac_check

.PHONY: shell
shell: 
	$(run_docker) /bin/bash
