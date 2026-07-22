# signal_detection/stop_the_clock.py
from . import draw_text_with_logo


def stop_the_clock(hand, body, cv2, frame, recorder):
    # Controlla se la mano è aperta, il braccio destro è sollevato e nessuna delle dita è chiusa
    if (hand is not None and hand.is_hand_opened and body.is_right_arm_up and not hand.is_hand_closed
            and not hand.is_one and not hand.is_two and not hand.is_three):
        if not recorder.is_recording or recorder.current_foul_type != "stop_the_clock":
            if recorder.is_recording:
                recorder.stop_recording()
            recorder.start_recording("stop_the_clock")

        # Mostra il messaggio "Stop the clock!" sul frame con il logo
        draw_text_with_logo(frame, "Stop the clock!")
    else:
        if recorder.is_recording and recorder.current_foul_type == "stop_the_clock":
            recorder.stop_recording()