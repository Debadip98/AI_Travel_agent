.PHONY: build

build:
	python -m json.tool meeting_output.json > /dev/null
