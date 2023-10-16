from flask import Flask, request, redirect, url_for, render_template
import os
import subprocess

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    files = request.files.getlist('file')
    for file in files:
        if file:
            file.save(os.path.join('AllImages', file.filename))
    return redirect(url_for('index'))

@app.route('/run_preprocess_and_encode')
def run_preprocess_and_encode():
    subprocess.call(['python', 'preprocess_and_encode.py'])
    return redirect(url_for('index'))

@app.route('/run_app')
def run_app():
    subprocess.call(['python', 'app.py'])
    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('admin_index.html')

if __name__ == '__main__':
    app.run(port=8000)
