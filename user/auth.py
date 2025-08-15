from face.face_detection import *
from face.get_photos import *
from face.encodings import get_encodings
from face.auto_login import auto_login
from user.registration import *


def reg_user(draw = True):

    '''
    
    Checks to see if user is in encodings, if not gather screenshots
    
    '''

    found = False

    manager = UserManager()
    matched_user = auto_login(manager, draw)
    
    if matched_user:
        print('User identified')
        name = matched_user.name
        found = True
        # return manager.users, manager.logged_in_user.name
    else:
        name, email = get_user_info()
        # Load users from disk
        users = manager.load()
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
            manager.save()
            found = True
        else:
            user_id = manager.email_to_id[email]
            user = manager.users[user_id]
            print(f"[INFO] User {user.name} already registered.")

    return found, name