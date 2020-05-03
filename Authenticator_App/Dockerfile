#From Image selected
FROM python:3.7.3-stretch

# Working Directory

WORKDIR /authentificator

# Copy source code to working directory

COPY . main.py /authentificator/

# Install packages from requirements.txt

RUN pip install --upgrade pip &&\
    pip install torch --no-cache-dir torch &&\
	pip install facenet_pytorch --no-cache-dir  &&\
    pip install -r requirements.txt

#Espose a port

EXPOSE 8080

CMD ["python", "main.py"]