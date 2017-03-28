#!/usr/bin/python
import sys
import json
import datetime
import os
import time

from task_creator import *
from review_info import *
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4 import QtGui

class MyThread(QtCore.QThread):
    trigger = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(MyThread, self).__init__(parent)

    def setup(self, thread_no):
        self.thread_no = thread_no

    def run(self):
        time.sleep(5)  # random sleep to imitate working
        self.trigger.emit(self.thread_no)


class ScanPopUp(QtGui.QWidget):
    def __init__(self, git_dirs, scn_btn):
        super(ScanPopUp, self).__init__()
        self.git_dirs = git_dirs
        self.scan_btn = scn_btn
        # main layout
        self.mainLayout = QtGui.QVBoxLayout()
        # add table inside main layout
        self.checks = []
        self.table = QtGui.QTableWidget()
        self.table.setRowCount(len(self.git_dirs))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(("Monitor", "Repository path"))
        for col in range(0, 2):
            for row in range(0, len(self.git_dirs)):
                self.table.setItem(row, 1, QtGui.QTableWidgetItem(self.git_dirs[row]))
                self.table.setColumnWidth(1, 300)

                # self.table.insertRow(row)
                checkItem = QtGui.QTableWidgetItem()
                checkItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                checkItem.setCheckState(Qt.Checked)
                checkItem.setTextAlignment(Qt.AlignAbsolute)
                self.table.setItem(row, 0, checkItem)

                self.table.setColumnWidth(0, 50)

        self.mainLayout.addWidget(self.table)

        self.button_save = QtGui.QPushButton("Save", self)
        self.button_discard = QtGui.QPushButton("Discard", self)
        self.button_discard.clicked.connect(self.discard_changes)

        QObject.connect(self.button_save, SIGNAL("clicked()"), self.save_changes)

        self.btn_hbox = QtGui.QHBoxLayout()
        self.btn_hbox.addStretch(0)
        self.btn_hbox.addWidget(self.button_save)
        self.btn_hbox.addWidget(self.button_discard)
        self.mainLayout.addLayout(self.btn_hbox)

        self.setLayout(self.mainLayout)
        self.setGeometry(100, 100, 400, 400)
        self.setWindowTitle("List of local repository")
        self.setWindowIcon(QtGui.QIcon("github-logo-icon.png"))
        # self.setFixedWidth(400)
        # self.setFixedHeight(400)

    def save_changes(self):
        checked_dir_list = [None]
        checked_dir_list_json = [None]
        for i in range(self.table.rowCount()):
            if self.table.item(i, 0).checkState() == Qt.Checked:
                checked_dir_list.append((self.table.item(i, 1)).text())

        for dir in range(0, len(checked_dir_list)):
            if checked_dir_list[dir]:
                checked_dir_list_json.append(str(checked_dir_list[dir]))

        del checked_dir_list_json[0]

        del checked_dir_list

        with open("config/dir_list.json", "wb") as dir_list_file:
            json.dump(checked_dir_list_json, dir_list_file)
            dir_list_file.close()
        del checked_dir_list_json
        self.scan_btn.setDisabled(False)
        self.close()

    def discard_changes(self):
        self.scan_btn.setDisabled(False)
        self.close()
        pass

