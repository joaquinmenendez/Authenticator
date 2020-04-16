CMD:
    virtualenv .venv
    source .venv/bin/acivate

install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt

all: CMD , install