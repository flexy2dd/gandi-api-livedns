ARGS = `arg="$(filter-out $@,$(MAKECMDGOALS))" && echo $${arg:-${1}}`

.DEFAULT_GOAL := build

build:
	@echo "Building"
	python3 -m build
.PHONY: build

upload:
	@echo "Upload to PyPI"
	python3 -m twine upload dist/*
.PHONY: upload
	
build-up: build upload
