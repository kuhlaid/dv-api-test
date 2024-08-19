# About

This notebook will be run against the demo server of the Dataverse at https://demo-dataverse.rdmc.unc.edu/dataverse/root.

## Configure a local Jupyter Server

`cd "/mnt/c/Users/pgale/University of North Carolina at Chapel Hill/TarcStudyDataRepository - Files/DataPull/364-dp/Note3/dv-api-test"`

`docker run -it --name 364-dp-DataverseApiTest --mount type=bind,source="$(pwd)",target="/home/jovyan/work" --add-host=host.docker.internal:host-gateway -p 10000:8888 quay.io/jupyter/scipy-notebook:latest`

## Notebook configuration

We will split our notebook configuration into several files (installer.py, _config.json, and worker.py). 

- The `installer.py` script installs Python modules our notebook may need. 

- The `_config.json` file(s) are used to define any configuration settings/variables so we can use the notebook code against multiple environments (demo, test, or production for example), thus making the notebook reusable by others. 

- The `worker.py` file contains our Python scripts since a notebook can become unweildy to use when all of the Python code is embeddd directly within the notebook. Although the main reason we use this external Python file is so our Python code can be placed within a Python object (or objects), making it much easier for the functions to interact with each other.o

## Packaging the Dataverse API handlers

At this point we want to setup a package/module that we can load from GitHub and use in our notebook since all of our dataset notebooks will be using the same code. Have the core code in an imported module will allow for ease of use by other users without the need to add the core functions into their notebook code. It simply makes things cleaner. At the moment we are simply using a locally stored file named `DvApiMod.py` to achieve this but having it moved to a plugin format will make it more extensible.

### Package files

This is an example of packaging on GitHub (which is what I want).
https://github.com/ceddlyburge/python_world/tree/master

https://packaging.python.org/en/latest/tutorials/packaging-projects/

### Using imported packages

https://github.com/wax911/plugin-architecture/blob/master/plugins/advanced-plugin/main.py#L14

## Issues

- We had originally placed our image files within .zip archives to minimize storage space and simplify the organizing of images, however the Dataverse code would not allow zip files to be replaced within a dataset without a duplicate file being created with a different filename (as of March 2024). Due to this problem we switched to simply organizing images by folder without archiving them into zip files.
