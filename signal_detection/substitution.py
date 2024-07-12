def substitution(hand, body, cv2, frame, recorder):
    if hand.is_hand_opened and body.are_forearms_crossed and not hand.is_hand_closed and not hand.is_one and not hand.is_two and not hand.is_three:
        cv2.putText(
            img=frame,
            text="Substitution",
            org=(50, 50),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(0, 255, 255),
            thickness=2
        )
