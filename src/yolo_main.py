import cv2
import argparse
from utils import *
import mediapipe as mp
from bodyPartAngle import BodyPartAngle
from excerciseType import excerciseType



ap = argparse.ArgumentParser()
ap.add_argument("-t",
                "--exercise_type",
                type=str,
                help='Type of activity to do',
                required=True)
ap.add_argument("-vs",
                "--video_source",
                type=str,
                help='Type of activity to do',
                required=False)
ap.add_argument("-vo",
                "--video_output",
                type=str,
                help='Type of activity to do',
                required=False)


args = vars(ap.parse_args())


args = vars(ap.parse_args())


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

if args["video_source"] is not None:
    cap = cv2.VideoCapture(args["video_source"])
else:
    cap = cv2.VideoCapture(0)  # webcam

cap.set(3, 800)  # width
cap.set(4, 480)  # height

# setup mediapipe

with mp_pose.Pose(min_detection_confidence=0.5,
                  min_tracking_confidence=0.5) as pose:
    counter = 0  # movement of exercise
    status = True  # state of move
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(args["video_output"], fourcc, fps, (800, 480))

    while cap.isOpened():

        ret, frame = cap.read()
        # result_screen = np.zeros((250, 400, 3), np.uint8)
        if not np.any(frame):
            break
        else:
            frame = cv2.resize(frame, (800, 480), interpolation=cv2.INTER_AREA)
        # recolor frame to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame.flags.writeable = False
        # make detection
        results = pose.process(frame)
        # recolor back to BGR
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark
            counter, status = excerciseType(landmarks).calculate_exercise(
                args["exercise_type"], counter, status)
        except:
            pass

        frame = score_table(args["exercise_type"], frame, counter, status)

        # render detections (for landmarks)
        # mp_drawing.draw_landmarks(
        #     frame,
        #     results.pose_landmarks,
        #     mp_pose.POSE_CONNECTIONS,
        #     mp_drawing.DrawingSpec(color=(255, 255, 255),
        #                            thickness=2,
        #                            circle_radius=2),
        #     mp_drawing.DrawingSpec(color=(174, 139, 45),
        #                            thickness=2,
        #                            circle_radius=2),
        # )
        out.write(frame)
        cv2.imshow('Video', frame)
        cv2.waitKey(10)

        if ret==False: break

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


    cap.release()
    out.release()
    cv2.destroyAllWindows()