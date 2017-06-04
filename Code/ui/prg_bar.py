# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scanning_repo.ui'
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

class Ui_DialogProgressBar(object):
    def setupUi(self, DialogProgressBar):
        DialogProgressBar.setObjectName(_fromUtf8("DialogProgressBar"))
        DialogProgressBar.resize(486, 104)
        self.progressBarRepo = QtGui.QProgressBar(DialogProgressBar)
        self.progressBarRepo.setGeometry(QtCore.QRect(20, 20, 451, 31))
        self.progressBarRepo.setProperty("value", 24)
        self.progressBarRepo.setTextVisible(False)
        self.progressBarRepo.setInvertedAppearance(False)
        self.progressBarRepo.setTextDirection(QtGui.QProgressBar.TopToBottom)
        self.progressBarRepo.setObjectName(_fromUtf8("progressBarRepo"))
        self.labelScanComplete = QtGui.QLabel(DialogProgressBar)
        self.labelScanComplete.setEnabled(True)
        self.labelScanComplete.setGeometry(QtCore.QRect(177, 28, 101, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.labelScanComplete.setFont(font)
        self.labelScanComplete.setMouseTracking(False)
        self.labelScanComplete.setToolTip(_fromUtf8(""))
        self.labelScanComplete.setInputMethodHints(QtCore.Qt.ImhNone)
        self.labelScanComplete.setObjectName(_fromUtf8("labelScanComplete"))
        self.pushButtonClose = QtGui.QPushButton(DialogProgressBar)
        self.pushButtonClose.setEnabled(False)
        self.pushButtonClose.setGeometry(QtCore.QRect(181, 65, 75, 23))
        self.pushButtonClose.setObjectName(_fromUtf8("pushButtonClose"))

        self.retranslateUi(DialogProgressBar)
        QtCore.QMetaObject.connectSlotsByName(DialogProgressBar)

    def retranslateUi(self, DialogProgressBar):
        DialogProgressBar.setWindowTitle(_translate("DialogProgressBar", "Scanning available repositories", None))
        self.progressBarRepo.setFormat(_translate("DialogProgressBar", "%p%", None))
        self.labelScanComplete.setText(_translate("DialogProgressBar", "scanning !", None))
        self.pushButtonClose.setText(_translate("DialogProgressBar", "Close", None))

