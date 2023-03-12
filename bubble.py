import math


class Bubble:
    monitorXPixels = 0
    monitorYPixels = 0

    def __init__(self, x, y, imageShape, isPopped=False, distanceFromFinger=100, ):
        self.x = x
        self.y = y
        self.xPixels = imageShape[0]
        self.yPixels = imageShape[1]        
        self.isPopped = isPopped
        self.distanceFromFinger = distanceFromFinger
    
    def calculateDistance(self, xCoordinateOfFinger, yCoordinateOfFinger):
        self.distanceFromFinger = math.sqrt(pow((self.x + self.xPixels / 2) - xCoordinateOfFinger, 2) + pow((self.y + self.yPixels / 2) - yCoordinateOfFinger, 2))

    def popBubble(self):
        if self.distanceFromFinger <= 65:
            self.isPopped = True

    def setMonitorDimension(self, monitorXPixels, monitorYPixels):
        Bubble.monitorXPixels = monitorXPixels
        Bubble.monitorYPixels = monitorYPixels
    
# add function to have another bubble object to check if there's an collisions
# function for a creating another vector
# add function for checking which side was there a collision, prerequisite, it must be in the distance below 65 from the center of the both bubbles