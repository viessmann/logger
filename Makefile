
include qualiter.makefile

VERSION := $(shell python setup.py --version)

.PHONY: install
install:  ## install all dependencies
	pip install -r requirements.txt && \
	pip install -r test-requirements.txt && \
	qualiter init logger

.PHONY: release
release:  ## push tag associated with current version
	git fetch
	git tag ${VERSION}
	git push origin --tags
