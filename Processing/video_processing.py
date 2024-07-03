import cv2
from ultralytics import YOLO
import mediapipe as mp
import importlib
import os
import time


def load_signal_detectors():
    """
        Dynamically loads signal detection functions from signal_detection package.

        Returns:
            dict: A dictionary containing signal detector functions mapped by their names.
        """
    signal_detectors = {}
    signal_detection_folder = os.path.join(os.path.dirname(__file__), '..', 'signal_detection')

    print(f"Looking for signal detectors in folder: {signal_detection_folder}")

    # Iterate through files in the signal detection folder
    for file in os.listdir(signal_detection_folder):
        # Check if the file is a Python script and not the package initializer
        if file.endswith('.py') and file != '__init__.py':
            # Extract module name from file name
            module_name = file[:-3]
            print(f"Found module: {module_name}")

            # Import the module dynamically
            module = importlib.import_module(f'signal_detection.{module_name}')
            print(f"Imported module: {module}")

            # Get the detection function from the module
            detector_function = getattr(module, f'{module_name}', None)
            if detector_function:
                print(f"Loaded detector function: {module_name}")
                signal_detectors[module_name] = detector_function
            else:
                print(f"Warning: No {module_name} function found in module {module}")

    return signal_detectors


def process_stream(video_source):
    """
    Process video stream from either webcam or file for signal detection.

    Args:
        video_source (int or str): Video source, either webcam (0) or file path.
    """
    # Load YOLOv8 pose model
    model = YOLO('yolov8n-pose.pt')

    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    # Initialize drawing utilities
    mp_drawing = mp.solutions.drawing_utils

    signal_detectors = load_signal_detectors()

    # Open the video source (0 for webcam, or file path)
    cap = cv2.VideoCapture(video_source)

    if not cap.isOpened():
        print(f"Error: Unable to open video source {video_source}")
        return

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        # Convert the frame to RGB for MediaPipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Process the frame for hand detection
        hands_detected = hands.process(frame_rgb)
        # If hands are detected, draw landmarks and connections on the frame

        if hands_detected.multi_hand_landmarks:
            # Landmarks of the hand detected
            handsLandmarks = hands_detected.multi_hand_landmarks[0]
            for detector_name, detector_function in signal_detectors.items():
                detector_function(handsLandmarks, cv2, frame)
                # Introduce a small delay
                time.sleep(0.05)  # 50 milliseconds delay

            for hand_landmarks in hands_detected.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(176, 132, 255), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
                )

        # YOLOv8 pose detection
        body_results = model(frame, conf=0.5)
        results_keypoint = body_results[0].keypoints.xyn.cpu().numpy()
        # Extracting keypoints
        # Yolo mappa i keypoints con coordinate X e Y
        # --> X va da sinistra dello schermo fino a destra da 0 a 1
        # --> Y va dal basso dello schermo fino in alto da 1 a 0
        for result_keypoint in results_keypoint:
            if len(result_keypoint) == 17:
                print("KeyPoint:" + str(result_keypoint[10][1]))

        annotated_frame = body_results[0].plot(boxes=False)

        cv2.imshow('RefLens - Stream Analysis', annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()

def process_video(video_path=None):
    """
    Process video file for signal detection.

    Args:
        video_path (str): Path to the video file. If None, uses webcam.
    """
    if video_path is None:
        process_stream(0)  # Use webcam
    else:
        process_stream(video_path)  # Use video file