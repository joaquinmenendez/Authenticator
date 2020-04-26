import pandas as pd
from flask import Flask, render_template, request, flash, redirect 
import os
from werkzeug.utils import secure_filename
from preProcessPhoto import preProcessPhoto



#Initialize variables
app = Flask(__name__)

#I need to work around this
app.secret_key = "secret key" #Flask ask me for a key. 
app.config['UPLOAD_FOLDER'] = './temp'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 #50 mb 
ALLOWED_EXTENSIONS = set(['jpg']) # Files allowed (check if PNG could work )


#Handy functions
def allowed_file(filename):
    '''
    This function is used to determine if they uploaded file has the apropiate extension
    '''
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def GET_probability(url, j_embedding):
    '''
    Send a face embedding to the sagemaker model using the API getaway
    '''
    return
###############################################################################################################################
# Home page
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')
###############################################################################################################################


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
test_posts = [
                {
                "File" : "file_name"
                }
            ]
@app.route('/test')
def test_page():
    return render_template('test.html', posts = test_posts)

@app.route('/test', methods=['POST'])
def upload_file():
	global filename #maybe there is a better way than using global, but it's the easier way now
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
			filename = secure_filename(file.filename) 
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			flash('File successfully uploaded')
			return redirect('/describe')
		else:
			flash('Allowed file types are csv')
			return redirect(request.url)


# Will need a button here to say 'Test this person' 


##############################################################################################################################
# POST request to Amazon Sagemaker

test_outpost_posts = {  
                        "File": "File name",
                        "Person": 'Person out from SM',
                        "Accuracy": 'Accuracy from SM',
                        "Role": "Role of the person from log"
                     }

@app.route('/test_output')
def test_output():
    return render_template('test_output.html', posts = test_outpost_posts)


# Useful also to visualize locally
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)