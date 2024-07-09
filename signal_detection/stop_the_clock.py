# signal_detection/stop_clock.py


def stop_the_clock(hand, body, cv2, frame):
    # Implement detection logic here

    # Example detection logic: Check if thumb and index tips are close
    # distance = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5

    # Debug print statements to verify detection logic
    print(
        f"Left wrist: ({body.left_wrist.y}), Ear ({body.left_ear.y}), Eye ({body.left_eye.y}),"
    )

    if body.arms_rotating:
        cv2.putText(
            img=frame,
            text="Arms Rotating",
            org=(50, 50),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(0, 255, 0),
            thickness=2
        )


"""
    if (hand.is_hand_opened and body.is_right_arm_up and not hand.is_hand_closed
            and not hand.is_one and not hand.is_two and not hand.is_three):
        cv2.putText(
            img=frame,
            text="Stop the clock!",
            org=(50, 50),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(0, 255, 0),
            thickness=2
        )

    if body.is_right_arm_bending:
        cv2.putText(
            img=frame,
            text="Right arm bending",
            org=(50, 50),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(0, 255, 0),
            thickness=2
        )

    if body.is_left_arm_bending:
        cv2.putText(
            img=frame,
            text="Left arm bending",
            org=(150, 50),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(0, 255, 0),
            thickness=2
        )

    if hand.is_hand_closed and not hand.is_hand_opened 
            and not hand.is_one and not hand.is_two and not hand.is_three:
        cv2.putText(
            img=frame,
            text="Hand Is Closed",
            org=(50, 50),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(0, 255, 255),
            thickness=2
        )

    if hand.is_one and not hand.is_hand_opened and not 
            hand.is_hand_closed and not hand.is_two and not hand.is_three:
        cv2.putText(
            img=frame,
            text="One",
            org=(50, 50),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(111, 255, 255),
            thickness=2
        )

    if hand.is_two and not hand.is_hand_opened and not 
            hand.is_hand_closed and not hand.is_one and not hand.is_three:
        cv2.putText(
            img=frame,
            text="Two",
            org=(50, 50),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(0, 255, 111),
            thickness=2
        )

    if hand.is_three and not hand.is_hand_opened and not 
            hand.is_hand_closed and not hand.is_one and not hand.is_two:
        cv2.putText(
            img=frame,
            text="Three",
            org=(50, 50),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(0, 111, 255),
            thickness=2
        )

"""
