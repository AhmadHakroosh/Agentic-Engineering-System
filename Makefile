.PHONY: format-check lint typecheck test-unit test-integration build security-scan clean

format-check:
	python3 scripts/validate_contracts.py

lint:
	python3 scripts/check_delivery_config.py

typecheck:
	@echo "No application type checker configured yet."

test-unit:
	python3 -m unittest discover -s tests -p 'test_*.py'

test-integration:
	@echo "No application integration tests configured yet."

build:
	mkdir -p dist
	printf '%s\n' '{"starter":"agentic-software-delivery","version":1}' > dist/manifest.json

security-scan:
	@echo "Configure the repository-approved SAST and dependency scanners here."

clean:
	rm -rf dist

