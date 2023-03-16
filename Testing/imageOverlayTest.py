import cv2

monitorXPixels = 1280
monitorYPixels = 720

import cv2

def imageOverlay(image, imageFront, x, y):
    x_offset = x
    y_offset = y

    h, w = imageFront.shape[:2]
    
    if y < 0:
        maxLength = (100 + y)
        print(maxLength)
        imageFront = cv2.resize(imageFront[h - maxLength:, :], (w, maxLength))
        y_offset = max(0, y - maxLength)

        y1, y2 = y_offset, y_offset + maxLength
        x1, x2 = x_offset, x_offset + w
        image[y1:y2, x1:x2] = cv2.addWeighted(image[y1:y2, x1:x2], 1.0,imageFront, .5, 0)
    elif y < monitorYPixels - 100 + 1:
        image[y_offset:y_offset+h, x_offset:x_offset+w] = cv2.addWeighted(image[y_offset:y_offset+h, x_offset:x_offset+w], 1.0, imageFront, .5, 0)
        
    elif y < monitorYPixels:
        maxLength = monitorYPixels-y
        imageFront = cv2.resize(imageFront[0:maxLength, :], (w, maxLength))
    
        image[y_offset:y_offset+maxLength, x_offset:x_offset+w] = cv2.addWeighted(image[y_offset:y_offset+maxLength, x_offset:x_offset+w], 1.0,imageFront, .5, 0)
    
    return image

def resetPath():
    pass

imageFront = cv2.imread("Assets/bubble.png")
imageFront = cv2.resize(imageFront, (100, 100))

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, monitorXPixels)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, monitorYPixels)

y = 500

while cap.isOpened():
    success, image = cap.read()

    if not success:
        print("Ignoring empty camera frame.")
        break
    
    y += 1

    if y == 720:
        y = -99

    imageOverlay(image, imageFront, 620, y)

    cv2.imshow("imageOverlayTesting", image)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()