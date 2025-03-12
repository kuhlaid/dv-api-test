# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.0.0] - 2025-03-12

- [x] created a Notebook configuration checker which prompts the user for their Dataverse domain and token and saves it to the configuration file (this should simplify the configuration for new users)
- [x] cleaning up the documentation
- [x] tried using widgets for the configuration form but you would need to use async actions to keep the processes running, so reverted to the simple `input()` function which keeps the processes running
- [x] adding `_cc__` prefix to constant configuration variables to distinguish them from other variables within a configuration
- [x] replace "dvDatasetMetadata.json" with "_cc__DvDatasetMetadata.json" to signify a constant file 

## [v0.0.9] - 2025-03-09

- [x] moving notebook and code to the root so it will start in Binder without issue
- [x] fixing issue with double zip not finding the zip file
- [x] adding pandas to the install script since MyBinder needs it
- [x] testing the framework and found that https://demo.dataverse.org site does not currently allow users to create collections via the API (submitted request to resolve this issue); will use https://demo-dataverse.rdmc.unc.edu in the meantime

## [v0.0.8] - 2025-03-09

- [x] simplified the Notebook and improved the documentation
- [x] added link to the README so the framework will easily load into MyBinder
- [x] add zip files to the framework since the handling of zip files can be confusing in the Dataverse (with differences between single and double zipped files)

## [v0.0.7] - 2024-09-16

- [x] adding `updateDatasetMetadata` method for updating the metadata for the dataset
- [x] removing the `datasetVersion` element from the dataset metadata since it only applies to the `create dataset` API endpoint, but will cause errors if kept in place for the updating the dataset metadata

## [v0.0.6] - 2024-09-05

- [x] adding comments about `_cc__blnSHOW_CURL_COMMANDS` variables to disable CURL command logs
- [x] adding a `createEmptyDatasetDraft` method which will force a clean draft state for a dataset (this is useful if you are not interested in any of the prior files saved to the dataset moving into a new version)

## [v0.0.6] - 2024-09-04

- [x] passing in parameters to methods instead of relying on the JSON schema of the requesting app

## [v0.0.5] - 2024-09-04

- [x] testing updates to the `DvApiMod5.13` package
- [x] **(IMPORTANT)** allow for passing the file upload parameters to the `addDatasetFile` method so users are not forced to us a set JSON format in their metadata

## [v0.0.4] - 2024-08-30

- [x] tested the full dataset metadata; I had made an update to the `DvApiMod5.13` package, but without  does not have a version attached to it when installing. This doesn't matter 99% of the time but without it the wheel that is created during the install keeps reverting to the cache likely because the name of the wheel remains the same; as a result the server needs to be restarted so that the latest version of the package is used in the notebook

## [v0.0.3] - 2024-08-28

- [x] resolved the Dataverse API class to an externally hosted Python plugin (https://github.com/kuhlaid/DvApiMod5.13) that seems to be working now

## [v0.0.2] - 2024-08-27

- [x] when publishing a dataset draft, check to make sure the collection is published first and publish if not
- [x] added ability to remove files from the draft state of a dataset
- [x] fix the error being thrown when deleting a dataset file
- [x] moving the Dataverse API class to an externally hosted Python plugin (https://github.com/kuhlaid/DvApiMod5.13); but it is not working

## [v0.0.1] - 2024-08-21

- [x] worked on version v5.13 of the the Dataverse API testing notebook
- [x] splitting the code by Dataverse versions tested (or to be tested)
