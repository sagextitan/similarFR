import cv2
import face_recognition
import os
import base64
import numpy as np
from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)

@app.route('/AllImages/<path:filename>')
def serve_static(filename):
    return send_from_directory('AllImages', filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find_similar_images', methods=['POST'])
def find_similar_images():
    image_data = request.form['image_data'].split(',')[1] 
    image_bytes = base64.b64decode(image_data)
    nparr = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    captured_face_encodings = face_recognition.face_encodings(frame)

   
    if len(captured_face_encodings) == 0:
        return jsonify({"similar_images": []})
    else:
        all_image_paths = os.listdir("AllImages")
        similar_images = []

        for image_path in all_image_paths:
            image = face_recognition.load_image_file(os.path.join("AllImages", image_path))
            face_encodings = face_recognition.face_encodings(image)

            for face_encoding in face_encodings:
                match_results = face_recognition.compare_faces(captured_face_encodings, face_encoding)
                if any(match_results):
                    similar_images.append(image_path)

        return jsonify({"similar_images": similar_images})

if __name__ == '__main__':
    app.run(debug=True)
