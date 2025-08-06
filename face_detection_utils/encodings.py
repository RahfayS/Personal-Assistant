import cv2
import face_recognition
import os
import pickle
import numpy as np


def get_encodings(name):
    """
    Processes screenshots of a user and returns the average 128D face encoding.

    Args:
        name (str): Name of the user (used to locate their image folder)

    Returns:
        numpy.ndarray or None: Mean face encoding vector or None if no faces found
    """

    data_dir = 'data'
    encodings = []

    for folder_name in os.listdir(data_dir):
        user = folder_name.split('_')[0]
        if name == user:
            folder_path = os.path.join(data_dir, folder_name)
            for filename in os.listdir(folder_path):
                img_path = os.path.join(folder_path, filename)
                img = cv2.imread(img_path)
                if img is None:
                    continue
                
                faces = face_recognition.face_encodings(img)
                if len(faces) > 0:
                    encodings.append(faces[0])

    encodings = np.array(encodings)
    mean_encodings = np.mean(encodings,axis = 0) # Convert to (1,128)
    return mean_encodings
