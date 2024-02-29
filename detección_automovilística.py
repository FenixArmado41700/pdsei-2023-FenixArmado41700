import cv2
import mediapipe as mp

import numpy as np
import vgamepad as vg



gamepad = vg.VX360Gamepad() #mando

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) #iniciar videocaptura

with mp_pose.Pose( # Crear contexto para la postura
    static_image_mode = False,
    model_complexity = 1) as pose:

    while True:
        ret, frame = cap.read()
        if ret == False:
            break
        height, width, _ = frame.shape
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #frame_rgb = cv2.resize(frame_rgb, (150,100))
        results = pose.process(frame_rgb)


        if results.pose_landmarks is not None:
            x1 = int(results.pose_landmarks.landmark[31].x * width)
            y1 = int(results.pose_landmarks.landmark[31].y * height)
            x2 = int(results.pose_landmarks.landmark[32].x * width)
            y2 = int(results.pose_landmarks.landmark[32].y * height)
            x3 = int(results.pose_landmarks.landmark[19].x * width)
            y3 = int(results.pose_landmarks.landmark[19].y * height)
            x4 = int(results.pose_landmarks.landmark[20].x * width)
            y4 = int(results.pose_landmarks.landmark[20].y * height)
            
            cv2.circle(frame, (x1, y1), 2, (255, 0, 0), 2)
            cv2.circle(frame, (x2, y2), 2, (255, 0, 0), 2)
            cv2.circle(frame, (x3, y3), 2, (255, 0, 0), 2)
            cv2.circle(frame, (x4, y4), 2, (255, 0, 0), 2)

            cv2.line(frame, (x1,y1), (x2, y2), (255, 0, 0), 4)
            cv2.line(frame, (x3, y3), (x4, y4), (255, 0, 0), 4)
            
            cv2.line(frame, (x1,y1), (x2,y2), (255,0,0), 4)

            if x1 - x2 != 0:
                m = (y1 - y2) / (x1 - x2)
                sigma = np.arctan(m)*(180/np.pi)
            else:
                sigma = 90

            distance = int(-1.7*(x1-x2)+306)
            distancia = 240
            if distance < 0:
                distance = 0
            elif distance > 255:
                distance = 255
            if x4 - x3 != 0:
                m = -(y4 - y3) / (x4 - x3)
                tetha = np.arctan(m)*(180/np.pi)
            else:
                tetha = 90

            if tetha > 60:
                tetha = 60
            if tetha < -60:
                tetha = -60
            gamepad.left_joystick(x_value=int(-546.1*tetha), y_value=0)  # values between -32768 and 32767
            
            if sigma > 10:
                gamepad.left_trigger(value=distance)
                gamepad.right_trigger(value=0)
            else:
                gamepad.right_trigger(value=distance)
                gamepad.left_trigger(value=0)
            

            gamepad.update()
 

        #    print(x1-x2)
        
        cv2.imshow("video", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
cap.release()
cv2.destroyAllWindows()