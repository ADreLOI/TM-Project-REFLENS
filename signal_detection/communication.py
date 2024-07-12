def communication(hand, body, cv2, frame, recorder):
    if hand.is_thumb_up and body.is_right_arm_extended and hand.orientation == "Up":
        # Se non si sta registrando o il tipo di fallo corrente non è "communication"
        if not recorder.is_recording or recorder.current_foul_type != "communication":
            # Se si sta registrando, ferma la registrazione
            if recorder.is_recording:
                recorder.stop_recording()
            # Avvia una nuova registrazione per il tipo di segnale "communication"
            recorder.start_recording("communication")
        cv2.putText(
            img=frame,
            text="Communication",
            org=(50, 50),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(0, 255, 255),
            thickness=2
        )
    else:
        # Se si sta registrando e il tipo di fallo corrente è "stop_the_clock_foul", ferma la registrazione
        if recorder.is_recording and recorder.current_foul_type == "stop_the_clock_foul":
            recorder.stop_recording()
