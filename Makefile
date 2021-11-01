.PHONY: help
help: ## Print this help message and exit
	@echo Usage:
	@echo "  make [target]"
	@echo
	@echo Targets:
	@awk -F ':|##' \
		'/^[^\t].+?:.*?##/ {\
			printf "  %-30s %s\n", $$1, $$NF \
		 }' $(MAKEFILE_LIST)

.PHONY: coverage
coverage: ## run code coverage report on module via unittest
	@./scripts/coverage.sh ${case}

.PHONY: unit
unit: ## execute monitor unittest suite, for single case make unit case=<NAME>
	@./scripts/unittest.sh ${case}

.PHONY: lint
lint: ## lint codebase using a combination of yamllint, shellcheck and flake8
	@./scripts/lint.sh

.PHONY: dev 
dev: config ## Run development environment
	@./scripts/dev.sh

.PHONY: clean
clean: ## Clean docker environment
	@./scripts/clean.sh

.PHONY: config
config: ## Run docker compose config validation
	@./scripts/config.sh

.PHONY: pull
pull: ## pull service containers
	@docker compose -f docker/docker-compose.yaml pull