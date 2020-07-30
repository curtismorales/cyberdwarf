install:
	pipenv install
	pipenv shell

fmt:
	isort .
	autoflake --recursive --in-place --remove-all-unused-imports --remove-unused-variables .
	black .

test:
	mypy .
