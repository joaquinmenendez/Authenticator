import argparse
import pandas as pd
import os
import pickle as pkl 
import numpy as np
from sklearn.svm import SVC
from sklearn.externals import joblib
import sklearn


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()

    # Hyperparameters are described here. In this simple example we are just including one hyperparameter.
    parser.add_argument('--C', type=float, default= 1)
    parser.add_argument('--kernel', type=str, default='linear')
    parser.add_argument('--gamma', type= str, default='scale')
    parser.add_argument('--probability', type= bool, default= True)

    

    # Sagemaker specific arguments. Defaults are set in the environment variables.
    parser.add_argument('--output-data-dir', type=str, default=os.environ['SM_OUTPUT_DATA_DIR'])
    parser.add_argument('--model-dir', type=str, default=os.environ['SM_MODEL_DIR'])
    parser.add_argument('--train', type=str, default=os.environ['SM_CHANNEL_TRAIN'])

    args, unknown = parser.parse_known_args()

    # Take the set of files and read them all into a single pandas dataframe
    with open(os.path.join(args.train, "data.pickle"), 'rb') as handle:
        data = pkl.load(handle)

    # labels are in the first column
    train_y = data['label']
    train_X = data['data']

    # Now use scikit-learn's NN to train the model.
    model = SVC(C = args.C,
                    kernel= args.kernel,
                    gamma = args.gamma,
                    probability= args.probability
                )


    
    model = model.fit(train_X, train_y)

    # Print the coefficients of the trained classifier, and save the coefficients
    joblib.dump(model, os.path.join(args.model_dir, "model.joblib"))
    
def model_fn(model_dir):
    """Deserialized and return fitted model
    Note that this should have the same name as the serialized model in the main method
    """
    model = joblib.load(os.path.join(model_dir, "model.joblib"))
    return model

def predict_fn(input_data, model):
    """ Returns a dictionary with the probabilities and the prediction """
    pred = model.predict(input_data)
    prob = model.predict_proba(input_data)
    prediction = {"prediction":pred,"proba":prob}
    return prediction