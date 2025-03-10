# This file simplifies the commands needed to install and start Jupyter Lab. Think of it as creating command shortcuts.
# The `venvSetup` command creates a virtual environment 'placeholder' with required plugins defined within `requirements.txt`.
# The `runJLab` command starts Jupyter Lab.

# Variables
PYTHON = python3
VENV_DIR = .venv

# Commands
venvSetup: 
	$(PYTHON) -m venv $(VENV_DIR)
	pip install --upgrade pip
	$(VENV_DIR)/bin/pip install -r requirements.txt

runJLab: 
	$(VENV_DIR)/bin/jupyter-lab
