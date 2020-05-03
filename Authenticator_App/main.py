import pandas as pd
from flask import Flask, render_template, request, flash, redirect, url_for
import os
from facenet_pytorch import InceptionResnetV1
from werkzeug.utils import secure_filename
from uploadAll import uploadAll
from preProcessPhoto import preProcessPhoto
from embeddingFaces import embeddings
from video2frame import video2frame
from testPhoto import testPhoto
from cropFace import cropFace
from train_deploy_model import train_deploy_model
import pickle
import json
import shutil
import copy
import time

# Initialize directories
directories = ['keys','keys/s3', 'keys/sagemaker', 'test', 'train', 'train/faces',
               'train/frames', 'train/embeddings', 'train/videos', 'zip_files']
for d in directories:
    try:
        os.mkdir('tmp/' + d)
    except OSError as e:
        print('{} already exists'.format('tmp/' + d))

# Initialize variables
# I did this already on `app.py` but just in case
app = Flask(__name__, static_url_path="/tmp", static_folder="tmp")
app.secret_key = "secret key"  # Flask ask me for a key.
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 mb

ALLOWED_IMAGES = set(['jpg', 'jpeg'])  # Files allowed (check if PNG could work)
ALLOWED_VIDEOS = set(['mp4', 'mov'])

#GLOBAL VARIABLES
MODEL = InceptionResnetV1(pretrained='vggface2').eval()  # Preload the resnet
COUNTER = 0
DEPLOY = 0

# Handy functions
def allowed_file(filename, allowed):
    '''
    This function is used to determine if they uploaded file has the apropiate extension
    '''
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed


###############################################################################################################################
# Home page
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')  # This would be Iuliias page
###############################################################################################################################
# Train page

train_post = []

train_dict = {
                "file": None,
                "path": None,
                "name": None,
                "role": None,
                "rotate": None,
                "frames": None,
            }


@app.route('/train')
def train_page():
    return render_template('/train.html', posts=train_post)


@app.route('/train', methods=['POST'])
def upload_video():
    global train_pos
    global COUNTER
    app.config['UPLOAD_FOLDER'] = './tmp/train/videos'
    if request.method == 'POST':  # Check if the post request has the file part
        file = request.files['file']
        print(file)
        if file and allowed_file(file.filename, ALLOWED_VIDEOS):
            ### CREATE A NEW SLOT ON TRAIN POST(SEE PARAMETERS ABOVE)
            train_post.append(copy.deepcopy(train_dict))
            ### UPDATE PARMATERS AND COUNTER FOR EVERY VIDEO UPLOADED
            train_post[COUNTER]['file'] = secure_filename(file.filename)  # Get file name
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],  train_post[COUNTER]['file']))  # Save file on tmp folder
            flash(f'{ train_post[COUNTER]["file"]} successfully uploaded')
            train_post[COUNTER]["path"] = os.path.join(app.config['UPLOAD_FOLDER'], train_post[COUNTER]['file'])  # Store the path
            train_post[COUNTER]["name"] = request.form['fname']
            train_post[COUNTER]["role"] = request.form['frole'] 
            train_post[COUNTER]["frames"] = int(request.form['fframes'] )
            # check for rotation
            if request.form.get('frotate') is None: 
                train_post[COUNTER]["rotate"] = None
            else:
                train_post[COUNTER]["rotate"] = request.form.get('frotate')
            COUNTER += 1
            return redirect('/train')
        else:
            flash(f'Cannot upload {file.filename} \n Allowed file types are: jpg')
            return redirect(request.url)

###############################################################################################################################*
# Uploading files

@app.route('/preprocess')
def preprocessed():
    try:
        image = os.listdir('tmp/train/faces')[0]
    except:
        image = None
    return render_template('/preprocess.html', image = image)

@app.route('/preprocess/', methods=['POST'])
def preprocess():
    global train_post
    #Took videos all videos uploaded
    videos = os.listdir('tmp/train/videos')
    for vid in videos:
        # Split to frames
        print(vid)
        vid_path = os.path.join('tmp/train/videos', vid)
        print(vid_path)
        print(train_post) 
        name = get_from_dict(vid,'file', train_post)["name"]
        rotate = get_from_dict(vid,'file', train_post)["rotate"]
        frames = get_from_dict(vid,'file', train_post)["frames"]
        video2frame(vid_path,name, output_file='tmp/train/frames', rotate=rotate, mod_num=frames)
        print(f'{vid} finished. Moving to next video')
        # Crop the faces from the frames
    
    frames = os.listdir('tmp/train/frames')
    for frame in frames:
        cropFace(os.path.join('tmp/train/frames', frame),
                 os.path.join('tmp/train/faces', frame))
    # Zip all faces to allow user to download them                 
    shutil.make_archive('tmp/zip_files/faces', 'zip', './tmp/train/faces')
    return render_template('/train.html' , finish_preprocess=True , posts=train_post)


