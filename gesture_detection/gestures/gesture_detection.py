class Detection:

    def __init__(self,mode = False, complexity = 1, min_detection_confidence = 0.7, min_tracking_confidence = 0.5):
        self.mode = mode
        self.complexity = complexity
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence