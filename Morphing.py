import numpy as np
from scipy import ndimage, spatial
from PIL import Image, ImageDraw
from matplotlib.path import Path
import imageio


def matrixGen(first, second):
    h = np.linalg.solve(np.array([[first[0][0], first[0][1], 1, 0, 0, 0],
                                  [0, 0, 0, first[0][0], first[0][1], 1],
                                  [first[1][0], first[1][1], 1, 0, 0, 0],
                                  [0, 0, 0, first[1][0], first[1][1], 1],
                                  [first[2][0], first[2][1], 1, 0, 0, 0],
                                  [0, 0, 0, first[2][0], first[2][1], 1]]),
                        np.array([[second[0][0]], [second[0][1]],
                                  [second[1][0]],[second[1][1]],
                                  [second[2][0]], [second[2][1]]]))
    rtn = np.array([[h[0][0], h[1][0], h[2][0]],
                  [h[3][0], h[4][0], h[5][0]],
                  [0, 0, 1]])
    return rtn


def blender(initial, end, vertices, H):
    target = Image.new('L', (initial.shape[1], initial.shape[0]), 0)
    ImageDraw.Draw(target).polygon([(vertices[0][0], vertices[0][1]), (vertices[1][0], vertices[1][1]), (vertices[2][0], vertices[2][1])], outline = 1, fill=1)
    mask1 = np.nonzero(target)
    together = np.vstack((list(mask1[1]), list(mask1[0]), np.ones((len(list(mask1[0]))))))
    result = np.linalg.inv(H).dot(together)
    end[list(mask1[0]), list(mask1[1])] = ndimage.map_coordinates(initial, [result[1], result[0]], order = 1, mode = "nearest")


def readPoints(path):
    try:
        with open(path, "r") as fp:
            points = fp.readlines()
    except IOError:
        print("Cannot open the file")
    for i in range(len(points)):
        points[i] = points[i].strip()
        points[i] = points[i].split()
        points[i][0] = float(points[i][0])
        points[i][1] = float(points[i][1])
    return points


def loadTriangles(leftPointFilePath, rightPointFilePath):
    leftPoints = readPoints(leftPointFilePath)
    rightPoints = readPoints(rightPointFilePath)
    leftPoints = np.array(leftPoints)
    temp = spatial.Delaunay(leftPoints)
    leftTriangles = list()
    rightTriangles = list()
    for i in temp.simplices.tolist():
        array = np.array([[leftPoints[i[0]][0], leftPoints[i[0]][1]],
                          [leftPoints[i[1]][0], leftPoints[i[1]][1]],
                          [leftPoints[i[2]][0], leftPoints[i[2]][1]]], dtype=np.float64)
        leftTriangles.append(Triangle(array))
        array = np.array([[rightPoints[i[0]][0], rightPoints[i[0]][1]],
                          [rightPoints[i[1]][0], rightPoints[i[1]][1]],
                          [rightPoints[i[2]][0], rightPoints[i[2]][1]]], dtype=np.float64)
        rightTriangles.append(Triangle(array))
    return (leftTriangles, rightTriangles)

def area(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1)
                + x3 * (y1 - y2)) / 2.0)


def triangleContain(vertices, point):
    a = area(vertices[0][0], vertices[0][1], vertices[1][0], vertices[1][1], vertices[2][0], vertices[2][1])
    a1 = area(point[0], point[1], vertices[1][0], vertices[1][1], vertices[2][0], vertices[2][1])
    a2 = area(vertices[0][0], vertices[0][1], point[0], point[1], vertices[2][0], vertices[2][1])
    a3 = area(vertices[0][0], vertices[0][1], vertices[1][0], vertices[1][1], point[0], point[1])
    if a == a1 + a2 + a3:
        return True
    else:
        return False


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
        tri = Path([(self.vertices[0][0], self.vertices[0][1]), (self.vertices[1][0], self.vertices[1][1]),
                    (self.vertices[2][0], self.vertices[2][1]), (self.vertices[0][0], self.vertices[0][1])])
        # define a region
        x = [self.vertices[0][0], self.vertices[1][0], self.vertices[2][0]]
        y = [self.vertices[0][1], self.vertices[1][1], self.vertices[2][1]]
        rangeX = (min(x), max(x))
        rangeY = (min(y), max(y))
        # check triangle contains point
        for x_axis in range(rangeX[0].astype(int), rangeX[1].astype(int) + 1):
            for y_axis in range(rangeY[0].astype(int), rangeY[1].astype(int) + 1):
                if triangleContain(self.vertices, (x_axis, y_axis)):
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

    def getImageAtAlpha(self, alpha):
        blankLeft = np.array(Image.new("L", (self.leftImage.shape[1], self.leftImage.shape[0]), "white"))
        blankRight = np.array(Image.new("L", (self.leftImage.shape[1], self.leftImage.shape[0]), "white"))
        for i in range(len(self.rightTriangles)):
            leftarr = self.leftTriangles[i].vertices
            rightarr = self.rightTriangles[i].vertices
            array = rightarr * alpha + leftarr * (1 - alpha)
            blender(self.leftImage, blankLeft, array, matrixGen(leftarr, array))
            blender(self.rightImage, blankRight, array, matrixGen(rightarr, array))
        image = blankRight * alpha + blankLeft * (1 - alpha)
        return image.astype(np.uint8)

    def saveVideo(self, targetFilePath, frameCount, frameRate, includeReversed=True):
        makemp4 = imageio.get_writer(targetFilePath, fps=frameRate)
        frame = list()
        ct = 1
        for alpha in np.linspace(0, 1, frameCount):
            img = self.getImageAtAlpha(alpha)
            makemp4.append_data(img)
            frame.append(img)
            imageio.imsave("/tmp" + "/IMG_{:02d}.jpg".format(ct), img)
            ct += 1
        if includeReversed:
            for n in reversed(frame):
                makemp4.append_data(n)
                imageio.imsave("/tmp" + "/IMG_{:02d}.jpg".format(ct), n)
                ct += 1
        makemp4.close()


if __name__ == "__main__":
    a = np.array([[0, 0], [2, 0], [2, 3]], dtype=np.float64)
    b = Triangle(a)
    left, right = loadTriangles("./TestData/points.left.txt", "./TestData/points.right.txt")
    leftimg = np.asarray(Image.open('./TestData/LeftGray.png'))
    rightimg = np.asarray(Image.open('./TestData/RightGray.png'))
    m = Morpher(leftimg, left, rightimg, right)
    pic = m.getImageAtAlpha(0.5)
    img = Image.fromarray(pic, 'L')
    img.save('my.png')
    img.show()
    # m.saveVideo("./test.mp4", 10, 5)
