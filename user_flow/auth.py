import cv2
from face_detection_utils.detection import *
from face_detection_utils.get_photos import *
from face_detection_utils.encodings import get_encodings
from face_detection_utils.auto_login import auto_login
from user_data_utils.registration import *
from gesture_control.gesture_utils import *

def reg_user(draw = True):

    '''
    
    Checks to see if user is in encodings, if not gather screenshots
    
    '''

    found = False

    manager = userManager()
    matched_user = auto_login(manager, draw)
    
    if matched_user:
        print('User identified')
        name = matched_user.name
        found = True
        # return manager.users, manager.logged_in_user.name
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

    return found, name