 Eye Blink Detection for Virtual Cursor

An assistive technology system that allows users to control the mouse cursor using eye movements and blinks, enabling hands-free interaction — especially useful for people with mobility impairments.



 Project Overview

This project uses:
A regular webcam
OpenCV and MediaPipe for eye and face landmark detection
PyAutoGUI for cursor movement and click simulation



 Features

Real-time eye tracking
Hands-free computer interaction
Cursor movement based on eye direction
Click and scroll using blinks
On-screen feedback



 System Architecture

Modules:
1. Video Capture
2. Preprocessing
3. Face & Eye Detection
4. Eye Movement Tracking
5. Blink Detection
6. Mouse Click Handling
7. Scroll Detection
8. Feedback Display




 Tech Stack

- Python 3.12+
- OpenCV
- MediaPipe
- PyAutoGUI
- NumPy



 Installation

```bash
git clone https://github.com/Alishabaiju/eye-blink-cursor-control.git
cd eye-blink-cursor-control
pip install -r requirements.txt
