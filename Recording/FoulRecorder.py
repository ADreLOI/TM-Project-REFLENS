import os
import cv2
import time


class BufferFrames:
    static_flag = False
    counter = 0
    buffer_size = 35
    context_frames_counter = 0
    images = []

    def __init__(self):
        print("Buffer inizializzato")

    def update_buffer(self, frame):
        if BufferFrames.static_flag:
            print("COLLECTING FRAMES...")
            if len(self.images) >= self.buffer_size:
                self.images.pop(0)
                self.context_frames_counter += 1
            self.images.append(frame)
            if self.context_frames_counter >= 5:
                self.static_flag = False

    def save_foul(self, foul_type):
        if not self.images:
            self.static_flag = True
            return

        self.static_flag = True
        directory = f"Recording/{foul_type}"  # Define directory and file name
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_name = f"{directory}/{foul_type}_{int(time.time())}.mp4"

        # Define video writer
        height, width, layers = self.images[0].shape
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(file_name, fourcc, 20.0, (width, height))

        # Write frames to video
        for frame in self.images:
            out.write(frame)

        out.release()
        print(f"Foul video saved: {file_name}")

        # Clear the buffer
        self.images.clear()
