![Status](https://img.shields.io/badge/Status-In%20Progress-yellow)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)
![NumPy](https://img.shields.io/badge/NumPy-Numerical%20Computing-orange)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](https://opensource.org/licenses/MIT)
![UI](https://img.shields.io/badge/UI-PyQt5%20%7C%20PySide6-purple)

---
# Stride Sentinel MK-I  
### Gait Recognition Demo System

---

## Overview

**Stride Sentinel MK-I** is a computer vision-based gait recognition system designed to identify individuals using their walking patterns through **Gait Energy Images (GEI)**.

This project demonstrates practical implementation of:
- Motion detection  
- Background subtraction  
- Human silhouette extraction  
- Biometric gait-based identification  

*Goal:* Build an intelligent vision system that recognizes individuals without relying on facial data — enabling privacy-aware biometric solutions.

---

## Features

- **Register Individuals**  
  Add and label new users within the system.

- **Save Gait Energy Image (GEI)**  
  Capture and store unique gait signatures.

- **Recognize Individuals**  
  Match live gait input with stored profiles.

- **Update Background Frame**  
  Dynamically recalibrate background for improved detection accuracy.

---

## Tech Stack

- **Python**
- **OpenCV** – Video processing & computer vision  
- **NumPy** – Numerical computations  
- **Pillow (PIL)** – Image handling  
- **PyQt5 / PySide6** – GUI framework  

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/silverbullet-ai/Stride_Sentinel
cd Stride-Sentinel-MK-I
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install opencv-python Pillow PyQt5 PySide6 numpy
```

>  `os` and `sys` are built-in Python modules and do not require installation.

---

## Project Setup

Before running the application:

1. Create a directory:

```
gei
```

This folder stores all generated **Gait Energy Images (GEIs)**.

2. Place your `.ui` file (Qt Designer file) in the root directory.

3. Ensure correct UI file reference in your code:

```python
loadUi("your_file_name.ui", self)
```

---

## Run the Application

```bash
python main.py
```

---

## Application Workflow

| Action       | Description                          |
|-------------|--------------------------------------|
| Register     | Add a new individual                |
| Save         | Store GEI for the individual        |
| Recognize    | Identify a person                   |
| Update BG    | Refresh background for detection    |

---

## How It Works

1. Capture live video feed using OpenCV  
2. Perform background subtraction  
3. Extract moving human silhouette  
4. Generate **Gait Energy Image (GEI)** by aggregating frames  
5. Compare GEIs for identification  

---

## Project Status

 **Currently In Progress**

### Planned Improvements

- Deep learning-based gait embeddings  
- Real-time confidence scoring  
- Multi-person detection & tracking  
- Persistent model training and storage  
- Performance optimization for real-time systems  

---

## Notes

- Ensure consistent lighting conditions for better accuracy  
- Maintain a fixed camera distance during registration  
- Use only one Qt framework (**PyQt5** *or* **PySide6**) to avoid conflicts  

---

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

## 🌌 Author

**Aahish**  
*"Building systems that see beyond what eyes can."*
