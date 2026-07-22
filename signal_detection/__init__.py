import cv2
import os

# Definisce il percorso del logo
logo_path = os.path.join(os.path.dirname(__file__), '..', 'Assets', 'Loghi', 'mini_logo.jpg')

# Carica il logo se il file esiste
logo = cv2.imread(logo_path) if os.path.exists(logo_path) else None


def draw_text_with_logo(frame, text, padding=10):
    """
    Disegna un banner in sovrimpressione sul frame contenente il testo del segnale e il logo.
    """
    font = cv2.FONT_HERSHEY_DUPLEX
    font_scale = 1
    font_thickness = 2
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)

    frame_height, frame_width, _ = frame.shape

    if logo is not None and logo.size > 0:
        # Calcola le dimensioni proporzionali del logo
        max_logo_height = text_size[1] + 2 * padding
        max_logo_width = int(logo.shape[1] * (max_logo_height / logo.shape[0]))
        resized_logo = cv2.resize(logo, (max_logo_width, max_logo_height))

        # Calcola posizione e dimensione del rettangolo di sfondo
        rect_width = text_size[0] + max_logo_width + 3 * padding
        rect_height = max(text_size[1], max_logo_height) + 2 * padding
        rect_x = max(padding, frame_width - rect_width - padding)
        rect_y = padding

        # Disegna lo sfondo
        cv2.rectangle(frame, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), (209, 230, 232), -1)

        # Disegna il testo
        text_x = rect_x + padding
        text_y = rect_y + ((rect_height - text_size[1]) // 2) + text_size[1]
        cv2.putText(frame, text, (text_x, text_y), font, font_scale, (0, 0, 0), font_thickness)

        # Sovrapponi il logo
        logo_x = text_x + text_size[0] + padding
        logo_y = rect_y + ((rect_height - max_logo_height) // 2)
        frame[logo_y:logo_y + max_logo_height, logo_x:logo_x + max_logo_width] = resized_logo
    else:
        # Fallback solo testo se il logo non è caricato
        rect_width = text_size[0] + 2 * padding
        rect_height = text_size[1] + 2 * padding
        rect_x = max(padding, frame_width - rect_width - padding)
        rect_y = padding

        cv2.rectangle(frame, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), (209, 230, 232), -1)
        text_x = rect_x + padding
        text_y = rect_y + text_size[1] + (padding // 2)
        cv2.putText(frame, text, (text_x, text_y), font, font_scale, (0, 0, 0), font_thickness)
