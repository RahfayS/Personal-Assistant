from user_flow.auth import reg_user
from gesture_control.gesture_main import gestures
import pyttsx3

def main():
    found, name = reg_user()
    if found:
        gestures()




if __name__ == '__main__':
    print('Welcome to realtime face recognition')
    main()