import cv2
import mediapipe as mp
import time
import cvzone
import threading
from bubble import Bubble

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

monitorXPixels = 1280
monitorYPixels = 720

results = None
image = None

def findHands(hands, cap):
    global results
    while cap.isOpened():
        results = hands.process(image)

pTime = 0
cTime = 0
frames = 0

imageFront = cv2.imread("Assets/bubble.jpeg", cv2.IMREAD_UNCHANGED)

bubble1 = Bubble(200, 200, imageFront.shape) 
bubble2 = Bubble(500, 100, imageFront.shape)
bubble3 = Bubble(700, 500, imageFront.shape)
bubble4 = Bubble(1000, 500, imageFront.shape)
bubbles = [bubble1, bubble2, bubble3, bubble4]

bubble1.setMonitorDimension(monitorXPixels, monitorYPixels)

cap = cv2.VideoCapture(700)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1980)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            break

    
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(image, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
        if frames == 0:
            threading.Thread(target=findHands, args=(hands, cap)).start()

        try:
            index_finger_tip = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # Accessing x,y,z coordinates of index finger tip landmark
            x_coord_of_index_finger_tip = (index_finger_tip.x * 1280)
            y_coord_of_index_finger_tip = (index_finger_tip.y * 720)

            for i in range(len(bubbles)):
                bubbles[i].calculateDistance(x_coord_of_index_finger_tip, y_coord_of_index_finger_tip)
                bubbles[i].popBubble()
        except:
            pass

            
        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if not results == None:
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
        
        for i in range(len(bubbles)):
            if not bubbles[i].isPopped:
                image = cvzone.overlayPNG(image, imageFront, [bubbles[i].x, bubbles[i].y])
        
        # Flip the image horizontally for a selfie-view display.
        cv2.imshow("MediaPipe Hands", image)
        # cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
        frames += 1
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()