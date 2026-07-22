# signal_detection/travelling.py
from . import draw_text_with_logo


def travelling(hand, body, cv2, frame, recorder):
    if body.detect_rotation(cv2):
        # Mostra il messaggio "Travelling!" sul frame
        draw_text_with_logo(frame, "Travelling!")