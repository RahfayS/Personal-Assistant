import cv2
import mediapipe
import time

def get_fps(prev_time):
    curr_time = time.time()

    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    return fps, prev_time


def put_text_top_left(frame, text, font=cv2.FONT_HERSHEY_SIMPLEX, scale=1, color=(255,255,255), thickness=2, margin=10):
    x, y = margin, margin + cv2.getTextSize(text, font, scale, thickness)[0][1]
    cv2.putText(frame, text, (x, y), font, scale, color, thickness)

def put_text_top_right(frame, text, font=cv2.FONT_HERSHEY_SIMPLEX, scale=1, color=(255,255,255), thickness=2, margin=10):
    text_width = cv2.getTextSize(text, font, scale, thickness)[0][0]
    x = frame.shape[1] - text_width - margin
    y = margin + cv2.getTextSize(text, font, scale, thickness)[0][1]
    cv2.putText(frame, text, (x, y), font, scale, color, thickness)


def put_text_bottom_left(frame, text, font=cv2.FONT_HERSHEY_SIMPLEX, scale=1, color=(255,255,255), thickness=2, margin=10):
    text_height = cv2.getTextSize(text, font, scale, thickness)[0][1]
    x = margin
    y = frame.shape[0] - margin
    cv2.putText(frame, text, (x, y), font, scale, color, thickness)

def put_text_bottom_right(frame, text, font=cv2.FONT_HERSHEY_SIMPLEX, scale=1, color=(255,255,255), thickness=2, margin=10):
    text_size = cv2.getTextSize(text, font, scale, thickness)[0]
    x = frame.shape[1] - text_size[0] - margin
    y = frame.shape[0] - margin
    cv2.putText(frame, text, (x, y), font, scale, color, thickness)


def channel_overlay(frame, modes, mode_idx, current):
    max_idx = len(modes) - 1

    next_idx = (mode_idx + 1) % len(modes)
    prev_idx = (mode_idx - 1) % len(modes)

    cv2.putText(frame, f'Current Mode: {current}', (500, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0),2)
    cv2.putText(frame, f'Next Mode: {modes[next_idx]}', (1000, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0),2)
    cv2.putText(frame, f'Previous Mode: {modes[prev_idx]}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0),2)

    


