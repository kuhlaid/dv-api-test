# @title This script takes care of installing extra modules if we need them.
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-cache-dir", package])

print("Installing the Notebook modules====>")
# =============== Below is the list of PIP packages we want installed
# If you do not need any of the following modules then you can skip running this script in your `_worker` script
install("Faker")    # this simply allows us to create fake data for our test files
install("pandas")   # lets us review dataset files easier
install("git+https://github.com/kuhlaid/DvApiMod5.13")  # this will install our custom Dataverse API Python plugin
install("ipywidgets")