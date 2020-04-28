import pandas as pd
from flask import Flask, render_template, request, flash, redirect, url_for
import os
from facenet_pytorch import InceptionResnetV1
from werkzeug.utils import secure_filename
from preProcessPhoto import preProcessPhoto
from testPhoto import testPhoto
import json


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
train_post = {
                "file": None,
                "path": None,
                "name": None,
                "role": None
            }


@app.route('/train')
def train_page():
    return render_template('train.html', posts=train_post)


@app.route('/train', methods=['POST'])
def upload_video():
    global train_post
    if request.method == 'POST':  # Check if the post request has the file part
        file = request.files['file']
        print(file)
        if file and allowed_file(file.filename, ALLOWED_VIDEOS):
            train_post['file'] = secure_filename(file.filename)  # Get file name
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'train/videos', train_post['file']))  # Save file on tmp folder
            flash(f'{ train_post["file"]} successfully uploaded')
            train_post["path"] = os.path.join(app.config['UPLOAD_FOLDER'], 'train/videos', train_post['file'])  # Store the path
            return redirect('/train')
        else:
            flash(f'Cannot upload {file.filename} \n Allowed file types are: jpg')
            return redirect(request.url)

###############################################################################################################################*
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
        post_response  = testPhoto(outputs_post["path"], keys=key_sage , model=MODEL)
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



##############################################################################################################################


# Useful also to visualize locally
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)