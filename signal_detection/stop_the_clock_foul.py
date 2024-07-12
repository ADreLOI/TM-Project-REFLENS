# signal_detection/stop_clock_foul.py

def stop_the_clock_foul(hand, body, cv2, frame, recorder):
    # Controlla se la mano è chiusa, il braccio destro è sollevato e la mano non è aperta
    if (hand.is_hand_closed and body.is_right_arm_up and not hand.is_hand_opened
            and not hand.is_one and not hand.is_two and not hand.is_three):
        # Se non si sta registrando o il tipo di fallo corrente non è "stop_the_clock_foul"
        if not recorder.is_recording or recorder.current_foul_type != "stop_the_clock_foul":
            # Se si sta registrando, ferma la registrazione
            if recorder.is_recording:
                recorder.stop_recording()
            # Avvia una nuova registrazione per il tipo di fallo "stop_the_clock_foul"
            recorder.start_recording("stop_the_clock_foul")
        # Mostra il messaggio "Stop the clock foul!" sul frame
        cv2.putText(
            img=frame,
            text="Stop the clock foul!",
            org=(50, 100),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(255, 0, 0),
            thickness=2
        )
    else:
        # Se si sta registrando e il tipo di fallo corrente è "stop_the_clock_foul", ferma la registrazione
        if recorder.is_recording and recorder.current_foul_type == "stop_the_clock_foul":
            recorder.stop_recording()
