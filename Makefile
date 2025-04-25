# This file simplifies the commands needed to install and start Jupyter Lab. Think of it as creating command shortcuts.
# The `venvSetup` command creates a virtual environment 'placeholder' with required plugins defined within `requirements.txt`.
# The `runJLab` command starts Jupyter Lab.

# Variables
PYTHON = python3
VENV_DIR = .venv

# since we are running the venv from the Makefile, the venv is not activating and thus `VIRTUAL_ENV` is not automatically exported as an environment variable
# here we set the absolute path to the virtual environment
export VIRTUAL_ENV = $(shell pwd)/$(VENV_DIR)

# Commands
# `venvSetup` will first remove an existing venv if it exists and rebuild the environment
# `runJLab` simply runs jupyter lab
venvCreate:
	( \
		rm -rf $(VENV_DIR); \
		$(PYTHON) -m venv $(VENV_DIR); \
		. .venv/bin/activate; \
		pip install --upgrade pip; \
		pip install -r requirements.txt; \
	)

runJLab:
	( \
       . .venv/bin/activate; \
       jupyter-lab; \
    )
	
	