@app.route('/embedding')
def embedding():
    global DEPLOY
    if DEPLOY == 0:
        label_embedding = {'data':[], 'label':[]}
        path = 'tmp/train/faces'
        faces = os.listdir('tmp/train/faces')
        for face in faces:
            name = face.split('_')[0]
            #Embeed the faces. Returns a dictionary
            emb_dic = embeddings(os.path.join(path, face), MODEL)
            label_embedding['data'].append(emb_dic['data'])
            label_embedding['label'].append(name)
        # Save this dictionary as a binary object
        with open('tmp/train/embeddings/data.pickle', 'wb') as handle:
            pickle.dump(label_embedding, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return render_template('/embedding.html')
    if DEPLOY == 1:
        return render_template('/model_is_deploying.html')


@app.route('/embedding/' , methods = ["POST"])
def deploy():
    global DEPLOY
    if DEPLOY == 0:
        print('Training and deploying model')
        key = os.listdir('tmp/keys/sagemaker')[0]
        train_deploy_model(keys= os.path.join('tmp/keys/sagemaker',key))
        DEPLOY = 0
        return render_template('/deploy.html')
    else:
        return render_template('/model_is_deploying.html')


################################################################################################################################
# Test page


test_posts = {
            "file": None,
            "path": None
            }


@app.route('/test')
def test_page():
    return render_template('test.html', posts=test_posts)


@app.route('/test', methods=['POST'])
def upload_file():
    app.config['UPLOAD_FOLDER'] = './tmp/test'
    global test_posts
    test_posts['file'] = None  # Remove older files uploaded
    if request.method == 'POST':  # Check if the post request has the file part
        file = request.files['file']
        if file and allowed_file(file.filename, ALLOWED_IMAGES):
            test_posts['file'] = secure_filename(file.filename) 
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], test_posts['file']))
            flash(f'{ test_posts["file"]} successfully uploaded')
            test_posts["path"] = os.path.join('tmp/test', test_posts['file'])  # Plot the file uploaded
            return redirect(request.url)
        else:
            flash(f'Cannot upload {file.filename} \n Allowed file types are: jpg')
            return redirect(request.url)


#############################################################################################################################
# Output from Test


outputs_post = {
				"file" : None,
                "path": None,
                "name": None,
                "accuracy": None,
                "role": None,
                "cropface": None
                }


@app.route('/output')
def output():
    global test_posts
    global outputs_post
    global train_post
    outputs_post["file"] = copy.deepcopy(test_posts['file']) # set the file
    outputs_post["path"] = copy.deepcopy(test_posts['path']) # set the file
    outputs_post["cropface"] = 'tmp/test/Cropped_' + outputs_post["file"]  # set the file
    try:
        key_sage = os.path.join('tmp/keys/sagemaker', os.listdir('tmp/keys/sagemaker')[0])
        post_response = testPhoto(outputs_post["path"], keys=key_sage, model=MODEL)
    except: 
        outputs_post["name"] = 'ERROR'
        return render_template('output_error.html', posts=outputs_post)

    post_response = json.loads(post_response)  # Convert the string dictionary into a real dictionary
    print(post_response['prediction'][0])
    print('Train post: {}'.format(train_post))
    outputs_post['name'] = post_response['prediction'][0]
    outputs_post['accuracy'] = str(max(post_response['proba'][0])*100).format("{}%")
    # name = get_from_dict(vid,'file', train_post)["name"]
    outputs_post['role'] = get_from_dict(outputs_post['name'],'name', train_post)["role"]
    return render_template('output.html', posts=outputs_post)


def get_from_dict(value, parameter, list_dict):
    '''
    Search in a list of dictionaries.
    Finds the dictionary which parameter match a value. 
    :Arguments:
        value
        parameter (string) : The key that I want to use to retrieve.
        list_dict (list(dict)): a list with the different parameters of the videos uploaded
    :return:
    res (dict): The Object that matches the value.
    '''
    res = None
    for sub in list_dict: 
        if sub[parameter] == value: 
            res = sub 
            return res
##############################################################################################################################
# Reset 


@app.route('/reset')
def reset():
    global train_post
    global test_posts
    global outputs_post
    global COUNTER
    global DEPLOY
    DEPLOY = 0
    COUNTER = 0
    train_post = []
    test_posts =  {
                    "file": None,
                    "path": None
                  }
    outputs_post = {
                    "file": None,
                    "path": None,
                    "name": None,
                    "accuracy": None,
                    "role": None,
                    "cropface": None
                    }
    for file in os.listdir('tmp/train/faces'):
        os.remove('tmp/train/faces/' + file)
    for file in os.listdir('tmp/train/frames'):
        os.remove('tmp/train/frames/' + file)
    for file in os.listdir('tmp/train/videos'):
        os.remove('tmp/train/videos/' + file)
    for file in os.listdir('tmp/train/embeddings'):
        os.remove('tmp/train/embeddings/' + file)
    for file in os.listdir('tmp/test'):
        os.remove('tmp/test/' + file)
    for file in os.listdir('tmp/zip_files'):
        os.remove('tmp/zip_files/' + file)
    return render_template('/home.html')

# About


@app.route('/about')
def about():
    return render_template('about.html')


# Loader.io

@app.route('/loaderio-08edafe149fb3355c1d9948d4204dc92/')
def loader():
    return render_template('loaderio-08edafe149fb3355c1d9948d4204dc92.html')

# Run main 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)