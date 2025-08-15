import face_recognition
import cv2
import numpy as np

def preprocess_frame(frame):
    '''
    Takes in a frame and process it by converting to rgb which is needed for haarcascade functions
    and returns the preprocessed frame

    Args: frame (np.array): BGR image from OpenCV

    Returns: frame (np.array): Flipped Horizontally gray image

    '''

    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (0,0), fx=0.35, fy=0.35)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return frame_gray



def detect_faces(gray):
    '''
    
    Takes in a frame and using haarcascades, detects any faces

    Args: frame (np.array): BGR image from OpenCV
    
    Returns: Boolean determining if faces where detected
    '''

    found = False

    face_cascade = cv2.CascadeClassifier('face_detection_utils/haarcascades/haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1,minNeighbors=5)
    if 0 < len(faces) < 2:
        found = True

    
    return found


def compare_faces(users, frame, threshold=0.5):
    '''
    Compares detected face encodings with multiple users and draws bounding boxes.

    Args:
        user_list: list of dicts/objects with 'name' and 'encoding' attributes
        frame: BGR frame (from cv2)
        threshold: max face distance to consider a match (default: 0.5)

    Returns:
        frame with bounding boxes and name labels
    '''
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Face locations, and encodings for all detected faces in the frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    if len(face_encodings) == 0:
        return frame

    output_frame = rgb_frame.copy()

    names = [user.name for user_id, user in users.items() if user.encoding is not None]
    encodings = [user.encoding for user_id, user in users.items() if user.encoding is not None]


    for frame_enc, face_loc in zip(face_encodings, face_locations):
        distances = face_recognition.face_distance(encodings,frame_enc) # Calculate the distance of all encoding in encodings relative to the encodings found in the frame. Returning an array of floats representing the euclidean distance between the 2 encodings

        name = 'Unknown'
        color = (0,0,255)

        if len(distances) > 0:
            min_dist = np.min(distances)
            min_idx = np.argmin(distances)

            if min_dist < threshold:
                # Find the name which best represents the encoding found in the frame
                name = names[min_idx]
                color = (0,255,0)
        # Bounding box points
        top, right, bottom, left = face_loc
        cv2.rectangle(output_frame, (left, top), (right, bottom), color, 2)
        cv2.putText(output_frame, name, (left, top - 10), cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 255, 255), 2)


    output_frame = cv2.cvtColor(output_frame,cv2.COLOR_RGB2BGR)
    return output_frame
