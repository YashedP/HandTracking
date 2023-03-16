import cv2
import numpy as np
import random

monitorXPixels = 1280
monitorYPixels = 720

def overlay_image_alpha(img, img_overlay, pos):
    """Overlay img_overlay on top of img at the position specified by pos and blend using the alpha channel of img_overlay.

    :param img: Background image
    :param img_overlay: Image to overlay
    :param pos: x,y coordinates where to place the top-left corner of img_overlay on top of img
    """
    x, y = pos

    # Image ranges
    y1, y2 = max(0, y), min(img.shape[0], y + img_overlay.shape[0])
    x1, x2 = max(0, x), min(img.shape[1], x + img_overlay.shape[1])

    # Overlay ranges
    y1o, y2o = max(0, -y), min(img_overlay.shape[0], img.shape[0] - y)
    x1o, x2o = max(0, -x), min(img_overlay.shape[1], img.shape[1] - x)

    # Exit if nothing to do
    if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
        return

    channels = img.shape[2]

    alpha = img_overlay[y1o:y2o,x1o:x2o,-1] / 255.0
    alpha_inv = 1.0 - alpha

    for c in range(channels):
        img[y1:y2,x1:x2,c] = (alpha * img_overlay[y1o:y2o,x1o:x2o,c] + alpha_inv *img[y1:y2,x1:x2,c])
    return img

imageFront = cv2.imread("Assets/bubble.png", cv2.IMREAD_UNCHANGED)
imageFront = cv2.resize(imageFront, (100, 100))

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, monitorXPixels)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, monitorYPixels)


while cap.isOpened():
    success, image = cap.read()

    if not success:
        print("Ignoring empty camera frame.")
        break
    
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    image = overlay_image_alpha(image, imageFront, [300,200])
    # imageOverlay(image, imageFront, 600, 450)

    cv2.imshow("imageOverlayTesting", image)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()