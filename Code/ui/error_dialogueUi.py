# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'error_dialogue.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ErrorDialogue(object):
    def setupUi(self, ErrorDialogue):
        ErrorDialogue.setObjectName(_fromUtf8("ErrorDialogue"))
        ErrorDialogue.resize(306, 161)
        self.label = QtGui.QLabel(ErrorDialogue)
        self.label.setGeometry(QtCore.QRect(120, 10, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.textBrowser = QtGui.QTextBrowser(ErrorDialogue)
        self.textBrowser.setGeometry(QtCore.QRect(20, 40, 261, 71))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.pushButton = QtGui.QPushButton(ErrorDialogue)
        self.pushButton.setGeometry(QtCore.QRect(109, 124, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))

        self.retranslateUi(ErrorDialogue)
        QtCore.QMetaObject.connectSlotsByName(ErrorDialogue)

    def retranslateUi(self, ErrorDialogue):
        ErrorDialogue.setWindowTitle(_translate("ErrorDialogue", "Error !", None))
        self.label.setText(_translate("ErrorDialogue", "Error !", None))
        self.textBrowser.setHtml(_translate("ErrorDialogue", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Something is wrong out there !</span></p></body></html>", None))
        self.pushButton.setText(_translate("ErrorDialogue", "OK", None))

