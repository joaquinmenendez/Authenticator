import argparse
import requests
import json

parser = argparse.ArgumentParser()  # Parser for command-line options
parser.add_argument("embedding", help="Embedding of a face", type=dict)

def APIcall(embedding):
    '''
    :Arguments:
        embedding (dict)
    :returns:
        Ideally a dictionary/json
    '''
    API_ENDPOINT = "https://axrjeb3ief.execute-api.us-east-1.amazonaws.com/test/predictimage"
    # Just in case I will need this in the future
    # API_KEY = ""
    data = {"data": embedding['embedding']}
    r = requests.post(url = API_ENDPOINT, data=data) 
    api_response = r.text 
    print(api_response)
    api_response_json = r.json()
    # I should choose what to construct for my outpu
    return api_response_json


def main():
    args = parser.parse_args()
    APIcall(args.embedding)


if __name__ == "__main__":
    main()