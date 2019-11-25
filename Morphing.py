import numpy as np
import scipy
import imageio
from PIL import Image, ImageDraw
from matplotlib.path import Path


def checkArray(instance, type):
    if not isinstance(instance, np.ndarray):
        raise TypeError("Input is not in type np.array")
    elif instance.dtype != type:
        raise TypeError("Input is not array in uint8")


def checkTrilist(instance):
    if not isinstance(instance, list):
        raise TypeError("Input is not a list")
    for n in instance:
        if not isinstance(n, Triangle):
            raise TypeError("Input is not list of class Triangle")


class Triangle:
    vertices = None

    def __init__(self, vertices):
        if not isinstance(vertices, np.ndarray):
            raise ValueError("Input is not in type np.array")
        elif vertices.dtype != "float64":
            raise ValueError("Input is not array in float64")
        elif vertices.shape != (3, 2):
            raise ValueError("Input is not in shape (3, 2)")
        self.vertices = vertices

    def getPoints(self):
        rtn = list()
        # generate path
        tri = Path([(self.vertices[0][0], self.vertices[0][1]), (self.vertices[1][0], self.vertices[1][1]),(self.vertices[2][0], self.vertices[2][1]), (self.vertices[0][0], self.vertices[0][1])])
        # define a region
        x = [self.vertices[0][0], self.vertices[1][0], self.vertices[2][0]]
        y = [self.vertices[0][1], self.vertices[1][1], self.vertices[2][1]]
        rangeX = (min(x), max(x))
        rangeY = (min(y), max(y))
        # check triangle contains point
        for x_axis in range(rangeX[0].astype(int), rangeX[1].astype(int) + 1):
            for y_axis in range(rangeY[0].astype(int), rangeY[1].astype(int) + 1):
                if tri.contains_point((x_axis, y_axis)):
                    rtn.append([x_axis, y_axis])
        return np.array(rtn, dtype=np.float64)


class Morpher:
    leftImage = None
    leftTriangles = list()
    rightImage = None
    rightTriangles = list()

    def __init__(self, leftImage, leftTriangles, rightImage, rightTriangles):
        checkArray(leftImage, "uint8")
        checkArray(rightImage, "uint8")
        checkTrilist(leftTriangles)
        checkTrilist(rightTriangles)
        self.leftImage = leftImage
        self.leftTriangles = leftTriangles
        self.rightImage = rightImage
        self.rightTriangles = rightTriangles

    # def getImageAtAlpha(self, alpha):

    # transform left triangle

    # transform right triangle

    # blending


if __name__ == "__main__":
    a = np.array([[0, 0], [0, 2], [2, 3]], dtype=np.float64)
    b = Triangle(a)
