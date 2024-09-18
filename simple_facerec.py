import face_recognition
import cv2
import os
import glob
import numpy as np
import dlib
from scipy.spatial import distance as dist

class SimpleFacerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []

        # Resize frame for a faster speed
        self.frame_resizing = 0.25

        # Intialize dlib's face detector and shape predictor
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

        # Variables to track blink detection
        self.blink_threshold = 0.3  # Adjust based on testing
        self.consecutive_frames = 2  # Blink must last this many frames
        self.blink_counter = 0
        self.blinks_detected = 0

    def load_encoding_images(self, images_path):
        """
        Load encoding images from path
        :param images_path:
        :return:
        """
        # Load Images
        images_path = glob.glob(os.path.join(images_path, "*.*"))

        print("{} encoding images found.".format(len(images_path)))

        # Store image encoding and names
        for img_path in images_path:
            img = cv2.imread(img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Get the filename only from the initial file path.
            basename = os.path.basename(img_path)
            (filename, ext) = os.path.splitext(basename)
            # Get encoding
            img_encoding = face_recognition.face_encodings(rgb_img)[0]

            # Store file name and file encoding
            self.known_face_encodings.append(img_encoding)
            self.known_face_names.append(filename)
        print("Encoding images loaded")

    def detect_known_faces(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        # Find all the faces and face encodings in the current frame of video
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        face_landmarks = []

        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            face_names.append(name)

            for face_loc in face_locations:
                # Extract the bounding box coordinates
                top, right, bottom, left = face_loc

                # Convert face location to dlib's rectangle format (already adjusted for resizing)
                face_rect = dlib.rectangle(int(left), int(top), int(right), int(bottom))

                # Detect facial landmarks
                landmarks = self.predictor(frame, face_rect)

                # Save landmarks for liveness detection
                face_landmarks.append(landmarks)

                # (Optional) Draw the landmarks on the frame for visualization
                for n in range(0, 68):  # There are 68 points in dlib's 68-point model
                    x = landmarks.part(n).x
                    y = landmarks.part(n).y
                    cv2.circle(frame, (x, y), 1, (255, 0, 0), -1)  # Blue color for landmarks

                # EAR calculation for blink detection
                left_eye = [landmarks.part(i) for i in range(36, 42)]
                right_eye = [landmarks.part(i) for i in range(42, 48)]

                left_EAR = self.calculate_EAR(left_eye)
                right_EAR = self.calculate_EAR(right_eye)
                avg_EAR = (left_EAR + right_EAR) / 2.0

                # Print EAR values to the terminal 
                print(f"Left EAR: {left_EAR}, Right EAR: {right_EAR}, Avg EAR: {avg_EAR}")

                # Blink detection logic
                if avg_EAR < self.blink_threshold:
                    self.blink_counter += 1
                else:
                    if self.blink_counter >= self.consecutive_frames:
                        self.blinks_detected += 1
                        print("Liveness detected")
                    self.blink_counter = 0  # Reset counter

        # Convert to numpy array to adjust coordinates with frame resizing quickly
        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        print(f"Locations: {face_locations}, Names: {face_names}, Landmarks: {face_landmarks}")
        return face_locations.astype(int), face_names, face_landmarks
        
    def calculate_EAR(self, eye):
        """
        Calculates the Eye Aspect Ratio (EAR)
        :param eye: 6 landmarks around the eye
        :return: EAR value
        """
        A = dist.euclidean((eye[1].x, eye[1].y), (eye[5].x, eye[5].y))
        B = dist.euclidean((eye[2].x, eye[2].y), (eye[4].x, eye[4].y))
        C = dist.euclidean((eye[0].x, eye[0].y), (eye[3].x, eye[3].y))

        EAR = (A + B) / (2.0 * C)
        return EAR
        
