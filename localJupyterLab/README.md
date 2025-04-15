# README

This is only for more advanced use cases or where MyBinder does not work for you or you simply want to use JupyterLab while offline.
 
If we want to run a local instance of JupyterLab https://jupyter.org/, and have Python installed on our computer, we can create a virtual environment using the commands below. *Note: the virtual environment will consume ~190Mb of storage as of this writing. You can remove the `.venv` folder to regain that storage space once you are finished with it since you can always rebuild it later. A `.ipynb_checkpoints` folder will be automatically created if you run or edit a Notebook file within JupyterLab.*

## Requirements

Most recent version of Python v3.x or greater.

## Cloning the repo

It is recommended (if you are using a Windows environment) to clone the repo using the following command to ensure the EOL characters are set to LF:

`git clone --config core.autocrlf=false https://github.com/kuhlaid/dv-api-test`

## Setting up the JupyterLab environment

In a shell terminal run the following:

```shell
# Bash commands
$ cd "/mnt/c/Users/pgale/LocalDev/dv-api-test"   # change this to your local copy of the `localJupyterLab` directory
$ make venvSetup  # this runs the commands found in the `venvSetup` step of the  Makefile (assuming Python 3.x installed) to create a virtual environment directory, .venv (if not already); venv is included in Python 3.3>; this will install the modules from the requirements.txt file
$ make runJLab    # run JupyterLab; this saves us the step of needing to activate and deactivate the virtual environment
$ # to stop JupyterLab you can use `Ctrl+C` on the keyboard
```

Once you have run the `make runJLab` command then check the command line for a link to start JupyterLab in your web browser (the link will look like http://127.0.0.1:8888/lab?token=xxx).