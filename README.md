# Facial_Recognition_Pipeline
A facial recognition pipeline using AWS Sagemaker

```bash
virtualenv .myenv
source .myenv/bin/activate
make install
```
A different approach is using a Docker container

```bash
docker pull pytorch/pytorch
```

I found a solution for the space problem. It seems that Amazon Cloud9 came with
an 8GB default size. In order to expand this you should run a small bash script (`resize.sh`).
A more detailed description could be consulted on this [link](https://docs.aws.amazon.com/cloud9/latest/user-guide/move-environment.html).

# Last thing done 2:52 4/17/2020
Now we can run the virtualenv withut problems. 
I did not tried the docker container (despite it's not necessary it could be fancy to offer this possibility)
