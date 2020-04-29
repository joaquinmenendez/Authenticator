from sagemaker.sklearn.estimator import SKLearn
import sagemaker
from sagemaker import get_execution_role
import boto3
import argparse
import json

parser = argparse.ArgumentParser() # Parser for command-line options
parser.add_argument("keys", help = "Name of the bucket to download from", type = str)
parser.add_argument("--instance", help = "Name of the video inside the bucket", type = str)
parser.add_argument("--instance_count", help = "Directory to store the video", type = int)
parser.add_argument("--endpoint_name", help = "Name of the endpoint in which to deploy the model", type = str) 
parser.add_argument("--model_path", help = "File with access keys", type = str) 
parser.add_argument("--hyperparms", help = "Hyperparameters for SVM", type = str) # Default is None
parser.add_argument("--bucket_name", help = "Bucket in which the data is stored", type = str)
parser.add_argument("--key_bucket", help = "Key of the pickle data with the data", type = str) 

def train_deploy_model(keys,
                  instance = 'ml.m4.xlarge', # Don't change this!
                  instance_count = 1, # Don't change this!
                  endpoint_name = "SVM-image-classifier-2020-04",
                  model_path = '/content/model/model.py',
                  bucket_name = 'video-facerecogproj',
                  key_bucket = 'data/data.pickle',
                  hyperparms = None):
  """
  This function trains a sagemaker model and deploys it.

    Args:
       keys (json): Json with credential keys
       instance (str): instance type to train model and deploy it
       instance_count (int): initial instance count for deploying the model
       model_path (str): Directory path where the model is located
       hyperparms (dictionary): Hyperparameters for SVM
    
    Returns:
       Print statement

  """
  with open(keys) as k:
    keys = json.load(k) 

  session = boto3.session.Session(aws_access_key_id = keys["AWS_ACCESS_KEY_ID"], 
                            aws_secret_access_key = keys["AWS_SECRET_ACCESS_KEY"], 
                            region_name = keys["REGION_NAME"])
  
  #sagemaker_session = sagemaker.local.LocalSession(boto_session = session)
  sagemaker_session = sagemaker.Session(boto_session = session)

  sklearn = SKLearn(
      entry_point = model_path,
      train_instance_type= instance,
      #train_instance_type='local',
      role = keys['ROLE'],
      sagemaker_session=sagemaker_session,
      hyperparameters= hyperparms
  )
  ## Data for training 
  inputs = sagemaker_session.upload_data(path='data', key_prefix=key_bucket, bucket=bucket_name)
  ## Training the model
  sklearn.fit({'train': inputs})
  ## Deploying the model
  predictor = sklearn.deploy(initial_instance_count = instance_count,
                            instance_type= instance,
                            endpoint_name = endpoint_name,
                            update_endpoint = True
                                )
  return print("Endpoint updated: {}".format(endpoint_name))

def main():
    args = parser.parse_args()
    train_deploy_model(args.keys,args.instance,args.instance_count,
                       args.endpoint_name,args.model_path,args.bucket_name,
                       args.key_bucket,args.hyperparms)

if __name__ == "__main__":
    main()
