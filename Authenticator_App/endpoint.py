import argparse
import os
import numpy as np
import json
import io
import boto3

parser = argparse.ArgumentParser() # Parser for command-line options
parser.add_argument("array", help="Numpy array with cropped image",type=np.array)
parser.add_argument("--keys", help="Json with credential keys", type=str)
 
def np2npy(array):
    npy = io.BytesIO()
    np.save(npy, array)
    return npy
    
def endpointConnection(array, keys = None):
    with open(keys) as k:
        keys = json.load(k) 
    if array.shape[0] == 1:
        npy = np2npy(array)
    else:
        npy = np2npy(array.reshape(1,-1))
    npy.seek(0)
    if not keys:
        runtime = boto3.client('runtime.sagemaker') 
    else:
        runtime = boto3.client('runtime.sagemaker', 
                          aws_access_key_id = keys["AWS_ACCESS_KEY_ID"], 
                          aws_secret_access_key = keys["AWS_SECRET_ACCESS_KEY"], 
                          region_name = keys["REGION_NAME"]
                          )
    response = runtime.invoke_endpoint(EndpointName=keys["ENDPOINT_NAME"],
                                       ContentType = 'application/x-npy',
                                       Body=npy)
    return response['Body'].read().decode()

def main():
    args = parser.parse_args()
    endpointConnection(args.array, args.keys)

if __name__ == "__main__":
    main()