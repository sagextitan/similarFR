import os
import face_recognition
import numpy as np
from multiprocessing import Pool, cpu_count

def encode_image(image_path):
    if image_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)
        
        if face_encodings:
            return (image_path, face_encodings)
    return None

def preprocess_and_encode_images(directory_path):
    image_paths = [os.path.join(directory_path, image_path) for image_path in os.listdir(directory_path)]
    
    with Pool(cpu_count() // 2) as p:
        results = p.map(encode_image, image_paths)
    
    encoded_faces = {image_path: encodings for image_path, encodings in results if encodings is not None}
    
    np.save('encoded_faces.npy', encoded_faces)

if __name__ == '__main__':
    preprocess_and_encode_images('AllImages')