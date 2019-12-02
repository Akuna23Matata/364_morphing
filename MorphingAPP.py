import sys

from PyQt5.QtCore import QPointF
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from MorphingGUI import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap, QPen, QBrush, QPainter, QPolygonF, QImage
import os
import Morphing
import numpy as np
from scipy.spatial import Delaunay
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import io


class MorphingAPP(QMainWindow, Ui_MainWindow):
    Left = False
    Right = False
    rightPoint = None
    leftPoint = None
    leftFile = None
    rightFile = None
    rightTri = None
    leftTri = None
    leftDot = None
    rightDot = None
    alpha = None

    def __init__(self, parent=None):
        super(MorphingAPP, self).__init__(parent)
        self.setupUi(self)
        self.checkBox.setEnabled(False)
        self.blendImg.setEnabled(False)
        self.horizontalSlider.setEnabled(False)
        self.textEdit.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.initstate()
        self.checkBox.toggled.connect(self.trianglecheck)
        self.horizontalSlider.valueChanged.connect(self.getAlpha)
        self.textEdit.setReadOnly(True)
        self.pushButton_3.clicked.connect(self.blend)
        self.resize(600, 400)
        

    def blend(self):
        left, right = Morphing.loadTriangles(self.leftFile + ".txt", self.rightFile + ".txt")
        leftimg = np.asarray(Image.open(self.leftFile))
        rightimg = np.asarray(Image.open(self.rightFile))
        m = Morphing.Morpher(leftimg, left, rightimg, right)
        pic = m.getImageAtAlpha(self.alpha)
        pixmap = QPixmap.fromImage(pic)
        self.blendImg.setPixmap(pixmap)


    def getAlpha(self):
        self.alpha = self.horizontalSlider.value() / 99
        tmp = '{0:0.2f}'.format(self.alpha)
        self.textEdit.setText(str(tmp))

    def trianglecheck(self):
        if self.checkBox.checkState():
            self.showTri()
        else:
            self.startImg.setPixmap(self.leftDot)
            self.endImg.setPixmap(self.rightDot)

    def showTri(self):
        leftPoints = np.array(self.leftPoint)
        rightPoints = np.array(self.rightPoint)
        if self.leftTri is None:
            temp = Delaunay(leftPoints)
            img = plt.imread(self.leftFile)
            fig, ax = plt.subplots()
            ax.imshow(img, cmap="gray")
            plt.triplot(leftPoints[:, 0], leftPoints[:, 1], temp.simplices, "r-", linewidth=1)
            plt.plot(leftPoints[:, 0], leftPoints[:, 1], 'ro')
            plt.axis("off")
            buf = io.BytesIO()
            plt.savefig(buf, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
            buf.seek(0)
            imgdata = buf.read()
            self.leftTri = QPixmap.fromImage(QImage.fromData(imgdata))
            buf.close()
        self.startImg.setPixmap(self.leftTri)
        self.startImg.setScaledContents(True)
        if self.rightTri is None:
            temp = Delaunay(rightPoints)
            img = plt.imread(self.rightFile)
            fig, ax = plt.subplots()
            ax.imshow(img, cmap="gray")
            plt.triplot(rightPoints[:, 0], rightPoints[:, 1], temp.simplices, "r-", linewidth=1)
            plt.plot(rightPoints[:, 0], rightPoints[:, 1], 'ro')
            plt.axis("off")
            buf = io.BytesIO()
            plt.savefig(buf, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
            buf.seek(0)
            imgdata = buf.read()
            self.rightTri = QPixmap.fromImage(QImage.fromData(imgdata))
            buf.close()
        self.endImg.setPixmap(self.rightTri)
        self.endImg.setScaledContents(True)


    def initstate(self):
        self.pushButton.clicked.connect(self.loadLData)
        self.pushButton_2.clicked.connect(self.loadRData)

    def loadedState(self):
        self.checkBox.setEnabled(True)
        self.blendImg.setEnabled(True)
        self.horizontalSlider.setEnabled(True)
        self.textEdit.setEnabled(True)
        self.pushButton_3.setEnabled(True)

    def loadRData(self):
        self.rightTri = None
        self.rightFile, _ = QFileDialog.getOpenFileName(self, caption='Open IMG file ...', filter="IMGs (*.png *.jpg)")
        if not self.rightFile:
            return
        rightPoint = self.rightFile + ".txt"
        self.Right = True
        if os.path.exists(rightPoint):
            with open(rightPoint, "r") as fp:
                self.rightPoint = fp.readlines()
            for i in range(len(self.rightPoint)):
                self.rightPoint[i] = self.rightPoint[i].strip()
                self.rightPoint[i] = self.rightPoint[i].split()
                self.rightPoint[i][0] = float(self.rightPoint[i][0])
                self.rightPoint[i][1] = float(self.rightPoint[i][1])
        self.loadDataFromFile(self.rightFile, self.endImg, self.rightPoint)

    def loadLData(self):
        self.leftTri = None
        self.leftFile, _ = QFileDialog.getOpenFileName(self, caption='Open IMG file ...', filter="IMGs (*.png *.jpg)")
        if not self.leftFile:
            return
        leftPoint = self.leftFile + ".txt"
        self.Left = True
        if os.path.exists(leftPoint):
            with open(leftPoint, "r") as fp:
                self.leftPoint = fp.readlines()
            for i in range(len(self.leftPoint)):
                self.leftPoint[i] = self.leftPoint[i].strip()
                self.leftPoint[i] = self.leftPoint[i].split()
                self.leftPoint[i][0] = float(self.leftPoint[i][0])
                self.leftPoint[i][1] = float(self.leftPoint[i][1])
        self.loadDataFromFile(self.leftFile, self.startImg, self.leftPoint)

    def loadDataFromFile(self, filePath, which, point):
        pixmap = QPixmap(filePath)
        if point is not None:
            painter = QPainter(pixmap)
            painter.drawPixmap(pixmap.rect(), pixmap)
            pen = QPen(QtCore.Qt.red, 5)
            painter.setPen(pen)
            painter.setBrush(QtCore.Qt.red)
            for n in point:
                painter.drawEllipse(QPointF(n[0], n[1]), 10, 10)
            del painter
        if point == self.leftPoint:
            self.leftDot = pixmap
        if point == self.rightPoint:
            self.rightDot = pixmap
        which.setPixmap(pixmap)
        which.setScaledContents(True)
        if self.Left & self.Right:
            self.loadedState()


if __name__ == "__main__":
    currentApp = QApplication(sys.argv)
    currentForm = MorphingAPP()

    currentForm.show()
    currentApp.exec_()
