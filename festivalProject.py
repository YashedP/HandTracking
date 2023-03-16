# animations
# Have a frame bigger than what we show to encapture the hands in case we wanted to pop the bubble but it was off screen so it wouldn't be able to find the bubble if half of our hand was off screen
# check bubble x and y less than 150 if they are, check if bubble is less than 100 distance from the center of each bubble and in the case it is, I make path for bubble to go left and bubble to go to right
# take the first 5 frames and average for fps to get the length of the bezier curve indexes and how long I want the indexes to show up
# TODO: Animations
# TODO: Collisions, check if bubbles overlap go over each other, check the direction, use the appropriate bezier to go left or right
# TODO: Make a randomLeftBezier, randomRightBezier methods in the file
# TODO: Add a GUI

import cv2
import mediapipe as mp
import time
import tkinter

from bubble import Bubble
import BezierCurves

def imageOverlay(bubbles, image):
    for i in range(len(bubbles)):
        if not bubbles[i].isPopped:
            x_offset = bubbles[i].x
            y_offset = bubbles[i].y

            h, w = imageFront.shape[:2]
            
            if y_offset < 0:
                maxLength = (100 + y_offset)

                imgFront = cv2.resize(imageFront[h - maxLength:, :], (w, maxLength))
                y_offset = max(0, y_offset - maxLength)

                # Image ranges
                y1, y2 = y_offset, y_offset + maxLength
                x1, x2 = x_offset, x_offset + w

                # Overlay ranges
                y1o, y2o = 0, imgFront.shape[0]
                x1o, x2o = 0, imgFront.shape[1]

                channels = image.shape[2]

                alpha = imgFront[y1o:y2o,x1o:x2o,-1] / 255.0
                alpha_inv = 1.0 - alpha

                for c in range(channels):
                    image[y1:y2,x1:x2,c] = (alpha * imgFront[y1o:y2o,x1o:x2o,c] + alpha_inv *image[y1:y2,x1:x2,c])
            elif y_offset < monitorYPixels - 100 + 1:
                x = bubbles[i].x
                y = bubbles[i].y

                # Image ranges
                y1, y2 = max(0, y), min(image.shape[0], y + imageFront.shape[0])
                x1, x2 = max(0, x), min(image.shape[1], x + imageFront.shape[1])

                # Overlay ranges
                y1o, y2o = max(0, -y), min(imageFront.shape[0], image.shape[0] - y)
                x1o, x2o = max(0, -x), min(imageFront.shape[1], image.shape[1] - x)

                channels = image.shape[2]

                alpha = imageFront[y1o:y2o,x1o:x2o,-1] / 255.0
                alpha_inv = 1.0 - alpha

                for c in range(channels):
                    image[y1:y2,x1:x2,c] = (alpha * imageFront[y1o:y2o,x1o:x2o,c] + alpha_inv *image[y1:y2,x1:x2,c])
                
            elif y_offset < monitorYPixels:
                maxLength = monitorYPixels-y_offset
                imgFront = cv2.resize(imageFront[0:maxLength, :], (w, maxLength))

                # Image ranges
                y1, y2 = max(0, y_offset), min(image.shape[0], y_offset + imageFront.shape[0])
                x1, x2 = max(0, x_offset), min(image.shape[1], x_offset + imageFront.shape[1])

                # Overlay ranges
                y1o, y2o = max(0, -y_offset), min(imgFront.shape[0], image.shape[0] - y_offset)
                x1o, x2o = max(0, -x_offset), min(imgFront.shape[1], image.shape[1] - x_offset)

                channels = image.shape[2]

                alpha = imgFront[y1o:y2o,x1o:x2o,-1] / 255.0
                alpha_inv = 1.0 - alpha

                for c in range(channels):
                    image[y1:y2,x1:x2,c] = (alpha * imgFront[y1o:y2o,x1o:x2o,c] + alpha_inv *image[y1:y2,x1:x2,c])
    return image


# Change these to change the resolution of the window output
monitorXPixels = 1980 # 1280, or 1980
monitorYPixels = 1080 # 720 or 1080

BezierCurves.monitorXPixels = monitorXPixels
BezierCurves.monitorYPixels = monitorYPixels

# Change the path to the image if need be
imageFront = cv2.imread("Assets/bubble.png", cv2.IMREAD_UNCHANGED)
imageFront = cv2.resize(imageFront, (100, 100))

# ------------------------------------------------

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

pTime = 0
cTime = 0
frames = 0

bubbles = [Bubble(imageFront.shape),   \
           Bubble(imageFront.shape),   \
           Bubble(imageFront.shape),   \
           Bubble(imageFront.shape),   \
           Bubble(imageFront.shape),   \
           Bubble(imageFront.shape),   \
           Bubble(imageFront.shape),   \
           Bubble(imageFront.shape),   \
           Bubble(imageFront.shape),   \
           Bubble(imageFront.shape),   \
           Bubble(imageFront.shape),   \
           Bubble(imageFront.shape),   \
           Bubble(imageFront.shape),   \
           Bubble(imageFront.shape),   \
           Bubble(imageFront.shape),   \
           Bubble(imageFront.shape)]

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

        if frames == 0:
            if cap.get(cv2.CAP_PROP_FRAME_WIDTH) == monitorXPixels and cap.get(cv2.CAP_PROP_FRAME_HEIGHT) == monitorYPixels:
                resize = False
            else:
                resize = True

        if resize:
            image = cv2.resize(image, (monitorXPixels, monitorYPixels)) 

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
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                x_coord_of_index_finger_tip = (index_finger_tip.x * monitorXPixels)
                y_coord_of_index_finger_tip = (index_finger_tip.y * monitorYPixels)
                
                for i in range(len(bubbles)):
                    bubbles[i].calculateDistance(x_coord_of_index_finger_tip, y_coord_of_index_finger_tip)
                    if not bubbles[i].isPopped:
                        bubbles[i].popBubble()



        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # If pressed the enter key, then the hand drawings show up
        if cv2.waitKey(1) & 0xFF == 13:
            showResults = not showResults
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Draws the hand drawings on on the hand if enter key is pressed
        if results.multi_hand_landmarks and showResults:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
        
        for i in range(len(bubbles)):
            if bubbles[i].y == monitorYPixels:
                bubbles[i].resetPath()
                bubbles[i].isPopped = False
            bubbles[i].index += 1
            bubbles[i].x = int(bubbles[i].coordinates[bubbles[i].index][0])
            bubbles[i].y = int(bubbles[i].coordinates[bubbles[i].index][1])

        # Overlays every bubble image onto the screen
        image = imageOverlay(bubbles, image)
    
        
        
        cv2.imshow("Bubbles", image)
        # Flip the image horizontally for a selfie-view display.
        # cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
        frames += 1
        if cv2.waitKey(1) & 0xFF == 27:
            break
cap.release()