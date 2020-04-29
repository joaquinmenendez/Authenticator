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
import pickle
import json
import shutil




# Initialize variables.
# Create tmp folder with train and test         !!!!!!!!!!!!!

# I did this already on `app.py` but just in case
app = Flask(__name__, static_url_path="/tmp", static_folder = "tmp")
app.secret_key = "secret key"  # Flask ask me for a key.
app.config['UPLOAD_FOLDER'] = './tmp'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 mb

ALLOWED_IMAGES = set(['jpg'])  # Files allowed (check if PNG could work )
ALLOWED_VIDEOS = set(['mp4'])  
MODEL = InceptionResnetV1(pretrained='vggface2').eval() #Preload the resnet



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

train_post = [
                {
                "file": None,
                "path": None,
                "name": "Joaquin",
                "role": "Accesso",
                "rotate": "ROTATE_90_COUNTERCLOCKWISE"
                }
            ]


@app.route('/train')
def train_page():
    return render_template('train.html')


@app.route('/train', methods=['POST'])
def upload_video():
    global train_post
    if request.method == 'POST':  # Check if the post request has the file part
        file = request.files['file']
        print(file)
        ######## HARDCODING CHANGE THIS LATER
        #  train_post[0]
        ############### HARCODED
        if file and allowed_file(file.filename, ALLOWED_VIDEOS):
            ### CREATE A NEW SLOT ON TRAIN POST(SEE PARAMETERS ABOVE)
            ### MAYBE UPDATE A COUNTER FOR EVERY VIDEO UPLOADED
            train_post[0]['file'] = secure_filename(file.filename)  # Get file name
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'train/videos', train_post[0]['file']))  # Save file on tmp folder
            flash(f'{ train_post[0]["file"]} successfully uploaded')
            train_post[0]["path"] = os.path.join(app.config['UPLOAD_FOLDER'], 'train/videos', train_post[0]['file'])  # Store the path
            return redirect('/train')
        else:
            flash(f'Cannot upload {file.filename} \n Allowed file types are: jpg')
            return redirect(request.url)

###############################################################################################################################*
# Uploading files


@app.route('/preprocess')
def upload_to_bucket():
    global train_post
    #Took videos all videos uploaded
    videos = os.listdir('tmp/train/videos')
    for vid in videos:
        # Split to frames
        vid_path = os.path.join('tmp/train/videos', vid)
        name = get_from_dict(vid,'file', train_post)["name"]
        rotate = get_from_dict(vid,'file', train_post)["rotate"]
        video2frame(vid_path,name, output_file='tmp/train/frames', rotate=rotate)
        # Crop the faces from the frames
    frames = os.listdir('tmp/train/frames')
    for frame in frames:
        cropFace(os.path.join('tmp/train/frames', frame),
                 os.path.join('tmp/train/faces', frame))
    # Zip all faces to allow user to download them                 
    shutil.make_archive('tmp/zip_files/faces', 'zip', 'tmp/train/faces')
    return render_template('preprocess.html')


@app.route('/embedding')
def embedding():
    keys_path = os.listdir('tmp/keys/s3')[0]  # Assuming an unique file
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
    #Upload the pickle object to the bucket                                                       ############### This should be choosen by the user
#    upload_location = 'DESDE_FLASK/Embeddings'
#    uploadAll('tmp/train/embeddings', upload_location, os.path.join('tmp/keys/s3', keys_path))
    return render_template('embedding.html')


@app.route('/loading')
def loading_SG(): 
    return render_template('loading.html')

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
    global filename  # maybe there is a better way than using global, but it's the easier way now
    global test_posts
    test_posts['file'] = None  # Remove older files uploaded
    if request.method == 'POST':  # Check if the post request has the file part
        file = request.files['file']
        if file and allowed_file(file.filename, ALLOWED_IMAGES):
            test_posts['file'] = secure_filename(file.filename) 
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], test_posts['file']))
            flash(f'{ test_posts["file"]} successfully uploaded')
            test_posts["path"] = os.path.join(app.config['UPLOAD_FOLDER'], test_posts['file'])  # Plot the file uploaded
            return redirect(request.url)
        else:
            flash(f'Cannot upload {file.filename} \n Allowed file types are: jpg')
            return redirect(request.url)
# Will need a button here to say 'Test this person'

#############################################################################################################################
outputs_post = {
				"file" : None,
                "path": None,
                "name": None,
                "accuracy": None,
                "role": None
                }


@app.route('/output')
def output():
    global outputs_post
    outputs_post["file"] = test_posts['file'] # set the file
    outputs_post["path"] = test_posts['path'] # set the file
    try:
        # embedding = preProcessPhoto(f'tmp/{outputs_post["file"]}',MODEL)
        key_sage = os.path.join('tmp/keys/sagemaker', os.listdir('tmp/keys/sagemaker')[0])
        post_response = testPhoto(outputs_post["path"], keys=key_sage, model=MODEL)
        outputs_post['name'] = post_response['prediction']
        outputs_post['accuracy'] = post_response['proba']
        outputs_post['role'] = get_role(outputs_post['name'], train_post)["role"]
        return render_template('/output.html', posts=outputs_post)
    except: 
        outputs_post["name"] = 'ERROR'
        return render_template('/output.html', posts=outputs_post)

def get_role(name, train_post):
    '''
    Search for a name in a list of dictionaries
    :return:
    res (dict): Dictionary that matches the name
    '''
    res = None
    for sub in train_post: 
        if sub['name'] == name: 
            res = sub 
            return res


def get_from_dict(value, parameter, list_dict):
    '''
    Search in a list of dictionaries.
    Finds the dictionary which parameter match a value. 
    :Arguments:
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
        assert False, 'No dictionary matches the value entered. Please check for errors or None types'

##############################################################################################################################


# Useful also to visualize locally
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)














# Viejo no sirve mas

@app.route('/upload')
def uploaded():
    path = 'tmp/train/faces'
    upload_location = 'DESDE_FLASK/Faces'                                      ############### This should be choosen by the user
    keys_path = os.listdir('tmp/keys/s3')[0]  # Assuming an unique file
    uploadAll(path, upload_location, os.path.join('tmp/keys/s3',keys_path))
    return render_template('upload.html')
