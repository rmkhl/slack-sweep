PKG_REVISION = $(shell git log --oneline --merges --since `date +'%Y-%m-01T00:00:00Z'` | wc -l)

PYTHON_SOURCE = setup.py $(MODULE)

pylint_HELP = Run pylinter against majority of the source tree
lint pylint: devenv
	$(VPYTHON) -m pylint $(PYTHON_SOURCE) tests
.PHONY: lint pylint

pycodestyle_HELP = Run pycodestyle against majority of the source tree
codestyle pycodestyle: devenv
	$(VPYTHON) -m pycodestyle
.PHONY: codestyle pycodestyle

wheel_HELP = Build the wheel
package wheel: devenv
	rm -rf dist build
	PKG_REVISION=$(PKG_REVISION) $(VPYTHON) setup.py sdist bdist_wheel
.PHONY: wheel package
