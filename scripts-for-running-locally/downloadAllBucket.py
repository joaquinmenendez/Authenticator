import re
import os
import boto3
import argparse

parser = argparse.ArgumentParser() # Parser for command-line options
parser.add_argument("file", help="Directory with the users and cropped images",type=str)
parser.add_argument("bucket", help="Bucket name",type=str)
parser.add_argument("--keys", help="Amazon keys",type=bool)

def get_s3_keys(bucket, user_keys = None):
    """
    Get a list of keys in an S3 bucket.
    
    Args:
       bucket (str): Bucket name
       user_keys (str): Returns all keys from a bucket

    Returns:
       keys (list): List of keys
    
    """
    keys = []
    if user_keys is None:
    				s3 = boto3.client('s3')
    else:
        s3 = boto3.client('s3', 
                      aws_access_key_id = user_keys["AWS_ACCESS_KEY_ID"], 
                      aws_secret_access_key = user_keys["AWS_SECRET_ACCESS_KEY"], 
                      region_name = user_keys["REGION_NAME"]
                      )    	   
                      
    resp = s3.list_objects_v2(Bucket= bucket)
    for obj in resp['Contents']:
        keys.append(obj['Key'])
    return keys

def download_keys(file, bucket, user_keys = None ,verbose = False):
    """
	   Download all the keys in a list to file
	   
				Args:
       file (str): Name of the directory that contains all images 
       model (object): Model to do embeddings
       tensor (): Returns embeddings as tensor, instead of numpy arrays
    

    Returns:
       train (list): List of embbedings
       test (list): List of labels
				
    """
    if user_keys is None:
    				s3 = boto3.client('s3')
    else:
        s3 = boto3.client('s3', 
                      aws_access_key_id = user_keys["AWS_ACCESS_KEY_ID"], 
                      aws_secret_access_key = user_keys["AWS_SECRET_ACCESS_KEY"], 
                      region_name = user_keys["REGION_NAME"]
                      )   
              
    keys = get_s3_keys(bucket, user_keys = None)
    create_dirs(keys, file)
                      
    for i,key in enumerate(keys):
        if verbose:
            print(key)
        try:
            # download as local file
            s3.download_file(bucket, key, os.path.join(file,key))
        except:
        				raise
    return print("{} files were downloaded!".format(i))

def create_dirs(keys, file):
    """
	    Given a set of keys will create the needed files
    
    Args:
       bucket (str): Bucket name
       file (str): File to create all folders

    Returns:
       keys (list): List of keys
    
    """
    if not os.path.exists(file):
        os.mkdir(file)
        
    folders = [re.split("/", key)[:-1] for key in keys]
    unique_folders = [list(x) for x in set(tuple(x) for x in folders)]
    success = 0
    for folders in unique_folders:
        path = os.path.join(file,"/".join(folders))
        if not os.path.exists(path):
            os.makedirs(path)
            success += 1
    return print("{} Folders were created".format(success))
    
     
def main():
				args = parser.parse_args()
				download_keys(args.file, args.bucket, args.user_keys)

if __name__ == "__main__":
    main()