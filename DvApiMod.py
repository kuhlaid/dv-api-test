# This script is used to separate the Dataverse API methods from our main Jupyter notebook code to simplify the code that users see




# @title Here we create a main working object (DvMod) so our configuration and database connections can more easily integrate. Also separating the code from the notebooks makes the notebook easier to read and manage.
import json
import pandas as pd         # Import the data analysis libraries
from pandas import DataFrame
from tqdm import tqdm # progress bar
import numpy as np
import requests
import time
import io
import hashlib
import os
import zipfile
# we use this to make sure our variable values are not printed to the notebook
from IPython.display import HTML, display, clear_output
from datetime import datetime
# currentDateAndTime = datetime.now().astimezone()    # get the current date and time to show when this notebook was last run

# @title By placing all of our Python function within a class object, it makes it much easier for information to be used across functions without needing to explicitly passing them into each function (instead we pass the entire Worker object into the functions so each function can do what it needs with the object)
class ObjDvApi:
    # @param objConfig (we initialize this object with our notebook configuration)
    def __init__(self,objConfig) -> None:
        self.objConfig = objConfig
        self.strDATAVERSE_PARENT_COLLECTION = self.objConfig["strDvApi_PARENT_COLLECTION"]
        self.strDATAVERSE_DOMAIN = self.objConfig["strDvApi_DOMAIN"]
        self.strDATAVERSE_API_TOKEN = self.objConfig["strDvApi_TOKEN"]
        print("Finished ObjDvApi init")
        
    
    # @title Create a new Dataverse collection (which is the same thing as creating a new Dataverse)
    def createCollection(self) -> None:
        print("start createCollection")
        strApiEndpoint = '%s/api/dataverses/%s' % (self.strDATAVERSE_DOMAIN, self.strDATAVERSE_PARENT_COLLECTION)
        print('making request: %s' % strApiEndpoint)
        objHeaders = {
            "Content-Type": "application/json",
            "X-Dataverse-Key": self.strDATAVERSE_API_TOKEN
        }
        r = requests.request("POST", strApiEndpoint, json=self.objConfig["objDvApi_COLLECTION_START"], headers=objHeaders) # it is nice I can simply send the JSON object without the need to create a separate JSON file
        self.printResponseInfo(r)
        print("end createCollection")
        

    # @title View a new Dataverse collection based on the collection alias
    def viewCollection(self) -> None:
        print("start viewCollection")
        strApiEndpoint = '%s/api/dataverses/%s' % (self.strDATAVERSE_DOMAIN, self.objConfig["objDvApi_COLLECTION_START"]["alias"])
        print('making request: %s' % strApiEndpoint)
        objHeaders = {
            "Content-Type": "application/json",
            "X-Dataverse-Key": self.strDATAVERSE_API_TOKEN
        }
        r = requests.request("GET", strApiEndpoint, headers=objHeaders)
        self.printResponseInfo(r)
        print("end viewCollection")
        

    # @title Delete a new Dataverse collection based on the collection alias
    def deleteCollection(self):
        print("start deleteCollection")
        strApiEndpoint = '%s/api/dataverses/%s' % (self.strDATAVERSE_DOMAIN, self.objConfig["objDvApi_COLLECTION_START"]["alias"])
        print('making request: %s' % strApiEndpoint)
        objHeaders = {
            "Content-Type": "application/json",
            "X-Dataverse-Key": self.strDATAVERSE_API_TOKEN
        }
        r = requests.request("DELETE", strApiEndpoint, headers=objHeaders)
        self.printResponseInfo(r)
        print("end deleteCollection")
        

    # @title List Dataverse collection contents based on the collection alias
    def viewCollectionContents(self) -> None:
        print("start viewCollectionContents")
        strApiEndpoint = '%s/api/dataverses/%s/contents' % (self.strDATAVERSE_DOMAIN, self.objConfig["objDvApi_COLLECTION_START"]["alias"])
        print('making request: %s' % strApiEndpoint)
        objHeaders = {
            "Content-Type": "application/json",
            "X-Dataverse-Key": self.strDATAVERSE_API_TOKEN
        }
        r = requests.request("GET", strApiEndpoint, headers=objHeaders)
        self.printResponseInfo(r)
        print("end viewCollectionContents")

    
    # @title Create a new dataset
    def createDataset(self):
        print("start createDataset")
        strApiEndpoint = '%s/api/dataverses/%s/datasets' % (self.strDATAVERSE_DOMAIN, self.objConfig["objDvApi_COLLECTION_START"]["alias"])
        print('making request: %s' % strApiEndpoint)
        objHeaders = {
            "Content-Type": "application/json",
            "X-Dataverse-Key": self.strDATAVERSE_API_TOKEN
        }
        r = requests.request("POST", strApiEndpoint, json=self.objConfig["objDvApi_DATASET_PART"], headers=objHeaders)  # this only creates a dataset placeholder with partial information
        # r = requests.request("POST", strApiEndpoint, json=self.objConfig["objDvApi_DATASET_FULL"], headers=objHeaders)  # full dataset properties not working (8/17)
        self.printResponseInfo(r)
        return r
        print("end createDataset")


    # @title Delete a dataset draft
    def deleteDatasetDraft(self, strDatasetId) -> None:
        print("start deleteDatasetDraft")
        strApiEndpoint = '%s/api/datasets/%s/versions/:draft' % (self.strDATAVERSE_DOMAIN, strDatasetId)
        print('making request: %s' % strApiEndpoint)
        objHeaders = {
            "X-Dataverse-Key": self.strDATAVERSE_API_TOKEN
        }
        r = requests.request("DELETE", strApiEndpoint, headers=objHeaders)
        self.printResponseInfo(r)
        print("end deleteDatasetDraft")

    
    # @title Upload a file to a dataset
    # @arguments objFile=JSON object defining the file for upload
    def addDatasetFile(self, objFile):
        # self.checkFileForUpload(strFileName,self.getWorkDirForPath(strLocalFilePath))  # check that we are ready for upload
        strApiEndpoint = '%s/api/datasets/:persistentId/add?persistentId=%s' % (self.strDATAVERSE_DOMAIN, objFile["strDvUrlPersistentId"])
        print(objFile)
        # --------------------------------------------------
        # Using a "jsonData" parameter, add optional description + file tags
        # --------------------------------------------------
        params = dict(description=objFile["strDataDescription"],
                    directoryLabel=objFile["strDirectoryLabel"],
                    fileName=objFile["strFileName"],
                    forceReplace="true",
                    categories=objFile["lstCatgories"])
        print("uploadFileToDv:",objFile["strFileName"],params)
        params_as_json_string = json.dumps(params)
        payload = dict(jsonData=params_as_json_string)
        fileobj = open(os.path.join(objFile["strUploadPath"],objFile["strFileName"]), 'rb')  # read the file
        objFilePost = {'file': (objFile["strFileName"], fileobj)}   # we have the new file object to save to the Dataverse
        objHeaders = {
            "X-Dataverse-Key": self.strDATAVERSE_API_TOKEN
        }
        print('making request: %s' % strApiEndpoint)
        r = requests.request("POST", strApiEndpoint, data=payload, files=objFilePost, headers=objHeaders)
        self.printResponseInfo(r)
        print("--end uploadFileToDv--")

    
    
    
    # @title General purpose method for printing response properties for testing
    # @argument r=response object from a requests.request()
    def printResponseInfo(self,r):
        print('-' * 40) # simple delineation so we know when this method is called in our output 
        print("json=",r.json())
        print("headers=",r.headers)
        print("response status=",r.status_code)
