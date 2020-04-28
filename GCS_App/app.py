from flask import Flask
from flask_nav import Nav
# Initialize variables

app = Flask(__name__,static_url_path = "/tmp", static_folder = "tmp")
nav = Nav(app)
app.secret_key = "secret key"  # Flask ask me for a key.
app.config['UPLOAD_FOLDER'] = './tmp'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 mb