# Facial_Recognition_Pipeline
A facial recognition pipeline using AWS Sagemaker

## Containerization 

It seems that Amazon Cloud9 came with an **8GB** default size.
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

We are using our own personal bucket (`video-facerecogproj`) for this project. 
In case that you wanted to replicate this project create a new bucket and write the **access** and **secret** keys into a json file like this:
```json
{"AWS_ACCESS_KEY_ID" : "---",
"AWS_SECRET_ACCESS_KEY" : "---",
"REGION_NAME" : "---",
"BUCKET_NAME" : "---"}
```
If you don't know how to obtain these credentials check this [tutorial](https://preventdirectaccess.com/docs/amazon-s3-quick-start-guide/)
The policy we used is in [`configuration_s3.json`](https://raw.githubusercontent.com/joaquinmenendez/Facial_Recognition_Pipeline/master/multimedia/configuration_s3.json?token=AKLBVDXAUB7C5CAKASBDOEC6VD47Q)


**Step by step**<br>
The script `pipeline_local.sh` took a video, took a frame every *n* frames, select only the face and save it. as a .jpg file
