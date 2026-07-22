<div align="center">

  <img src="./Assets/Loghi/logo_bis.jpg" alt="RefLens Logo" width="500"/>

  # RefLens — FIBA Basketball Referee Signal Detector

  [![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
  [![YOLOv8](https://img.shields.io/badge/YOLOv8-Pose_Estimation-00FFFF?style=for-the-badge&logo=ultralytics&logoColor=black)](https://docs.ultralytics.com/)
  [![MediaPipe](https://img.shields.io/badge/MediaPipe-Hands-00599C?style=for-the-badge&logo=google&logoColor=white)](https://mediapipe.dev)
  [![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
  [![License](https://img.shields.io/badge/License-GPL_v3-blue.svg?style=for-the-badge)](./LICENSE)

  **An AI-powered real-time computer vision system for recognizing official FIBA referee signals and automatically recording game video highlights.**

</div>

---

## Table of Contents

- [About The Project](#about-the-project)
  - [Purpose & Applications](#purpose--applications)
- [Key Features](#key-features)
- [Supported FIBA Signals](#supported-fiba-signals)
- [Project Architecture](#project-architecture)
- [System Requirements & Installation](#system-requirements--installation)
  - [Hardware Requirements](#hardware-requirements)
  - [Installation Steps](#installation-steps)
- [Usage](#usage)
- [Automatic Highlight Recording](#automatic-highlight-recording)
- [Authors & Credits](#authors--credits)
- [License](#license)

---

## About The Project

**RefLens** is an advanced Computer Vision application developed as an academic project for the **Tecnologie Multimediali** (Multimedia Technologies) course. 

The primary goal of RefLens is to detect, interpret, and log official **FIBA (International Basketball Federation)** referee signals executed by game officials during basketball matches. 

### Purpose & Applications
- **Table Officials & Referees (UdC Support):** Assist court tables and referees by logging signals in real-time, minimizing human errors during intense match play.
- **Broadcasting & Media:** Provide instant visual pop-ups and notifications for live streams, sports broadcasts, and fan telemetry.
- **Educational Tool:** Help novice fans, commentators, and viewers understand basketball rules and referee calls seamlessly.

---

## Key Features

- **Hybrid AI Architecture:** Combines **YOLOv8-Pose** for body posture/arm tracking with **MediaPipe Hands** for ultra-fine finger gesture recognition.
- **Real-Time & File Stream Processing:** Analyzes live webcam feeds or pre-recorded match video files (`.mp4`, `.avi`, `.mov`, `.mkv`).
- **Dynamic Signal Detection Engine:** Modular, plug-and-play architecture for detecting specific FIBA referee signals.
- **Automated Video Clip Recording:** Automatically captures and exports short `.mp4` video clips into designated directories whenever a signal or foul is recognized.
- **Modern Graphical User Interface:** Built with `tkinter` and `Pillow`, offering dark-mode hover controls, logo headers, and dual input selection.

---

## Supported FIBA Signals

| Signal | Description | Image |
| :--- | :--- | :---: |
| **Stop the clock (Violation)** | Raise right arm vertically with an open hand. | ![Stop the clock](./Assets/FIBA%20Signals/stop_the_clock.png) |
| **Stop the clock for foul** | Raise right arm vertically with a closed fist. | ![Stop the clock foul](./Assets/FIBA%20Signals/stop_the_clock_foul.png) |
| **Three points attempt** | Raise right arm forming a "3" gesture (thumb, index, middle fingers extended). | ![Three points attempt](./Assets/FIBA%20Signals/three_points_attempt.png) |
| **Communication** | Extend right arm horizontally with a "thumbs up" gesture. | ![Communication](./Assets/FIBA%20Signals/communication.png) |
| **Substitution** | Cross forearms in front of the chest to form an "X". | ![Substitution](./Assets/FIBA%20Signals/substitution.png) |
| **Travelling** | Rotate hands/arms horizontally in front of the body. | ![Travelling](./Assets/FIBA%20Signals/travelling.png) |

---

## Project Architecture

```
TM-Vision/
├── Assets/
│   ├── FIBA Signals/          # Reference images for FIBA signals
│   ├── Loghi/                 # Application logos and icons
│   ├── camera.png             # UI webcam button icon
│   └── upload.png             # UI file upload button icon
├── Dynamics/
│   ├── body.py                # YOLOv8 pose keypoints & spatial math logic
│   └── hand.py                # MediaPipe hand landmarks gesture classifier
├── Processing/
│   └── video_processing.py    # Main stream loop, frame renderer & detector pipeline
├── Recording/
│   └── rec.py                 # Automatic foul clip recorder & video exporter
├── signal_detection/          # Dynamic plugin modules for each FIBA signal
│   ├── __init__.py            # Banner overlay renderer with logo
│   ├── communication.py       # Communication gesture detector
│   ├── stop_the_clock.py      # Stop clock violation detector
│   ├── stop_the_clock_foul.py # Stop clock foul detector
│   ├── substitution.py        # Substitution gesture detector
│   ├── three_points_attempt.py# 3-Point attempt detector
│   └── travelling.py          # Travelling rotation detector
├── main.py                    # Graphical User Interface entry point
├── requirements.txt           # Python dependencies manifest
├── yolov8n-pose.pt            # Pre-trained YOLOv8 pose model weights
└── README.md                  # Project documentation
```

---

## System Requirements & Installation

### Hardware Requirements
- **Recommended:** Dedicated GPU with CUDA support for high FPS real-time detection.
- **Minimum:** Any standard multi-core CPU (Webcam stream FPS will depend on CPU throughput).

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MattDema/TM-Vision.git
   cd TM-Vision
   ```

2. **Create and activate a virtual environment (recommended):**
   - **Windows:**
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **Linux / macOS:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   > **Note for PyTorch GPU Acceleration:** If you have an NVIDIA GPU, install CUDA-enabled PyTorch by following instructions at [pytorch.org](https://pytorch.org/get-started/locally/).

---

## Usage

Launch the main application interface by executing `main.py`:

```bash
python main.py
```

### Graphical Interface Controls:
1. **Use Webcam:** Starts real-time stream analysis using your connected camera feed (Device index `0`).
2. **Use an Existing Video:** Opens a file dialog to select a pre-recorded match video (`.mp4`, `.avi`, `.mov`).
3. Press **`q`** at any time during stream playback to close the video analysis window.

---

## Automatic Highlight Recording

When a FIBA referee signal is detected, **RefLens** activates its `FoulRecorder` engine:
- Video frames are continually saved in a sliding ring buffer.
- Upon signal confirmation, the program automatically compiles and exports an `.mp4` video file into the `Recording/<signal_name>/` folder.
- Video files are timestamped (e.g., `Recording/communication/communication_1721636400.mp4`).

---

## Authors & Credits

Developed by:
- **Andrea Lo Iacono** — [<andrea.loiacono@studenti.unitn.it>](mailto:andrea.loiacono@studenti.unitn.it)
- **Matthew De Marco** — [<matthew.demarco@studenti.unitn.it>](mailto:matthew.demarco@studenti.unitn.it)

*Università degli Studi di Trento — Course: Tecnologie Multimediali*

---

## License

Distributed under the **GNU General Public License v3.0 (GPL-3.0)**. See [`LICENSE`](./LICENSE) for more information.