# @title This script takes care of installing extra modules if we need them.
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# =============== Below is the list of PIP packages we want installed
# If you do not need any of the following modules then you can skip running this script in your `_worker` script
install("Faker")    # this simply allows us to create fake data for our test files
install("curlify")  # this allows us to see the CURL equivalent to the API requests we perform so we can send them to Dataverse support if needed
install("DvApiMod_pip_package @ git+https://github.com/kuhlaid/DvApiMod5.13.git") # this will install our custom Dataverse API Python plugin
