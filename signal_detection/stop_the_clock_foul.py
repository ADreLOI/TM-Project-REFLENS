def stop_the_clock_foul(hand, body, cv2, frame):

    if (hand.is_hand_closed and body.is_right_arm_up and not hand.is_hand_opened
            and not hand.is_one and not hand.is_two and not hand.is_three):
        cv2.putText(
            img=frame,
            text="Stop the clock for foul 2!",
            org=(50, 50),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(0, 255, 233),
            thickness=2
        )
