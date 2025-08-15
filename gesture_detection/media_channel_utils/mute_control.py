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
        nose = pose_landmarks[0]

        # Mouth corner landmarks
        left_corner,right_corner = pose_landmarks[9], pose_landmarks[10]

        if draw:
            cv2.circle(frame,(nose[1],nose[2]),2,(0,255,0),2)
            cv2.circle(frame,(index_tip[1],index_tip[2]),2,(255,0,0),2)
            cv2.line(frame,(left_corner[1],left_corner[2]),(right_corner[1],right_corner[2]),(0,0,255),2)
        
        if left_corner[2] > index_tip[2] > nose[2]:
            self.count += 1

            if self.count == 5:
                subprocess.run(["osascript", "-e", "set volume output muted true"])
                print('APP MUTED')
        else:
            self.count = 0
    


