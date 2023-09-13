import os
import face_recognition
import numpy as np

def preprocess_and_encode_images(directory_path):
    encoded_faces = {}
    
    for image_path in os.listdir(directory_path):
        if image_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
            image = face_recognition.load_image_file(os.path.join(directory_path, image_path))
            face_encodings = face_recognition.face_encodings(image)
            
            if face_encodings:
                encoded_faces[image_path] = face_encodings
    
    np.save('encoded_faces.npy', encoded_faces)

if __name__ == '__main__':
    preprocess_and_encode_images('AllImages')
