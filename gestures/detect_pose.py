import mediapipe as mp
from gestures.base import Detection


class DetectPose(Detection):

    def __init__(self, mode = False, complexity = 1, min_detection_confidence = 0.7, min_tracking_confidence = 0.5, last_detection_time = 0, upper_body_only = False, smooth_landmarks = True):
        super().__init__(mode, complexity, min_detection_confidence, min_tracking_confidence, last_detection_time)

        self.upper_body_only = upper_body_only
        self.smooth_landmarks = smooth_landmarks

        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(self.mode,complexity,self.smooth_landmarks,self.upper_body_only,self.min_detection_confidence, self.min_tracking_confidence)
        self.mp_draw = mp.solutions.drawing_utils

    def detect_pose(self,frame, draw = True):
        
        results = self.pose.process(frame)

        h,w,c = frame.shape

        landmarks = []

        if results.pose_landmarks:
            for id, lm in enumerate(results.pose_landmarks.landmark):

                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarks.append([id,cx,cy])

            if draw:
                self.mp_draw.draw_landmarks(frame,results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
        else:
            return None
        return landmarks

