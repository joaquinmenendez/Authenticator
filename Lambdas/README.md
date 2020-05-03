

## Containerization 

It seems that Amazon Cloud9 came with an **8GB** default size.
In order to expand this you should run a small bash script (`resize.sh`).
A more detailed description could be consulted on this [link](https://docs.aws.amazon.com/cloud9/latest/user-guide/move-environment.html).

```bash
bash resize.sh
```

### Create the virtual environment
```bash
virtualenv .myenv
source .myenv/bin/activate
make install
```

### Configuration

We  used our own personal bucket (`video-facerecogproj`) for this project. 
In case that you wanted to replicate this project create a new bucket and write the **access** and **secret** keys into a json file like this:
```json
{"AWS_ACCESS_KEY_ID" : "---",
"AWS_SECRET_ACCESS_KEY" : "---",
"REGION_NAME" : "---",
"BUCKET_NAME" : "---"}
```
If you don't know how to obtain these credentials check this [tutorial](https://preventdirectaccess.com/docs/amazon-s3-quick-start-guide/)
The policy we used is in [`configuration_s3.json`](https://raw.githubusercontent.com/joaquinmenendez/Facial_Recognition_Pipeline/master/multimedia/configuration_s3.json?token=AKLBVDXAUB7C5CAKASBDOEC6VD47Q)

**Lambda**
This Lambda function tooks a video in a bucket and generates images in a .jpg format in the same Bucket.
The lambda function can be called with a POST request.
The folder `Lambdas` contains the `getVideo.py` script that goes inside the Lambda function,
a bash script `call_getVideo.sh` to send the POST request and a JSON file with the fields you must complete to run the POST.

Skeleton of the JSON file: 
```json
{
"AWS_ACCESS_KEY_ID" : " ",
"AWS_SECRET_ACCESS_KEY" : " ",
"REGION_NAME" : "us-east-1",
"BUCKET_NAME" : " ",
"PERSON_NAME" : " ",
"KEY" : " ",
"ROTATE" : "ROTATE_90_CLOCKWISE",
"MOD_NUM" : 5 
}
```


**Tutorials**
- [Creating layers for Lambda Function](https://medium.com/@avijitsarkar123/how-lambda-layer-reduced-my-deployment-package-size-b571ebff79f1)<br>
- [Configurate POST Request](https://docs.aws.amazon.com/apigateway/latest/developerguide/integrating-api-with-aws-services-lambda.html#api-as-lambda-proxy-expose-post-method-with-json-body-to-call-lambda-function)<br>
- [Create and test API getaway](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-create-api-as-simple-proxy-for-lambda.html#api-gateway-create-api-as-simple-proxy-for-lambda-test) <br>