class Git_UI(QtGui.QWidget):
    get_dir_dialog = None

    def __init__(self):
        super(Git_UI, self).__init__()

        try:
            with open('config/config.json', 'rb') as config_file:
                self.config_raw = json.load(config_file)
                config_file.close()
        except IOError: # If file not found make a dummy dictonary
            self.config_raw = {
                    "user": None,
                    "email": None,
                    "id": None,
                    "secret": None,
                    "time": None,
                    "bckup_dir": None,
                    "prj_dir": None,
                    "pgm_lng": None,
                    "days": {None}
                }
            pass
        # ----------- Labels ----------
        user_name = QtGui.QLabel('Git Username')
        usr_email = QtGui.QLabel('Email')
        client_id = QtGui.QLabel('Git Client ID')
        client_secret = QtGui.QLabel('Git Client Secret')

        button_apply = QtGui.QPushButton("OK", self)
        button_apply.clicked.connect(self.apply_action)

        button_cancle = QtGui.QPushButton("Exit", self)
        button_cancle.clicked.connect(self.cancel)

        button_get_init_dir = QtGui.QPushButton("Browse", self)
        button_get_init_dir.clicked.connect(self.get_dir)

        self.button_scan_repo = QtGui.QPushButton("Scan", self)
        self.button_scan_repo.clicked.connect(self.scan_action)

        button_open_help = QtGui.QPushButton("Help", self)
        button_open_help.clicked.connect(self.openHelp)

        # self.showProgress = QtGui.QProgressBar()
        self.show_lable = QtGui.QLabel()

        self.user_nameEdit = QtGui.QLineEdit()
        try:
            self.user_nameEdit.setText(self.config_raw["user"])
        except:
            pass

        self.client_idEdit = QtGui.QLineEdit()
        try:
            self.client_idEdit.setText(self.config_raw["id"])
        except:
            pass

        self.client_secretEdit = QtGui.QLineEdit()
        try:
            self.client_secretEdit.setText(self.config_raw["secret"])
        except:
            pass

        self.usr_emailEdit = QtGui.QLineEdit()
        try:
            self.usr_emailEdit.setText(self.config_raw["email"])
        except:
            pass

        self.get_init_dirEdit = QtGui.QLineEdit()
        try:
            self.get_init_dirEdit.setText(self.config_raw["bckup_dir"])
        except:
            self.get_init_dirEdit.setText("Initial project backup directory!")
            pass

        # ---- Create Layout for main tab --
        ui_mainLayout = QtGui.QVBoxLayout()
        form = QtGui.QFormLayout()

        form.addRow(user_name, self.user_nameEdit)
        form.addRow(usr_email, self.usr_emailEdit)
        form.addRow(client_id, self.client_idEdit)
        form.addRow(client_secret, self.client_secretEdit)
        form.addRow(button_get_init_dir, self.get_init_dirEdit)

        # --- create a box to store two buttons -----
        main_buttons = QtGui.QHBoxLayout()
        main_buttons.addWidget(self.button_scan_repo)
        main_buttons.addWidget(button_open_help)
        main_buttons.addWidget(button_apply)
        main_buttons.addWidget(button_cancle)
        form.addRow(main_buttons)
        ui_mainLayout.addLayout(form)
        # ui_mainLayout.addWidget(self.showProgress)
        ui_mainLayout.addWidget(self.show_lable)

        # -- Create a layout for schedular
        setTimeMainLayout = QtGui.QVBoxLayout()
        setTimeLayout = QtGui.QFormLayout()

        scheduled_time = QtGui.QLabel("Activate at [HH:MM]")

        self.scheduled_timeEdit = QtGui.QLineEdit()
        try:
            time_now = str(datetime.datetime.now().time())
            hr_min = time_now[0:5]
            self.scheduled_timeEdit.setText(hr_min)
        except:
            pass

        setTimeLayout.addRow(scheduled_time, self.scheduled_timeEdit)

        setWeekGridLayout = QtGui.QGridLayout()

        # --- Open JSON file ------
        self.chkbx_Sunday = QtGui.QCheckBox("Sunday")
        try:
            if self.config_raw["days"]["Sunday"]:
                self.chkbx_Sunday.setChecked(True)
        except:
            pass

        self.chkbx_Monday = QtGui.QCheckBox("Monday")
        try:
            if self.config_raw["days"]["Monday"]:
                self.chkbx_Monday.setChecked(True)
        except:
            pass

        self.chkbx_Tuesday = QtGui.QCheckBox("Tuesday")
        try:
            if self.config_raw["days"]["Tuesday"]:
                self.chkbx_Tuesday.setChecked(True)
        except:
            pass

        self.chkbx_Wednesnday = QtGui.QCheckBox("Wednesday")
        try:
            if self.config_raw["days"]["Wednesday"]:
                self.chkbx_Wednesnday.setChecked(True)
        except:
            pass

        self.chkbx_Thursday = QtGui.QCheckBox("Thursday")
        try:
            if self.config_raw["days"]["Thursday"]:
                self.chkbx_Thursday.setChecked(True)
        except:
            pass

        self.chkbx_Friday = QtGui.QCheckBox("Friday")
        try:
            if self.config_raw["days"]["Friday"]:
                self.chkbx_Friday.setChecked(True)
        except:
            pass

        self.chkbx_Saturday = QtGui.QCheckBox("Saturday")
        try:
            if self.config_raw["days"]["Saturday"]:
                self.chkbx_Saturday.setChecked(True)
        except:
            pass

        buttonLayout = QtGui.QHBoxLayout()
        setWeekGridLayout.addWidget(self.chkbx_Sunday, 1, 0)
        setWeekGridLayout.addWidget(self.chkbx_Monday, 1, 1)
        setWeekGridLayout.addWidget(self.chkbx_Tuesday, 1, 2)
        setWeekGridLayout.addWidget(self.chkbx_Wednesnday, 1, 3)

        setWeekGridLayout.addWidget(self.chkbx_Thursday, 2, 0)
        setWeekGridLayout.addWidget(self.chkbx_Friday, 2, 1)
        setWeekGridLayout.addWidget(self.chkbx_Saturday, 2, 2)
        labelWidget = QtGui.QLabel("Recur every week on: ")

        setTimeMainLayout.addLayout(setTimeLayout)
        setTimeMainLayout.addWidget(labelWidget)
        setTimeMainLayout.addLayout(setWeekGridLayout)

        setTimeMainLayout.addLayout(buttonLayout)
        setTimeMainLayout.addStretch(0)

        # --- Layout for Source monitor setup ---
        self.setSMMainLayout = QtGui.QVBoxLayout()
        self.setSMLayout = QtGui.QFormLayout()
        self.setCombBox = QtGui.QHBoxLayout()
        self.getProjectDir = QtGui.QPushButton("Browse")
        self.getProjectDir.clicked.connect(self.getScrDir)

        self.getProjectDirEdit = QtGui.QLineEdit()

        try:
                if self.config_raw["prj_dir"]:
                    self.getProjectDirEdit.setText(str(self.config_raw["prj_dir"]))
                else:
                    self.getProjectDirEdit.setText("Browse for a project source directory.")
        except:
            self.getProjectDirEdit.setText("Browse for a project source directory.")
            pass

        self.setLanguateLebel = QtGui.QLabel("Select Language :")
        self.pgm_lngs = ["C", "C++", "C#", "Java", "VB.Net", "Delphi", "HTML", "Visual Basic"]
        self.chooseLangueage = QtGui.QComboBox()
        self.chooseLangueage.addItems(self.pgm_lngs)
        self.setSMLayout.addRow(self.getProjectDir, self.getProjectDirEdit)
        self.setSMLayout.addRow(self.setLanguateLebel, self.chooseLangueage)
        self.setSMMainLayout.addLayout(self.setSMLayout)
        self.setSMMainLayout.addLayout(self.setCombBox)
        self.setSMMainLayout.addStretch(1)

        try:
            for inx in range(0, len(self.pgm_lngs)):
                if self.config_raw["pgm_lng"] == self.pgm_lngs[inx]:
                    break
            self.chooseLangueage.setCurrentIndex(inx)
        except:
            pass

        # ----- Create a tab widget -----
        self.tabs = QtGui.QTabWidget()

        # -------- Create tabs --------
        # -- Main window tab ----
        self.tabMain = QtGui.QWidget()
        self.tabMain.setLayout(ui_mainLayout)

        # -- Edit Trigger Tab ------
        self.tabSch = QtGui.QWidget()
        self.tabSch.setLayout(setTimeMainLayout)

        # -- Source Monitor Tab -----
        self.tabSM = QtGui.QWidget()
        self.tabSM.setLayout(self.setSMMainLayout)

        # -- add tabs ---
        self.tabs.addTab(self.tabMain, "Config User")
        self.tabs.addTab(self.tabSch, "Edit Trigger")
        self.tabs.addTab(self.tabSM, "Code Matrics")

        # -- set title and show ---
        self.tabs.setGeometry(300, 300, 400, 240)
        # self.tabs.setFixedSize(400, 240)
        self.tabs.setWindowIcon(QtGui.QIcon('github-logo-icon.png'))
        self.tabs.setWindowTitle('Git report tool: TemcoNepal')
        self.tabs.show()
        pass

    def apply_action(self):
        self.manage_scheduler()
        if not self.user_nameEdit.text() or not self.usr_emailEdit.text() or not self.client_idEdit.text() or not \
                self.client_secretEdit.text() or not self.scheduled_timeEdit.text() or not \
                self.get_init_dirEdit.text() or not ':' in self.get_init_dirEdit.text() or not \
                self.getProjectDirEdit.text() or not ':' in self.getProjectDirEdit.text():
            self.error_message()

        else:
            dict_all_info = {
                "user": str(self.user_nameEdit.text()),
                "email": str(self.usr_emailEdit.text()),
                "id": str(self.client_idEdit.text()),
                "secret": str(self.client_secretEdit.text()),
                "time": str(self.scheduled_timeEdit.text()),
                "bckup_dir": str(self.get_init_dirEdit.text()),
                "prj_dir": str(self.getProjectDirEdit.text()),
                "pgm_lng": str(self.chooseLangueage.currentText()),
                "days": self.week_days
            }
            # print dict_all_info
            try:
                self.reviewInfo = Info_review(dict_all_info)
                self.reviewInfo.show()
            except UnboundLocalError:
                self.error_not_scanned()
                pass

    def get_dir(self):
        self.get_dir_dialog = QtGui.QFileDialog.getExistingDirectory(None,
                                                                     'Select initial directory into which repos are cloned:',
                                                                     'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        self.get_init_dirEdit.setText(str(self.get_dir_dialog))
        pass

    def cancel(self):
        sys.exit()
        pass

    def error_message(self):
        error = QtGui.QErrorMessage()
        error.setWindowTitle("Invalid data inputs!")
        error.setWindowIcon(QtGui.QIcon("github-logo-icon.png"))
        if not '@' in self.usr_emailEdit.text() or not "." in self.usr_emailEdit.text():
            error.showMessage("Invalid email!")
        elif not ':' in self.get_init_dirEdit.text():
            error.showMessage("Please input appropriate an initial backup directory, scan and save!")
        elif not ':' in self.getProjectDirEdit.text():
            error.showMessage("Please browse a appropriate project directory for Code Metrics evaluation!")
        else:
            error.showMessage("Data fields are empty!")
        error.exec_()
        pass

    def error_msg_scan(self):
        error_scan = QtGui.QErrorMessage()
        error_scan.setWindowTitle("Invalid data inputs!")
        error_scan.setWindowIcon(QtGui.QIcon("github-logo-icon.png"))
        error_scan.showMessage("Please browse for appropriate backup directory first!")
        error_scan.exec_()
    pass

    def error_not_scanned(self):
        error_not_scnd = QtGui.QErrorMessage()
        error_not_scnd.setWindowTitle("Not scanned for repository !")
        error_not_scnd.setWindowIcon(QtGui.QIcon("github-logo-icon.png"))
        error_not_scnd.showMessage("Please scan for local backup git repositories save!")
        error_not_scnd.exec_()
        pass

    def manage_scheduler(self):

        # -- Get current date ------------------
        time = self.scheduled_timeEdit.text()
        time = time + ":00"
        time = time + ".000"
        current_date = str(datetime.datetime.now().date())
        final_date_time = current_date + "T" + time
        # ---------------------------------------

        # ---------- arrange repetation ---------
        self.week_days = {
            "Sunday": None,
            "Monday": None,
            "Tuesday": None,
            "Wednesday": None,
            "Thursday": None,
            "Friday": None,
            "Saturday": None,
        }
        self.if_no_days_set = 0
        if self.chkbx_Sunday.isChecked():
            self.week_days["Sunday"] = True
            self.if_no_days_set += 1
        if self.chkbx_Monday.isChecked():
            self.week_days["Monday"] = True
            self.if_no_days_set += 1
        if self.chkbx_Tuesday.isChecked():
            self.week_days["Tuesday"] = True
            self.if_no_days_set += 1
        if self.chkbx_Wednesnday.isChecked():
            self.week_days["Wednesday"] = True
            self.if_no_days_set += 1
        if self.chkbx_Thursday.isChecked():
            self.week_days["Thursday"] = True
            self.if_no_days_set += 1
        if self.chkbx_Friday.isChecked():
            self.week_days["Friday"] = True
            self.if_no_days_set += 1
        if self.chkbx_Saturday.isChecked():
            self.week_days["Saturday"] = True
            self.if_no_days_set += 1

        if not self.if_no_days_set:
            self.chkbx_Monday.setChecked(True)
            self.week_days["Monday"] = True

        # -- Arrange app dir --------------------------
        app_file_to_run = "\\app_backend.exe"
        # app_file_to_run = "\\trigger_backend.bat"
        current_path = str(os.getcwd())
        app_file_to_run = current_path + app_file_to_run
        app_path = current_path + '\\'
        # ----------------------------------------------

        MakeXMLSCH(self.week_days, final_date_time, app_file_to_run, app_path)
        pass

    def openHelp(self):
        os.startfile("Manual_git_report_tool.chm")
        pass

    def scan_action(self):
        self.button_scan_repo.setDisabled(True)
        if not ':' in self.get_init_dirEdit.text():
            self.error_msg_scan()
        else:
            print "Searching for git repo on local computer. It may take a while."

            git_dir = []
            for root, dirs, files in os.walk(str(self.get_init_dirEdit.text())):
                for name in dirs:
                    if name.endswith(".git"):
                        git_dir.append(root)

                        print "searching on " + root
                        root = root[len(str(self.get_init_dirEdit.text())):]

                        myDirVar = str(self.get_init_dirEdit.text()).split("\\")

                        myDirStr = myDirVar[len(myDirVar) - 1]

                        self.show_lable.wordWrap()
                        self.show_lable.setText(str("Searching: ~" + "\\" + str(myDirStr) + str(root)))
                        QtCore.QCoreApplication.processEvents()
            # print "Done with searching of repo !"
            self.show_lable.setText("Done searching for available repositories!")
            # print git_dir
            self.PopUp = ScanPopUp(git_dir, self.button_scan_repo)
            self.PopUp.show()
            pass
    pass

    def getScrDir(self):
        get_dir = QtGui.QFileDialog.getExistingDirectory(None,
                                                         'Select source file containing directory',
                                                         # 'G:\\Study\\ELECTRONICS PROJECTS\\CPC\\project\\mega32_20x4_cpc_fm\\mega32_20x4_cpc_fm', QtGui.QFileDialog.ShowDirsOnly)
                                                         'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        # print "Obtained direcory is : " + str(get_dir)
        self.getProjectDirEdit.setText(str(get_dir))
        pass

def main():
    app = QtGui.QApplication(sys.argv)
    ex = Git_UI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
