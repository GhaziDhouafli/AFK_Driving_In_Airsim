import cv2
import airsim
import os
import tempfile
import mediapipe as mp
import time
import numpy as np
import math


def get_label(index, hand, results):
    output = None
    for idx, classification in enumerate(results.multi_handedness):
        if classification.classification[0].index == index:
            # Process results
            label = classification.classification[0].label
            score = classification.classification[0].score
            text = '{}'.format(label)

            # Extract Coordinates
            coords = tuple(np.multiply(
                np.array((hand.landmark[mp_hands.HandLandmark.WRIST].x, hand.landmark[mp_hands.HandLandmark.WRIST].y)),
                [10, 10]).astype(float))

            output = text, coords

    return output

# connect to the AirSim simulator
client = airsim.CarClient()
client.confirmConnection()
client.enableApiControl(True)
print("API Control enabled: %s" % client.isApiControlEnabled())
car_controls = airsim.CarControls()

tmp_dir = os.path.join(tempfile.gettempdir(), "airsim_car")
print ("Saving images to %s" % tmp_dir)
try:
    os.makedirs(tmp_dir)
except OSError:
    if not os.path.isdir(tmp_dir):
        raise

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


cap = cv2.VideoCapture(0)
with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        start = time.time()
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


        if results.multi_hand_landmarks:
            right=[]
            left=[]
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                          mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                          )
                if get_label(num, hand, results):
                    text, coord = get_label(num, hand, results)
                    if (text=='Right'):
                        right=[coord[0]-5,coord[1]-5]
                    else:
                        left = [coord[0]-5, coord[1]-5]
                    if (len(right)==2 and len(left)==2):
                        u=right[0]-left[0]
                        m=right[1]-left[1]
                        n=1
                        if (m<0):
                            n=-1

                        v=math.sqrt((right[0]-left[0])**2 + (right[1]-left[1])**2)
                        angle=math.acos(u/v)
                        angle=n*(angle*180)/3.14
                        print(angle)
                        car_state = client.getCarState()
                        print("Speed %d, Gear %d" % (car_state.speed, car_state.gear))
                        if (angle < -160) or (angle> 160) or (0 < angle < 25):
                            # go forward
                            car_controls.throttle = 0.5
                            car_controls.steering = 0
                            client.setCarControls(car_controls)
                            print("Go Forward")
                            time.sleep(1)  # let car drive a bit
                        elif (25<=angle<=65):
                            # Go forward + steer right
                            car_controls.throttle = 0.5
                            car_controls.steering = 0.5
                            client.setCarControls(car_controls)
                            print("Go Forward, steer right")
                            time.sleep(0.5)  # let car drive a bit
                        elif(-65<=angle<=-25):
                            # Go forward + steer right
                            car_controls.throttle = 0.5
                            car_controls.steering = -0.5
                            client.setCarControls(car_controls)
                            print("Go Forward, steer left")
                            time.sleep(0.5)  # let car drive a bit
        end = time.time()
        totalTime = end - start

        cv2.imshow('MediaPipe Hands', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
#restore to original state
client.reset()

client.enableApiControl(False)





