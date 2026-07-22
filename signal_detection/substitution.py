# signal_detection/substitution.py
from . import draw_text_with_logo


def substitution(hand, body, cv2, frame, recorder):
    # Verifica che gli avambracci siano incrociati e che la mano sia aperta se rilevata
    if body.are_forearms_crossed and (hand is None or (hand.is_hand_opened and not hand.is_hand_closed)):
        if not recorder.is_recording or recorder.current_foul_type != "substitution":
            if recorder.is_recording:
                recorder.stop_recording()
            recorder.start_recording("substitution")
        draw_text_with_logo(frame, "Substitution!")
    else:
        if recorder.is_recording and recorder.current_foul_type == "substitution":
            recorder.stop_recording()
