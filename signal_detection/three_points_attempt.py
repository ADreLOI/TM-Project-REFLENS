# signal_detection/three_points_attempt.py
from . import draw_text_with_logo


def three_points_attempt(hand, body, cv2, frame, recorder):
    # Controlla se il braccio destro è sollevato, la mano non è chiusa e il segno di tre dita è fatto
    if (hand is not None and body.is_right_arm_up and not hand.is_hand_closed and hand.is_three):
        if not recorder.is_recording or recorder.current_foul_type != "three_points_attempt":
            if recorder.is_recording:
                recorder.stop_recording()
            recorder.start_recording("three_points_attempt")
        draw_text_with_logo(frame, "Three Points Attempt!")
    else:
        if recorder.is_recording and recorder.current_foul_type == "three_points_attempt":
            recorder.stop_recording()
