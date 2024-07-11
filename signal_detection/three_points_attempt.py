# Detector for "Three Points Attempt" basketball foul


def three_points_attempt(hand, body, cv2, frame, buffer):
    if (body.is_right_arm_up and not hand.is_hand_closed
            and hand.is_three):
        buffer.save_foul("three_point_attempt")
        cv2.putText(
            img=frame,
            text="Three points attempt!",
            org=(50, 50),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(0, 255, 0),
            thickness=2
        )
