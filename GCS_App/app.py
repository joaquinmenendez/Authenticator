from flask import Flask

# Initialize variables

app = Flask(__name__,static_url_path = "/tmp", static_folder = "tmp")
app.secret_key = "secret key"  # Flask ask me for a key.
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 mb