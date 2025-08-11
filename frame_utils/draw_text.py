import cv2
import mediapipe
import time

def get_fps(prev_time):
    curr_time = time.time()

    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    return fps, prev_time


def put_text_top_right(frame, text, font = cv2.FONT_HERSHEY_SIMPLEX, font_scale = 1, color = (0,0,0), thickness = 2, x_pad = 10, y_pad = 50):
    (t_width, t_height), _ = cv2.getTextSize(text, font,font_scale,thickness)

    x = frame.shape[1] - t_width - x_pad
    y = t_height + x_pad

    frame = cv2.putText(frame, text, (x, y), font, font_scale, color, thickness)
    return frame

def put_text_top_left(frame, text, font = cv2.FONT_HERSHEY_SIMPLEX, font_scale = 1, color = (0,0,0), thickness = 2, x_pad = 10, y_pad = 50):
    x = x_pad
    y = y_pad

    frame = cv2.putText(frame, text, (x, y), font, font_scale, color, thickness)
    return frame

def channel_overlay(frame, modes, mode_idx, current):
    max_idx = len(modes) - 1

    next_idx = (mode_idx + 1) % len(modes)
    prev_idx = (mode_idx - 1) % len(modes)

    cv2.putText(frame, f'Current Mode: {current}', (500, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0),2)
    cv2.putText(frame, f'Next Mode: {modes[next_idx]}', (1000, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0),2)
    cv2.putText(frame, f'Previous Mode: {modes[prev_idx]}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0),2)

    


