# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.0.5] - future

- [ ] need to add a package version so that when users install the package, the package version is shown to the user

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
