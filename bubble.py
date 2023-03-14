import math
import BezierCurves

class Bubble:
    # static variables
    monitorXPixels = 0
    monitorYPixels = 0
    bubblesPopped = 0
    
    def __init__(self, imageShape, isPopped=False, distanceFromFinger=100, index=0):
        self.coordinates = BezierCurves.generateRandomizeBezier()
        self.index = index
        self.x = int(self.coordinates[self.index][0])
        self.y = int(self.coordinates[self.index][1])
        self.xPixels = imageShape[1]
        self.yPixels = imageShape[0]
        self.isPopped = isPopped
        self.distanceFromFinger = distanceFromFinger
        self.distanceThreshold = self.xPixels / 2

    def calculateDistance(self, xCoordinateOfFinger, yCoordinateOfFinger):
        self.distanceFromFinger = math.sqrt(pow((self.x + self.xPixels / 2) - xCoordinateOfFinger, 2) + pow((self.y + self.yPixels / 2) - yCoordinateOfFinger, 2))

    def popBubble(self):
        if self.distanceFromFinger <= self.distanceThreshold:
            Bubble.bubblesPopped += 1
            self.isPopped = True

    def setMonitorDimension(self, monitorXPixels, monitorYPixels):
        Bubble.monitorXPixels = monitorXPixels
        Bubble.monitorYPixels = monitorYPixels
    
    # Prerequisite, the distance of the 2 bubbles must be less than 100 (2 bubble radiuses)
    def changeDirection(self, otherBubble):
        if otherBubble.x > self.x:
            return "left"
        else:
            return "right"
        
    def resetPath(self):
        self.coordinates = BezierCurves.generateRandomizeBezier()
        self.index = 0
        self.x = int(self.coordinates[self.index][0])
        self.y = int(self.coordinates[self.index][1])