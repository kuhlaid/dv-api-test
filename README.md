# README

This directory contains the Juptyer notebook and a framework for performing tests against the [Dataverse Project](https://dataverse.org/) API version 5.13. This framework simplifies common curation tasks into a reusable processes to help ensure quality assurance and is appropriate for curating any data to the Dataverse.

## Show me the action

To begin working with the Jupyter Notebook in this repository, simply click on the Binder icon below to create a virtual JupyterLab environment in your web browser. Then you can return to this README file within MyBinder or wherever you are reading this for further instruction.

[![MyBinder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/kuhlaid/dv-api-test/HEAD)

## Who is the audience?

Those who might want to use this code/Notebook are researchers or data curators who need to archive data within the [Dataverse Project](https://dataverse.org/). Reading further assumes you either know how to use a Jupyter notebook or at least some basic Python, or are willing to learn. Secondly these instructions assume you know how to use the Dataverse on a basic level; this will not be a tutorial on using the Dataverse (at least not extensively). You will also need to set up a Dataverse account on https://demo.dataverse.org/ or some other host (preferably on a demo site for testing purposes). If you only plan to use the Dataverse to publish one dataset and then never use it again, then this resource might not be for you. If you are publishing to the Dataverse regularly then you should consider using this tool to work with the Dataverse API (unless you already know your way around the Dataverse API).

## Why is this code/resource useful?

This resource was created to help simplify the use of the Dataverse API and also provide you with processes that you likely would not learn about unless you worked with the API extensively. The Dataverse API allows you to automate many of the processes that should not be performed manually if you are more than a one time user of the Dataverse. Having reproducible curation steps that can be automated can greatly increase the efficiency and quality assurance for your data curation. Also, the Dataverse API can be tricky to learn and the documentation can be confusing. On top of this, unless you are an applications analyst, the API documentation can be confusing and knowing which API to use or what development environment you should use can seem out of reach for the general public.

## What is included in this code repository?

A Jupyter notebook `dataverseTest.ipynb` is provided along with the code and instructions to work with the notebook.

## Using the notebook

I suggest loading this repository code into https://mybinder.org/ using the link at the top of this document; as of March 2025, MyBinder.org is a free service. *Note: As of this writing, Google Colab DOES NOT support the advanced configuration of this repository, so Colab is not the environment you want to use for this code.* 

For those wanting to run JupyterLab locally (due to the sensitivity of the data you are working with or some other reason) you can use the instructions within the `localJupyterLab` folder. 

Another option is to use Docker by running a container with the following command `docker run -it --name myDataverseApiTest --mount type=bind,source="$(pwd)",target="/home/jovyan/work" --add-host=host.docker.internal:host-gateway -p 10000:8888 quay.io/jupyter/scipy-notebook:latest`; this allows you to keep your data files locally on your computer but you need to run this command from a location where you data files are located AND this repository code needs to be in that same location/directory tree (which is not always optimal). Anyway, I'm not here to tell you which environment you have to use, but just providing some options I have worked with.

### Understanding the files used with the Notebook

I purposely do not embed the bulk of the Python code used for this Notebook, within the Notebook itself. For a heavily coded Notebook this simply makes the Notebook bulky and difficult to read. Also, separating the Notebook configuration from the Notebook allows you to keep your configuration secrets (such as API tokens) OUT OF your GitHub repository; *NEVER save your API tokens or secrets to your Notebook or within any file in your repository.*
