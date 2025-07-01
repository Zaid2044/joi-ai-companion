import cv2
import mediapipe as mp
import math

class VisionProcessor:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        self.emotion = "NEUTRAL"

    def _calculate_lip_corner_height(self, landmarks):
        left_corner = landmarks[61]
        right_corner = landmarks[291]
        upper_lip_center = landmarks[0]
        lower_lip_center = landmarks[17]

        if any(lm is None for lm in [left_corner, right_corner, upper_lip_center, lower_lip_center]):
            return 0

        midpoint_y = (upper_lip_center.y + lower_lip_center.y) / 2
        avg_corner_y = (left_corner.y + right_corner.y) / 2
        
        vertical_distance = avg_corner_y - midpoint_y
        
        face_height = math.dist((landmarks[10].x, landmarks[10].y), (landmarks[152].x, landmarks[152].y))
        
        if face_height == 0:
            return 0
        
        normalized_distance = vertical_distance / face_height
        return normalized_distance

    def get_emotion(self):
        return self.emotion

    def process_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False
        results = self.face_mesh.process(rgb_frame)
        rgb_frame.flags.writeable = True
        bgr_frame_with_mesh = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                self.mp_drawing.draw_landmarks(
                    image=bgr_frame_with_mesh,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=self.drawing_spec,
                    connection_drawing_spec=self.drawing_spec)

                normalized_lip_height = self._calculate_lip_corner_height(face_landmarks.landmark)

                if normalized_lip_height < -0.015:
                    self.emotion = "HAPPY"
                elif normalized_lip_height > 0.01:
                    self.emotion = "SAD"
                else:
                    self.emotion = "NEUTRAL"
        else:
            self.emotion = "NEUTRAL"

        return bgr_frame_with_mesh, self.emotion

    def close(self):
        self.face_mesh.close()