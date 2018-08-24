
include qualiter.makefile

VERSION := $(shell python setup.py --version)

.PHONY: install
install:  ## install all dependencies & build virtual environment
	pip install -r requirements.txt && \
	pip install -r test-requirements.txt && \
	qualiter init logger
