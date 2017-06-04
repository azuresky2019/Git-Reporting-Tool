# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
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

class Ui_DialogAbout(object):
    def setupUi(self, DialogAbout):
        DialogAbout.setObjectName(_fromUtf8("DialogAbout"))
        DialogAbout.resize(307, 123)
        self.pushButtonOk = QtGui.QPushButton(DialogAbout)
        self.pushButtonOk.setGeometry(QtCore.QRect(112, 92, 75, 23))
        self.pushButtonOk.setObjectName(_fromUtf8("pushButtonOk"))
        self.label = QtGui.QLabel(DialogAbout)
        self.label.setGeometry(QtCore.QRect(60, 20, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(DialogAbout)
        self.label_2.setGeometry(QtCore.QRect(120, 50, 61, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.retranslateUi(DialogAbout)
        QtCore.QMetaObject.connectSlotsByName(DialogAbout)

    def retranslateUi(self, DialogAbout):
        DialogAbout.setWindowTitle(_translate("DialogAbout", "About", None))
        self.pushButtonOk.setText(_translate("DialogAbout", "OK", None))
        self.label.setText(_translate("DialogAbout", "Git Report tool Temco Nepal", None))
        self.label_2.setText(_translate("DialogAbout", "Version 0.1", None))

