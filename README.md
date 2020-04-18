# Facial_Recognition_Pipeline
A facial recognition pipeline using AWS Sagemaker

## Containerization 

It seems that Amazon Cloud9 came with an **8GB// default size.
In order to expand this you should run a small bash script (`resize.sh`).
A more detailed description could be consulted on this [link](https://docs.aws.amazon.com/cloud9/latest/user-guide/move-environment.html).

### Virtual environment
```bash
virtualenv .myenv
source .myenv/bin/activate
make install
```

### Docker container (need to finish run_docker)

```bash
docker pull pytorch/pytorch
bash run_docker.sh
```

## Functions 
**Step by step**
1) uploadBucket.py (need to write)
2) downloadBucket.py
3) video2frame.py
4) faceRecognition.py (need to write)
    

