# signal_detection/stop_clock_foul.py
from . import draw_text_with_logo


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
        draw_text_with_logo(frame, "Stop the clock foul!")
    else:
        # Se si sta registrando e il tipo di fallo corrente è "stop_the_clock_foul", ferma la registrazione
        if recorder.is_recording and recorder.current_foul_type == "stop_the_clock_foul":
            recorder.stop_recording()
