# VisionMouse-AI 🖐️🖱️

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Enabled-green.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Hands-orange.svg)](https://mediapipe.dev/)
[![License](https://img.shields.io/badge/license-MIT-purple.svg)](https://opensource.org/licenses/MIT)

VisionMouse-AI is an advanced Computer Vision based touchless mouse control system. It utilizes MediaPipe hand tracking and OpenCV to translate real-time hand gestures into precise system input commands, including cursor navigation, left/right clicks, dragging, and vertical scrolling.

---

## 📑 Table of Contents
1. Key Features
2. Hand Gesture Mapping
3. Prerequisites & Installation
4. Usage
5. System Architecture & Smoothing
6. License

---

## 🚀 Key Features

* Precise Cursor Navigation: Uses landmark tracking with exponential moving average smoothing to prevent cursor jitter.
* Multi-Hand Gesture Controls: Separate gesture profiles mapped to Right and Left hands for conflict-free controls.
* High DPI Aware: Built-in Windows User32 API integration ensuring full support for high-resolution (4K/1080p) scaled displays.
* Touchless Mouse Operations: Supports left-click, right-click, continuous left-click dragging, and vertical wheel scrolling.

---

## 🖐️ Hand Gesture Mapping

### 🖐️ Right Hand (Navigation & Secondary Actions)
* Cursor Movement: Move your Index Finger Tip (Landmark 8) across the camera viewport.
* Right-Click: Pinch Thumb Tip (Landmark 4) and Index Finger Tip (Landmark 8) closely (< 22px).

### 🤚 Left Hand (Clicking, Dragging & Scrolling)
* Left-Click: Quick pinch between Thumb Tip (Landmark 4) and Index Finger Tip (Landmark 8).
* Left-Click Drag: Hold the Thumb and Index pinch for more than 0.4 seconds to initiate drag mode; release the pinch to drop.
* Scroll Up: Raise Middle Finger Tip (Landmark 12) above the upper palm thresholds.
* Scroll Down: Lower Index Finger Tip (Landmark 8) below lower knuckle thresholds.

---

## 🛠️ Prerequisites & Installation

### Requirements
* Windows OS (Uses ctypes Win32 API calls)
* Python 3.8 or higher
* Web Camera (Internal or USB)

1. Clone the repository:
git clone https://github.com/BehradB289/VisionMouse-AI.git
cd VisionMouse-AI

2. Create and activate a Python virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install required dependencies:
pip install opencv-python mediapipe numpy

---

## 💻 Usage

Run the main script from your terminal:

python gesture_mouse.py

Press 'q' in the camera window or press Ctrl+C in the terminal to exit the application safely.

---

## 🧠 System Architecture & Smoothing

The application processes frames using MediaPipe's Hands solution (`model_complexity=0`) for ultra-low latency inference. To bridge the gap between camera resolution (640x480) and display screen resolutions, linear interpolation (`np.interp`) maps finger coordinates to display bounds. Cursor jitter is neutralized using an adjustable exponential moving average smoothing factor (`smoothening = 9`).

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
