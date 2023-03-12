import math

class Bubble:
    def __init__(self, x, y, isPopped=False, distanceFromFinger=100):
        self.x = x
        self.y = y
        self.isPopped = isPopped
        self.distanceFromFinger = distanceFromFinger
    
    def calculateDistance(self, xCoordinateOfFinger, yCoordinateOfFinger, xPixelLength, yPixelLength):
        self.distanceFromFinger = math.sqrt(pow((self.x + xPixelLength / 2) - xCoordinateOfFinger, 2) + pow((self.y + yPixelLength / 2) - yCoordinateOfFinger, 2))

    def popBubble(self):
        if self.distanceFromFinger <= 65:
            self.isPopped = True