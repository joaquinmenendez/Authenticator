import argparse
from facenet_pytorch import InceptionResnetV1
from PIL import Image
import torchvision.transforms as transforms
import json
import numpy as np

parser = argparse.ArgumentParser()  # Parser for command-line options
parser.add_argument("file", help="Directory with the users and cropped images", type=str)
parser.add_argument("--tensor", help="Returns embeddings as tensor, instead of numpy arrays", type=bool)


def embeddings(file, model, tensor=False):
    """
    Creates an embedding of the image in the file
    Args:
        file (str): Directory of the image

    Returns:
        embeddings (obj): Returns the embedding of the image in a numpy array or tensor 

    """
    #model = InceptionResnetV1(pretrained='vggface2').eval()  # I am calling this from preProcessPhoto.py
    img = Image.open(file).convert('RGB')
    img_tensor = transforms.functional.to_tensor(img)
    embedding = model(img_tensor.unsqueeze(0))[0]
    if not tensor:
        embedding = embedding.detach().numpy()
    dic = {}
    dic["data"] = embedding
    #print ('Embeddings calculated')
    return dic


def main():
    args = parser.parse_args()
    return embeddings(args.file, args.tensor)


if __name__ == "__main__":
    main()