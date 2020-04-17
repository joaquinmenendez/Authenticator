install:
	pip install --upgrade pip &&\
	pip install facenet_pytorch --no-cache-dir  &&\
	pip install torch --no-cache-dir torch &&\
	pip install -r requirements.txt &&\
	pip install git+git://github.com/PnS2019/pnslib.git 
	
all: install