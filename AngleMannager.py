import numpy
import math

class AngleMannager:

    def __init__(self):
        self.centerPoint = None
        self.cornerPoint = None
        self.finalPoint = None


    def calculateAngle(self):
        horizontalVector = [self.centerPoint[0]-self.cornerPoint[0],0]
        angleVector = [self.finalPoint[0]-self.cornerPoint[0], (self.finalPoint[1]-self.cornerPoint[1])]
        try:
            angleValue = numpy.arccos((horizontalVector[0] * angleVector[0]) / (
                        (((angleVector[0] ** 2) + (angleVector[1] ** 2)) ** (1 / 2)) * abs(horizontalVector[0])))
            angleValue = (angleValue * 180)/math.pi
        except ZeroDivisionError:
            pass
        return round(angleValue, 3)

    def reset(self):
        self.centerPoint = None
        self.cornerPoint = None
        self.finalPoint = None

