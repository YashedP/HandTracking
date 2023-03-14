import cv2
from bubble import Bubble

monitorXPixels = 1280
monitorYPixels = 720

def imageOverlay(bubbles, image):
    for i in range(len(bubbles)):
        if not bubbles[i].isPopped:
            x_offset = bubbles[i].x
            y_offset = bubbles[i].y
            h, w = imageFront.shape[:2]
            image[y_offset:y_offset+h, x_offset:x_offset+w] = cv2.addWeighted(image[y_offset:y_offset+h, x_offset:x_offset+w], 1.0, imageFront, 1.0, 0)
    return image

imageFront = cv2.imread("Assets/original.png")
imageFront = cv2.resize(imageFront, (100, 100))

bubble1 = Bubble(100, 100, imageFront.shape) 
bubble2 = Bubble(200, 200, imageFront.shape)
bubble3 = Bubble(600, 300, imageFront.shape)
bubble4 = Bubble(800, 400, imageFront.shape)
bubble5 = Bubble(630, 80, imageFront.shape)
bubble6 = Bubble(700, 120, imageFront.shape)
bubble6 = Bubble(900, 70, imageFront.shape)
bubble7 = Bubble(1000, 369, imageFront.shape)
bubble8 = Bubble(200, 400, imageFront.shape)
bubble9 = Bubble(500, 600, imageFront.shape)
bubbles = [bubble1, bubble2, bubble3, bubble4, bubble5, bubble6, bubble7, bubble8, bubble9]

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, monitorXPixels)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, monitorYPixels)

while cap.isOpened():
    success, image = cap.read()

    if not success:
        print("Ignoring empty camera frame.")
        break
    
    imageOverlay(bubbles, image)
    # # Set the position of the overlay
    # x_offset = 50
    # y_offset = 50

    # # Get the size of the overlay
    # h, w = imageFront.shape[:2]

    # # Perform the overlay
    # image[y_offset:y_offset+h, x_offset:x_offset+w] = cv2.addWeighted(image[y_offset:y_offset+h, x_offset:x_offset+w], 1.0, imageFront, 1.0, 0)

    cv2.imshow("imageOverlayTesting", image)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()