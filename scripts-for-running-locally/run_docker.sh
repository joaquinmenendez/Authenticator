#!/bin/bash
docker run &&\
-p 8888:8888 &&\
-e GRANT_SUDO=yes &&\
--user root &&\
-v ${PWD}:/pytorch_docker &&\
pytorch/pytorch