# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MorphingGUI.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(713, 735)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(70, 20, 141, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(410, 20, 141, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.startImg = QtWidgets.QLabel(self.centralwidget)
        self.startImg.setGeometry(QtCore.QRect(60, 80, 251, 221))
        self.startImg.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.startImg.setText("")
        self.startImg.setObjectName("startImg")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 310, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Abyssinica SIL")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(460, 310, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Abyssinica SIL")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(300, 320, 131, 21))
        self.checkBox.setObjectName("checkBox")
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(80, 360, 501, 20))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 360, 62, 17))
        font = QtGui.QFont()
        font.setFamily("Abyssinica SIL")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(80, 390, 62, 17))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(560, 380, 62, 17))
        self.label_5.setObjectName("label_5")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(590, 350, 71, 31))
        self.textEdit.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.textEdit.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.textEdit.setObjectName("textEdit")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(290, 620, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Abyssinica SIL")
        font.setPointSize(14)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(290, 650, 141, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.endImg = QtWidgets.QLabel(self.centralwidget)
        self.endImg.setGeometry(QtCore.QRect(400, 80, 251, 221))
        self.endImg.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.endImg.setText("")
        self.endImg.setObjectName("endImg")
        self.startImg_3 = QtWidgets.QLabel(self.centralwidget)
        self.startImg_3.setGeometry(QtCore.QRect(230, 390, 251, 221))
        self.startImg_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.startImg_3.setText("")
        self.startImg_3.setObjectName("startImg_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 713, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Load Starting Image"))
        self.pushButton_2.setText(_translate("MainWindow", "Load Ending Image"))
        self.label.setText(_translate("MainWindow", "Starting Image"))
        self.label_2.setText(_translate("MainWindow", "Ending Image"))
        self.checkBox.setText(_translate("MainWindow", "Show Triangles"))
        self.label_3.setText(_translate("MainWindow", "Alpha"))
        self.label_4.setText(_translate("MainWindow", "0.0"))
        self.label_5.setText(_translate("MainWindow", "1.0"))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">0.0</span></p></body></html>"))
        self.label_6.setText(_translate("MainWindow", "Blending Result"))
        self.pushButton_3.setText(_translate("MainWindow", "Blend"))

