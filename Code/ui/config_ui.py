# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'config_repos.ui'
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

class Ui_DialogConfRepo(object):
    def setupUi(self, DialogConfRepo):
        DialogConfRepo.setObjectName(_fromUtf8("DialogConfRepo"))
        DialogConfRepo.resize(485, 526)
        self.tableWidgetMon = QtGui.QTableWidget(DialogConfRepo)
        self.tableWidgetMon.setGeometry(QtCore.QRect(10, 30, 441, 261))
        self.tableWidgetMon.setObjectName(_fromUtf8("tableWidgetMon"))
        self.tableWidgetMon.setColumnCount(2)
        self.tableWidgetMon.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetMon.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetMon.setHorizontalHeaderItem(1, item)
        self.labelMon = QtGui.QLabel(DialogConfRepo)
        self.labelMon.setGeometry(QtCore.QRect(14, 10, 151, 16))
        self.labelMon.setObjectName(_fromUtf8("labelMon"))
        self.labelNoMon = QtGui.QLabel(DialogConfRepo)
        self.labelNoMon.setGeometry(QtCore.QRect(10, 300, 231, 16))
        self.labelNoMon.setObjectName(_fromUtf8("labelNoMon"))
        self.tableWidgetNewRepo = QtGui.QTableWidget(DialogConfRepo)
        self.tableWidgetNewRepo.setGeometry(QtCore.QRect(10, 320, 441, 131))
        self.tableWidgetNewRepo.setObjectName(_fromUtf8("tableWidgetNewRepo"))
        self.tableWidgetNewRepo.setColumnCount(2)
        self.tableWidgetNewRepo.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetNewRepo.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetNewRepo.setHorizontalHeaderItem(1, item)
        self.horizontalLayoutWidget = QtGui.QWidget(DialogConfRepo)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(272, 470, 191, 41))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButtonUpdate = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.pushButtonUpdate.setObjectName(_fromUtf8("pushButtonUpdate"))
        self.horizontalLayout.addWidget(self.pushButtonUpdate)
        self.pushButtonDiscard = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.pushButtonDiscard.setObjectName(_fromUtf8("pushButtonDiscard"))
        self.horizontalLayout.addWidget(self.pushButtonDiscard)

        self.retranslateUi(DialogConfRepo)
        QtCore.QMetaObject.connectSlotsByName(DialogConfRepo)

    def retranslateUi(self, DialogConfRepo):
        DialogConfRepo.setWindowTitle(_translate("DialogConfRepo", "Update Repository", None))
        item = self.tableWidgetMon.horizontalHeaderItem(0)
        item.setText(_translate("DialogConfRepo", "Monitored", None))
        item = self.tableWidgetMon.horizontalHeaderItem(1)
        item.setText(_translate("DialogConfRepo", "Repository Path", None))
        self.labelMon.setText(_translate("DialogConfRepo", "Repositories being monitored", None))
        self.labelNoMon.setText(_translate("DialogConfRepo", "Repositories being unmonitored or newly added", None))
        item = self.tableWidgetNewRepo.horizontalHeaderItem(0)
        item.setText(_translate("DialogConfRepo", "Not Monitored", None))
        item = self.tableWidgetNewRepo.horizontalHeaderItem(1)
        item.setText(_translate("DialogConfRepo", "Repository Path", None))
        self.pushButtonUpdate.setText(_translate("DialogConfRepo", "Update", None))
        self.pushButtonDiscard.setText(_translate("DialogConfRepo", "Discard", None))

