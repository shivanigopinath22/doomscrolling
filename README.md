# DoomScrolling Stop

An AI-powered computer vision application that monitors user attention through webcam-based face and eye tracking. When the system detects that the user is repeatedly looking away from the screen, it triggers an intervention video to help reduce distractions and improve focus.

The project uses MediaPipe Face Mesh, OpenCV, and head pose estimation techniques to determine whether the user is actively engaged with their screen.

---

## Overview

DoomScrolling Stop is designed to encourage focused work sessions by monitoring a user's visual attention in real time. The system analyzes facial landmarks, eye position, and head orientation to determine whether the user is looking at the screen.

If the user continuously looks away from the screen for a predefined duration, the application launches a fullscreen intervention video. Once the user returns their attention to the screen, the intervention is automatically stopped.

---

## Features

- Real-time webcam monitoring
- Face landmark detection using MediaPipe Face Mesh
- Eye tracking through iris position analysis
- Head pose estimation
- Attention state classification
- Automatic intervention video playback
- Automatic intervention termination when focus is restored
- Live visual feedback and debugging information

---

## Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy
- VLC Media Player
- Computer Vision
- Face Landmark Detection
- Head Pose Estimation

---

## Project Structure

```text
doomscrolling-stop/
│
├── main.py
├── requirements.txt
├── README.md
└── alarm.mp4 (optional)
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/shivanigopinath22/doomscrolling-stop.git
cd doomscrolling-stop
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install VLC Media Player

Download and install VLC Media Player:

https://www.videolan.org/vlc/

---

## Configuration

Update the following variables in `main.py` according to your system:

```python
VIDEO_PATH = r"PATH_TO_YOUR_VIDEO.mp4"
VLC_PATH = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
```

Example:

```python
VIDEO_PATH = r"C:\Users\Username\Videos\alarm.mp4"
```

Any MP4 file can be used as the intervention video.

---

## Running the Application

```bash
python main.py
```

After launching the application:

1. Allow webcam access if prompted.
2. Position yourself in front of the camera.
3. The application will begin tracking facial landmarks and eye movements.
4. If attention drifts away from the screen for a sufficient period, the intervention video will automatically play.
5. Returning attention to the screen will stop the intervention.

---

## How It Works

### Face Detection and Landmark Extraction

The application uses MediaPipe Face Mesh to extract detailed facial landmarks from a live webcam feed.

### Head Pose Estimation

Head orientation is estimated using selected facial landmarks, including:

- Nose tip
- Chin
- Eye corners
- Mouth corners

These points are used to estimate the pitch angle of the user's head.

### Eye Tracking

The system monitors iris position relative to the eyelids to estimate gaze direction.

### Attention Classification

A user is considered to be looking at the screen when:

- Head orientation remains within a defined range
- Iris position indicates forward attention

### Intervention Mechanism

When the user repeatedly looks away from the screen:

1. VLC Media Player is launched.
2. A predefined intervention video is played in fullscreen mode.
3. Once attention returns to the screen, the video is automatically closed.

---

## Applications

- Digital wellbeing
- Focus improvement
- Productivity enhancement
- Study assistance
- Attention monitoring
- Distraction reduction

---

## Platform Support

| Operating System | Status |
|------------------|---------|
| Windows 10/11 | Tested |
| macOS | Requires configuration changes |
| Linux | Requires configuration changes |

The core computer vision functionality is cross-platform. However, users may need to update VLC executable paths and video configurations depending on their operating system.

---

## Future Improvements

- Audio-based alerts
- Custom intervention messages
- Browser extension integration
- Focus analytics dashboard
- Productivity tracking
- Mobile application support
- User-configurable attention thresholds
- AI-generated motivational interventions

---
- Weekly focus reports

## Demo

Screenshots or demonstration videos can be added here.

Example:

```text
Face Detection Interface
Eye Tracking Visualization
Attention Monitoring State
Intervention Trigger Event
```

---

## Known Limitations

- Requires a functioning webcam
- Requires VLC Media Player installation
- Performance may vary under poor lighting conditions
- Attention detection thresholds may require calibration for different users

---

## Contributing

Contributions, improvements, and feature suggestions are welcome.

To contribute:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a pull request

---

## License

This project is released under the MIT License.

---

## Author

Shivani Gopinath

M.Sc. Artificial Intelligence & Machine Learning  
Vellore Institute of Technology

GitHub: https://github.com/shivanigopinath22
