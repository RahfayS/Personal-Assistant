import cv2
import face_recognition
from user_data_utils.registration import *
import time

def auto_login(manager,draw, threshold=0.55):
    users = manager.load_users()

    if len(users) == 0:
        print('[WARN] No users found.')
        return None

    known_encodings = []
    known_ids = []

    for user_id, user in users.items():
        if user.encoding is not None:
            known_encodings.append(user.encoding)
            known_ids.append(user_id)

    if not known_encodings:
        print('[ERROR] No encodings found.')
        return None

    cap = cv2.VideoCapture(1)
    matched_user = None

    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb)
        face_encodings = face_recognition.face_encodings(rgb, face_locations)

        for encoding, face_location in zip(face_encodings, face_locations):
            distances = face_recognition.face_distance(known_encodings, encoding)

            if len(distances) == 0:
                continue

            min_dist = min(distances)
            min_idx = distances.tolist().index(min_dist)

            if min_dist < threshold:
                matched_user = users[known_ids[min_idx]]
                print(f"[INFO] Logged in as {matched_user.name}")

                if draw:
                # Draw welcome box
                    top, right, bottom, left = face_location
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, f"Welcome {matched_user.name}", (left, top - 10),
                                cv2.FONT_HERSHEY_PLAIN, 1.4, (255, 255, 255), 2)
                else:
                    top, right, bottom, left = face_location
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 255), 1)
                    cv2.putText(frame, "Unknown", (left, top - 10),
                                cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 255, 255), 2)

        # Resize and show
        cv2.imshow('Login', frame)

        if time.time() - start_time > 3:
            break

        # Only quit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return matched_user
