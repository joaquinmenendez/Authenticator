# Dockerfile to build our container
#Base image 
FROM pytorch/pytorch
USER root

# Working Directory
WORKDIR /pytorch_docker

# Copy source code to working directory
COPY . draft.py /pytorch_docker/

# Install packages from requirements.txt and github

RUN pip install --upgrade pip &&\
    pip install -r requirements.txt &&\
    pip install git+git://github.com/PnS2019/pnslib.git 
#Espose a port(just in case we want to run an app in the future)

EXPOSE 8080
