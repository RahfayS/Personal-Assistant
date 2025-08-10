import cv2
import math
import numpy as np
from frame_utils.draw_text import put_text_top_right


def change_volume(frame,landmarks,vc):

    lm_1, lm_2 = landmarks[4], landmarks[8]

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

    frame = put_text_top_right(frame, f'VOLUME: {vol}')


    return frame,vol

def close_app(frame,landmarks,fist_tracker,hand_label):

    # Use the width of the palm as a standard unit of measurement

    wrist, pinky_mcp = landmarks[0], landmarks[17]

        # Get the coords of the landmarks
    wrist_x, wrist_y = wrist[1], wrist[2]
    pinky_x, pinky_y = pinky_mcp[1], pinky_mcp[2]

    # We will use for standard unit of measurement
    width_x = (pinky_x - wrist_x)
    width_y = (pinky_y - wrist_y)

    width_angle = math.atan2(width_y, width_x)

    # Now lets compare some key landmarks relative to palm width
    index_mcp, middle_mcp, ring_mcp, pinky_mcp, = landmarks[5], landmarks[9], landmarks[13], landmarks[17]
    index_pip, middle_pip, ring_pip, pinky_pip = landmarks[6], landmarks[10], landmarks[14], landmarks[19]

    # Find the arc tangent of index_mcp and index_pip

    index_angle = math.atan2(index_mcp[2]-index_pip[2], index_mcp[1] - index_pip[1])
    middle_angle = math.atan2(middle_mcp[2]-middle_pip[2], middle_mcp[1] - middle_pip[1])
    ring_angle = math.atan2(ring_mcp[2]-ring_pip[2], ring_mcp[1] - ring_pip[1])
    pinky_angle = math.atan2(pinky_mcp[2]-pinky_pip[2], pinky_mcp[1] - pinky_pip[1])

    index_rel = normalize_angle(math.degrees(index_angle - width_angle),hand_label)
    middle_rel = normalize_angle(math.degrees(middle_angle - width_angle),hand_label)
    ring_rel = normalize_angle(math.degrees(ring_angle - width_angle),hand_label)
    pinky_rel = normalize_angle(math.degrees(pinky_angle - width_angle),hand_label)

    angles = []
    angles.append([index_rel,middle_rel,ring_rel,pinky_rel])

    isClosed,prev,count = fist_tracker.closed_fist(angles,frame)

    return isClosed





def normalize_angle(angle,hand_label):
    # Noramlize the angle so that it is within [0-360)
    angle = (angle + 360) % 360

    # Convert the angle if the left hand is in frame
    if hand_label == 'Left':
        angle = (360 - angle) % angle
    
    return angle