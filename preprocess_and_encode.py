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

def preprocess_and_encode_images(directory_path, save_partial=False):
    encoded_faces_path = 'encoded_faces.npy'
    try:
        encoded_faces = np.load(encoded_faces_path, allow_pickle=True).item()
    except FileNotFoundError:
        encoded_faces = {}

    image_paths = [os.path.join(directory_path, image_path) for image_path in os.listdir(directory_path)]
    
    with Pool(cpu_count() // 2) as p:
        for image_path in image_paths:
            if image_path not in encoded_faces:
                try:
                    result = p.map(encode_image, [image_path])
                    if result[0] is not None:
                        encoded_faces[result[0][0]] = result[0][1]
                        if save_partial:
                            np.save(encoded_faces_path, encoded_faces)
                except Exception as e:
                    print(f"Error encoding image {image_path}: {e}")
                    if not save_partial:
                        break

    if not save_partial or (save_partial and not os.path.exists(encoded_faces_path)):
        np.save(encoded_faces_path, encoded_faces)

if __name__ == '__main__':
    preprocess_and_encode_images('AllImages')