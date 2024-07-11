# signal_detection/stop_clock.py


def stop_the_clock(hand, body, cv2, frame, buffer):
    # Implement detection logic here

    if (hand.is_hand_opened and body.is_right_arm_up and not hand.is_hand_closed
            and not hand.is_one and not hand.is_two and not hand.is_three):
        buffer.save_foul("stop_the_clock")
        cv2.putText(
            img=frame,
            text="Stop the clock!",
            org=(50, 50),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(0, 255, 0),
            thickness=2
        )