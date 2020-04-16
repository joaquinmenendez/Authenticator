install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt &&\
	pip install --no-cache-dir torch &&\
	pip install git+git://github.com/PnS2019/pnslib.git &&\
	pip install -q -U imutils git+https://github.com/the-house-of-black-and-white/hall-of-faces.git

all: install