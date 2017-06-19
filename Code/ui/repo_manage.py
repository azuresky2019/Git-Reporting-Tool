# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'repo_list.ui'
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

class Ui_repo_manager(object):
    def setupUi(self, repo_manager):
        repo_manager.setObjectName(_fromUtf8("repo_manager"))
        repo_manager.resize(472, 371)
        self.tableWidgetListRepo = QtGui.QTableWidget(repo_manager)
        self.tableWidgetListRepo.setGeometry(QtCore.QRect(10, 20, 441, 241))
        self.tableWidgetListRepo.setObjectName(_fromUtf8("tableWidgetListRepo"))
        self.tableWidgetListRepo.setColumnCount(2)
        self.tableWidgetListRepo.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetListRepo.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetListRepo.setHorizontalHeaderItem(1, item)
        self.progressBarScanning = QtGui.QProgressBar(repo_manager)
        self.progressBarScanning.setGeometry(QtCore.QRect(10, 280, 441, 23))
        self.progressBarScanning.setProperty("value", 0)
        self.progressBarScanning.setObjectName(_fromUtf8("progressBarScanning"))
        self.horizontalLayoutWidget = QtGui.QWidget(repo_manager)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(272, 320, 171, 41))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButtonSave = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.pushButtonSave.setEnabled(False)
        self.pushButtonSave.setObjectName(_fromUtf8("pushButtonSave"))
        self.horizontalLayout.addWidget(self.pushButtonSave)
        self.pushButtonDiscard = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.pushButtonDiscard.setEnabled(False)
        self.pushButtonDiscard.setObjectName(_fromUtf8("pushButtonDiscard"))
        self.horizontalLayout.addWidget(self.pushButtonDiscard)

        self.retranslateUi(repo_manager)
        QtCore.QMetaObject.connectSlotsByName(repo_manager)

    def retranslateUi(self, repo_manager):
        repo_manager.setWindowTitle(_translate("repo_manager", "Git Repositories", None))
        item = self.tableWidgetListRepo.horizontalHeaderItem(0)
        item.setText(_translate("repo_manager", "Monitor", None))
        item = self.tableWidgetListRepo.horizontalHeaderItem(1)
        item.setText(_translate("repo_manager", "Project Path", None))
        self.pushButtonSave.setText(_translate("repo_manager", "Save", None))
        self.pushButtonDiscard.setText(_translate("repo_manager", "Discard", None))

