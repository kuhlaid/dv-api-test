from faker import Faker
from faker.providers import profile
import datetime, ipywidgets as widgets, json, logging, os, requests, shutil, time, zipfile
import pandas as pd
from functools import partial
from pandas import DataFrame
from os.path import exists
from DvApiMod_pip_package import ObjDvApi # pull in the Dataverse API functions from our external file that we installed
from IPython.display import HTML, display, clear_output

handler = logging.StreamHandler()  # event logging (this needs to be outside the class otherwise it will create duplicate instances)

def ClearOutput(strNotice=""):
    '''
    Run this function to 'reset' any code output and replace it with the `strNotice` value.

     Parameters
     ----------
     strNotice : string (Any string such as "Your configuration is complete" to use for replacing code output.)
    '''
    clear_output(wait=True)
    print(strNotice)

    
class ConfigCheck:
    '''
    This object handles checking the Notebook configuration for valid Dataverse API settings.
    '''
    def __init__(self,strConfigFile):
        '''
        This method initializes our Notebook configuration validator.

         Parameters
         ----------
         strConfigFile : string ("_config_dataverseTest.json" the filename we will give to our Notebook configuration)
        '''
        self.blnApiConfig = False
        self.strConfigFile=strConfigFile
        blnConfigExisting = self.blnConfigExisting(strConfigFile)  # check if the configuration file exists
        if (not blnConfigExisting):
            shutil.copyfile("example._config_dataverseTest.json", strConfigFile)# create a copy of the existing config file
            blnConfigExisting = self.blnConfigExisting(strConfigFile)
        if (blnConfigExisting): # check again for the config file
            self._config = self.validJson(strConfigFile, True)
            ClearOutput("The Notebook has finished installing required modules")
        self.checkDataverseToken()


    def checkDataverseToken(self):
        '''
        This method queries the Dataverse API to simply check the token expiration and verify the configuration is correct for the Dataverse API.
        '''
        # ClearOutput() # NOTE: DO NOT run ClearOutput after the `input()` function is called otherwise the input() will not be visible the next time it is run (so we need to keep showing the output at this point until the configuration is valid)
        strApiEndpoint = '%s/api/users/token' % self._config["_cc__strDvApi_DOMAIN"]
        # print('making request: %s:%s' % (strApiEndpoint, self._config["_cc__strDvApi_TOKEN"]))
        objHeaders = {
            "Content-Type": "application/json",
            "X-Dataverse-Key": self._config["_cc__strDvApi_TOKEN"]
        }
        r = requests.request("GET", strApiEndpoint, headers=objHeaders) # it is nice I can simply send the JSON object without the need to create a separate JSON file
        rObj = r.json()
        if "ERROR" not in rObj["status"]:
            self.blnApiConfig=True
            with open(self.strConfigFile, mode='w') as objConfig: # save any config changes
                objConfig.write(json.dumps(self._config, indent=2))
                objConfig.close() # *** WE MUST CLOSE THE FILE AFTER CREATING IT OTHERWISE WE WILL NOT BE ABLE TO OPEN THE FILE FOR UPLOAD ***
            ClearOutput("Your Dataverse API configuration looks good")
        else:
            self.createDvConnectionForm() # there was an error with the Dataverse API configuration so we load the configuration form
            

    def createDvConnectionForm(self):
        '''
        Build a simple form to update the Notebook configuration before checking the connection to the Dataverse API.
        '''
        print("You Notebook configuration is incorrect. Please enter a valid Dataverse API token and domain below.")
        print("Dataverse API token currently set:",self._config["_cc__strDvApi_TOKEN"])
        print("Dataverse domain currently set:",self._config["_cc__strDvApi_DOMAIN"])
        txtToken=input('Dataverse API token:')
        # txtDomain=input('Dataverse domain:')
        # self._config["_cc__strDvApi_DOMAIN"]=txtDomain
        self._config["_cc__strDvApi_TOKEN"]=txtToken
        self.checkDataverseToken()
       

    def blnConfigExisting(self, strConfigFile):
        '''
        Check if the configuration file exists.
        '''
        return os.path.isfile(strConfigFile)
    

