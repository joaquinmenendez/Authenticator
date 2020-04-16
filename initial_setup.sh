#!/bin/bash
# Simple script to create a venv and run the makefile

#sudo apt install virtualenv
virtualenv .venv
source .venv/bin/activate
make ./Makefile