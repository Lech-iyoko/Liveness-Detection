<<<<<<< HEAD
"Liveness Detection" 
=======
# Liveness-Detection
## A python script using OpenCV EAR benchmark for face recognition and liveness detection

A Face recognition model that uses the Anti-spoofing mechanism "Liveness Detection" to show how security for face recognition can be enhanced

* Project Overview
  - Developed a facial recognition system using OpenCV and face_recognition libraries.
  - Implemented liveness detection through Dlib’s Eye Aspect Ratio (EAR) to distinguish between live faces and spoofing attempts using blink detection.
  - Enhanced security by verifying blinks in real-time video streams to differentiate between live users and fraudulent attempts.

* Steps Included:
  - Install Required Libraries: Install OpenCV, dlib, and face_recognition.
  - Collect Dataset: Collect images/videos for training/testing facial recognition and liveness detection.
  - Face Detection & Encoding:
    - Detect faces and compute face encodings using the face_recognition library.
    - Implement EAR-based liveness detection for blink verification using Dlib’s shape predictor.
  - Build the Model:
    - Integrate real-time video streams to identify users and check for liveness.
    - Ensure accurate distinction between real and spoofed faces.
  - Test the Model: Test using various video inputs and refine for accuracy and performance.
  - Deploy & Integrate: Deploy the model for real-world application in a live camera setup.

* Technology Stack:
  - Python: For the implementation of algorithms.
  - OpenCV: For image processing and real-time video manipulation.
  - Dlib: For facial landmarks and eye aspect ratio calculation.
  - face_recognition library: For face encoding and recognition.

* Goals:
  - Improve liveness detection accuracy.
  - Develop a robust system suitable for security applications.
  - Demonstrate expertise in computer vision and real-time processing.


>>>>>>> 8cc33273f2cfe39e20840759426bbfc9a6232d98
