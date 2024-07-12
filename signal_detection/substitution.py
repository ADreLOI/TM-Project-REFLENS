# signal_detection/substitution.py
from . import draw_text_with_logo


def substitution(hand, body, cv2, frame, recorder):
    # Verifica che gli avambracci siano incrociati
    if hand.is_hand_opened and body.are_forearms_crossed and not hand.is_hand_closed and not hand.is_one and not hand.is_two and not hand.is_three:
        # Se non si sta registrando o il tipo di fallo corrente non è "substitution"
        if not recorder.is_recording or recorder.current_foul_type != "substitution":
            # Se si sta registrando, ferma la registrazione
            if recorder.is_recording:
                recorder.stop_recording()
            # Avvia una nuova registrazione per il tipo di fallo "substitution"
            recorder.start_recording("substitution")
        # Mostra il messaggio "Substitution!" sul frame
        draw_text_with_logo(frame, "Substitution!")
    else:
        # Se si sta registrando e il tipo di fallo corrente è "substitution", ferma la registrazione
        if recorder.is_recording and recorder.current_foul_type == "substitution":
            recorder.stop_recording()

