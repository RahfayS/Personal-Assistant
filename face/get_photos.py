import cv2
import os
import time

def get_screenshots(name):
    '''
    Takes a frame, generates 10 screenshots which then will be used to create encodings

    Args: Takes in the users name

    Returns: a boolean indicating success
    
    '''

    data_dir = 'data'

    max_screenshots = 10
    count = 0
    last_capture_time = 0
    collecting = True

    # Creating the folder path where we will store the user screenshots
    folder = os.path.join(data_dir,f'{name}_images')

    if not os.path.exists(folder):
        os.makedirs(folder)

    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print('Webcam not Detected')
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            continue

        display_frame = frame.copy()
        
        cv2.putText(display_frame,'Press S to start Screenshotting', (125,125),2,cv2.FONT_HERSHEY_COMPLEX, (255,255,255),2)
        cv2.imshow('Screenshot frames',display_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            while count < max_screenshots:
                ret, frame = cap.read()
                if not ret:
                    break
                if time.time() - last_capture_time > 0.3:
                    filename = os.path.join(folder, f'{name}_screenshot_{count}.jpg')
                    cv2.imwrite(filename, frame)
                    count +=1
                    last_capture_time = time.time()

                    cv2.putText(frame,f"Capturing... ({count}/{max_screenshots})",(125,125), 1, cv2.FONT_HERSHEY_COMPLEX_SMALL, (233,234,123),2)
                    cv2.imshow('Screenshot frames',frame)
                    cv2.waitKey(1)
            break
        elif key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return True
