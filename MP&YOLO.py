import cv2
from ultralytics import YOLO
import mediapipe as mp
from detect_fouls import detect_foul

# Load YOLOv8 pose model
model = YOLO('yolov8n-pose.pt')

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize drawing utilities
mp_drawing = mp.solutions.drawing_utils

video_path = '/Users/matthew/Desktop/UNI/2023:24/Tecnologie Multimediali/Progetto/Some scripts/RefLens/mp4/Videos to Test/BCL Micd Up Moments - Yohan Rosso - Referee - Basketball Champions League.mp4'

# Open the camera
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break
    # Convert the frame to RGB for MediaPipe
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Process the frame for hand detection
    hands_detected = hands.process(frame_rgb)
    # If hands are detected, draw landmarks and connections on the frame
    results = model(frame, conf=0.5)
    if hands_detected.multi_hand_landmarks:
        #Landmarks of the hand detected
        handsLandmarks = hands_detected.multi_hand_landmarks[0]
        for hand_landmarks in hands_detected.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(176, 132, 255), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
            )
            # YOLOv8
        results = model(frame, conf=0.5)
        results_keypoint = results[0].keypoints.xyn.cpu().numpy()
        for result_keypoint in results_keypoint:
            if len(result_keypoint) == 17:
                print("KeyPoint:" + str(result_keypoint[10][1]))
        detect_foul(handsLandmarks,cv2,frame)

    #Extracting keypoints
    #Yolo mappa i keypoints con coordinate X e Y
    # --> X va da sinistra dello schermo fino a destra da 0 a 1
    # --> Y va dal basso dello schermo fino in alto da 1 a 0

    annotated_frame = results[0].plot(boxes=False)

    # Display the frame
    cv2.imshow('YOLOv8 Pose and MediaPipe Hands Integration', annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()