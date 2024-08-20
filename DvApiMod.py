# This script is used to separate the Dataverse API methods from our main Jupyter notebook code to simplify the code that users see

# @title Here we create a main working object (DvMod) so our configuration and database connections can more easily integrate. Also separating the code from the notebooks makes the notebook easier to read and manage.
import curlify
import json
import logging
# import pandas as pd         # Import the data analysis libraries
# from pandas import DataFrame
# from tqdm import tqdm # progress bar
# import numpy as np
import requests
import io
import hashlib
import os
# import zipfile
# we use this to make sure our variable values are not printed to the notebook
# from IPython.display import HTML, display, clear_output

# @title By placing all of our Python function within a class object, it makes it much easier for information to be used across functions without needing to explicitly passing them into each function (instead we pass the entire Worker object into the functions so each function can do what it needs with the object)
class ObjDvApi:
    # @param objConfig (we initialize this object with our notebook configuration)
    def __init__(self,objConfig) -> None:
        self.eventLogger()
        self.objConfig = objConfig
        self.strDATAVERSE_PARENT_COLLECTION = self.objConfig["strDvApi_PARENT_COLLECTION"]
        self.strDATAVERSE_DOMAIN = self.objConfig["strDvApi_DOMAIN"]
        self.strDATAVERSE_API_TOKEN = self.objConfig["strDvApi_TOKEN"]
        self.logger.info("Finished ObjDvApi init")


    # @title We will pull the logging settings from our Worker class so there is no need to add them in this script
    def eventLogger(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel('INFO')
        
    
    # @title Create a new Dataverse collection (which is the same thing as creating a new Dataverse)
    def createCollection(self) -> None:
        self.logger.info("start createCollection")
        strApiEndpoint = '%s/api/dataverses/%s' % (self.strDATAVERSE_DOMAIN, self.strDATAVERSE_PARENT_COLLECTION)
        self.logger.info('making request: %s' % strApiEndpoint)
        objHeaders = {
            "Content-Type": "application/json",
            "X-Dataverse-Key": self.strDATAVERSE_API_TOKEN
        }
        r = requests.request("POST", strApiEndpoint, json=self.objConfig["objDvApi_COLLECTION_START"], headers=objHeaders) # it is nice I can simply send the JSON object without the need to create a separate JSON file
        self.printResponseInfo(r)
        self.logger.info("end createCollection")
        

    # @title View a new Dataverse collection based on the collection alias
    def viewCollection(self) -> None:
        self.logger.info("start viewCollection")
        strApiEndpoint = '%s/api/dataverses/%s' % (self.strDATAVERSE_DOMAIN, self.objConfig["objDvApi_COLLECTION_START"]["alias"])
        self.logger.info('making request: %s' % strApiEndpoint)
        objHeaders = {
            "Content-Type": "application/json",
            "X-Dataverse-Key": self.strDATAVERSE_API_TOKEN
        }
        r = requests.request("GET", strApiEndpoint, headers=objHeaders)
        self.printResponseInfo(r)
        self.logger.info("end viewCollection")
        

    # @title Delete a new Dataverse collection based on the collection alias
    def deleteCollection(self):
        self.logger.info("start deleteCollection")
        strApiEndpoint = '%s/api/dataverses/%s' % (self.strDATAVERSE_DOMAIN, self.objConfig["objDvApi_COLLECTION_START"]["alias"])
        self.logger.info('making request: %s' % strApiEndpoint)
        objHeaders = {
            "Content-Type": "application/json",
            "X-Dataverse-Key": self.strDATAVERSE_API_TOKEN
        }
        r = requests.request("DELETE", strApiEndpoint, headers=objHeaders)
        self.printResponseInfo(r)
        self.logger.info("end deleteCollection")
        

    # @title List Dataverse collection contents based on the collection alias
    def viewCollectionContents(self) -> None:
        self.logger.info("start viewCollectionContents")
        strApiEndpoint = '%s/api/dataverses/%s/contents' % (self.strDATAVERSE_DOMAIN, self.objConfig["objDvApi_COLLECTION_START"]["alias"])
        self.logger.info('making request: %s' % strApiEndpoint)
        objHeaders = {
            "Content-Type": "application/json",
            "X-Dataverse-Key": self.strDATAVERSE_API_TOKEN
        }
        r = requests.request("GET", strApiEndpoint, headers=objHeaders)
        self.printResponseInfo(r)
        self.logger.info("end viewCollectionContents")

    
    # @title Create a new dataset
    def createDataset(self):
        self.logger.info("start createDataset")
        strApiEndpoint = '%s/api/dataverses/%s/datasets' % (self.strDATAVERSE_DOMAIN, self.objConfig["objDvApi_COLLECTION_START"]["alias"])
        self.logger.info('making request: %s' % strApiEndpoint)
        objHeaders = {
            "Content-Type": "application/json",
            "X-Dataverse-Key": self.strDATAVERSE_API_TOKEN
        }
        r = requests.request("POST", strApiEndpoint, json=self.objConfig["objDvApi_DATASET_PART"], headers=objHeaders)  # this only creates a dataset placeholder with partial information
        # r = requests.request("POST", strApiEndpoint, json=self.objConfig["objDvApi_DATASET_FULL"], headers=objHeaders)  # full dataset properties not working (8/17)
        self.printResponseInfo(r)
        return r
        self.logger.info("end createDataset")


    # @title Delete a dataset draft
    def deleteDatasetDraft(self, strDatasetId) -> None:
        self.logger.info("start deleteDatasetDraft")
        strApiEndpoint = '%s/api/datasets/%s/versions/:draft' % (self.strDATAVERSE_DOMAIN, strDatasetId)
        self.logger.info('making request: %s' % strApiEndpoint)
        objHeaders = {
            "X-Dataverse-Key": self.strDATAVERSE_API_TOKEN
        }
        r = requests.request("DELETE", strApiEndpoint, headers=objHeaders)
        self.printResponseInfo(r)
        self.logger.info("end deleteDatasetDraft")


    # @title Request the dataset contents from the Dataverse so we can compare with what we have locally
    def getDvDatasetContents(self,objFile):
        # use the requests module from Python to make a simple request to the Dataverse to check the contents
        url = self.strDATAVERSE_DOMAIN+"/api/datasets/:persistentId/versions/:latest?persistentId="+objFile["strDvUrlPersistentId"]
        headers = {
            "Content-Type": "application/json",
            "X-Dataverse-Key": self.strDATAVERSE_API_TOKEN
        }
        r = requests.request("GET", url, headers=headers)
        self.dictDatasetContents = r.json()    # convert the response to a dict
        
    
    # @title Add a new file to a dataset (or replace an existing one)
    # @arguments objFile=JSON object defining the file for upload
    def addDatasetFile(self, objFile):
        self.getDvDatasetContents(objFile)
        objFileReturn = self.checkFileForUpload(objFile["strFileName"], os.path.join(objFile["strUploadPath"],objFile["strFileName"]))  # check that we are ready for upload
        self.logger.info(objFileReturn)
        # --------------------------------------------------
        # Using a "jsonData" parameter, add optional description + file tags
        # --------------------------------------------------
        params = dict(description=objFile["strDataDescription"],
                    directoryLabel=objFile["strDirectoryLabel"],
                    fileName=objFile["strFileName"],
                    categories=objFile["lstCatgories"])
        self.logger.info("addDatasetFile:",objFile["strFileName"],params)
        params_as_json_string = json.dumps(params)
        payload = dict(jsonData=params_as_json_string)
        if (objFileReturn["blnFileExists"]==False): # if the file does not already exist in the dataset we upload it using the 'add' API endpoint
            strApiEndpoint = '%s/api/datasets/:persistentId/add?persistentId=%s' % (self.strDATAVERSE_DOMAIN, objFile["strDvUrlPersistentId"])
            # self.logger.info(objFile)
        elif (objFileReturn["blnMd5Match"]==True): # we want to update the file metadata
            strApiEndpoint = '%s/api/files/%s/metadata' % (self.strDATAVERSE_DOMAIN, objFileReturn["dataFile"]["id"])
        else:  # we have an existing file and the MD5 checksum does not match, we need to replace the file
            strApiEndpoint = '%s/api/files/%s/replace' % (self.strDATAVERSE_DOMAIN, objFileReturn["dataFile"]["id"])

        fileobj = open(os.path.join(objFile["strUploadPath"],objFile["strFileName"]), 'rb')  # read the file
        objFilePost = {'file': (objFile["strFileName"], fileobj)}   # we have the new file object to save to the Dataverse
        objHeaders = {
            "X-Dataverse-Key": self.strDATAVERSE_API_TOKEN
        }
        self.logger.info('making request: %s' % strApiEndpoint)
        if (objFileReturn["blnMd5Match"]==True and objFileReturn["blnFileExists"]==True): # we handle a metadata only update differently
            self.logger.info('metadata only update')
            r = requests.request("POST", strApiEndpoint, data=payload, headers=objHeaders)
            self.logger.info(curlify.to_curl(r.request))
        else:
            r = requests.request("POST", strApiEndpoint, data=payload, files=objFilePost, headers=objHeaders)
        self.printResponseInfo(r)
        self.logger.info("--end uploadFileToDv--")

    
    
    
    # @title General purpose method for printing response properties for testing
    # @argument r=response object from a requests.request()
    def printResponseInfo(self,r) -> None:
        self.logger.info('-' * 40) # simple delineation so we know when this method is called in our output 
        self.logger.info("json="+str(r.json()))
        self.logger.info("headers="+str(r.headers))
        self.logger.info("response status="+str(r.status_code))


    # @title Check that we have changes to a file before we try uploading to the Dataverse
    # @param File name, a description we will use to describe the file in the Dataverse
    # @return objFileReturn (existing file object)
    def checkFileForUpload(self, strFileName, strFilePath):
        # check for an existing file in the Dataverse
        objFileReturn={"blnFileExists":False, "blnMd5Match":True}  # assumptions for our files
        strExistingMd5=''
        # self.logger.info(len(self.dictDatasetContents['data']['files']))
        for dvFile in self.dictDatasetContents['data']['files']: # loop through the files in the dataset to find the one we want to replace
            strExistingMd5 = dvFile['dataFile']['md5']
            if 'originalFileName' in dvFile['dataFile']:    # NOTE: some files are unique in the Dataverse in that they are not labeled the same way due to the original format switched to tab delimited format, so we need to check for an `originalFileName` element
                if (dvFile['dataFile']['originalFileName']==strFileName):
                    objFileReturn=dvFile
                    objFileReturn["blnFileExists"]=True
                    break
            else:
                if (dvFile['label']==strFileName):     # check files other than files converted to tab delimited in the Dataverse
                    objFileReturn=dvFile
                    objFileReturn["blnFileExists"]=True
                    break
        if (objFileReturn["blnFileExists"]==True): # if the file we are wanting to upload currently exists in the the Dataverse dataset, we check the MD5 checksum of both files and only upload if the MD5 differs
            newFileMd5 = self.md5(strFilePath)
            self.logger.info("MD5 are local "+newFileMd5+" and dataset "+strExistingMd5)
            if (newFileMd5==strExistingMd5):
                self.logger.info("MD5 hashes match on "+strFileName+", so do not upload new file")
                self.blnUploadFile=False
                objFileReturn["blnMd5Match"] = True
            else:
                self.logger.info("Something has changed with the file so we can upload a new version of the file to the Dataverse",newFileMd5,"==",strExistingMd5)
                objFileReturn["blnMd5Match"] = False
        return objFileReturn


    # @title Generates an MD5 hash for a given file (used to check against files being uploaded to prevent duplicate file uploads)
    # @argument Path to file being checked
    def md5(self, fileToCheck):
        hash_md5 = hashlib.md5()
        with open(fileToCheck, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
