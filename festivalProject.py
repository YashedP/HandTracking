# animations
# bezier's curve
# bubbles come in from the top and trickle down from the top of the screen going down.
#! Meaning, I must splice up the images by 100 pictures, ranging from the rows being shown and disappearing
# Have a frame bigger than what we show to encapture the hands in case we wanted to pop the bubble but it was off screen so it wouldn't be able to find the bubble if half of our hand was off screen

import cv2
import mediapipe as mp
import time
import random
from bubble import Bubble
import numpy as np

def imageOverlay(bubbles, image):
    for i in range(len(bubbles)):
        if not bubbles[i].isPopped:
            x_offset = bubbles[i].x
            y_offset = bubbles[i].y
            h, w = imageFront.shape[:2]
            image[y_offset:y_offset+h, x_offset:x_offset+w] = cv2.addWeighted(image[y_offset:y_offset+h, x_offset:x_offset+w], 1.0, imageFront, .5, 0)
    return image

# Change these to change the resolution of the window output
monitorXPixels = 1280 # 1280, or 1980
monitorYPixels = 720 # 720 or 1080

# Change the path to the image if need be
imageFront = cv2.imread("Assets/original.png")
imageFront = cv2.resize(imageFront, (100, 100))

# ------------------------------------------------

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

pTime = 0
cTime = 0
frames = 0

bubbles = [Bubble(100, 100, imageFront.shape),   \
           Bubble(200, 200, imageFront.shape),   \
           Bubble(600, 300, imageFront.shape),   \
           Bubble(800, 400, imageFront.shape),   \
           Bubble(630, 80, imageFront.shape),    \
           Bubble(700, 120, imageFront.shape),   \
           Bubble(900, 70, imageFront.shape),    \
           Bubble(1000, 369, imageFront.shape),  \
           Bubble(200, 400, imageFront.shape),   \
           Bubble(500, 600, imageFront.shape)]
bubbles[0].setMonitorDimension(monitorXPixels, monitorYPixels)

# Sets the pixels of the input picture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, monitorXPixels)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, monitorYPixels)

showResults = False
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        # If the camera is not found
        if not success:
            print("Ignoring empty camera frame.")
            break
        #! Uncomment this if the webcam input is not the desired resolution
        # image = cv2.resize(image, (monitorXPixels, monitorYPixels)) 

        # Finds the FPS
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        #! Shows FPS on screen
        # cv2.putText(image, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        
        bubblesPopped = bubbles[0].bubblesPopped
        cv2.putText(image, str(int(bubblesPopped)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        
        # Every 3 frames, find hands on image
        if frames % 3 == 0:
            results = hands.process(image)
        
        # Gets the index finger coordinate
        try:
            index_finger_tip = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            x_coord_of_index_finger_tip = (index_finger_tip.x * monitorXPixels)
            y_coord_of_index_finger_tip = (index_finger_tip.y * monitorYPixels)

            for i in range(len(bubbles)):
                bubbles[i].calculateDistance(x_coord_of_index_finger_tip, y_coord_of_index_finger_tip)
                if not bubbles[i].isPopped:
                    bubbles[i].popBubble()
        except TypeError:
            pass
        
        # If pressed the enter key, then the hand drawings show up
        if cv2.waitKey(1) & 0xFF == 13:
            showResults = not showResults

        # Draws the hand drawings on on the hand if enter key is pressed
        if results.multi_hand_landmarks and showResults:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
        
        # Overlays every bubble image onto the screen
        image = imageOverlay(bubbles, image)
    
        for i in range(len(bubbles)):
            if bubbles[i].y > monitorYPixels - bubbles[i].yPixels - 8:
                max = 1
            else:
                max = 8
            bubbles[i].y += random.randint(1, max)
            if bubbles[i].y > monitorYPixels - bubbles[i].yPixels:
                bubbles[i].y = 0
                bubbles[i].isPopped = False
        
        
        cv2.imshow("MediaPipe Hands", image)
        # Flip the image horizontally for a selfie-view display.
        # cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
        frames += 1
        if cv2.waitKey(1) & 0xFF == 27:
            break
cap.release()