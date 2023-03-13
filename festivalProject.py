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
            x = bubbles[i].x
            y = bubbles[i].y

            roi = image[y:y+imageFront.shape[0], x:x+imageFront.shape[1]]

            img2gray = cv2.cvtColor(imageFront, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)

            img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
            img2_fg = cv2.bitwise_and(imageFront, imageFront, mask=mask)
            dst = cv2.add(img1_bg, img2_fg)

            image[y:y+imageFront.shape[0], x:x+imageFront.shape[1]] = dst
    
    return image

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


# Change these to change the resolution of the window output
monitorXPixels = 1280 # 1280, or 1980
monitorYPixels = 720 # 720 or 1080



pTime = 0
cTime = 0
frames = 0



# imageFront = cv2.imread("Assets/bubble.jpeg", cv2.IMREAD_UNCHANGED)
imageFront = cv2.imread("Assets/original.png")
imageFront = cv2.resize(imageFront, (100, 100))

bubble1 = Bubble(100, 100, imageFront.shape) 
bubble2 = Bubble(200, 200, imageFront.shape)
bubble3 = Bubble(600, 300, imageFront.shape)
bubble4 = Bubble(800, 400, imageFront.shape)
bubble5 = Bubble(630, 80, imageFront.shape)
bubble6 = Bubble(700, 120, imageFront.shape)
bubbles = [bubble1, bubble2, bubble3, bubble4, bubble5, bubble6]

bubble1.setMonitorDimension(monitorXPixels, monitorYPixels)

# sets the pixels of the camera
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
        # monitorXPixels, monitorYPixels = cap.read()

        # if camera not Found
        if not success:
            print("Ignoring empty camera frame.")
            break
    
        # image = cv2.resize(image, (monitorXPixels, monitorYPixels)) 

        
        
        # Finds the FPS
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        # Shows FPS on screen
        # cv2.putText(image, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        bubblesPopped = bubbles[0].bubblesPopped
        cv2.putText(image, str(int(bubblesPopped)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)



        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        

        
        # Every 3 frames, find hands on image
        if frames % 3 == 0:
            results = hands.process(image)
        
        
        # Example of getting index finger tip landmark coordinates.
        try:
            index_finger_tip = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # Accessing x,y,z coordinates of index finger tip landmark
            x_coord_of_index_finger_tip = (index_finger_tip.x * monitorXPixels)
            y_coord_of_index_finger_tip = (index_finger_tip.y * monitorYPixels)

            for i in range(len(bubbles)):
                bubbles[i].calculateDistance(x_coord_of_index_finger_tip, y_coord_of_index_finger_tip)
                if not bubbles[i].isPopped:
                    bubbles[i].popBubble()
        except:
            pass
            
        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        if cv2.waitKey(1) & 0xFF == 13:
            showResults = not showResults

        if results.multi_hand_landmarks and showResults:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
        


        # if bubble not "popped"
        for i in range(len(bubbles)):
            if not bubbles[i].isPopped:
                image = imageOverlay(bubbles, image)



        for i in range(len(bubbles)):
            if bubbles[i].y > monitorYPixels - bubbles[i].yPixels - 25:
                max = 1
            else:
                max = 8
            bubbles[i].y += random.randint(1, max)
            if bubbles[i].y > monitorYPixels - bubbles[i].yPixels:
                bubbles[i].y = 0
                bubbles[i].isPopped = False
        
        
        # Flip the image horizontally for a selfie-view display.
        cv2.imshow("MediaPipe Hands", image)
        # cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
        frames += 1
        if cv2.waitKey(1) & 0xFF == 27:
            break
cap.release()