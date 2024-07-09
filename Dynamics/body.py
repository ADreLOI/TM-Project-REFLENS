import time

from pydantic import BaseModel
from collections import namedtuple
import numpy as np

# Define a namedtuple for keypoints
Keypoint = namedtuple('Keypoint', ['x', 'y'])


class GetKeypoint(BaseModel):
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


class Body:
    def __init__(self, body_keypoints: np.ndarray):
        self.body_keypoints = [Keypoint(*keypoint) for keypoint in body_keypoints]
        self.keypoints = GetKeypoint()
        self.init_body()

    def get_coordinates(self, keypoint_name: str):
        keypoint_index = getattr(self.keypoints, keypoint_name)
        return self.body_keypoints[keypoint_index]

    def init_body(self):
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
        return (self.left_wrist.y < self.left_eye.y < self.left_ear.y and
                self.left_wrist.y < self.left_elbow.y < self.left_shoulder.y and
                self.left_elbow.y < self.left_eye.y < self.left_ear.y)

    @property
    def is_right_arm_up(self):
        return (self.right_wrist.y < self.right_eye.y < self.right_ear.y and
                self.right_wrist.y < self.right_elbow.y < self.right_shoulder.y and
                self.right_elbow.y < self.right_eye.y < self.right_ear.y)

    @property
    def is_left_arm_bending(self):
        if self.left_hip.y > self.left_wrist.y > self.left_shoulder.y:
            if self.left_shoulder.x < self.right_shoulder.x or self.right_shoulder.x == self.left_shoulder.x:
                return self.left_wrist.x > self.left_shoulder.x or self.left_wrist.x == self.left_shoulder.x
            else:
                return self.left_wrist.x < self.left_shoulder.x or self.left_wrist.x == self.left_shoulder.x

    @property
    def is_right_arm_bending(self):
        if self.right_hip.y > self.right_wrist.y > self.right_shoulder.y:
            if self.right_shoulder.x > self.left_shoulder.x or self.right_shoulder.x == self.left_shoulder.x:
                return self.right_wrist.x < self.right_shoulder.x or self.right_wrist.x == self.right_shoulder.x
            else:
                return self.right_wrist.x > self.right_shoulder.x or self.right_wrist.x == self.right_shoulder.x

    @property
    def arms_rotating(self):
        if self.is_left_arm_bending and self.is_right_arm_bending:
            min_rotations = 2
            i = 0
            while i < min_rotations:
                starting_timestamp = time.time()
                starting_position = self.is_wrist_above_the_other
                #time.sleep(0.25)  # rotation takes approximately 250 milliseconds
                finishing_position = self.is_wrist_above_the_other
                if starting_timestamp < time.time() and starting_position == finishing_position:
                    i += 1
            if i >= min_rotations:
                return True
            else:
                return False

    @property
    def is_wrist_above_the_other(self):
        if self.right_wrist.y <= self.left_wrist.y:
            return True
        else:
            return False
