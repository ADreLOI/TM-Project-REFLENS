# signal_detection/stop_clock.py

def stop_the_clock(handsLandmarks, cv2, frame):
    # Implement detection logic here
    thumb_tip = handsLandmarks.landmark[4]
    index_tip = handsLandmarks.landmark[8]

    # Example detection logic: Check if thumb and index tips are close
    distance = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5

    # Debug print statements to verify detection logic
    print(f"Thumb tip: ({thumb_tip.x}, {thumb_tip.y}), Index tip: ({index_tip.x}, {index_tip.y}), Distance: {distance}")

    if distance < 0.1:
        cv2.putText(
            img=frame,
            text="Stop Clock Signal Detected",
            org=(50, 50),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(0, 255, 0),
            thickness=2
        )
