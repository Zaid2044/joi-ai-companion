import cv2
import mediapipe as mp

class VisionProcessor:
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=0, min_detection_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils

    def process_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False
        results = self.face_detection.process(rgb_frame)
        rgb_frame.flags.writeable = True
        bgr_frame_with_detections = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)

        if results.detections:
            for detection in results.detections:
                self.mp_drawing.draw_detection(bgr_frame_with_detections, detection)
        
        return bgr_frame_with_detections

    def close(self):
        self.face_detection.close()