from pydantic import BaseModel
from collections import namedtuple
import math
import numpy as np
import time
import os
from ultralytics import YOLO

# Definisce un namedtuple per i punti chiave
Keypoint = namedtuple('Keypoint', ['x', 'y'])


class GetKeypoint(BaseModel):  # Definisce la classe GetKeypoint utilizzando BaseModel di Pydantic
    NOSE:           int = 0
    LEFT_EYE:       int = 1
    RIGHT_EYE:      int = 2
    LEFT_EAR:       int = 3
    RIGHT_EAR:      int = 4
    LEFT_SHOULDER:  int = 5
    RIGHT_SHOULDER: int = 6
    LEFT_ELBOW:     int = 7
    RIGHT_ELBOW:    int = 8
    LEFT_WRIST:     int = 9
    RIGHT_WRIST:    int = 10
    LEFT_HIP:       int = 11
    RIGHT_HIP:      int = 12
    LEFT_KNEE:      int = 13
    RIGHT_KNEE:     int = 14
    LEFT_ANKLE:     int = 15
    RIGHT_ANKLE:    int = 16


class BufferFrames:
    static_flag = False
    counter = 0
    images = []

    def __init__(self):
        print("Buffer inizializzato")


class Body:  # Definisce la classe Body
    def __init__(self, body_keypoints: np.ndarray):
        # Inizializza la classe Body con i punti chiave del corpo
        self.body_keypoints = [Keypoint(*keypoint) for keypoint in body_keypoints]
        self.keypoints = GetKeypoint()
        self.init_body()

    def get_coordinates(self, keypoint_name: str):
        # Ottiene le coordinate di un punto chiave dato il suo nome
        keypoint_index = getattr(self.keypoints, keypoint_name)
        return self.body_keypoints[keypoint_index]

    def distance(self, point1, point2):
        # Calcola la distanza euclidea tra due punti di riferimento.
        return math.sqrt(
            (point1.x - point2.x) ** 2 +
            (point1.y - point2.y) ** 2
        )

    def dot_product(self, point1, point2, point3):
        # Calcola il prodotto scalare dei vettori punto1->punto2 e punto2->punto3.
        return (point2.x - point1.x) * (point3.x - point2.x) + (point2.y - point1.y) * (point3.y - point2.y)

    def calculate_angle(self, point1, point2, point3):
        # Calcola il prodotto scalare.
        dot = self.dot_product(point1, point2, point3)

        # Calcola le distanze dei vettori.
        mag1 = self.distance(point1, point2)
        mag2 = self.distance(point2, point3)

        if mag1 == 0 or mag2 == 0:
            return False  # Evita la divisione per zero

        cos_angle = dot / (mag1 * mag2)
        return -1.1 <= cos_angle <= -0.8

    def init_body(self):
        # Inizializza i punti chiave del corpo utilizzando i nomi definiti in GetKeypoint
        self.nose = self.get_coordinates('NOSE')
        self.left_eye = self.get_coordinates('LEFT_EYE')
        self.right_eye = self.get_coordinates('RIGHT_EYE')
        self.left_ear = self.get_coordinates('LEFT_EAR')
        self.right_ear = self.get_coordinates('RIGHT_EAR')
        self.left_shoulder = self.get_coordinates('LEFT_SHOULDER')
        self.right_shoulder = self.get_coordinates('RIGHT_SHOULDER')
        self.left_elbow = self.get_coordinates('LEFT_ELBOW')
        self.right_elbow = self.get_coordinates('RIGHT_ELBOW')
        self.left_wrist = self.get_coordinates('LEFT_WRIST')
        self.right_wrist = self.get_coordinates('RIGHT_WRIST')
        self.left_hip = self.get_coordinates('LEFT_HIP')
        self.right_hip = self.get_coordinates('RIGHT_HIP')
        self.left_knee = self.get_coordinates('LEFT_KNEE')
        self.right_knee = self.get_coordinates('RIGHT_KNEE')
        self.left_ankle = self.get_coordinates('LEFT_ANKLE')
        self.right_ankle = self.get_coordinates('RIGHT_ANKLE')

    @property
    def is_left_arm_up(self):
        # Determina se il braccio sinistro è sollevato controllando le coordinate dei punti chiave
        return (self.left_wrist.y < self.left_eye.y < self.left_ear.y and
                self.left_wrist.y < self.left_elbow.y < self.left_shoulder.y and
                self.left_elbow.y < self.left_eye.y < self.left_ear.y)

    @property
    def is_right_arm_up(self):
        # Determina se il braccio destro è sollevato controllando le coordinate dei punti chiave
        return (self.right_wrist.y < self.right_eye.y < self.right_ear.y and
                self.right_wrist.y < self.right_elbow.y < self.right_shoulder.y and
                self.right_elbow.y < self.right_eye.y < self.right_ear.y)

    @property
    def is_left_arm_bending(self):
        # Determina se il braccio sinistro è piegato basandosi sulle coordinate dei punti chiave
        if self.left_hip.y > self.left_wrist.y > self.left_shoulder.y:
            if self.left_shoulder.x <= self.right_shoulder.x:
                return self.left_wrist.x >= self.left_shoulder.x
            else:
                return self.left_wrist.x <= self.left_shoulder.x
        return False

    @property
    def is_right_arm_bending(self):
        # Determina se il braccio destro è piegato basandosi sulle coordinate dei punti chiave
        if self.right_hip.y > self.right_wrist.y > self.right_shoulder.y:
            if self.right_shoulder.x >= self.left_shoulder.x:
                return self.right_wrist.x <= self.right_shoulder.x
            else:
                return self.right_wrist.x >= self.right_shoulder.x
        return False

    @property
    def is_left_arm_extended(self):
        # Determina se il braccio sinistro è esteso basandosi sulle coordinate dei punti chiave
        if self.left_hip.y > self.left_wrist.y:
            return self.calculate_angle(self.left_elbow, self.left_shoulder, self.left_wrist)
        return False

    @property
    def is_right_arm_extended(self):
        # Determina se il braccio destro è esteso basandosi sulle coordinate dei punti chiave
        if self.right_hip.y > self.right_wrist.y:
            return self.calculate_angle(self.right_elbow, self.right_shoulder, self.right_wrist)
        return False

    @property
    def are_forearms_crossed(self):
        # Determina se gli avambracci effettuano una 'X'
        if self.right_hip.y > self.right_wrist.y > self.right_shoulder.y and self.left_hip.y > self.left_wrist.y > self.left_shoulder.y:
            threshold = self.distance(self.right_elbow, self.right_wrist)
            return (self.right_wrist.y < self.right_elbow.y and
                    self.left_wrist.y < self.left_elbow.y and
                    self.distance(self.left_shoulder, self.right_wrist) <= threshold and
                    self.distance(self.right_shoulder, self.left_wrist) <= threshold)
        return False

    def detect_rotation(self, cv2):
        # Rileva il fallo di travelling, analizza i frame successivi e deduce se è avvenuto
        if self.is_right_arm_bending and self.is_left_arm_bending and self.right_wrist.y < self.left_wrist.y and (
                (self.right_wrist.y - self.left_wrist.y) < -0.10):
            print("ARMS IN ABS ZONE; POSSIBLE TRAVELLING SIGNAL INCOMING; CHECKING...")
            if len(BufferFrames.images) < 20:
                BufferFrames.static_flag = True
                return False
            else:
                # I frame sono stati collezionati, possiamo analizzarli
                BufferFrames.static_flag = False
                directory = "Recording/travelling"
                os.makedirs(directory, exist_ok=True)

                file_name = f"{directory}/travelling_{int(time.time())}.mp4"
                height, width, _ = BufferFrames.images[0].shape
                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                out = cv2.VideoWriter(file_name, fourcc, 10, (width, height))
                for frame in BufferFrames.images:
                    out.write(frame)
                out.release()

                # Carica modello YOLOv8 pose per l'analisi del buffer
                model = YOLO('yolov8n-pose.pt')
                starting_position = None
                previous_frame = None
                is_rotating = False
                finish = False

                for i, img_frame in enumerate(BufferFrames.images):
                    results = model(img_frame, conf=0.5, verbose=False)
                    if len(results[0].keypoints) == 0 or len(results[0].keypoints.xyn) == 0:
                        continue
                    
                    body_keypoints = results[0].keypoints.xyn.cpu().numpy()[0]
                    body = Body(body_keypoints)

                    if i == 0 or starting_position is None:
                        starting_position = body
                        previous_frame = body
                        continue

                    # Confronta i movimenti del polso
                    if body.right_wrist.y <= starting_position.right_wrist.y or (
                            -0.21 < (body.right_wrist.y - starting_position.right_wrist.y) < 0.21):
                        is_rotating = True
                    else:
                        if body.right_wrist.y >= starting_position.right_wrist.y or (
                                -0.21 < (body.right_wrist.y - starting_position.right_wrist.y) < 0.21):
                            is_rotating = True
                        else:
                            is_rotating = False
                            print("ERROR NOT ROTATING")
                            BufferFrames.images.clear()
                            return False

                    if (-0.10 < (previous_frame.right_wrist.y - body.right_wrist.y) < 0.10) and i == len(BufferFrames.images) - 1:
                        print("TRAVELLING FINISHED AND ACCOMPLISHED")
                        finish = True

                    if not finish and i == len(BufferFrames.images) - 1:
                        print("FINISHED WITHOUT DETECTING TRAVELLING")
                        is_rotating = False

                    previous_frame = body

                BufferFrames.images.clear()
                return is_rotating
        return False