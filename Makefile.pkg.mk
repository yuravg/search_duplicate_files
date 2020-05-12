MAKE = make --no-print-directory
DIR  = $(shell basename `pwd`)

project ?= ""

.PHONY: help
help:
	@echo ""
	@echo "Usage:  make [target(s)]"
	@echo "where target is any of:"
	@echo ""
	@echo "  build      - build packge"
	@echo "  install    - install package"
	@echo "  uninstall  - uninstall package"
	@echo "  all        - run target build, install"
	@echo "  rall       - run targets uninstall, all"
	@echo "  clean      - clean derived files(egg-info, ditr, etc.)"
	@echo "  completion - write bash completion file"
	@echo ""

.PHONY: clean build install all uninstall completion rall
clean:
	rm -rf *.egg-info || true
	rm -rf ./dist/ || true

build:
	$(MAKE) clean
	python setup.py bdist_wheel

last_pkg_name =$(lastword $(sort $(wildcard dist/*)))
install:
	@echo "+-------------------------------------------------------------------------+"
	@echo "| Installation package: $(last_pkg_name)"
	@echo "+-------------------------------------------------------------------------+"
	pip install $(last_pkg_name)

all:
	$(MAKE) build
	$(MAKE) install

uninstall:
	pip uninstall --yes $(project) || true

completion:
	sduplicate completion

rall:
	$(MAKE) uninstall
	$(MAKE) all
