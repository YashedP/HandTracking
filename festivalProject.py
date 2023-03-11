# idea, either merge the 2 photos using cv2
# idea, combine the image data
# idea, change to gpu usage
# try getting the rectangle to move with the pointer finger
# understand how they're tracking the pointer finger constantly or maybe I don't, I already have the x value from the results

import cv2
import mediapipe as mp
import time

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

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
            
            bubble = cv2.imread("bubble.png")
            x, y, w, h = 100, 100, 200, 300
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # bubble = cv2.resize(bubble, image.shape)
            # print(bubble.shape)
            # image = cv2.add(image, bubble)
            # cv2.imshow("bubble", bubble)

            if frames % 3 == 0:
                results = hands.process(image)
                print(results.multi_hand_landmarks)
            
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
            # Flip the image horizontally for a selfie-view display.
            cv2.imshow("MediaPipe Hands", image)


            # dst = cv2.addWeighted(image, 0.7, bubble, 0.3, 0)
            # cv2.imshow("window", dst)

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