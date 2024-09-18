import cv2
from simple_facerec import SimpleFacerec

# Initialize simple face recoggnition module
sfr = SimpleFacerec()
sfr.load_encoding_images(r"C:\Users\alech\Downloads\Lech_faces\Lech_faces\Test data")

# Load camera
cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))


# read frames
while True:
  ret, frame = cap.read()

  # Detect faces
  face_location, face_name, face_landmarks = sfr.detect_known_faces(frame)
  for face_loc, name in zip(face_location, face_name):
    print("Face location:", face_loc)
    y1, x1, y2, x2 = face_loc[0], face_loc[1] , face_loc[2] , face_loc[3] 

    cv2.putText(frame, name, (x1,y1 -10), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,200), 2)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0,0,200), 4)

  # Write the frame to the video file
  out.write(frame)

  cv2.imshow("Frame", frame)

  key = cv2.waitKey(1)
  if key == 27:
    break

cap.release()
out.release()
cv2.destroyAllWindows()

















