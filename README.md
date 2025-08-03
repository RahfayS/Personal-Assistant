# 👁️ CV Modules for Project AURA - Computer Vision Assistant Features

This repository is a collection of modular **Computer Vision mini-projects** designed as standalone learning tools and feature components for the larger **AURA Personal Assistant** system.

Each module focuses on a specific CV skill (e.g., face recognition, gesture control, object detection) and is built with the intent to be plug-and-play into AURA later.

---

## 🚀 What’s Inside

| Module Name         | Description                                              | Skills Covered                              | Status     |
|---------------------|----------------------------------------------------------|----------------------------------------------|------------|
| `face_detection`    | Detects faces in real-time using webcam                  | Haar, OpenCV DNN, frame processing           | ✅ Complete |
| `face_recognition`  | Recognizes known users from webcam feed                  | Dlib encodings, ROI cropping, dataset mgmt   | ✅ Complete |
| `object_detection`  | Detects objects using YOLOv8 (pre-trained)               | YOLO inference, drawing boxes, NMS           | 🔄 WIP      |
| `hand_gestures`     | Recognizes hand landmarks and maps to gestures           | MediaPipe Hands, gesture classification      | 🔲 Planned  |
| `emotion_recognition` | Detects facial emotion from webcam                    | CNNs, emotion datasets, facial landmarks     | 🔲 Planned  |
| `eye_gaze_blink`    | Tracks eye direction & blink detection                   | EAR ratio, eye ROI, smoothing                | 🔲 Planned  |
| `pose_estimation`   | Estimates full-body pose with landmarks                  | MediaPipe Pose, movement classification      | 🔲 Planned  |

---

## 🧠 Project Goals

- Learn essential **computer vision skills** through focused, practical mini-projects.
- Build robust, modular components for integration into the full **AURA AI Assistant**.
- Reinforce learning with clean architecture, reusability, and extensibility in mind.

