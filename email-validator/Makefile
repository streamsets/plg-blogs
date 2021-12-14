FONT_ESC := $(shell printf '\033')
FONT_BOLD := ${FONT_ESC}[1m
FONT_NC := ${FONT_ESC}[0m #No color

all:
	@echo "Use a specific goal. To list all goals, type 'make help'"

.PHONY: version # Prints project version
version:
	@cat VERSION

.PHONY: build # Builds for current OS binary
build:
	@mvn clean compile package

.PHONY: install # installs the project
install:
	@mvn clean install

.PHONY: put # Put jar file into Snowflake
put:
	@snowsql -a $(account) -w $(warehouse) -d $(database) -s $(schema) -u $(user) -f put_command.sql

# .PHONY: test # Runs unit tests
# test:
# 	@go test -v ./...

.PHONY: help # Generates list of goals with description
help:
	@echo "Available goals:\n"
	@grep '^.PHONY: .* #' Makefile | sed "s/\.PHONY"