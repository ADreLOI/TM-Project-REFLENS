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
        distance = math.sqrt(
            (point1.x - point2.x) ** 2 +
            (point1.y - point2.y) ** 2
        )
        return distance

    def dot_product(self, point1, point2, point3):
        # Calcola il prodotto scalare dei vettori punto1->punto2 e punto2->punto3.
        return (point2.x - point1.x) * (point3.x - point2.x) + (point2.y - point1.y) * (point3.y - point2.y)

    def calculate_angle(self, point1, point2, point3):
        # Calcola il prodotto scalare.
        dot = self.dot_product(point1, point2, point3)

        # Calcola le distanze dei vettori.
        mag1 = self.distance(point1, point2)
        mag2 = self.distance(point2, point3)

        # Calcola il coseno dell'angolo.
        if mag1 == 0 or mag2 == 0:
            return False  # Evita la divisione per zero

        cos_angle = dot / (mag1 * mag2)

        # Verifica se il valore del coseno è entro la soglia per un gomito esteso.
        # Per un gomito esteso, cos(theta) dovrebbe essere vicino a -1 (ad esempio, da -0.9 a -1.0)
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
            if self.left_shoulder.x < self.right_shoulder.x or self.right_shoulder.x == self.left_shoulder.x:
                return self.left_wrist.x > self.left_shoulder.x or self.left_wrist.x == self.left_shoulder.x
            else:
                return self.left_wrist.x < self.left_shoulder.x or self.left_wrist.x == self.left_shoulder.x

    @property
    def is_right_arm_bending(self):
        # Determina se il braccio destro è piegato basandosi sulle coordinate dei punti chiave
        if self.right_hip.y > self.right_wrist.y > self.right_shoulder.y:
            if self.right_shoulder.x > self.left_shoulder.x or self.right_shoulder.x == self.left_shoulder.x:
                return self.right_wrist.x < self.right_shoulder.x or self.right_wrist.x == self.right_shoulder.x
            else:
                return self.right_wrist.x > self.right_shoulder.x or self.right_wrist.x == self.right_shoulder.x

    @property
    def is_left_arm_extended(self):
        # Determina se il braccio sinistro è esteso basandosi sulle coordinate dei punti chiave
        if self.left_hip.y > self.left_wrist.y:
            return self.calculate_angle(self.left_elbow, self.left_shoulder, self.left_wrist)

    @property
    def is_right_arm_extended(self):
        # Determina se il braccio destro è esteso basandosi sulle coordinate dei punti chiave
        if self.right_hip.y > self.right_wrist.y:
            return self.calculate_angle(self.right_elbow, self.right_shoulder, self.right_wrist)

    @property
    def are_forearms_crossed(self):
        # Determina se gli avrambracci effettuano una 'X'
        if self.right_hip.y > self.right_wrist.y > self.right_shoulder.y and self.left_hip.y > self.left_wrist.y > self.left_shoulder.y:
            threshold = self.distance(self.right_elbow, self.right_wrist)
            return self.right_wrist.y < self.right_elbow.y and self.left_wrist.y < self.left_elbow.y and self.distance(self.left_shoulder, self.right_wrist) <= threshold and self.distance(self.right_shoulder, self.left_wrist) <= threshold

    def detect_rotation(self, cv2):
        print("Rotation function")
        # Detect traveling position, then analyze bunch of frame after that and check if one wrist is moving down the other
        # then checking another bunch of frames after to check if it is moving back to starting position.
        if self.is_right_arm_bending and self.is_left_arm_bending and self.right_wrist.y < self.left_wrist.y and (
                (self.right_wrist.y - self.left_wrist.y) < -0.10):
            print("ARMS IN ABS ZONE; POSSIBLE TRAVELLING SIGNAL INCOMING; CHECKING...")
            if len(BufferFrames.images) != 20:
                BufferFrames.static_flag = True
            else:
                # Frames collected, starting to analyze
                BufferFrames.static_flag = True
                print("PUBLISHING THE VIDEO")
                # Definisce la directory e il nome del file
                directory = f"Recording/travelling"
                if not os.path.exists(directory):
                    os.makedirs(directory)
                file_name = f"{directory}/travelling_{int(time.time())}.mp4"
                height, width, layers = BufferFrames.images[0].shape
                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                out = cv2.VideoWriter(file_name, fourcc, 10, (width, height))
                for frame in BufferFrames.images:
                    print(len(BufferFrames.images))
                    out.write(frame)  # frame is a numpy.ndarray with shape (1280, 720, 3)
                out.release()

                # Load YOLOv8 pose model
                model = YOLO('yolov8n-pose.pt')
                i = 0
                starting_position = BufferFrames.images[i]
                is_rotating = False
                finish = False
                previous_frame = BufferFrames.images[i]

                while i < len(BufferFrames.images):
                    # Analyze the frame
                    print("CYCLE LOOP")
                    results = model(BufferFrames.images[i], conf=0.5)
                    body_keypoints = results[0].keypoints.xyn.cpu().numpy()[0]
                    body = Body(body_keypoints)
                    if i != 0:
                        # Can start to compare the frames
                        if body.right_wrist.y <= starting_position.right_wrist.y or (
                                (body.right_wrist.y - starting_position.right_wrist.y) < 0.21
                                and (body.right_wrist.y - starting_position.right_wrist.y) > -0.21):
                            # The wrist is going lower!
                            is_rotating = True
                            print("CURRENT FRAME Y(GOING DOWN):" + str(body.right_wrist.y))
                            print("STARTING FRAME Y(GOING DOWN):" + str(starting_position.right_wrist.y))
                        else:
                            # Wrist can be starting to going up to reach starting position
                            if body.right_wrist.y >= starting_position.right_wrist.y or (
                                    (body.right_wrist.y - starting_position.right_wrist.y) < 0.21 and (
                                    body.right_wrist.y - starting_position.right_wrist.y) > -0.21):
                                is_rotating = True
                                print("CURRENT FRAME Y(GOING UP):" + str(body.right_wrist.y))
                                print("STARTING FRAME Y(GOING UP):" + str(starting_position.right_wrist.y))
                            else:
                                # Wrist not rotating correctly
                                is_rotating = False
                                print("ERROR NOT ROTATING")
                                print("CURRENT FRAME Y:" + str(body.right_wrist.y))
                                print("STARTING FRAME Y:" + str(starting_position.right_wrist.y))
                                print("NUMBER FRAME:" + str(i))

                                return is_rotating

                        if ((previous_frame.right_wrist.y - body.right_wrist.y) < 0.10 and (
                                previous_frame.right_wrist.y - body.right_wrist.y) > -0.10) and i == len(
                                BufferFrames.images) - 1:
                            print("TRAVELLING FINISHED AND ACCOMPLISHED")
                            finish = True
                        if not finish and i == len(BufferFrames.images) - 1:
                            print("FINISHED WITHOUT DETECTING TRAVELLING")
                            is_rotating = False
                    else:
                        print("STARTIN  ASSIGN")
                        starting_position = body
                    previous_frame = body
                    i += 1
                return is_rotating
        else:
            print(self.right_wrist.y - self.left_wrist.y)