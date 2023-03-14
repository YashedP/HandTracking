import numpy as np
import bezier
import random
import matplotlib.pyplot as plt

def generateRandomizeBezier():
    lengthOfImage = 100

    randomizeDegree = 3
    starting_Y_Value = 0
    end_Y_Value = 720 - lengthOfImage

    starting_X_Value = random.randint(0, 1280 - lengthOfImage)
    end_X_Value = random.randint(0, 1280 - lengthOfImage)
    nodesX = []
    nodesY = []
    for i in range(randomizeDegree - 1):
        randomized_X_Coord = random.randint(0, 1280 - lengthOfImage)
        randomized_Y_Coord = random.randint(0, 720 - lengthOfImage)
        nodesX.append(randomized_X_Coord)
        nodesY.append(randomized_Y_Coord)

    nodes1 = np.asfortranarray([
        [starting_X_Value] + nodesX + [end_X_Value],
        [starting_Y_Value] + nodesY + [end_Y_Value],
    ])

    return generateBezier(nodes1, randomizeDegree)

def generateBezier(nodes, degree):
    curve = bezier.Curve(nodes, degree)

    points = []
    # xList = []
    # yList = []
    for i in range(0, 100, 1):
        i = i/100

        points.append(curve.evaluate(i * 1.0))
        # xList.append(curve.evaluate(i * 1.0)[0])
        # yList.append(curve.evaluate(i * 1.0)[1])

    return points
    # plotBezier(xList, yList)

def plotBezier(xList, yList):
    plt.plot(xList, yList)
    plt.ylabel('some numbers')
    plt.axis([0, 1280, 0, 620])
    plt.show()

print(generateRandomizeBezier())