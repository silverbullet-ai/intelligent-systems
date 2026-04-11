![Status](https://img.shields.io/badge/status-active-success)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![OpenCV](https://img.shields.io/badge/opencv-computer%20vision-green)
![MediaPipe](https://img.shields.io/badge/mediapipe-hand%20tracking-orange)

# Musicon  
### Gesture-Based Media & Volume Control

---

## Overview  
**Musicon** is a real-time computer vision system that enables hands-free control of media playback and system volume using intuitive hand gestures.

Built using **MediaPipe** and **OpenCV**, the system detects hand landmarks and maps gestures to system-level actions, eliminating the need for physical input devices.

---

## Key Features  

### Media Control (Left Hand)
| Gesture | Action |
|--------|--------|
| 1 Finger | Previous Track |
| 2 Fingers | Play / Pause |
| 3 Fingers | Next Track |

### Volume Control (Right Hand)
- Dynamic control using distance between **thumb and index finger**
- Supports smooth interpolation for precise adjustments
- Covers full range from **mute to maximum volume**

---

## Technology Stack  

- **Python**  
- **OpenCV** — real-time video processing  
- **MediaPipe** — hand tracking and landmark detection  
- **NumPy** — numerical computations  
- **PyCaw** — system audio control (Windows)  
- **PyAutoGUI** — keyboard automation  

---

## Installation  

```bash
git clone https://github.com/your-username/musicon.git
cd musicon
```

Install required dependencies:

```bash
pip install opencv-python mediapipe numpy pycaw pyautogui comtypes
```

---

## Usage  

```bash
python musicon.py
```

Press `q` to terminate the application.

---

## System Workflow  

1. Captures video stream from the webcam  
2. Detects and tracks hand landmarks using MediaPipe  
3. Differentiates between left and right hands  
4. Interprets gestures based on landmark positions  
5. Maps gestures to:
   - Media playback controls  
   - System volume adjustments  

---

## Project Structure  

```
musicon/
├── musicon.py
└── README.md
```

---

## Considerations  

- Optimal performance requires **adequate lighting conditions**  
- Ensure **webcam permissions** are enabled  
- Media control shortcuts (`Ctrl + B`, `Ctrl + P`, `Ctrl + F`) may vary depending on the target application  

---

## Roadmap  

- Customizable gesture mappings  
- Cross-platform audio support (Linux/macOS)  
- GUI-based configuration panel  
- Adaptive gesture sensitivity  
- Integration of learning-based gesture recognition  

---

## Contributing  

Contributions are welcome.  
Please open an issue to discuss proposed changes before submitting a pull request.

---

## License  

This project is licensed under the **MIT License**.

---

## Vision  

> A seamless human-computer interface driven purely by intent and motion.
