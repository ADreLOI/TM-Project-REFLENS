import os
import glob
import time

import cv2
from pydantic import BaseModel
from collections import namedtuple
import numpy as np

# Define a namedtuple for keypoints
Keypoint = namedtuple('Keypoint', ['x', 'y'])


class FoulRecorder:
    def __init__(self, buffer_size=30):
        self.buffer = []
        self.buffer_size = buffer_size

    def update_buffer(self, frame):
        if len(self.buffer) >= self.buffer_size:
            self.buffer.pop(0)
        self.buffer.append(frame)

    def save_foul(self, foul_type):
        if not self.buffer:
            return

        # Define directory and file name
        directory = f"Processing/{foul_type}"
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_name = f"{directory}/{foul_type}_{int(time.time())}.mp4"

        # Define video writer
        height, width, layers = self.buffer[0].shape
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(file_name, fourcc, 20.0, (width, height))

        # Write frames to video
        for frame in self.buffer:
            out.write(frame)

        out.release()
        print(f"Foul video saved: {file_name}")

        # Clear the buffer
        self.buffer.clear()
class BufferFrames:
    static_flag = False
    index = 0
    images = []
    def __init__(self):
        print("Buffer inizializzato")

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

    def detect_rotation(self,cv2):
        print("Rotation function")
        #Detect traveling position, then analyze bunch of frame after that and check if one wrist is moving down the other
        #then checking another bunch of frames after to check if it is moving back to starting position.
        if self.is_right_arm_bending and self.is_left_arm_bending:
            print("ARMS IN ABS ZONE; POSSIBLE TRAVELLING SIGNAL INCOMING; CHECKING...")
            BufferFrames.static_flag = True
            if BufferFrames.index == 150:
                #Frames collected, starting to analyze
                BufferFrames.static_flag = False
                print("PUBLISHING THE VIDEO")
                out = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 20.0, (1280,720))
                for frame in BufferFrames.images:
                    print(len(BufferFrames.images))
                    out.write(frame)  # frame is a numpy.ndarray with shape (1280, 720, 3)
                out.release()


def load_images_from_folder(cv2, folder):
    images = []
    for filename in os.listdir(folder):
        print("FILENAME:" + str(filename))
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images