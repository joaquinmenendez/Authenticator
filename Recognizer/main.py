import pandas as pd
from flask import Flask, render_template, request, flash, redirect, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = './temp'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 #50 mb 
ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello(): 
    return '</br>\
    <title>Authentificator</title> \
    <h2 style="text-align: center; color: #16167f; font-size:35px "><strong>Welcome to Autentificator!</a></strong></h2>\
	<p style="text-align: center; font-size:25px "> This app identifies your team members and shares the appropriate access rights to keep your business safe.</p>\
	<p style="text-align: center; font-size:25px "> <a href="./upload" target="_top"> \
    <iframe src="https://www.youtube.com/embed/3oFRQvsKq0s" text-align: center; width="853" height="480" frameborder="0" allowfullscreen></iframe>\
    <p style="text-align: center; font-size:25px "><strong> Teach the algortihm to recognize your team </strong></a></p>'

@app.route('/upload')
def upload_form():
	return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
	global filename
	if request.method == 'POST':
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

@app.route('/test')
def test():
    return '''
    '</br>\
    <h2 style="text-align: center; color: #16167f; font-size:35px "><strong>Your model is ready!</a></strong></h2>\
    <h2 style="text-align: center; color: #16167f; font-size:30px "><strong>Upload a new video to evaluate the performance</a></strong></h2>'''


# Useful also to visualize locally
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
