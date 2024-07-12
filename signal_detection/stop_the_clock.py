# signal_detection/stop_clock.py

def stop_the_clock(hand, body, cv2, frame, recorder):
    # Stampa le coordinate del polso sinistro, dell'orecchio sinistro e dell'occhio sinistro
    print(
        f"Left wrist: ({body.left_wrist.y}), Ear ({body.left_ear.y}), Eye ({body.left_eye.y}),"
    )

    # Controlla se la mano è aperta, il braccio destro è sollevato e nessuna delle dita è chiusa
    if (hand.is_hand_opened and body.is_right_arm_up and not hand.is_hand_closed
            and not hand.is_one and not hand.is_two and not hand.is_three):
        # Se non si sta registrando o il tipo di fallo corrente non è "stop_the_clock"
        if not recorder.is_recording or recorder.current_foul_type != "stop_the_clock":
            # Se si sta registrando, ferma la registrazione
            if recorder.is_recording:
                recorder.stop_recording()
            # Avvia una nuova registrazione per il tipo di fallo "stop_the_clock"
            recorder.start_recording("stop_the_clock")
        # Mostra il messaggio "Stop the clock!" sul frame
        cv2.putText(
            img=frame,
            text="Stop the clock!",
            org=(50, 50),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(0, 255, 0),
            thickness=2
        )
    else:
        # Se si sta registrando e il tipo di fallo corrente è "stop_the_clock", ferma la registrazione
        if recorder.is_recording and recorder.current_foul_type == "stop_the_clock":
            recorder.stop_recording()

"""
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