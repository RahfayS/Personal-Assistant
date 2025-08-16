import cv2
import subprocess


class MuteControl():


    def __init__(self):
        self.count = 0

    def mute_app(self,frame, hand_landmarks, pose_landmarks, draw = True):
        
        if hand_landmarks is None or pose_landmarks is None:
            return
        # Assign Key Landmarks for shush gesture
        index_tip = hand_landmarks[8]
        _, index_x, index_y = index_tip

        nose = pose_landmarks[0]
        _, nose_x, nose_y = nose

        # Mouth corner landmarks
        mouth_right, mouth_left = pose_landmarks[9], pose_landmarks[10]
        _, mouth_left_x, mouth_left_y = mouth_left
        _, mouth_right_x, mouth_right_y = mouth_right

        mouth_y = (mouth_left_y + mouth_right_y) // 2

        if draw:
            cv2.circle(frame,(index_x,index_y), 5, (0,255,255),2)
            cv2.circle(frame,(nose_x,nose_y),5,(255,0,0),2)
            cv2.line(frame,(mouth_left[1],mouth_left[2]),(mouth_right[1], mouth_right[2]),(0,255,0),2)

            
        if mouth_y > index_y > nose_y and mouth_left_x <= index_x <= mouth_right_x:
            self.count += 1
            if self.count == 3:
                subprocess.run(["osascript", "-e", "set volume output muted true"])
                print('APP MUTED')
        else:
            self.count = 0
    


