# Musicon — Gesture-Based Music Control System

Musicon is a computer vision-based system that allows users to control music playback and volume using **hand gestures**.

It replaces traditional input methods (keyboard/mouse) with a more natural and intuitive interaction model using real-time hand tracking.

---

## Features

* Hand gesture recognition using computer vision
* Volume control through finger distance
* Play / Pause functionality
* Real-time processing with minimal latency

---

## How It Works

Musicon uses:

* **OpenCV** → for video capture and image processing
* **MediaPipe** → for hand landmark detection
* Gesture logic → to map hand movements to actions

### Flow:

1. Capture video from webcam
2. Detect hand landmarks
3. Calculate finger positions/distances
4. Map gestures to system commands

---

## Tech Stack

* Python
* OpenCV
* MediaPipe
* Pycaw (for volume control)

---

## How to Run

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python main.py
```

---

## Use Case

This project demonstrates how computer vision can be used to build **natural user interfaces (NUI)** and real-time interactive systems.

---

## Future Improvements

* Gesture customization
* Multi-hand support
* UI overlay for feedback
* Integration with other media platforms

---

## Final Note

Musicon represents a step toward building systems that feel more **human, responsive, and intuitive**.
