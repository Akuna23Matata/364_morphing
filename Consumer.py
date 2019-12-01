
#######################################################
#   Author:     <Your Full Name>
#   email:      <Your Email>
#   ID:         <Your course ID, e.g. ee364j20>
#   Date:       <Start Date>
#######################################################

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from BasicUI import *
import re


class Consumer(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):

        super(Consumer, self).__init__(parent)
        self.setupUi(self)
        self.componentName = [self.txtComponentName_1, self.txtComponentName_2, self.txtComponentName_3, self.txtComponentName_4, self.txtComponentName_5, self.txtComponentName_6, self.txtComponentName_7,
                              self.txtComponentName_8, self.txtComponentName_9, self.txtComponentName_10, self.txtComponentName_11, self.txtComponentName_12, self.txtComponentName_13, self.txtComponentName_14,
                              self.txtComponentName_15, self.txtComponentName_16, self.txtComponentName_17, self.txtComponentName_18, self.txtComponentName_19, self.txtComponentName_20]
        self.componentNum = [self.txtComponentCount_1, self.txtComponentCount_2, self.txtComponentCount_3, self.txtComponentCount_4, self.txtComponentCount_5,
                             self.txtComponentCount_6, self.txtComponentCount_7, self.txtComponentCount_8, self.txtComponentCount_9, self.txtComponentCount_10,
                             self.txtComponentCount_11, self.txtComponentCount_12, self.txtComponentCount_13, self.txtComponentCount_14, self.txtComponentCount_15,
                             self.txtComponentCount_16, self.txtComponentCount_17, self.txtComponentCount_18, self.txtComponentCount_19, self.txtComponentCount_20]
        self.btnSave.setEnabled(False)
        self.btnSave.clicked.connect(self.save)
        self.btnClear.clicked.connect(self.reset)
        for n in self.componentName:
            n.textChanged.connect(self.updateState)
        for n in self.componentNum:
            n.textChanged.connect(self.updateState)
        self.txtStudentID.textChanged.connect(self.updateState)
        self.txtStudentName.textChanged.connect(self.updateState)
        self.cboCollege.currentIndexChanged.connect(self.updateState)
        self.chkGraduate.stateChanged.connect(self.updateState)
        self.btnLoad.clicked.connect(self.loadData)

    def updateState(self):
        self.btnSave.setEnabled(True)
        self.btnLoad.setEnabled(False)

    def reset(self):
        self.txtStudentName.clear()
        self.txtStudentID.clear()
        self.cboCollege.setCurrentIndex(0)
        for n in self.componentName:
            n.clear()
        for n in self.componentNum:
            n.clear()
        self.chkGraduate.setChecked(False)
        self.btnSave.setEnabled(False)
        self.btnLoad.setEnabled(True)

    def save(self):
        rtn = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Content>\n    <StudentName graduate=\""
        if self.chkGraduate.isChecked():
            rtn += "true\">"
        else:
            rtn += "false\">"
        rtn += self.txtStudentName.text() + "</StudentName>\n"
        rtn += "    <StudentID>" + self.txtStudentID.text() + "</StudentID>\n"
        rtn += "    <College>" + self.cboCollege.itemText(self.cboCollege.currentIndex()) + "</College>\n"
        rtn += "    <Components>\n"
        for n in range(0,20):
            if(self.componentName[n].text()):
                rtn += "        <Component name=\"" + self.componentName[n].text() + "\" count=\"" + self.componentNum[n].text() + "\" />\n"
        rtn += "    </Components>\n"
        rtn += "</Content>\n"
        with open("./target.xml", "w") as nFile:
            nFile.write(rtn)


    def loadData(self):
        """
        *** DO NOT MODIFY THIS METHOD! ***
        Obtain a file name from a file dialog, and pass it on to the loading method. This is to facilitate automated
        testing. Invoke this method when clicking on the 'load' button.

        You must modify the method below.
        """
        filePath, _ = QFileDialog.getOpenFileName(self, caption='Open XML file ...', filter="XML files (*.xml)")

        if not filePath:
            return

        self.loadDataFromFile(filePath)

    def loadDataFromFile(self, filePath):
        """
        Handles the loading of the data from the given file name. This method will be invoked by the 'loadData' method.
        
        *** YOU MUST USE THIS METHOD TO LOAD DATA FILES. ***
        *** This method is required for unit tests! ***
        """
        with open(filePath, "r") as nFile:
            text = nFile.read()
        #first find name and graduate
        if(re.search(">.+?</StudentName>", text)):
            name = re.findall(">.+?</StudentName>", text)[0][1:-14]
            self.txtStudentName.setText(name)
        if(re.search(">.+?</StudentID>", text)):
            sID = re.findall(">.+?</StudentID>", text)[0][1:-12]
            self.txtStudentID.setText(sID)
        college = re.findall(">.+?</College>", text)[0][1:-10]
        self.cboCollege.setCurrentIndex(self.cboCollege.findText(college))
        if re.findall("graduate=\".+?\"", text)[0] == "graduate=\"true\"":
            self.chkGraduate.setChecked(True)
        else:
            self.chkGraduate.setChecked(False)
        component = re.findall("<Component name=\".+?\" count=\".+?\" />", text)
        i = 0
        for n in component:
            if i >= 20:
                pass
            else:
                name = re.findall("name=\".+?\"", n)[0][6:-1]
                count = re.findall("count=\".+?\"", n)[0][7:-1]
                self.componentName[i].setText(name)
                self.componentNum[i].setText(count)
                i += 1
        self.btnSave.setEnabled(True)
        self.btnLoad.setEnabled(False)




if __name__ == "__main__":
    currentApp = QApplication(sys.argv)
    currentForm = Consumer()

    currentForm.show()
    currentApp.exec_()
