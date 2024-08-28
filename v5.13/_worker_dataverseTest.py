from faker import Faker
from faker.providers import profile
import json
import logging
import os
import pandas as pd
from pandas import DataFrame
# import shutil
from os.path import exists
from DvApiMod_pip_package import ObjDvApi # pull in the Dataverse API functions from our external file that we installed
from IPython.display import HTML, display
import time, datetime

handler = logging.StreamHandler()  # event logging (this needs to be outside the class otherwise it will create duplicate instances)

# @title By placing all of our Python function within a class object, it makes it much easier for information to be used across functions without needing to explicitly passing them into each function (instead we pass the entire Worker object into the functions so each function can do what it needs with the object)
class Worker:
    # @param strEnvironment (ex. demo or prod, would represent the environment you wish for the notebook code to run against)
    def __init__(self,strConfigFile):
        f = open (strConfigFile, "r") # read the notebook configuration settings
        self._config = json.loads(f.read())
        f.close()
        self.eventLogger()
        self.ObjDvApi = ObjDvApi(self._config) # here we pass our notebook configuration to the ObjDvApi module and extend the functionality of this object with the ObjDvApi object
        self.strUploadPath = self._config["strDOCKER_WORKING_DIR"]+self._config["strLOCAL_UPLOAD_DIR"] # creating this because we will reuse it several places
        self.objDatasetMetaPath = os.path.join(self._config["strDOCKER_WORKING_DIR"],"dvDatasetMetadata.json")
        self.logger.info("Finished installing and importing modules for the "+strConfigFile+" environment")
        # it is a good idea to end your functions with a print statement so you can visually see when the function ends in the notebook output


    # @title This will set our system logging messages, which can be turned off in the configuration if desired
    def eventLogger(self):
        # time.time()-14400 # this is a hack for Windows computers on EST time (4 hours or 14400 seconds behind)
        formatter = logging.Formatter(datetime.datetime.fromtimestamp(time.time()-14400).strftime('%Y-%m-%d %H:%M:%S EST') + ' %(name)s [%(levelname)s] %(message)s') # define how we want to messages formatted (starting with the current time, script name, type of message, and message
        handler.setFormatter(formatter)
        if self._config["blnSHOW_DEBUG_STATEMENTS"]:  # if we have debugging output enabled in our configuration then turn it on
            logging.getLogger().addHandler(handler) # add it to the root logger
        # fhandler = logging.FileHandler(filename=os.path.join(self._config["strDOCKER_WORKING_DIR"],'myapp.log'), mode='a')  # note that this file handler does not use the Formatter so the date/times are not included
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel('INFO') # this needs to be here but the level does not matter
              
                
    # @title Generate fake data for testing
    def createSampleData(self):
        fake = Faker('en_US')
        fake.add_provider(profile)
        lstProfiles = []
        for _ in range(5):  # create five fake profile records 
            lstProfiles.append(fake.profile(['name','username','address','mail']))
        # self.logger.info(lstProfiles)
        return lstProfiles


    # @title Generate files for the dataset
    def createTestFiles(self, strTestList):
        self.logger.info("start createTestFiles")
        if not os.path.exists(self.strUploadPath):
            os.mkdir(self.strUploadPath)  # create file path if not exists for storing our sample data
        for obj in self._config[strTestList]:
            if "blnJsonToCsv" in obj and obj["blnJsonToCsv"] == "true":
                objJson = self.createSampleData() # create sample data and save to a CSV file
                pd.DataFrame.from_dict(objJson).to_csv(os.path.join(self.strUploadPath,obj["strFileName"]), index=False)
            else:
                with open(os.path.join(self.strUploadPath,obj["strFileName"]), mode='w') as objFile:
                    objFile.write(json.dumps(self.createSampleData(), indent=2))
                    objFile.close() # *** WE MUST CLOSE THE FILE AFTER CREATING IT OTHERWISE WE WILL NOT BE ABLE TO OPEN THE FILE FOR UPLOAD ***
        self.logger.info("end createTestFiles")


    # @title Delete the dataset defined for this notebook (we cannot call deleteDatasetDraft from the notebook since we need to pass the dataset ID to the method) 
    def deleteDataset(self):
        self.logger.info("start deleteDataset")
        self.readDvDatasetMetadata()
        if self.objDatasetMeta["strDvDATASET_ID"] == "":
            raise RuntimeError("***ERROR: No dataset id found.***")
    
        self.ObjDvApi.deleteDatasetDraft(self.objDatasetMeta["strDvDATASET_ID"])
        with open(self.objDatasetMetaPath, mode='w') as jsonFile:
                objConfig = {"strAbout": ""}
                objConfig["strDvDATASET_ID"] = ""
                objConfig["strDvUrlPersistentId"] = ""
                jsonFile.write(json.dumps(objConfig, indent=2))
        self.logger.info("end deleteDataset")


    def getDatasetFiles(self, strVersion):
        self.logger.info("start getDatasetFiles")
        self.readDvDatasetMetadata()
        if self.objDatasetMeta["strDvDATASET_ID"] == "":
            raise RuntimeError("***ERROR: No dataset id found.***")
        objResponse = self.ObjDvApi.getDatasetFiles(self.objDatasetMeta["strDvDATASET_ID"], strVersion)
        lstDataFiles = []
        objJson = objResponse.json()
        for objData in objJson["data"]: # we need to extract the file details (such as ID)
            lstDataFiles.append(objData["dataFile"])
        return lstDataFiles
        self.logger.info("end getDatasetFiles")

        
    # @title View dataset files
    def viewDatasetFiles(self, strVersion):
        self.logger.info("start viewDatasetFiles")
        lstDataFiles = self.getDatasetFiles(strVersion)
        dfData = pd.DataFrame(lstDataFiles)
        display(HTML(dfData[["id", "filename", "description"]].to_html())) # print out a nice table listing the files
        self.logger.info("end viewDatasetFiles")


    # @title Initiates the creation of a dataset
    def createDataset(self):
        self.logger.info("start createDataset")
        r = self.ObjDvApi.createDataset()
        if r.status_code==201:
            objRJson = r.json()
            self.logger.info(r.json())
            with open(self.objDatasetMetaPath, mode='w') as jsonFile:
                objConfig = {"strAbout": "This file is used to store the dataset identifiers."}
                objConfig["strDvDATASET_ID"] = objRJson["data"]["id"]
                objConfig["strDvUrlPersistentId"] = objRJson["data"]["persistentId"]
                jsonFile.write(json.dumps(objConfig, indent=2))
        self.logger.info("end createDataset")


    # @title Read the dataset metadata
    def readDvDatasetMetadata(self):
        f = open(self.objDatasetMetaPath, "r")
        self.objDatasetMeta = json.loads(f.read())
        f.close()

    
    # @title Upload files to the dataset
    # @arguments strTestList="the list name in the configuration to use for uploading files"
    def uploadTestFiles(self, strTestList):
        self.logger.info("start uploadTestFiles")
        self.readDvDatasetMetadata() # retrieve the dataset identifiers
        for objFile in self._config[strTestList]:  # for each test file
            objFile["strUploadPath"] = self.strUploadPath # we add a few extra properties to the object before sending it to the addDatasetFile method
            objFile["strDvUrlPersistentId"] = self.objDatasetMeta["strDvUrlPersistentId"]
            self.ObjDvApi.addDatasetFile(objFile) # we simply pass the objFile so we can use the configuration file to determine the elements linked to the object (spare us from altering the arguments of the addDatasetFile method
        self.logger.info("end uploadTestFiles")

    
    # @title Publish a dataset
    def publishDatasetDraft(self, strType="minor"):
        self.logger.info("start publishDatasetDraft")
        self.readDvDatasetMetadata() # retrieve the dataset identifiers
        objDatasetMeta = self.objDatasetMeta
        objDatasetMeta["dv_alias"] = self._config["objDvApi_COLLECTION_START"]["alias"]
        self.ObjDvApi.publishDatasetDraft(objDatasetMeta,strType)
        self.logger.info("end publishDatasetDraft")


    # @title Delete files we no longer want to use in a new version of the dataset
    # @arguments strNewFileList="the list name in the configuration to use for defining the files we want in the dataset"
    def removeUnusedFiles(self,strNewFileList, strVersion):
        self.logger.info("start removeUnusedFiles")
        lstDatasetFiles = self.getDatasetFiles(strVersion)
        lstNewFiles = []
        for newFile in self._config[strNewFileList]:
            lstNewFiles.append(newFile["strFileName"])
        for objFile in lstDatasetFiles:
            if 'originalFileName' in objFile: # we must check for files (such as CSV) that are converted to TAB once they are uploaded to the Dataverse and use their original file name when comparing
                if objFile["originalFileName"] not in lstNewFiles:
                    print("remove",objFile["originalFileName"])
                    self.ObjDvApi.removeFile(objFile["id"])
            else:
                if objFile["filename"] not in lstNewFiles:
                    print("remove",objFile["filename"])
                    self.ObjDvApi.removeFile(objFile["id"])
        self.logger.info("end removeUnusedFiles")
                