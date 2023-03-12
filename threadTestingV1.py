import cv2
import mediapipe as mp
import time
import threading

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

results = None
image = None

def findHands(hands, cap):
    global results
    while cap.isOpened():
        results = hands.process(image)

pTime = 0
cTime = 0
frames = 0

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
            # Flip the image horizontally for a selfie-view display.
            cv2.imshow("MediaPipe Hands", image)
            # cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
            frames += 1
            if cv2.waitKey(5) & 0xFF == 27:
                break
cap.release()

# # Load input image
# input_image = cv2.imread("input.jpg")

# # Create bilateral filter object with 9x9 window size, 75 sigma color, and 75 sigma space
# bilateral_filter = cv2.cuda.createBilateralFilter(9, 75, 75)

# # Upload input image to GPU memory
# gpu_input_image = cv2.cuda_GpuMat()
# gpu_input_image.upload(input_image)

# # Filter input image on the GPU
# gpu_output_image = bilateral_filter.apply(gpu_input_image)

# # Download filtered image from GPU memory
# output_image = gpu_output_image.download()

# # Display input and output images
# cv2.imshow("Input", input_image)
# cv2.imshow("Output", output_image)
# cv2.waitKey(0)