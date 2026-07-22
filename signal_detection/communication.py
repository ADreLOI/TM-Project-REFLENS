# signal_detection/communication.py
from . import draw_text_with_logo


def communication(hand, body, cv2, frame, recorder):
    # Verifica che la mano e il braccio soddisfino la condizione di "Communication"
    if hand is not None and hand.is_thumb_up and body.is_right_arm_extended and hand.orientation == "Up":
        # Se non si sta registrando o il tipo di fallo corrente non è "communication"
        if not recorder.is_recording or recorder.current_foul_type != "communication":
            if recorder.is_recording:
                recorder.stop_recording()
            recorder.start_recording("communication")
        # Mostra il messaggio "Communication!" sul frame con il logo
        draw_text_with_logo(frame, "Communication!")
    else:
        # Se si sta registrando e il tipo di segnale corrente è "communication", ferma la registrazione
        if recorder.is_recording and recorder.current_foul_type == "communication":
            recorder.stop_recording()
