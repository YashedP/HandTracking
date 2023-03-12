# idea, change to gpu usage
# animations
# add a bubble object class
# add a course of the bubble to go, directions
# add multiple bubbles

import cv2
import mediapipe as mp
import time
import cvzone
import math
import bubble


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles





pTime = 0
cTime = 0
frames = 0



imageFront = cv2.imread("Assets/bubble.jpeg", cv2.IMREAD_UNCHANGED)


# this is bubble1, change all of these attributes to an object
x = 200
y = 200
bubble1X = 0
bubble1Y = 0
bubble1 = True
distanceBubble1 = 100



# sets the pixels of the camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1980)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)


with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        
        # if camera not Found
        if not success:
            print("Ignoring empty camera frame.")
            break
    
        
        
        
        # Finds the FPS
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        # Shows FPS on screen
        cv2.putText(image, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)



        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        

        
        # Every 3 frames, find hands on image
        if frames % 3 == 0:
            results = hands.process(image)
            # print(results.multi_hand_landmarks)
        
       
        # Example of getting index finger tip landmark coordinates.
        try:
            index_finger_tip = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # Accessing x,y,z coordinates of index finger tip landmark
            x_coord_of_index_finger_tip = (index_finger_tip.x * 1280)
            y_coord_of_index_finger_tip = (index_finger_tip.y * 720)

            # Finds distance from pointer finger to the center of bubble1
            distanceBubble1 = math.sqrt(pow(bubbleX - x_coord_of_index_finger_tip, 2) + pow(bubbleY - y_coord_of_index_finger_tip, 2))
            # if finger is in range of the picture (50x50 image)
            if distanceBubble1 <= 65:
                bubble1 = False
            print("The distance from the bubble and my finger is " + str(distanceBubble1))
        except:
            print("Finger not found")
       
        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
        
        
        
        # if bubble not "popped"
        if bubble1:
            image = cvzone.overlayPNG(image, imageFront, [x, y])

        # Find the center of the bubble
        bubbleX = x + (imageFront.shape[0]) / 2
        bubbleY = y + (imageFront.shape[1]) / 2

        
        
        
        
        
        # Flip the image horizontally for a selfie-view display.
        cv2.imshow("MediaPipe Hands", image)
        # cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
        frames += 1
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()