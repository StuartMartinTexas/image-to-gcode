from flask import Flask, request, send_file
import subprocess
import os

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/process-image', methods=['POST'])
def process_image():
    img = request.files['image']
    img_path = 'input.png'
    gcode_path = 'output.gcode'
    img.save(img_path)
    cmd = ['python3', 'image_to_gcode.py', '-i', img_path, '-o', gcode_path, '--threshold', '100']
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        return result.stderr.decode(), 500
    return send_file(gcode_path, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
