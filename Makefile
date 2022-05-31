# https://docs.streamlit.io/library/components/publish
.ONESHELL:

.PHONY: release install run

release:
	cd pydantlit/frontend && npm run build
	python setup.py sdist bdist_wheel

install:
	virtualenv venv
	. venv/bin/activate;
	pip install .
	cd pydantlit/frontend && npm install

run-frontend:
	cd pydantlit/frontend && npm run start

run-dark:
	. venv/bin/activate
	streamlit run pydantlit/__init__.py  --theme.primaryColor E3BF28 --theme.base dark;

run-light:
	. venv/bin/activate
	streamlit run pydantlit/__init__.py --theme.primaryColor E3BF28 --theme.base light;

publish:
	. venv/bin/activate
	python3 -m twine upload --repository testpypi dist/*
