# signal_detection/three_points_attempt.py

def three_points_attempt(hand, body, cv2, frame, recorder):
    # Controlla se il braccio destro è sollevato, la mano non è chiusa e il segno di tre dita è fatto
    if (body.is_right_arm_up and not hand.is_hand_closed
            and hand.is_three):
        # Se non si sta registrando o il tipo di fallo corrente non è "three_points_attempt"
        if not recorder.is_recording or recorder.current_foul_type != "three_points_attempt":
            # Se si sta registrando, ferma la registrazione
            if recorder.is_recording:
                recorder.stop_recording()
            # Avvia una nuova registrazione per il tipo di fallo "three_points_attempt"
            recorder.start_recording("three_points_attempt")
        # Mostra il messaggio "Three points attempt!" sul frame
        cv2.putText(
            img=frame,
            text="Three points attempt!",
            org=(50, 50),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(0, 255, 0),
            thickness=2
        )
    else:
        # Se si sta registrando e il tipo di fallo corrente è "three_points_attempt", ferma la registrazione
        if recorder.is_recording and recorder.current_foul_type == "three_points_attempt":
            recorder.stop_recording()
