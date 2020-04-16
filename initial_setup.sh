#!/bin/bash
# Simple script to create a venv and run the makefile

#sudo apt install virtualenv
python3 -m venv .venv
source .venv/bin/activate
make