import cv2
import math
import subprocess
import time
import pyautogui

class ClosedFist():

    def __init__(self):
        self.last_update_time = 0
        self.count = 0
        self.last_detection_time = 0
    
        
    def closed_fist(self,frame,landmarks,hand_label):

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

        index_angle = self.calculate_atan(index_mcp,index_pip,width_angle,hand_label)
        middle_angle = self.calculate_atan(middle_mcp,middle_pip,width_angle,hand_label)
        ring_angle = self.calculate_atan(ring_mcp,ring_pip,width_angle,hand_label)
        pinky_angle = self.calculate_atan(pinky_mcp,pinky_pip,width_angle,hand_label)

        angles = [index_angle, middle_angle, ring_angle, pinky_angle]

        isPaused = self.play_or_pause(angles,frame)

        return isPaused
    
    def calculate_atan(self,lm_1, lm_2,width_angle,hand_label):
        angle = math.atan2(lm_1[2] - lm_2[2], lm_1[1] - lm_2[1])
        angle = math.degrees(angle - width_angle)

        # Noramlize the angle so that it is within [0-360)
        angle = (angle + 360) % 360

        # Convert the angle if the left hand is in frame
        if hand_label == 'Left':
            angle = (360 - angle) % angle
        
        return angle
        
    def play_or_pause(self, angles, frame):
        MIN = 70
        MAX = 95

        curr = time.time()

        if self.count != 0:
            cv2.putText(frame, f'Pausing... {self.count}/3', (150, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)

        if curr - self.last_detection_time > 3:
            self.count = 0

        for angle in angles:
            if MIN < angle < MAX and (curr - self.last_update_time >= 1.5):
                self.count += 1
                self.last_update_time = curr
                self.last_detection_time = curr

                if self.count == 3:
                    app = self.check_app()
                    if app in ['Safari', 'Google Chrome']:
                        browser = app

                        applescript = f'''
                            tell application "{browser}"
                                do JavaScript "var video=document.querySelector('video'); if(video) {{ video.paused ? video.play() : video.pause(); }}" in front document
                            end tell
                            '''                              
                        subprocess.run(["osascript", "-e", applescript])

                    return True,app
        return False, None
