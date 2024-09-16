# About this repository

The purpose of this repository is to provide a Jupyter notebook that tests some of the basic functions of the Dataverse Project API, beginning with version 5.13 (https://guides.dataverse.org/en/5.13/api/).

The repository is notable for its external Python scripts, which are responsible for processing the majority of the notebook. Keeping the Python in external files allows for reusability and less duplication of code which can occur by placing all your Python within a Jupyter notebook. Not to mention, a heavily coded notebook can look bloated if you embed all scripts within the notebook.

## Versions

Notebooks specific to a version of the Dataverse API are placed with the `v` folders, denoting the version of Dataverse the notebook was tested against.

## Cloning this repository

Clone this repository using the following command to prevent Windows end of line characters from being used in a Windows environment:

`git clone --config core.autocrlf=false https://github.com/kuhlaid/dv-api-test.git`

