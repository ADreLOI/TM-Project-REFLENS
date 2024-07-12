import cv2
import os
import time

class FoulRecorder:
    def __init__(self, buffer_size=30, fps=20.0):
        # Inizializza il registratore con buffer vuoti, dimensione del buffer e frame per second (fps)
        self.buffers = {}
        self.buffer_size = buffer_size
        self.fps = fps
        self.current_foul_type = None
        self.is_recording = False

    def start_recording(self, foul_type):
        # Imposta il tipo di fallo corrente
        self.current_foul_type = foul_type
        # Se il tipo di fallo non è presente nei buffer, crea una nuova lista
        if foul_type not in self.buffers:
            self.buffers[foul_type] = []
        # Imposta la registrazione su True
        self.is_recording = True

    def stop_recording(self):
        # Se c'è un tipo di fallo corrente e presente nei buffer
        if self.current_foul_type and self.current_foul_type in self.buffers:
            # Salva il video del fallo
            self.save_foul(self.current_foul_type)
            # Pulisce il buffer del tipo di fallo corrente
            self.buffers[self.current_foul_type].clear()
        # Ferma la registrazione e resetta il tipo di fallo corrente
        self.is_recording = False
        self.current_foul_type = None

    def update_buffer(self, frame):
        # Se è in corso una registrazione e c'è un tipo di fallo corrente
        if self.is_recording and self.current_foul_type:
            buffer = self.buffers[self.current_foul_type]
            # Se il buffer ha raggiunto la dimensione massima, rimuove il primo frame
            if len(buffer) >= self.buffer_size:
                buffer.pop(0)
            # Aggiunge il nuovo frame al buffer
            buffer.append(frame)

    def save_foul(self, foul_type):
        # Se il tipo di fallo non è nei buffer o il buffer è vuoto, esce
        if foul_type not in self.buffers or not self.buffers[foul_type]:
            return

        # Definisce la directory e il nome del file
        directory = f"Recording/{foul_type}"
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_name = f"{directory}/{foul_type}_{int(time.time())}.mp4"

        # Definisce il video writer
        height, width, layers = self.buffers[foul_type][0].shape
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(file_name, fourcc, self.fps, (width, height))

        # Scrive i frame nel video
        for frame in self.buffers[foul_type]:
            out.write(frame.astype('uint8'))

        out.release()
        print(f"Foul video saved: {file_name}")