class Worker:
    '''
    This object handles our Notebook code after configuration is complete.
    '''
    def __init__(self,strConfigFile):
        '''
        This method initializes our Worker object.

         Parameters
         ----------
         strConfigFile : string ("_config_dataverseTest.json" the filename we gave the Notebook configuration)
        '''
        self._config = self.validJson(strConfigFile, True)  # read the notebook configuration settings and check for a valid JSON configuration file
        self.eventLogger()
        self.ObjDvApi = ObjDvApi(self._config) # here we pass our notebook configuration to the ObjDvApi module and extend the functionality of this object with the ObjDvApi object
        self.resetUploadPath()
        self.objDatasetMetaPath = os.path.join(self._config["_cc__strWORKING_DIR"],"_cc__DvDatasetMetadata.json")
        self.logger.info("Finished installing and importing modules for the "+strConfigFile+" environment")
        # it is a good idea to end your functions with a print statement so you can visually see when the function ends in the notebook output


    def resetUploadPath(self):
        '''
        Anytime we are doing things with files with regards to upload path, we need to run this method to reset the path to default upload path so we do not inadvertently use a path for a file that is not applicable.
        '''
        self.strUploadPath = self._config["_cc__strWORKING_DIR"]+self._config["_cc__strLOCAL_UPLOAD_DIR"] # creating this because we will reuse it several places

    
    def createCollection(self, strInit):
        '''
        This method sends our Dataverse Collection information to the DvApiMod_pip_package.

         Parameters
         ----------
         strInit : string (name of the object within our _config file which defines our Dataverse Collection properties)
        '''
        self.ObjDvApi.createCollection(self._config[strInit])  # initialize a new collection


    def viewCollection(self, strInit):
        '''
        View a new Dataverse collection based on the collection alias.

         Parameters
         ----------
         strInit : string (name of the object within our _config file which defines our Dataverse Collection properties)
        '''
        self.ObjDvApi.viewCollection(self._config[strInit]["alias"])  # view collection based on the alias


    def deleteCollection(self, strInit):
        '''
        Delete a new Dataverse collection based on the collection alias.

         Parameters
         ----------
         strInit : string (name of the object within our _config file which defines our Dataverse Collection properties)
        '''
        self.ObjDvApi.deleteCollection(self._config[strInit]["alias"])  # delete collection based on the alias

 
    def viewCollectionContents(self, strInit):
        '''
        List Dataverse collection contents based on the collection alias.

         Parameters
         ----------
         strInit : string (name of the object within our _config file which defines our Dataverse Collection properties)
        '''
        self.ObjDvApi.viewCollectionContents(self._config[strInit]["alias"])  # list collection contents based on the alias
  

    def eventLogger(self):
        '''
        This will set our system logging messages, which can be turned off in the configuration if desired.
        '''
        formatter = logging.Formatter(datetime.datetime.fromtimestamp(time.time()-14400).strftime('%Y-%m-%d %H:%M:%S EST') + ' %(name)s [%(levelname)s] %(message)s') # define how we want to messages formatted (starting with the current time, script name, type of message, and message
        handler.setFormatter(formatter)
        if self._config["_cc__blnSHOW_DEBUG_STATEMENTS"]:  # if we have debugging output enabled in our configuration then turn it on
            logging.getLogger().addHandler(handler) # add it to the root logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel('INFO') # this needs to be here but the level does not matter
              

    def createSampleData(self):
        '''
        Generate fake data for testing.
        '''
        fake = Faker('en_US')
        fake.add_provider(profile)
        lstProfiles = []
        for _ in range(5):  # create five fake profile records 
            lstProfiles.append(fake.profile(['name','username','address','mail']))
        return lstProfiles


    def get_nested(self, data, keys):
        '''
        Takes keys in a format like 'a.b.c' to more easily access dict/object properties dynamically.
        
         Parameters
         ----------
         data : object/dict
         keys : string (format like 'a.b.c' where each property in the tree is separated by a `.`)
        '''
        if isinstance(keys, str):
            keys = keys.split('.')
        temp = data
        for key in keys:
            try:
                temp = temp[key]
            except (TypeError, KeyError):
                return None
        return temp
    
    
    def removeTempArchive(self,strFilePath):
        '''
        Remove the archive we create as a temporary placeholder when building zip files.
        
         Parameters
         ----------
         strFilePath : string (path to the file we wish to delete)
        '''
        print("removeTempArchive")
        isExisting = os.path.isfile(strFilePath)  # check if archive exists
        if (isExisting):
            print("removing temp archive "+strFilePath)
            os.remove(strFilePath)    # remove temp archive
            time.sleep(0.5) # try to ensure the archive is removed before moving on
        print("end removeTempArchive")


    def createZipFile(self, strZipConfig):
        '''
        Create an archive file. Remove the old file first if one exists in the event it may be corrupted.
        
         Parameters
         ----------
         strZipConfig : string (reference to the zip file object name defined in the Notebook _config)
        '''
        self.logger.info("start createZipFile")
        if not os.path.exists(self.strUploadPath):
            os.mkdir(self.strUploadPath)
        filePath=self.strUploadPath
        zp=os.path.join(self.strUploadPath,self._config[strZipConfig]["strFileName"]) # zip path
        self.removeTempArchive(zp)
        zpFolderName = self._config[strZipConfig]["strFileName"].replace(".zip", "")
        zpFolderPath=os.path.join(self.strUploadPath,zpFolderName)
        if not os.path.exists(zpFolderPath):  # create folder for archive files
            os.mkdir(zpFolderPath)
        self.strUploadPath = zpFolderPath
        self.createTextFiles(strZipConfig+".files")  # create archive contents 
        isExisting = os.path.isfile(zp)  # check if the archive exists
        if (not isExisting):
            print("create zip archive for",zpFolderName)
            shutil.make_archive(os.path.join(os.getcwd(),filePath,zpFolderName), 'zip', root_dir=os.path.join(os.getcwd(),filePath,zpFolderName), base_dir="") # this only archives the files found within the archive directory
            # shutil.make_archive(os.path.join(os.getcwd(),filePath,zpFolderName), 'zip', root_dir=os.path.join(os.getcwd(),filePath), base_dir=zpFolderName) # this includes the directory AND files under that directory within archive, but we only want the files for our example

        # Wait for the zip file to be fully written (check file size)
        initial_size = 0
        while True:
            try:
                current_size = os.path.getsize(zp)
                if current_size == initial_size and current_size > 0:
                    break  # File size has stabilized, assuming zipping is done
                else:
                    initial_size = current_size
                    time.sleep(0.1)  # Check every 100ms
            except FileNotFoundError:
                print("FileNotFoundError")
                time.sleep(0.1) #File not yet created, wait and check again
        
        try: # make sure we can access the zip file content
            with zipfile.PyZipFile(zp, 'r') as myzip:
                for obj in self._config[strZipConfig]["files"]:
                    if obj["strFileName"] not in myzip.namelist():  # check if a file exists within the zip archive
                        raise RuntimeError("***ERROR: Missing file "+obj["strFileName"]+" in the "+zpFolderName+".zip archive***")
        except FileNotFoundError:
            print("Error: One or more files not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
    
        
        self.resetUploadPath()
        print("it looks like the zip file was created successfully")
                    

    def doubleZip(self, strZipConfig):
        '''
        Zip (archive) files uploaded to the Dataverse are treated differently depending on whether the zip is "double zipped" or not. Double zipping a file will prevent the Dataverse from extracting the archive contents when it is uploaded to a dataset. If you do not double zip an archive then the archive contents will unzip when uploaded to the Dataverse and only the archive  contents will be listed in the dataset (not the zip file itself). However, once a double zipped file is uploaded to a Dataverse dataset, it is conveted to single zipped (so anyone downloading the file will receive a single zipped file). Keep this in mind when working with archive files to decide if you need to double zip your archive or not.
    We will name double zipped files `.zip.zip` to distinguish between single zip `.zip`.
        
         Parameters
         ----------
         strZipConfig : string (reference to the zip file object name defined in the Notebook _config)
        '''
        print("start doubleZip")
        zp=os.path.join(self.strUploadPath,self._config[strZipConfig]["strFileName"]) # zip path
        self.removeTempArchive(zp+".tmpzip")  # remove temp archive
        with zipfile.PyZipFile(zp+".tmpzip", 'w') as myzip1:  # create a placeholder temporary file first
            pass
        with zipfile.PyZipFile(zp+".tmpzip", 'w') as myzip2:  # double zip the file into a temporary zip
            myzip2.write(zp,self._config[strZipConfig]["strFileName"]+".zip")
            time.sleep(0.5) # try to ensure the archive is created before moving on
            pass
        shutil.copyfile(zp+".tmpzip", zp+".zip") # finally we copy the double-zipped archive temp file to the main archive
        self.removeTempArchive(zp+".tmpzip") # we remove the temp zip file
        print("end double zip")
            

    def createTextFiles(self, strTestList):
        '''
        Generate text files for the dataset.
        
         Parameters
         ----------
         strTestList : string (reference to the list of files defined in the Notebook _config that we want created)
        '''
        self.logger.info("start createTextFiles")
        if not os.path.exists(self.strUploadPath):
            os.mkdir(self.strUploadPath)  # create file path if not exists for storing our sample data (this directory is included in the repository since creating directories through Python is not allowed in some environments and must be done manually)
        for obj in self.get_nested(self._config, strTestList):
            if "blnJsonToCsv" in obj and obj["blnJsonToCsv"] == "true":
                objJson = self.createSampleData() # create sample data and save to a CSV file
                pd.DataFrame.from_dict(objJson).to_csv(os.path.join(self.strUploadPath,obj["strFileName"]), index=False)
                self.logger.info("created file: "+obj["strFileName"])
            else:
                with open(os.path.join(self.strUploadPath,obj["strFileName"]), mode='w') as objFile:
                    objFile.write(json.dumps(self.createSampleData(), indent=2))
                    objFile.close() # *** WE MUST CLOSE THE FILE AFTER CREATING IT OTHERWISE WE WILL NOT BE ABLE TO OPEN THE FILE FOR UPLOAD ***
                self.logger.info("created file: "+obj["strFileName"])
        self.logger.info("end createTextFiles")


    def deleteDataset(self):
        '''
        Delete the dataset defined for this notebook (we cannot call deleteDatasetDraft from the notebook since we need to pass the dataset ID to the method) .
        '''
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
        '''
        Retrieve the list of files from a dataset.
        
         Parameters
         ----------
         strVersion : string (reference to the version of a dataset we want to see the files for)
        '''
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


    def viewDatasetFiles(self, strVersion):
        '''
        Display dataset files.
        
         Parameters
         ----------
         strVersion : string (reference to the version of a dataset we want to see the files for)
        '''
        self.logger.info("start viewDatasetFiles")
        lstDataFiles = self.getDatasetFiles(strVersion)
        dfData = pd.DataFrame(lstDataFiles)
        if dfData.empty==True:
            print("It appears the dataset is empty. Try adding some files to the dataset first.")
        else:
            display(HTML(dfData[["id", "filename", "description"]].to_html())) # print out a nice table listing the files
        self.logger.info("end viewDatasetFiles")


    def createDataset(self, strCollection, strDatasetMetadata):
        '''
        Initiates the creation of a dataset.
        
         Parameters
         ----------
         strCollection : string (reference to the collection object within the Notebook _config)
         strDatasetMetadata : string (reference to the dataset metadata object within the Notebook _config)
        '''
        self.logger.info("start createDataset")
        r = self.ObjDvApi.createDataset(self._config[strCollection]["alias"], self._config[strDatasetMetadata])
        if r.status_code==201:
            objRJson = r.json()
            self.logger.info(r.json())
            with open(self.objDatasetMetaPath, mode='w') as jsonFile:
                objConfig = {"strAbout": "This file is used to store the dataset identifiers."}
                objConfig["strDvDATASET_ID"] = objRJson["data"]["id"]
                objConfig["strDvUrlPersistentId"] = objRJson["data"]["persistentId"]
                jsonFile.write(json.dumps(objConfig, indent=2))
        self.logger.info("end createDataset")


    def updateDatasetMetadata(self, strDatasetMetadata):
        '''
        Update the dataset metadata.
        
         Parameters
         ----------
         strDatasetMetadata : string (reference to the dataset metadata object within the Notebook _config)
        '''
        self.logger.info("start updateDatasetMetadata")
        self.readDvDatasetMetadata() # retrieve the dataset identifiers
        r = self.ObjDvApi.updateDatasetMetadata(self.objDatasetMeta["strDvUrlPersistentId"], self._config[strDatasetMetadata])
        if r.status_code==200:
            objRJson = r.json()
            self.logger.info(r.json())
        self.logger.info("end updateDatasetMetadata")


    def readDvDatasetMetadata(self):
        '''
        Read the basic dataset identity metadata.
        '''
        isExisting = os.path.isfile(self.objDatasetMetaPath)  # check if dataset description file exists
        if (isExisting):
            self.objDatasetMeta = self.validJson(self.objDatasetMetaPath, True)
        else:
            print("Run the createDataset() method first so the Notebook has the dataset details to work with.")
    

    def uploadFiles(self, strTestList):
        '''
        Upload files to the dataset.

         Parameters
         ----------
         strTestList : string (name of the object within our _config file which defines our list of files to upload)
        '''
        self.logger.info("start uploadFiles")
        self.readDvDatasetMetadata() # retrieve the dataset identifiers
        for objFile in self._config[strTestList]:  # for each test file
            self.prepFileUpload(objFile)
        self.logger.info("end uploadFiles")


    def prepFileUpload(self, objFile):
        '''
        Add files to the dataset.

         Parameters
         ----------
         objFile : dict (file metadata defined in the Notebook _config)
        '''
        objFile["strUploadPath"] = self.strUploadPath # we add a few extra properties to the object before sending it to the addDatasetFile method
        objFile["strDvUrlPersistentId"] = self.objDatasetMeta["strDvUrlPersistentId"]
        if objFile["strDvUrlPersistentId"] == "":
            raise RuntimeError("***ERROR: No dataset id found. Try running the createDataset method (there should be data in the _cc__DvDatasetMetadata.json file before uploading will work.***")
        # here we map our file metadata to the Dataverse API parameters for adding a file
        objParams = dict(description=objFile["strDataDescription"],
            directoryLabel=objFile["strDirectoryLabel"],
            fileName=objFile["strFileName"],
            categories=objFile["lstCatgories"])
        self.ObjDvApi.addDatasetFile(objFile,objParams) # we simply pass the objFile so we can use the configuration file to determine the elements linked to the object (spare us from altering the arguments of the addDatasetFile method


    def publishDatasetDraft(self, strCollection, strType="minor"):
        '''
        Publish a dataset.

         Parameters
         ----------
         strCollection : string (reference to the collection object within the Notebook _config)
         strType : string ("minor" or "major" version update)
        '''
        self.logger.info("start publishDatasetDraft")
        self.readDvDatasetMetadata() # retrieve the dataset identifiers
        objDatasetMeta = self.objDatasetMeta
        self.ObjDvApi.publishDatasetDraft(objDatasetMeta,strType, self._config[strCollection]["alias"])
        self.logger.info("end publishDatasetDraft")


    def createEmptyDatasetDraft(self):
        '''
        Create empty dataset draft. To create an empty draft we first must try adding a temporary file to the dataset. 
        '''
        self.logger.info("start createEmptyDatasetDraft")
        self.readDvDatasetMetadata() # retrieve the dataset identifiers
        # create an empty file for the dataset
        objFile = {
          "strFileName": "emptyFile.csv",
          "type": "application/octet-stream",
          "strDataDescription": "empty file",
          "strDirectoryLabel": "data/testing",
          "lstCatgories": []
        }
        pd.DataFrame.from_dict({}).to_csv(os.path.join(self.strUploadPath,objFile["strFileName"]), index=False)   
        self.prepFileUpload(objFile)  # add the empty file to the dataset
        lstDatasetFiles = self.getDatasetFiles(":draft") # retrieve the files currently found in the dataset draft
        for objFile in lstDatasetFiles:  # remove all of those files (now we can upload the files we want)
            if 'originalFileName' in objFile: # we must check for files (such as CSV) that are converted to TAB once they are uploaded to the Dataverse and use their original file name when comparing
                print("remove",objFile["originalFileName"])
                self.ObjDvApi.removeFile(objFile["id"])
            else:
                print("remove",objFile["filename"])
                self.ObjDvApi.removeFile(objFile["id"])
        self.logger.info("end createEmptyDatasetDraft")


    def validJson(self, strFilePath, blnReturn=False):
        '''
        Ensure we are working with a valid JSON file or our JSON file has not corrupted.

         Parameters
         ----------
         strFilePath : string (path to the file)
         blnReturn : boolean (whether we want to return the JSON object after validation passes)
        '''
        f = open(strFilePath, "r")
        try:
            objJson = json.loads(f.read()) # put JSON-data to a variable
            f.close()
            if blnReturn:
                return objJson
        except json.decoder.JSONDecodeError:
            raise RuntimeError("***ERROR: Invalid JSON for "+strFilePath+"***")
                