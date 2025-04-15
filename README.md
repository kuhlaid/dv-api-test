# README

The purpose of this repository is to provide a [Dataverse Project](https://dataverse.org/) API testing Notebook using Python scripting, in addition to providing a curation workflow for depositing data into a repository (only the deposit and prep portion of the workflow). The code written for this Notebook was designed to be compatible with the Dataverse v5.13 and later. I encourage you to experiment with changing the scripts within the `_worker` file because if you break the code you can always download a fresh copy from the repository.

See the `CHANGELOG.md` file for issues needing to be addressed and recent changes.

## Get started

To begin working with the Jupyter Notebook from this repository, simply click on the `launch Binder` icon below. This will create a virtual JupyterLab environment in your web browser and will copy the repository code to Binder (https://mybinder.org/). Then you can return to this README file within Binder or wherever you are reading this for further instruction.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/kuhlaid/dv-api-test/HEAD?urlpath=%2Fdoc%2Ftree%2Fnotebook.ipynb)

## Who is the audience?

Those who might want to use this code/Notebook are researchers or data curators who need to archive data within the [Dataverse Project](https://dataverse.org/). Reading further assumes you either know how to use a Jupyter Notebook or at least some basic Python, or are willing to learn. Secondly these instructions assume you know how to use the Dataverse on a basic level; this will not be a tutorial on using the Dataverse (at least not extensively). You will also need to set up a Dataverse account on https://demo.dataverse.org/ or some other host (preferably on a demo site for testing purposes). If you only plan to use the Dataverse to publish one dataset and then never use it again, then this resource might not be for you. If you are publishing to the Dataverse regularly then you should consider using this tool to work with the Dataverse API (unless you already know your way around the Dataverse API).

## Why is this code/resource useful?

This resource was created to help simplify the use of the Dataverse API and also provide you with processes that you likely would not learn about unless you worked with the API extensively. The Dataverse API allows you to automate many of the processes that should not be performed manually if you are more than a one time user of the Dataverse. Having reproducible automationed curation steps can greatly increase the efficiency and quality assurance for your data curation. Also, the Dataverse API can be tricky to learn and the documentation can be confusing. On top of this, unless you are an applications analyst, the API documentation can be confusing and knowing which API to use or what development environment you should use can seem out of reach for the general public.

## What is included in this code repository?

A Jupyter Notebook `notebook.ipynb` is provided along with the code and instructions to work with the Notebook.

# Using the Notebook

## Basic JupyterLab

I suggest loading this repository code into https://mybinder.org/ using the link at the top of this document; as of March 2025, MyBinder.org is a free JupyterLab service. MyBinder.org is useful for learning how to work with Jupyter Notebooks, but is not ideal for any serious data curation. *Note: As of this writing, Google Colab DOES NOT support the advanced configuration of this repository, so Colab is not an environment you can use with this code.*

## Preferred JupyterLab set up

This is only for more advanced use cases or where MyBinder does not work for you or you simply want to use JupyterLab while offline.
 
If we want to run a local instance of JupyterLab https://jupyter.org/, and have Python installed on our computer, we can create a virtual environment using the commands below. *Note: the virtual environment will consume ~190Mb of storage as of this writing. You can remove the `.venv` folder to regain that storage space once you are finished with it since you can always rebuild it later. A `.ipynb_checkpoints` folder will be automatically created if you run or edit a Notebook file within JupyterLab.*

### Requirements

- [ ] Most recent version of Python v3.x or greater (see https://www.python.org/downloads/).
- [ ] Most recent version of Git (see https://git-scm.com/downloads).
- (optional) A tool such as VSCode for working with Git (see https://code.visualstudio.com/download).

### Cloning the repo

It is recommended (if you are using a Windows environment) to clone this repository using the following command to ensure the EOL characters are set to LF:

`git clone --config core.autocrlf=false https://github.com/kuhlaid/dv-api-test`

### Setting up the JupyterLab environment

In a shell terminal run the following:

```shell
# Bash commands
$ cd "/mnt/c/Users/pgale/LocalDev/dv-api-test"   # change this to your local copy of the `localJupyterLab` directory
$ make venvSetup  # this runs the commands found in the `venvSetup` step of the  Makefile (assuming Python 3.x installed) to create a virtual environment directory, .venv (if not already); venv is included in Python 3.3>; this will install the modules from the requirements.txt file and can take at least several minutes to run as components are installed
$ make runJLab    # run JupyterLab; this saves us the step of needing to activate and deactivate the virtual environment
$ # to stop JupyterLab you can use `Ctrl+C` on the keyboard
```

Once you have run the `make runJLab` command then check the command line for a link to start JupyterLab in your web browser (the link will look like http://127.0.0.1:8888/lab?token=xxx).

## Alternate JupyterLab set up using Docker

Another option is to use Docker by running a container with the following command `docker run -it --name myDataverseApiTest --mount type=bind,source="$(pwd)",target="/home/jovyan/work" --add-host=host.docker.internal:host-gateway -p 10000:8888 quay.io/jupyter/scipy-Notebook:latest`; this allows you to keep your data files locally on your computer but you need to run this command from a location where you data files are located AND this repository code needs to be in that same location/directory tree (which is not always optimal). Anyway, I'm not here to tell you which environment you have to use, but just providing some options I have worked with.

## Understanding the files used with the Notebook

I purposely do not embed the bulk of the Python code used for this Notebook, within the Notebook itself. For a heavily coded Notebook this simply makes the Notebook bulky and difficult to read. Also, separating the Notebook configuration from the Notebook allows you to keep your configuration secrets (such as API tokens) OUT OF your GitHub repository; *NEVER save your API tokens or secrets to your Notebook or within any file in your repository.*

The Notebook configuration settings are stored within one JSON file. When you run the first block of code in the Jupyter Notebook, the `example._config.json` contents will be copied to a `_config.json` file (henceforth referred to as the _config file). The _config file is the only file you are required to edit. The _config file contains the settings of the Notebook and specifies which Dataverse you are using, the files you wish to upload to the Dataverse, and settings to use for your Dataverse collection and dataset. We use a JSON file for the configuration because it is formatted text. JSON can be treated as an object containing properties that scripts such as Python are able to easily manipulate and is the suggested method of storing Notebook configurations (see https://en.wikipedia.org/wiki/JSON).

**NOTE: Property names within the _config file beginning with a `_cc__` prefix are constant configuration variables. Renaming these properties will cause some code to break so only modify the values of these properties.**

When you run the first code block of the Jupyter Notebook, you will be prompted to enter the Dataverse API token and Dataverse domain to use with the Notebook. These settings will be saved to the _config file and the code will automatically check to see that the API settings are correct.

The config file contains three properties `_cc__strDvApi_DOMAIN, _cc__strDvApi_PARENT_COLLECTION, and _cc__strDvApi_TOKEN` (example shown below) that define the Dataverse you wish to use and your token to connect to it. For the purposes of testing I suggest using the `https://demo.dataverse.org` domain and the `:root` parent collection with that domain (*Note the colon in `:root` is important for creating collections*). So if you are keeping these settings the same then you will only need to create a token and paste it into the configuration where it says `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`. You can likely find your token for the demo Dataverse at https://demo.dataverse.org/dataverseuser.xhtml?selectTab=apiTokenTab.

**NOTE: When running the Notebook, the first code block will ask you for your Dataverse API token, so you do not need to manaually update the `_config.json` file as the Notebook will do that for you.**

```
  "_cc__strDvApi_DOMAIN": "https://demo.dataverse.org",
  "_cc__strDvApi_PARENT_COLLECTION": ":root",
  "_cc__strDvApi_TOKEN": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
```

**NOTE: The `_config` file is meant to be modified so feel free to add additional properties as needed. However do not rename existing property names unless you know they are not being used by the `_worker` or other scripts, or the code might throwing errors. For example you could copy the `lstTEST_FILES` array, rename it `lst_FILES` and change the filenames within the list, then upload these files (after you have created them) using `objWorker.uploadTestFiles("lst_FILES")` command in the Notebook.**

Below is an explanation of some key variables found in the configuration file.

- `_cc__strDvApi_DOMAIN` the Dataverse domain you are using
- `strDvApi_NAME` name you want to provide for your Dataverse 
- `_cc__strDvApi_PARENT_COLLECTION` the Dataverse collection alias your Dataverse will be stored under
- `_cc__strDvApi_TOKEN` your Dataverse API token
- `objDvApi_COLLECTION_START` the properties you will use to initialize your Dataverse
- `objDvApi_DATASET_INIT` - you can use this object to initialize a dataset and contains most of the default metadata fields **note: we intentionally leave the `datasetVersion` element out of the metadata so we can use the same metadata for both the creation of the dataset and update**
- `objDvApi_DATASET_INIT_PART` - this is another dataset initialization object
- `objDvApi_DATASET_UPDATE` - this is another dataset initialization object that we can use to update the dataset metadata
- `_cc__strWORKING_DIR` defines the internal working path of the Notebook but if you are using My Binder to test then you will not need to change this setting
- `_cc__strLOCAL_UPLOAD_DIR` the name of the folder generated by the Notebook for creating files to send to the Dataverse API
- `_cc__blnSHOW_DEBUG_STATEMENTS` a boolean flag (0="do not show debug statements in the Notebook", 1="show debug statements within the Notebook output")
- `_cc__blnSHOW_CURL_COMMANDS` a boolean flag (0="do not show CURL statements in the Notebook", 1="show CURL statements within the Notebook output")
- `lstTEST_FILES` a list of test files to generate for the API tests
- `lstTEST_FILES2` a second set of test files to generate for the API tests

Another file you will notice once you create a Dataverse dataset, is a `_cc__DvDatasetMetadata.json` file. This file is generated by the Notebook to keep track of the dataset you are working with. If you delete it then the Notebook will no longer be able to track the dataset (for adding or updating files for example).

## Where is the Python code

The Notebook in this repository purposely does not contain the bulk of the Python code used to run it. Instead the Python is split into ancillary files `_installer` and `_worker` with `_worker` carrying the bulk of the Python code. Also the code uses the plugin from https://github.com/kuhlaid/DvApiMod5.13 (there is no need to look at this unless you want to know the gory details of how it works or wish to extend it). A heavily coded Notebook simply makes the Notebook bulky and difficult to read. Also, separating the Notebook configuration from the Notebook allows you to keep your configuration secrets (such as API tokens) OUT OF your GitHub repository; *NEVER save your API tokens or secrets to your Notebook or within any file in your repository.*

# About the Notebook code (getting technical, if you are so inclined)

The code blocks in the Notebook are intentionally brief because most users are not concerned with what the code looks like (at least initially). If you want to know what the scripts do then review the .py files that we import into the Notebook. However we will briefly describe a line of code so you have a general idea of what is happening behind the scenes.

The `objWorker.ObjDvApi.DvCreateCollection()` command for example, runs the `DvCreateCollection()` method, which is found in the `ObjDvApi` object, and makes a Dataverse API request to create a new repository/collection. The `ObjDvApi` is defined in an external Python file which contains reusable methods for working with the Dataverse API (see https://github.com/kuhlaid/DvApiMod5.13). We use this same class for all of our datasets, so keeping the methods in a single file for reuse is better than manually adding into the code of each of our datasets and making our working code script more densely worded than it needs to be.

## The objWorker

The `objWorker` is the object that we customize for each dataset and simply acts as a template for importing different classes/objects we want to attach to it. For instance, we attach the `ObjDvApi` to our `objWorker` object so whatever functionality exists in the `ObjDvApi` class can be used in our `objWorker` class. The `.` between `objWorker.ObjDvApi` simply represents that `ObjDvApi` is an extension of `objWorker`. An analogy would be adding a dustpan to a broom (or `broom.dustpan`) to extend the functionality of the broom, so the broom can now be used to pick up dust and not simply push it around.

**NOTE: Most of the methods listed below take a simple string that represents a property of the `_config` file. So, for the `objWorker.createCollection()` method we pass it the `objDvApi_COLLECTION_START` string and the method then reads the `objDvApi_COLLECTION_START` property from the `_config` file. This allows us to use the Notebook code with different configurations, without the need to modify the code.**

Below we explain the objWorker methods that allow you to work with the a Dataverse collection.

### objWorker.createCollection([name of config object - e.g. `objDvApi_COLLECTION_START`])

The `createCollection` method creates a new Dataverse collection (which is the same thing as creating a new Dataverse) using the `strDvApi_NAME` value from the _config file.

### objWorker.viewCollection([name of config object - e.g. `objDvApi_COLLECTION_START`])

This method simply returns details of a Dataverse collection based on the collection alias.

### objWorker.createDataset([name of collection config object - e.g. `objDvApi_COLLECTION_START`], [name of dataset config object - e.g. `objDvApi_DATASET_INIT_PART`])

This method creates a Dataverse dataset placeholder using properties defined within the `objDvApi_DATASET_INIT_PART` object of the Notebook `_config`. Feel free to change the property values except for maybe the `dataverseType` which uses set values. You can review them in the Dataverse User Guide https://guides.dataverse.org/en/6.5/api/native-api.html#create-a-dataverse-collection. There are more properties that can be included in this object and a more comprehensive list is found in the `objDvApi_DATASET_UPDATE` object that is used in later steps to show how existing metadata can be updated for a dataset.

Using the https://guides.dataverse.org/en/5.13/_downloads/4e04c8120d51efab20e480c6427f139c/dataset-create-new-all-default-fields.json referenced in https://guides.dataverse.org/en/5.13/api/native-api.html#create-a-dataset-in-a-dataverse-collection, will be our dataset template.

### objWorker.createTextFiles([name of config list - e.g. `lstTEST_FILES`])

This generates some test files to send to the Dataverse. If you have your own files you wish to upload to the Dataverse then you can skip this step. Just make sure the files you want to upload are defined in the `_config` similar to the `lstTEST_FILES` array. NOTE: this method will only create plain text files.

### objWorker.createZipFile([name of config object - e.g. `myZipFile`])

This generates a zip file with sample text files defined in the `_config`. 

### objWorker.doubleZip([name of config object - e.g. `myZipFile`])

This takes a zip file an double zips it. 

### objWorker.uploadFiles([name of config list - e.g. `lstTEST_FILES`])

**NOTE: It is strongly recommended that you run the `createEmptyDatasetDraft()` method before uploading files if you are receiving file upload errors. See the notes on `createEmptyDatasetDraft()` later in this document for more information. If you are receiving file upload errors, running `createEmptyDatasetDraft()` will likely resolve this issue.**

This uploads a list of files defined in the `_config` to the dataset.

When we upload a file to a dataset, it is advisable to check the MD5 hash of the file you are attempting to upload. Our `ObjDvApi` class handles this for you. If the MD5 hash is the same and you upload the file to the dataset, then a new file will be added to the dataset with a file name ending in a number. Thus you will end up with two duplicate files in the dataset with two different names (which you should not do). We have added an MD5 hash checking method to our `ObjDvApi` class that will check for matching MD5 hashes and will use the `file replace` API if files already exist in the dataset. Hence another good reason to use this Notebook code.

### objWorker.updateDatasetMetadata([name of dataset config object - e.g. `objDvApi_DATASET_UPDATE`])

This allows us to update our dataset metadata. After running this method check the Dataverse dataset webpage to see how it has updated.

### objWorker.publishDatasetDraft([name of collection config object - e.g. `objDvApi_COLLECTION_START`], [string version type - e.g. `major`])

When you publish a dataset draft you have the option to specify whether the published changes are (major or minor). This defines if the published version consists of minor or major revisions. If you don't know or do not care simply use `major` unless you are making frequent updates to the dataset.

(see https://guides.dataverse.org/en/5.13/api/native-api.html#publish-a-dataset for gory details)

### objWorker.createEmptyDatasetDraft()

This method does not take any arguments and will empty the draft dataset defined in `_cc__DvDatasetMetadata.json`. You should use the `createEmptyDatasetDraft` method anytime you are updating a Dataset with new files. This will clean out any existing files and allow you to upload a completely new set of files as a new version of the Dataset (whether the files are named differently from the previous files does not matter). 

The Dataverse will not allow you to upload a file that currently exists in the dataset with the same MD5 checksum (same content), however you can replace the metadata for the file. **It is best practice to run this method anytime you wish to update the Dataset with new files.**

This is the best action to take when you want to ensure a clean dataset draft with no files from the last published version of the dataset needing to be replaced by incoming files. The `createEmptyDatasetDraft` method uploads an empty file to the dataset to initiate a new draft state for the dataset (if it does not already exist), then queries the dataset for the current files found in the draft state, then removes all files in the draft state. From here you have an empty dataset draft for importing the newest files for your dataset.

As some background, this method was created to resolve the problem of some types of files (such as zip files) failing to replace existing zip files in the dataset. This problem may occur with other files as well so simply using this method will alleviate the need for file replacement and issues with that API endpoint.

### objWorker.viewDatasetFiles([string version type - e.g. `:draft`])

This method queries the Dataverse for the information on files currently residing in a Dataset referenced in `_cc__DvDatasetMetadata.json`. You can pass this method the version of the Dataset you are curious about (which will likely be `:draft` in most cases).

### objWorker.deleteDataset()

Will delete the dataset draft defined in `_cc__DvDatasetMetadata.json`. This will not delete published Dataset versions (since that is not possible).

### objWorker.deleteCollection([name of config object - e.g. `objDvApi_COLLECTION_START`])

This will delete a Dataverse collection (if there are no datasets present). Once you publish something it is basically set in place for good.

### objWorker.viewCollectionContents([name of config object - e.g. `objDvApi_COLLECTION_START`])

This method returns basic information regarding the contents of a Dataverse Collection.

## Words of caution

**For Windows users, if you copy and paste anything into a file within JupyterLab, and that copied content contains hidden CRLF end of line characters, it will likely cause unexpected loss of text or shifting of text within the file. JupyterLab does not work well with CRLF (Windows EOL characters), so if you start noticing text move around unexpected or disappear, it is probably this annoying CRLF issue within JupyterLab and you need to convert the file to LF line endings before fixing things with the file. I had this problem come up within this README file and hopefully no critical instructions were lost. (see https://github.com/jupyterlab/jupyterlab/issues/2951)**