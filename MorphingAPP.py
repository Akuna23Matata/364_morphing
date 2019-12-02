import sys

from PIL.ImageQt import ImageQt
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
    rightPoint = list()
    leftPoint = list()
    leftFile = None
    rightFile = None
    rightTri = None
    leftTri = None
    leftDot = None
    rightDot = None
    alpha = None
    tmpLDot = None
    tmpLDotPic = None
    tmpRDot = None
    tmpRDotPic = None
    addLDot = list()
    addRDot = list()
    changed = True
    size = None

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
        self.startImg.mousePressEvent = self.getLDot
        self.endImg.mousePressEvent = self.getRDot
        self.mousePressEvent = self.savechange

    def delLtmp(self, event):
        if event.key() == QtCore.Qt.Key_Backspace:
            self.tmpLDot = None
            self.tmpLDotPic = None
            self.startImg.setPixmap(self.leftDot)

    def delRtmp(self, event):
        if event.key() == QtCore.Qt.Key_Backspace:
            self.tmpRDot = None
            self.tmpRDotPic = None
            self.endImg.setPixmap(self.rightDot)

    def savechange(self, event):
        if self.tmpRDot is None:
            return
        if self.tmpLDot is None:
            return
        self.addLDot.append(self.tmpLDot)
        self.addRDot.append(self.tmpRDot)
        self.tmpRDot = None
        self.tmpLDot = None
        self.loadDataFromFile(self.leftFile, self.startImg, self.leftPoint, None, self.addLDot)
        self.loadDataFromFile(self.rightFile, self.endImg, self.rightPoint, None, self.addRDot)
        self.updateDotFile()



    def getLDot(self, event):
        if self.tmpLDot is None:
            x = event.pos().x() * float(self.size.width()) / 251
            y = event.pos().y() * float(self.size.height()) / 221
            self.tmpLDot = [x,y]
            self.loadDataFromFile(self.leftFile, self.startImg, self.leftPoint, self.tmpLDot, self.addLDot)
            self.keyPressEvent = self.delLtmp
        elif self.tmpRDot != None:
            self.addLDot.append(self.tmpLDot)
            self.addRDot.append(self.tmpRDot)
            self.tmpRDot = None
            x = event.pos().x() * float(self.leftDot.size().width()) / 251
            y = event.pos().y() * float(self.leftDot.size().height()) / 221
            self.tmpLDot = [x, y]
            self.loadDataFromFile(self.leftFile, self.startImg, self.leftPoint, self.tmpLDot, self.addLDot)
            self.loadDataFromFile(self.rightFile, self.endImg, self.rightPoint, None, self.addRDot)
            self.updateDotFile()

    def updateDotFile(self):
        if self.leftPoint == None:
            left = self.addLDot
        else:
            left = self.addLDot + self.leftPoint
        f = open(self.leftFile + ".txt", "w")
        for n in left:
            f.write(str(round(n[0],1)) + "\t" + str(round(n[1], 1)) + "\n")
        f.close()
        if self.rightPoint == None:
            right = self.addRDot
        else:
            right = self.addRDot + self.rightPoint
        f = open(self.rightFile + ".txt", "w")
        for n in right:
            f.write(str(round(n[0], 1)) + "\t" + str(round(n[1], 1)) + "\n")
        f.close()


    def getRDot(self, event):
        if self.tmpLDot is None:
            return
        if self.tmpRDot != None:
            return
        x = event.pos().x() * float(self.leftDot.size().width()) / 251
        y = event.pos().y() * float(self.leftDot.size().height()) / 221
        self.tmpRDot = [x,y]
        self.loadDataFromFile(self.rightFile, self.endImg, self.rightPoint, self.tmpRDot, self.addRDot)
        self.keyPressEvent = self.delRtmp

    def blend(self):
        left, right = Morphing.loadTriangles(self.leftFile + ".txt", self.rightFile + ".txt")
        leftimg = np.asarray(Image.open(self.leftFile))
        rightimg = np.asarray(Image.open(self.rightFile))
        m = Morphing.Morpher(leftimg, left, rightimg, right)
        pic = m.getImageAtAlpha(self.alpha)
        img = Image.fromarray(pic, 'L')
        qim = ImageQt(img)
        pix = QPixmap.fromImage(qim)
        self.blendImg.setPixmap(pix)
        self.blendImg.setScaledContents(True)

    def getAlpha(self):
        self.alpha = self.horizontalSlider.value() / 99
        tmp = '{0:0.2f}'.format(self.alpha)
        self.textEdit.setText(str(tmp))

    def trianglecheck(self):
        if self.checkBox.checkState():
            if self.leftPoint is None:
                self.showTri("b-")
            if self.addLDot != list():
                self.showTri("y-")
            else:
                self.showTri("r-")
        else:
            self.startImg.setPixmap(self.leftDot)
            self.endImg.setPixmap(self.rightDot)

    def showTri(self, color):
        if self.leftPoint is None:
            left = self.addLDot
        else:
            left = self.leftPoint + self.addLDot
        if self.rightPoint is None:
            right = self.addRDot
        else:
            right = self.rightPoint + self.addRDot
        if not os.path.exists(self.leftFile + ".txt"):
            return
        leftPoints = np.array(left)
        rightPoints = np.array(right)
        if self.changed:
            temp = Delaunay(leftPoints)
            img = plt.imread(self.leftFile)
            _, ax = plt.subplots()
            ax.imshow(img, cmap="gray")
            plt.triplot(leftPoints[:, 0], leftPoints[:, 1], temp.simplices, color, linewidth=0.6)
            plt.plot(leftPoints[:, 0], leftPoints[:, 1], 'ro')
            plt.axis("off")
            buf = io.BytesIO()
            plt.savefig(buf, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
            plt.close("all")
            buf.seek(0)
            imgdata = buf.read()
            self.leftTri = QPixmap.fromImage(QImage.fromData(imgdata))
            buf.close()
        self.startImg.setPixmap(self.leftTri)
        self.startImg.setScaledContents(True)
        if self.changed:
            temp = Delaunay(rightPoints)
            img = plt.imread(self.rightFile)
            _, ax = plt.subplots()
            ax.imshow(img, cmap="gray")
            plt.triplot(rightPoints[:, 0], rightPoints[:, 1], temp.simplices, color, linewidth=1)
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
        else:
            self.rightPoint = None
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
        else:
            self.leftPoint = None
        self.loadDataFromFile(self.leftFile, self.startImg, self.leftPoint)

    def loadDataFromFile(self, filePath, which, point, tmpPoint = None, newPoint = None):
        pixmap = QPixmap(filePath)
        self.size = pixmap.size()
        painter = QPainter(pixmap)
        painter.drawPixmap(pixmap.rect(), pixmap)
        if point is not None:
            pen = QPen(QtCore.Qt.red, 5)
            painter.setPen(pen)
            painter.setBrush(QtCore.Qt.red)
            for n in point:
                painter.drawEllipse(QPointF(n[0], n[1]), 10, 10)
        if tmpPoint != None:
            painter.setPen(QPen(QtCore.Qt.green, 5))
            painter.setBrush(QtCore.Qt.green)
            painter.drawEllipse(QPointF(tmpPoint[0], tmpPoint[1]), 10, 10)
            if point == self.leftPoint:
                self.tmpLDotPic = pixmap
            else:
                self.tmpRDotPic = pixmap
        if newPoint != None:
            painter.setPen(QPen(QtCore.Qt.blue, 5))
            painter.setBrush(QtCore.Qt.blue)
            for n in newPoint:
                painter.drawEllipse(QPointF(n[0], n[1]), 10, 10)
            if point == self.leftPoint:
                self.leftDot = pixmap
            if point == self.rightPoint:
                self.rightDot = pixmap
        del painter
        which.setPixmap(pixmap)
        which.setScaledContents(True)
        if self.Left & self.Right:
            self.loadedState()


if __name__ == "__main__":
    currentApp = QApplication(sys.argv)
    currentForm = MorphingAPP()

    currentForm.show()
    currentApp.exec_()
