import argparse
from embeddingFaces import embeddings
from cropFace import cropFace

parser = argparse.ArgumentParser()  # Parser for command-line options
parser.add_argument("file_path", help="Directory file of the image preprocess", type=str)

def preProcessPhoto(file_path, model):
    '''
    The function tooks a photo,  crops the face and get the embeddings for that face using resnet.
    :arguments:
        file_path (str) : The path where the image is stored
        model (facenet model): The model that will be used to embeed the faces.
        
    :return:
        j_embedding (JSON object): A JSON object with the following structure: {"body" : [embedding numpy array]}
    '''
    name_file = file_path.split('/')[-1]  # Get the name of the file
    print(f'Processing: {name_file}')
    cropFace(file_path, output_img = f'tmp/test/Cropped_{name_file}', color = 'RGB')  # Crop the face. color (str) : BGR is default in cropFace.py. Choose 'RGB' to overwrite"
    j_embedding = embeddings(f'tmp/test/Cropped_{name_file}', model=model, tensor=False)  # Get the embedding of the face
    return j_embedding


def main():
    args = parser.parse_args()
    preProcessPhoto(args.file_path)

if __name__ == '__main__':
    main()