from pydantic import BaseModel
from collections import namedtuple
import math
import numpy as np

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


    """
    @property
    def arms_rotating(self):
        # Determina se le braccia stanno ruotando controllando se entrambi i bracci sono piegati
        if self.is_left_arm_bending and self.is_right_arm_bending:
            min_rotations = 2
            i = 0
            while i < min_rotations:
                starting_timestamp = time.time()
                starting_position = self.is_wrist_above_the_other
                time.sleep(0.25)  # la rotazione dura approssimativamente 250 millisecondi
                finishing_position = self.is_wrist_above_the_other
                if starting_timestamp < time.time() and starting_position == finishing_position:
                    i += 1
            if i >= min_rotations:
                return True
            else:
                return False

    @property
    def is_wrist_above_the_other(self):
        # Determina se un polso è sopra l'altro
        if self.right_wrist.y <= self.left_wrist.y:
            return True
        else:
            return False
    """
