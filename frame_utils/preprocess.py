import cv2
import mediapipe

def preprocess(frame):
    '''
    
    Process frame for mediapipe use
    
    '''
    if frame is not None and frame.shape[0] > 0 and frame.shape[1] > 0:
        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (0,0), fx = 0.75, fy = 0.75)
    else:
        print('[WARN] Frame empty')

    return frame
