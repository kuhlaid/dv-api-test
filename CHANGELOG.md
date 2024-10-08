# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [vxxx] - future

- [ ] create a package that performs some 'starter' processing (e.g. creating a metadata starter file with the list of files, variables, etc. with '[placeholder]' values where the curator can fill in the blanks) of files someone wants to push to a repository; this would align with the code we are using and provide an example for how others can begin the curation process
- [ ] *NOT IMPORTANT* add zip files to the test if wanting to demonstrate issues with zip file replacement

## [v0.0.7] - 2024-09-16

- [x] adding `updateDatasetMetadata` method for updating the metadata for the dataset
- [x] removing the `datasetVersion` element from the dataset metadata since it only applies to the `create dataset` API endpoint, but will cause errors if kept in place for the updating the dataset metadata

## [v0.0.6] - 2024-09-05

- [x] adding comments about `blnSHOW_CURL_COMMANDS` variables to disable CURL command logs
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
