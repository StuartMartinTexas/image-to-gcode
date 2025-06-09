from flask import Flask, request, send_file, Response
import subprocess
import os
from filter_whiteboard import filter_white_background

app = Flask(__name__, static_folder='static')

# 🔒 --- Basic Auth Setup ---
USERNAME = 'stuart'
PASSWORD = 'homeboard'

def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

def authenticate():
    return Response(
        'Authentication Required.', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

@app.before_request
def require_auth():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()

# 🌐 Routes
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/process-image', methods=['POST'])
def process_image():
    img = request.files['image']
    prompt = request.form.get('prompt', '')  # for future use

    img_path = 'input.png'
    filtered_path = 'filtered.png'
    gcode_path = 'output.gcode'

    # Save uploaded image
    img.save(img_path)

    # Filter out non-whiteboard background
    filter_white_background(img_path, filtered_path)

    # Generate G-code from filtered image
    cmd = ['python3', 'image_to_gcode.py', '-i', filtered_path, '-o', gcode_path, '--threshold', '100']
    result = subprocess.run(cmd, capture_output=True)

    if result.returncode != 0:
        return result.stderr.decode(), 500

    return send_file(gcode_path, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
