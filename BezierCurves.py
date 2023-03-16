import numpy as np
import bezier
import random
import matplotlib.pyplot as plt

monitorXPixels = 0
monitorYPixels = 0 
lengthOfImage = 100

def generateRandomBezier():
    randomizeDegree = random.randint(2, 3)

    starting_X_Value = random.randint(0, monitorXPixels - lengthOfImage)
    end_X_Value = random.randint(0, monitorXPixels - lengthOfImage)
    starting_Y_Value = -99
    end_Y_Value = monitorYPixels

    nodesX = []
    nodesY = []
    for i in range(randomizeDegree - 1):
        randomized_X_Coord = random.randint(0, monitorXPixels - lengthOfImage)
        randomized_Y_Coord = random.randint(0, monitorYPixels)
        nodesX.append(randomized_X_Coord)
        nodesY.append(randomized_Y_Coord)

    nodes1 = np.asfortranarray([
        [starting_X_Value] + nodesX + [end_X_Value],
        [starting_Y_Value] + nodesY + [end_Y_Value],
    ])

    return generateBezier(nodes1, randomizeDegree)

def generateRandomLeftBezier(x, y):
    pass

def generateRandomRightBezier(x, y):
    pass

def generateBezier(nodes, degree):
    curve = bezier.Curve(nodes, degree)

    points = []
    # xList = []
    # yList = []
    randomizeIncrement = random.randint(20, 50)
    for i in range(0, 10000, randomizeIncrement):
        i = i/10000

        points.append(curve.evaluate(float(i)))
        # xList.append(curve.evaluate(float(i))[0])
        # yList.append(curve.evaluate(float(i))[1])
    
    points.append(curve.evaluate(1.0))

    return points
    # plotBezier(xList, yList)

def plotBezier(xList, yList):
    plt.plot(xList, yList)
    plt.ylabel('some numbers')
    plt.axis([0, 1280, 0, 620])
    plt.show()