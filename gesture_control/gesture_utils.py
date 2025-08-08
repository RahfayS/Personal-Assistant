import cv2
import time
import math
from frame_utils.draw_text import put_text_top_right

def change_volume(frame, lm_1, lm_2,vc):
    
    # Get the coords of the landmarks representing the thumb and index finger

    x1, y1 = lm_1[1], lm_1[2]
    x2, y2 = lm_2[1], lm_2[2]

    # Get the cords of the center of the landmarks

    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

    # Draw circles on the landmarks, then measure the length between the circles, which we will use to control the volume
    frame = cv2.circle(frame, (x1,y1),10,(255,255,255), cv2.FILLED)
    frame = cv2.circle(frame, (x2,y2),10,(255,255,255), cv2.FILLED)
    frame = cv2.line(frame, (x1,y1), (x2,y2), (0,125,125), 2)

    frame = cv2.circle(frame, (cx,cy),10,(0,255,00), cv2.FILLED)

    # Calculate the length between the circles/landmarks
    length = math.hypot(x2 - x1, y2 - y1)

    if length < 50:
        frame = cv2.circle(frame, (cx,cy),15, (0,0,255), cv2.FILLED)

    vol = vc.set_volume(length)

    return frame,vol

