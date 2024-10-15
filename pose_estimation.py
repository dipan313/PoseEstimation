import cv2 as cv
import mediapipe as mp
from time import time

# Initialize mediapipe pose class
mp_pose = mp.solutions.pose
# Set up pose function for video
pose_video = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)

# Initialize the VideoCapture object to read from the webcam (0 or 1 depending on the camera used)
video = cv.VideoCapture(0)

# Create a named window for resizing purpose
cv.namedWindow('Pose Detection', cv.WINDOW_NORMAL)

# Set video camera size
video.set(3, 1280)  # Width
video.set(4, 960)   # Height

# Initialize a variable to store the time of the previous frame
time1 = 0

def detecPose(frame, pose_video, display=False):
    # Initialize mediapipe drawing utils for drawing landmarks on frame
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # Convert the frame to RGB for processing by MediaPipe
    frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = pose_video.process(frame_rgb)

    # Draw the landmarks on the frame
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
                                  ,mp_drawing.DrawingSpec(color=(225,117,66),thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245,66,230),thickness=2, circle_radius=2)
                                  )
    
    return frame, results.pose_landmarks

# Iterate until the video is accessed successfully
while video.isOpened():
    # Read a frame
    ok, frame = video.read()

    # Check if the frame is not read properly
    if not ok:
        break

    # Flip the image horizontally for a later selfie-view display
    frame = cv.flip(frame, 1)

    # Get the height and width of the frame
    frame_height, frame_width, _ = frame.shape

    # Resize the frame (make sure the aspect ratio remains intact)
    frame = cv.resize(frame, (int(frame_width * (640 / frame_height)), 640))

    # Perform pose landmark detection
    frame, _ = detecPose(frame, pose_video, display=False)

    # Set the time for this frame to the current time
    time2 = time()

    # Calculate FPS if time difference is greater than 0
    if (time2 - time1) > 0:
        # Calculate the FPS
        frames_per_second = 1.0 / (time2 - time1)

        # Write the calculated FPS on the frame
        cv.putText(frame, 'FPS: {}'.format(int(frames_per_second)), (10, 30), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)

    # Update the previous frame time to this frame time
    time1 = time2

    # Display the frame with the calculated FPS
    cv.imshow('Pose Detection', frame)

    # Wait until a key is pressed (check for 'ESC' to exit)
    key = cv.waitKey(1) & 0xFF
    if key == 27:  # ESC key
        break

# Release the VideoCapture object and close any OpenCV windows
video.release()
cv.destroyAllWindows()
