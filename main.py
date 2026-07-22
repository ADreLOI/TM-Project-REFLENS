import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance
import sys
import os

# Ottiene la directory dello script corrente
current_dir = os.path.dirname(os.path.abspath(__file__))

# Aggiunge la directory radice del progetto a sys.path
sys.path.append(current_dir)

# Importa la funzione di elaborazione video
from Processing.video_processing import process_video

# Funzione per gestire l'elaborazione della webcam
def handle_webcam_processing():
    # Chiama process_video senza argomenti per utilizzare la webcam
    process_video()

# Funzione per gestire l'elaborazione del file video
def handle_video_file_processing():
    # Apre un file dialog per selezionare un file video
    filename = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov;*.mkv"), ("All files", "*.*")])
    # Se un file è selezionato, lo elabora
    if filename:
        print("Selected video file:", filename)
        process_video(filename)

# Inizializza la finestra principale
root = tk.Tk()
root.title("RefLens - FIBA Signal Detection")

# Imposta l'icona della finestra se disponibile
icon_path = os.path.join(current_dir, 'Assets', 'Loghi', 'mini_logo_refined.ico')
if os.path.exists(icon_path):
    try:
        root.iconbitmap(icon_path)
    except Exception:
        pass

# Ottiene la larghezza e l'altezza dello schermo
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calcola la posizione della finestra per essere al centro dello schermo
window_width = 800
window_height = 600
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

# Imposta la dimensione e la posizione della finestra
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
root.resizable(False, False)

# Imposta il colore di sfondo della finestra
root.configure(bg='#E8E6D1')

# Funzione per creare un pulsante con immagine e effetto hover
def create_image_button(canvas, image_path, x, y, command):
    # Apre e ridimensiona l'immagine
    img = Image.open(image_path)
    img.thumbnail((100, 100), Image.LANCZOS)
    
    # Aggiunge sfondo all'immagine
    img_with_bg = Image.new("RGBA", (100, 100), "#E8E6D1")
    img_with_bg.paste(img, ((100 - img.size[0]) // 2, (100 - img.size[1]) // 2), img)
    photo = ImageTk.PhotoImage(img_with_bg)

    # Crea una versione più scura dell'immagine per l'effetto hover
    enhancer = ImageEnhance.Brightness(img_with_bg)
    img_darker = enhancer.enhance(0.7)
    photo_darker = ImageTk.PhotoImage(img_darker)

    # Crea il pulsante sul canvas
    button_id = canvas.create_image(x, y, image=photo, anchor="center")
    
    # Mantiene i riferimenti per evitare la garbage collection
    if not hasattr(canvas, 'button_images'):
        canvas.button_images = []
    canvas.button_images.extend([photo, photo_darker])

    # Definisce i gestori di eventi per l'interazione con il pulsante
    def on_enter(event):
        canvas.itemconfig(button_id, image=photo_darker)

    def on_leave(event):
        canvas.itemconfig(button_id, image=photo)

    def on_click(event):
        command()

    # Associa gli eventi al pulsante
    canvas.tag_bind(button_id, "<Enter>", on_enter)
    canvas.tag_bind(button_id, "<Leave>", on_leave)
    canvas.tag_bind(button_id, "<Button-1>", on_click)

# Crea un canvas per contenere i pulsanti e il testo
canvas = tk.Canvas(root, bg="#E8E6D1", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Carica e ridimensiona il logo
logo_path = os.path.join(current_dir, 'Assets', 'Loghi', 'mini_logo.jpg')
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    logo_width, logo_height = logo.size
    new_logo_height = 50
    new_logo_width = int(new_logo_height * logo_width / logo_height)
    resized_logo = logo.resize((new_logo_width, new_logo_height), Image.LANCZOS)
    logo_photo = ImageTk.PhotoImage(resized_logo)

    # Contenitore per l'intestazione
    header_frame = tk.Frame(root, bg='#E8E6D1')
    header_frame.place(relx=0.5, rely=0.1, anchor="center")

    app_name_label = tk.Label(header_frame, text="RefLens", font=("Segoe UI", 40, "bold"), fg="#000000", bg="#E8E6D1")
    app_name_label.pack(side="left")

    logo_label = tk.Label(header_frame, image=logo_photo, bg="#E8E6D1")
    logo_label.image = logo_photo
    logo_label.pack(side="left", padx=10)

# Altri elementi dell'interfaccia grafica
info_label = tk.Label(root, text="Select Input Method", font=("Segoe UI", 20, "bold"), fg="#000000", bg="#E8E6D1")
info_label.place(relx=0.5, rely=0.3, anchor="center")

# Etichette sopra i pulsanti
webcam_label = tk.Label(root, text="Use Webcam", font=("Segoe UI", 15), fg="#000000", bg="#E8E6D1")
webcam_label.place(relx=0.25, rely=0.45, anchor="center")

video_label = tk.Label(root, text="Use an Existing Video", font=("Segoe UI", 15), fg="#000000", bg="#E8E6D1")
video_label.place(relx=0.75, rely=0.45, anchor="center")

# Pulsanti con immagini
create_image_button(canvas, os.path.join(current_dir, 'Assets', 'camera.png'), 200, 400, handle_webcam_processing)
create_image_button(canvas, os.path.join(current_dir, 'Assets', 'upload.png'), 600, 400, handle_video_file_processing)

if __name__ == "__main__":
    root.mainloop()
