import pandas as pd
from flask import Flask, render_template, request, flash, redirect 
import os
from facenet_pytorch import InceptionResnetV1
from werkzeug.utils import secure_filename
from preProcessPhoto import preProcessPhoto
import json
from flask_nav import Nav

# Initialize variables.
# I did this already on `app.py` but just in case
app = Flask(__name__,static_url_path = "/tmp", static_folder = "tmp")
nav = Nav(app)
app.secret_key = "secret key"  # Flask ask me for a key.
app.config['UPLOAD_FOLDER'] = './tmp'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 mb

ALLOWED_EXTENSIONS = set(['jpg'])  # Files allowed (check if PNG could work )
MODEL = InceptionResnetV1(pretrained='vggface2').eval()


#Handy functions
def allowed_file(filename):
    '''
    This function is used to determine if they uploaded file has the apropiate extension
    '''
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
###############################################################################################################################
# Home page
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')  # This would be Iuliias page
###############################################################################################################################

# Train page
train_post = [{ 
                "video" : "video_file_name",
                "person" : "person_name",
                "role" : "role"
                },
                { 
                "video" : "ADDED_video_file_name",
                "person" : "ADDED_person_name",
                "role" : "ADDED_role"
                }
            ]

@app.route('/train')
def train_page():
    return render_template('train.html', posts=train_post)


###############################################################################################################################*
# Test page

test_posts = {
				"file" : None,
				"path" : None
			}

@app.route('/test')
def test_page():
    return render_template('test.html', posts=test_posts)


@app.route('/test', methods=['POST'])
def upload_file():
    global filename  # maybe there is a better way than using global, but it's the easier way now
    global test_posts
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            test_posts['file'] = secure_filename(file.filename) 
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], test_posts['file']))
            flash(f'{ test_posts["file"]} successfully uploaded')
            test_posts["path"] = os.path.join(app.config['UPLOAD_FOLDER'], test_posts['file'])  # Plot the file uploaded
            return redirect('/test')
        else:
            flash(f'Cannot upload {file.filename} \n Allowed file types are: jpg')
            return redirect(request.url)
# Will need a button here to say 'Test this person'


outputs_post = {
				"file" : None,
                "embedding" : None
                }


@app.route('/output')
def output():
	global outputs_post
	outputs_post["file"] = test_posts['file'] #set the file
	embedding = preProcessPhoto(f'tmp/{outputs_post["file"]}',MODEL)
	outputs_post['embedding'] = embedding['data']
	return render_template('/output.html', posts=outputs_post)

##############################################################################################################################
# POST request to Amazon Sagemaker

api_posts = {  
                        "File": "File name",
                        "Person": 'Person out from SageMaker',
                        "Accuracy": 'Accuracy from SageMaker',
                        "Role": "Role of the person from log"
                     }

@app.route('/api_output')
def api_output():
    global api_posts
    return render_template('api_output.html', posts=api_posts)


# Useful also to visualize locally
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)