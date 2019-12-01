import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from MorphingGUI import *
from PyQt5.QtGui import QIcon, QPixmap


class MorphingAPP(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MorphingAPP, self).__init__(parent)
        self.setupUi(self)
        self.checkBox.setEnabled(False)
        self.blendImg.setEnabled(False)
        self.horizontalSlider.setEnabled(False)
        self.textEdit.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.initstate()

    def initstate(self):
        self.pushButton.clicked.connect(self.loadLData)
        self.pushButton_2.clicked.connect(self.loadRData)

    def loadRData(self):
        filePath, _ = QFileDialog.getOpenFileName(self, caption='Open IMG file ...', filter="IMGs (*.png *.jpg)")
        if not filePath:
            return
        self.rightPoint = filePath + ".txt"
        self.loadDataFromFile(filePath, self.endImg)


    def loadLData(self):
        filePath, _ = QFileDialog.getOpenFileName(self, caption='Open IMG file ...', filter="IMGs (*.png *.jpg)")
        if not filePath:
            return
        self.leftPoint = filePath + ".txt"
        self.loadDataFromFile(filePath, self.startImg)

    def loadDataFromFile(self, filePath, which):
        pixmap = QPixmap(filePath)
        which.setPixmap(pixmap)
        which.setScaledContents(True)


if __name__ == "__main__":
    currentApp = QApplication(sys.argv)
    currentForm = MorphingAPP()

    currentForm.show()
    currentApp.exec_()
