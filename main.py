import cv2
from face_detection_utils.detection import *
from face_detection_utils.get_photos import *
from face_detection_utils.encodings import get_encodings
from face_detection_utils.auto_login import auto_login
from user_data_utils.registration import *

def main():
    manager = userManager()
    identified = auto_login(manager)

    if identified:
        print('User identified')
    else:
        name, email = get_user_info()
        # Load users from disk
        users = manager.load_users()
        print(users)

        if email not in manager.email_to_id:
            user = manager.register_user(name, email)

            success = get_screenshots(name)
            if not success:
                print('[ERROR] Failed to capture screenshots')
                return  
            encoding = get_encodings(user.name)
            if encoding is None:
                print('[ERROR] failed to extract face encodings')
                return
            user.encoding = encoding
            manager.save_users()
        else:
            user_id = manager.email_to_id[email]
            user = manager.users[user_id]
            print(f"[INFO] User {user.name} already registered.")

        cap = cv2.VideoCapture(1)
        count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            output_frame = compare_faces(users, frame)
            resized = cv2.resize(output_frame,(0,0), fx= 0.3, fy=0.3)
            cv2.imshow('Face Recognition', resized)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()



if __name__ == '__main__':
    print('Welcome to realtime face recognition')
    main()