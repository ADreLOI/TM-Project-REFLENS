# signal_detection/communication.py
from . import draw_text_with_logo


def communication(hand, body, cv2, frame, recorder):
    # Verifica che il braccio destro sia esteso e che il pollice stia facendo il Thumbs Up
    if hand.is_thumb_up and body.is_right_arm_extended and hand.orientation == "Up":
        # Se non si sta registrando o il tipo di fallo corrente non è "communication"
        if not recorder.is_recording or recorder.current_foul_type != "communication":
            # Se si sta registrando, ferma la registrazione
            if recorder.is_recording:
                recorder.stop_recording()
            # Avvia una nuova registrazione per il tipo di segnale "communication"
            recorder.start_recording("communication")
        # Mostra il messaggio "Communication!" sul frame con il logo
        draw_text_with_logo(frame, "Communication!")
    else:
        # Se si sta registrando e il tipo di fallo corrente è "stop_the_clock_foul", ferma la registrazione
        if recorder.is_recording and recorder.current_foul_type == "stop_the_clock_foul":
            recorder.stop_recording()
