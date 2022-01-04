.PHONY: build
build:
	docker build \
		-t stac_check .

.PHONY: run
run:
	docker run \
		stac_check

.PHONY: shell
shell:
	$(run_docker) /bin/bash
