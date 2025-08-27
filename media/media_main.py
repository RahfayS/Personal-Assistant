import cv2, time
import threading
from manager.media_controller import MediaController
from manager.gesture_manager import GestureManager
from utils.draw_text import put_text_top_left, get_fps
from utils.preprocess import preprocess

def media_main():

    # --- Init ---
    detectors = GestureManager()
    controllers = MediaController()
    prev_time = 0

    cap = cv2.VideoCapture(1)


    while True:
        ret, frame = cap.read()
        if frame is None or not ret:
            continue

        # Process the frame for mediapipe functions
        frame_rgb = preprocess(frame)
        display_frame = frame_rgb.copy()

        # --- Gesture results ---
        results = detectors.process(display_frame)

        # --- Apply Action ---
        controllers.apply(display_frame,results)

        # --- UI ---
        fps, prev_time = get_fps(prev_time)
        put_text_top_left(display_frame, f'FPS: {int(fps)}')

        # --- Display ---
        display_frame = cv2.cvtColor(display_frame,cv2.COLOR_RGB2BGR)
        cv2.imshow('Gesture Detection', display_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()
