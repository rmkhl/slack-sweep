# Most likely you are looking into the wrong place, this holds generic
# functions and definitions used to implement overall functionality,
# then again if you are planning on expanding this make  to support
# something new it does not already do then, this is possibly the
# place to go to

# Automatically setup/update the virtualenv
VPYTHON := .venv/bin/python3

.venv/pyvenv.cfg: requirements.txt setup.py
	rm -rf .venv
	$(PYTHON) -m venv .venv
	$(VPYTHON) -m pip install --upgrade pip
	$(VPYTHON) -m pip install -r requirements.txt

virtualenv_HELP = setup/update development virtualenv
devenv virtualenv: .venv/pyvenv.cfg
.PHONY: devenv virtualenv

# minor tricekery to add newline to foreach output
define nl


endef

# The default target and generic help
help:
	@echo Available commands:
	@echo ===================
	$(foreach command, $(_MAKE-COMMANDS), $(if $(command), @echo $(command): "$(if $($(command)_HELP), $($(command)_HELP), no description)"${nl}))
.PHONY: help
