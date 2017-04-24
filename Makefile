test:
	nosetests --cover-package=pydor --with-coverage

package:
	python setup.py sdist
	python setup.py bdist_wheel

.PHONY: test
