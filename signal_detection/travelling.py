
def travelling(hand, body, cv2, frame):
    if body.detect_rotation(cv2):
        cv2.putText(
            img=frame,
            text="TRAVELLING",
            org=(50, 50),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(0, 255, 0),
            thickness=2
        )
        cv2.imwrite("./Buffer/Travelling.jpg", frame)
    else:
        print("NO")
