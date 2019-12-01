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
        self.pushButton.clicked.connect(self.loadData())

    def loadData(self):
        """
        *** DO NOT MODIFY THIS METHOD! ***
        Obtain a file name from a file dialog, and pass it on to the loading method. This is to facilitate automated
        testing. Invoke this method when clicking on the 'load' button.

        You must modify the method below.
        """
        filePath, _ = QFileDialog.getOpenFileName(self, caption='Open XML file ...', filter="XML files (*.png)")

        if not filePath:
            return

        self.loadDataFromFile(filePath)

    def loadDataFromFile(self, filePath):
        pixmap = QPixmap(filePath)
        self.startImg.setPixmap(pixmap)


if __name__ == "__main__":
    currentApp = QApplication(sys.argv)
    currentForm = MorphingAPP()

    currentForm.show()
    currentApp.exec_()
