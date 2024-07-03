# main.py
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance
import sys
import os


# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Append the path for the processing script
sys.path.append(os.path.join(current_dir, 'Processing'))

# Import the processing function
from video_processing import process_video

# Function to handle webcam processing
def handle_webcam_processing():
    # Call process_video without arguments to use the webcam
    process_video()

# Function to handle video file processing
def handle_video_file_processing():
    # Open a file dialog to select a video file
    filename = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    # If a file is selected, print its path and process it
    if filename:
        print("Selected video file:", filename)
        # Pass the video file path to process_video
        process_video(filename)

# Initialize the main window
root = tk.Tk()
root.title("RefLens")

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the position for the window to be in the middle of the screen
window_width = 800
window_height = 600
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

# Set window size and position
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Set window background color
root.configure(bg='#2E3440')

# Function to create image button with hover effect
def create_image_button(canvas, image_path, x, y, command):
    # Open and resize the image
    img = Image.open(image_path)
    img.thumbnail((100, 100), Image.LANCZOS)  # Resize image to fit within (100, 100)
    # Add background to the image
    img_with_bg = Image.new("RGBA", (100, 100), "#2E3440")
    img_with_bg.paste(img, ((100 - img.size[0]) // 2, (100 - img.size[1]) // 2), img)
    photo = ImageTk.PhotoImage(img_with_bg)

    # Create a darker version of the image for hover effect
    enhancer = ImageEnhance.Brightness(img_with_bg)
    img_darker = enhancer.enhance(0.7)
    photo_darker = ImageTk.PhotoImage(img_darker)

    # Create the button on the canvas
    button_id = canvas.create_image(x, y, image=photo, anchor="center")
    # Keep a reference to avoid garbage collection
    canvas.image = photo
    canvas.image_darker = photo_darker

    # Define event handlers for button interaction
    def on_enter(event):
        canvas.itemconfig(button_id, image=photo_darker)

    def on_leave(event):
        canvas.itemconfig(button_id, image=photo)

    def on_click(event):
        command()

    # Bind events to the button
    canvas.tag_bind(button_id, "<Enter>", on_enter)
    canvas.tag_bind(button_id, "<Leave>", on_leave)
    canvas.tag_bind(button_id, "<Button-1>", on_click)

# Create a canvas to hold the buttons and text
canvas = tk.Canvas(root, bg="#2E3440", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Add app name label
app_name_label = tk.Label(root, text="RefLens", font=("Helvetica", 36, "bold"), fg="#D8DEE9", bg="#2E3440")
app_name_label.place(relx=0.5, rely=0.1, anchor="center")

# Additional GUI elements
info_label = tk.Label(root, text="Select input method", font=("Helvetica", 18), fg="#D8DEE9", bg="#2E3440")
info_label.place(relx=0.5, rely=0.3, anchor="center")

# Add labels above the buttons
webcam_label = tk.Label(root, text="Use Webcam", font=("Helvetica", 14), fg="#D8DEE9", bg="#2E3440")
webcam_label.place(relx=0.25, rely=0.45, anchor="center")

video_label = tk.Label(root, text="Use an Existing Video", font=("Helvetica", 14), fg="#D8DEE9", bg="#2E3440")
video_label.place(relx=0.75, rely=0.45, anchor="center")

# Create buttons with images on the canvas
create_image_button(canvas, os.path.join(current_dir, 'Assets', 'camera.png'), 200, 400, handle_webcam_processing)
create_image_button(canvas, os.path.join(current_dir, 'Assets', 'upload.png'), 600, 400, handle_video_file_processing)

# Run the application
root.mainloop()
