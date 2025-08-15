from user_flow.auth import reg_user
from gesture_detection.media_channel_utils.media_main import media_main
from channel_management.get_mode_channel import get_channel

def main():
    found, name = reg_user()
    if found:
        channel = get_channel()
        match channel:
            case 'Idle':
                print(f'CURRENT MODE: {channel}')
            case 'Study':
                print(f'CURRENT MODE: {channel}')
                pass
            case 'Media':
                print(f'CURRENT MODE: {channel}')
                media_main()
                pass



if __name__ == '__main__':
    print('Welcome to realtime face recognition')
    main()