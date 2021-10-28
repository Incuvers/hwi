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

.PHONY: compose 
compose: config ## Run development environment
	@./scripts/compose.sh

.PHONY: clean
clean: ## Clean docker environment
	@./scripts/clean.sh

.PHONY: config
config: ## Run docker compose config validation
	@./scripts/config.sh

.PHONY: pull
pull: ## pull service containers
	@docker compose -f docker/docker-compose.yaml pull