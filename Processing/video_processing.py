import cv2
from ultralytics import YOLO
import mediapipe as mp
import importlib
import os

from Dynamics.hand import Hand
from Dynamics.body import Body
from Recording.rec import FoulRecorder
from Dynamics.body import BufferFrames

def load_signal_detectors():
    """
    Carica dinamicamente le funzioni di rilevamento dei segnali dal package signal_detection.

    Ritorna:
        dict: Un dizionario contenente le funzioni di rilevamento dei segnali mappate dai loro nomi.
    """
    signal_detectors = {}
    signal_detection_folder = os.path.join(os.path.dirname(__file__), '..', 'signal_detection')

    print(f"Looking for signal detectors in folder: {signal_detection_folder}")

    # Itera attraverso i file nella cartella di rilevamento dei segnali
    for file in os.listdir(signal_detection_folder):
        # Controlla se il file è uno script Python e non l'inizializzatore del pacchetto
        if file.endswith('.py') and file != '__init__.py':
            # Estrae il nome del modulo dal nome del file (rimuove .py)
            module_name = file[:-3]
            print(f"Found module: {module_name}")

            # Importa il modulo dinamicamente utilizzando importlib
            module = importlib.import_module(f'signal_detection.{module_name}')
            print(f"Imported module: {module}")

            # Ottiene la funzione di rilevamento dal modulo
            detector_function = getattr(module, f'{module_name}', None)
            if detector_function:
                print(f"Loaded detector function: {module_name}")
                # Aggiunge la funzione di rilevamento al dizionario
                signal_detectors[module_name] = detector_function
            else:
                print(f"Warning: No {module_name} function found in module {module}")

    return signal_detectors


def process_stream(video_source):
    """
    Elabora il flusso video dalla webcam o dal file per il rilevamento dei segnali.

    Args:
        video_source (int or str): Sorgente video, webcam (0) o percorso del file.
    """
    # Carica il modello YOLOv8 pose
    model = YOLO('yolov8n-pose.pt')

    # Inizializza MediaPipe Hands per il rilevamento delle mani
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    # Inizializza le utilità di disegno di MediaPipe
    mp_drawing = mp.solutions.drawing_utils

    # Carica le funzioni di rilevamento dei segnali
    signal_detectors = load_signal_detectors()

    # Inizializza il registratore di falli
    recorder = FoulRecorder(buffer_size=120, fps=10.0)

    # Apri la sorgente video (0 per la webcam o percorso del file)
    cap = cv2.VideoCapture(video_source)

    if not cap.isOpened():
        print(f"Error: Unable to open video source {video_source}")
        return

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # Converti il frame da BGR a RGB per MediaPipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Elabora il frame per il rilevamento delle mani
        hands_detected = hands.process(frame_rgb)

        # Rilevamento della posa con YOLOv8
        results = model(frame, conf=0.5)

        # Se vengono rilevate le mani, disegna i punti di riferimento e le connessioni sul frame
        if hands_detected.multi_hand_landmarks:
            handsLandmarks = hands_detected.multi_hand_landmarks[0]

            for hand_landmarks in hands_detected.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(176, 132, 255), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
                )

            # Estrae i punti chiave del corpo dai risultati di YOLOv8
            body_keypoints = results[0].keypoints.xyn.cpu().numpy()[0]

            # Crea istanze delle classi Hand e Body utilizzando i punti di riferimento rilevati
            hand = Hand(handsLandmarks)
            body = Body(body_keypoints)

            # Aggiorna il buffer del registratore con il frame corrente
            recorder.update_buffer(frame)

            # Chiama le funzioni di rilevamento dei segnali
            for detector_name, detector_function in signal_detectors.items():
                detector_function(hand, body, cv2, frame, recorder)

        # Annotazione del frame con i risultati del rilevamento della posa
        annotated_frame = results[0].plot(boxes=False)

        # Mostra il frame annotato in una finestra
        cv2.imshow('RefLens - Stream Analysis', annotated_frame)
        if BufferFrames.static_flag == True:
            print("COLLECTING FRAMES...")
            BufferFrames.images.append(frame)
            if len(BufferFrames.images) == 20:
                BufferFrames.static_flag = False

        # Esce dal ciclo se viene premuto il tasto 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Rilascia la sorgente video e chiudi tutte le finestre
    cap.release()
    cv2.destroyAllWindows()


def process_video(video_path=None):
    """
    Elabora il file video per il rilevamento dei segnali.

    Args:
        video_path (str): Percorso del file video. Se None, usa la webcam.
    """
    if video_path is None:
        process_stream(0)  # Usa la webcam
    else:
        process_stream(video_path)  # Usa il file video
