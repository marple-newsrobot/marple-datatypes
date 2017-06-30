
.PHONY: clean-pyc clean-build


tests: clean-pyc
	PYTHONPATH=. py.test tests --verbose

test: clean-pyc
	PYTHONPATH=. py.test $(file) --verbose

deploy:
	git push origin master

serve:
	export FLASK_APP=api/app.py; export FLASK_DEBUG=1; export PYTHONPATH=.; flask run
