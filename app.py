import cv2
import face_recognition
import os
import base64
import numpy as np
from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)

def load_and_preprocess_image(image_data):
    image_data = image_data.split(',')[1]
    image_bytes = base64.b64decode(image_data)
    nparr = np.frombuffer(image_bytes, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

tolerance = 0.48

encoded_faces_path = ('encoded_faces.npy')

try:
    encoded_faces = np.load(encoded_faces_path, allow_pickle=True).item()
except FileNotFoundError:
    encoded_faces = {}

@app.route('/AllImages/<path:filename>')
def serve_static(filename):
    return send_from_directory('AllImages', filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find_similar_images', methods=['POST'])
def find_similar_images():
    image_data = request.form['image_data']

    frame = load_and_preprocess_image(image_data)

    captured_face_encodings = face_recognition.face_encodings(frame)

    if len(captured_face_encodings) == 0:
        return jsonify({"similar_images": []})
    else:
        similar_images = []

        for image_path, face_encodings in encoded_faces.items():
            for face_encoding in face_encodings:
                captured_face_encodings_np = np.array(captured_face_encodings)
                face_encoding_np = np.array(face_encoding)

                match_results = face_recognition.compare_faces(captured_face_encodings_np, face_encoding_np, tolerance=tolerance)
                if any(match_results):
                    similar_images.append(image_path)

        return jsonify({"similar_images": similar_images})

if __name__ == '__main__':
    app.run(debug=True)
