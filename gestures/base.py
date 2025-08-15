import mediapipe as mp 

class Detection:

    def __init__(self,mode = False, complexity = 1, min_detection_confidence = 0.7, min_tracking_confidence = 0.5,last_detection_time = 0):
        self.mode = mode
        self.complexity = complexity
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self.last_detection_time = last_detection_time


class TrackHands(Detection):

    def __init__(self, mode = False, complexity = 1, min_detection_confidence = 0.7, min_tracking_confidence = 0.5, max_num_hands = 1, last_detection_time = 0):
        super().__init__(mode, complexity, min_detection_confidence, min_tracking_confidence,last_detection_time)
        self.max_hands = max_num_hands
        

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
    static_image_mode=self.mode,
    max_num_hands=self.max_hands,
    model_complexity=self.complexity,
    min_detection_confidence=self.min_detection_confidence,
    min_tracking_confidence=self.min_tracking_confidence
)

        self.mp_drawing = mp.solutions.drawing_utils
    
    def detect_hands(self, frame_rgb, draw = False):

        landmarks = []
        
        # Returns a results object containing information about landmarks (position coords)
        results = self.hands.process(frame_rgb)

        hand_label = None

        if results.multi_hand_landmarks:
            # Iterate through all 21 landmarks for each hand detected
            for hands,handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                # Iterate through each landmark position getting their corresponding id
                for id, lm in enumerate(hands.landmark):
                    # get frame dimensions

                    # Get the handedness of the hand detected in the frame
                    hand_label = handedness.classification[0].label

                    h, w, c = frame_rgb.shape

                    cx, cy = int(lm.x * w), int(lm.y * h)

                    landmarks.append([id, cx, cy])

                    if draw:
                        self.mp_drawing.draw_landmarks(frame_rgb, hands, self.mp_hands.HAND_CONNECTIONS)
        else:
            return None,None
        return landmarks, hand_label
