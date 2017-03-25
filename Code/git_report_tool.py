#!/usr/bin/python
import sys
import json
import datetime
import os

import xml.etree.cElementTree as ET

from PyQt4.QtCore import *
from PyQt4 import QtGui

class ScanPopUp(QtGui.QWidget):
    def __init__(self):
        super(ScanPopUp, self).__init__()

        with open('config/user_infoUI.json', 'rb') as ui_file:
            ui_file_raw = json.load(ui_file)
            ui_file.close()

        print "Searching for git repo on local computer. It may take a while."
        self.git_dirs = [root
                    for root, dirs, files in os.walk(str(ui_file_raw["init_root_dir"]))  # change path here
                    for name in dirs
                    if name.endswith(".git")]
        print "Done with searching of repo !"

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

        self.btn_hbox =QtGui.QHBoxLayout()
        self.btn_hbox.addStretch(1)
        self.btn_hbox.addWidget(self.button_save)
        self.btn_hbox.addWidget(self.button_discard)

        self.mainLayout.addLayout(self.btn_hbox)
        # self.mainLayout.addRows(self.btn_hbox)

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
        self.close()

    def discard_changes(self):
        self.close()
        pass

class Git_UI(QtGui.QWidget):
    get_dir_dialog = None
    def __init__(self):
        super(Git_UI, self).__init__()

        # ----------- Labels ----------
        user_name = QtGui.QLabel('Git Username')
        usr_email = QtGui.QLabel('Email')
        client_id = QtGui.QLabel('Git Client ID')
        client_secret = QtGui.QLabel('Git Client Secret')

        button_apply = QtGui.QPushButton("OK", self)
        button_apply.clicked.connect(self.apply_action)

        button_cancle = QtGui.QPushButton("Cancel", self)
        button_cancle.clicked.connect(self.cancel)

        button_get_init_dir = QtGui.QPushButton("Browse", self)
        button_get_init_dir.clicked.connect(self.get_dir)

        button_scan_repo = QtGui.QPushButton("Scan", self)
        button_scan_repo.clicked.connect(self.scan_action)

        button_open_help = QtGui.QPushButton("Help", self)
        button_open_help.clicked.connect(self.openHelp)

        try:
            with open('config/user_infoUI.json', 'rb') as ui_file:
                ui_raw = json.load(ui_file)
                ui_file.close()
        except:
            pass

        self.user_nameEdit = QtGui.QLineEdit()
        try:
            self.user_nameEdit.setText(ui_raw["username"])
        except:
            pass

        self.client_idEdit = QtGui.QLineEdit()
        try:
            self.client_idEdit.setText(ui_raw["client_id"])
        except:
            pass

        self.client_secretEdit = QtGui.QLineEdit()
        try:
            self.client_secretEdit.setText(ui_raw["client_secret"])
        except:
            pass

        self.usr_emailEdit = QtGui.QLineEdit()
        try:
            self.usr_emailEdit.setText(ui_raw["user_email"])
        except:
            pass

        self.get_init_dirEdit = QtGui.QLineEdit()
        try:
            self.get_init_dirEdit.setText(ui_raw["init_root_dir"])
        except:
            self.get_init_dirEdit.setText("Initial project backup directory!")
            pass

        # ---- Create a form layout -----
        form = QtGui.QFormLayout()

        form.addRow(user_name, self.user_nameEdit)
        form.addRow(usr_email, self.usr_emailEdit)
        form.addRow(client_id, self.client_idEdit)
        form.addRow(client_secret, self.client_secretEdit)
        form.addRow(button_get_init_dir, self.get_init_dirEdit)

        # --- create a box to store two buttons -----
        main_buttons = QtGui.QHBoxLayout()
        main_buttons.addWidget(button_scan_repo)
        main_buttons.addWidget(button_open_help)
        main_buttons.addWidget(button_apply)
        main_buttons.addWidget(button_cancle)
        form.addRow(main_buttons)

         # -- Create a layout for schedular
        setTimeMainLayout = QtGui.QVBoxLayout()
        setTimeLayout  = QtGui.QFormLayout()

        scheduled_time = QtGui.QLabel("Activate at [HH:MM]")

        self.scheduled_timeEdit = QtGui.QLineEdit()
        try:
            time_now = str(datetime.datetime.now().time())
            hr_min = time_now[0:5]
            self.scheduled_timeEdit.setText(hr_min)
        except:
            pass

        # --- Open JSON file ------
        try:
            with open("config/days_chkbox.json", 'rb') as days_chkbox:
                prev_week_days = json.load(days_chkbox)
                print prev_week_days
                days_chkbox.close()
        except:
            pass

        setTimeLayout.addRow(scheduled_time, self.scheduled_timeEdit)

        setWeekGridLayout = QtGui.QGridLayout()

        self.chkbx_Sunday = QtGui.QCheckBox("Sunday")
        try:
            if prev_week_days["Sunday"]:
                self.chkbx_Sunday.setChecked(True)
        except:
            pass

        self.chkbx_Monday = QtGui.QCheckBox("Monday")
        try:
            if prev_week_days["Monday"]:
                self.chkbx_Monday.setChecked(True)
        except:
            pass

        self.chkbx_Tuesday = QtGui.QCheckBox("Tuesday")
        try:
            if prev_week_days["Tuesday"]:
                self.chkbx_Tuesday.setChecked(True)
        except:
            pass

        self.chkbx_Wednesnday = QtGui.QCheckBox("Wednesday")
        try:
            if prev_week_days["Wednesday"]:
                self.chkbx_Wednesnday.setChecked(True)
        except:
            pass

        self.chkbx_Thursday = QtGui.QCheckBox("Thursday")
        try:
            if prev_week_days["Thursday"]:
                self.chkbx_Thursday.setChecked(True)
        except:
            pass

        self.chkbx_Friday = QtGui.QCheckBox("Friday")
        try:
            if prev_week_days["Friday"]:
                self.chkbx_Friday.setChecked(True)
        except:
            pass

        self.chkbx_Saturday = QtGui.QCheckBox("Saturday")
        try:
            if prev_week_days["Saturday"]:
                self.chkbx_Saturday.setChecked(True)
        except:
            pass

        self.button_set_time = QtGui.QPushButton("Save")
        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addWidget(self.button_set_time)
        self.button_set_time.clicked.connect(self.manage_scheduler)
        buttonLayout.addStretch(1)


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
        setTimeMainLayout.addSpacing(5)

        # ----- Create a tab widget -----
        self.tabs =  QtGui.QTabWidget()

        # -------- Create tabs --------
        self.tabMain = QtGui.QWidget()
        self.tabMain.setLayout(form)

        self.tabSch = QtGui.QWidget()
        self.tabSch.setLayout(setTimeMainLayout)


        # -- add tabs ---
        self.tabs.addTab(self.tabMain, "Config User")
        self.tabs.addTab(self.tabSch, "Edit Trigger")

        # -- set title and show ---
        self.tabs.setGeometry(300, 300, 400, 220)
        self.tabs.setFixedSize(400, 220)
        self.tabs.setWindowIcon(QtGui.QIcon('github-logo-icon.png'))
        self.tabs.setWindowTitle('Git report tool: TemcoNepal')
        self.tabs.show()
        pass

    def apply_action(self):
        self.write_json()
        if not self.info_fromUI["username"] or not self.info_fromUI["user_email"] or not self.info_fromUI["client_id"] or not self.info_fromUI["client_secret"] or not self.info_fromUI["scheduled_time"] or not self.info_fromUI["init_root_dir"]:
            self.error_message()
        else:
            # self.manage_scheduler(str(self.scheduled_timeEdit.text()))
            os.system("SCHTASKS /Create /XML config/temco_git_tool.xml /TN TemcoGitReport /F")
            sys.exit()
        pass

    def write_json(self):
        self.info_fromUI = {
            "username":str(self.user_nameEdit.text()),
            "user_email":str(self.usr_emailEdit.text()),
            "client_id":str(self.client_idEdit.text()),
            "client_secret":str(self.client_secretEdit.text()),
            "scheduled_time":str(self.scheduled_timeEdit.text()),
            "init_root_dir":str(self.get_init_dirEdit.text())
        }
        with open("config/user_infoUI.json", "wb") as user_ui_json:
            json.dump(self.info_fromUI, user_ui_json)
            user_ui_json.close()

    def get_dir(self):
        self.get_dir_dialog = QtGui.QFileDialog.getExistingDirectory(None,
                                                                'Select initial directory into which repos are cloned:',
                                                                'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        print "Obtained direcory is : " + str(self.get_dir_dialog)
        self.get_init_dirEdit.setText(str(self.get_dir_dialog))
        pass

    def cancel(self):
        sys.exit()
        pass
    def error_message(self):
        error = QtGui.QErrorMessage()
        error.showMessage("Data fields are empty !")
        error.exec_()
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
            "Sunday":None,
            "Monday":None,
            "Tuesday":None,
            "Wednesday":None,
            "Thursday":None,
            "Friday":None,
            "Saturday":None,
        }

        if self.chkbx_Sunday.isChecked():
            self.week_days["Sunday"] = True
        if self.chkbx_Monday.isChecked():
            self.week_days["Monday"] = True
        if self.chkbx_Tuesday.isChecked():
            self.week_days["Tuesday"] = True
        if self.chkbx_Wednesnday.isChecked():
            self.week_days["Wednesday"] = True
        if self.chkbx_Thursday.isChecked():
            self.week_days["Thursday"] = True
        if self.chkbx_Friday.isChecked():
            self.week_days["Friday"] = True
        if self.chkbx_Saturday.isChecked():
            self.week_days["Saturday"] = True

        # -- Arrange app dir --------------------------
        app_file_to_run = "\\app_backend.exe"
        current_path = str(os.getcwd())
        app_file_to_run = current_path + app_file_to_run
        app_path = current_path + '\\'
        # ----------------------------------------------

        with open("config/days_chkbox.json", 'wb') as days_chkbox:
            json.dump(self.week_days, days_chkbox)
            days_chkbox.close()

        MakeXML(self.week_days, final_date_time, app_file_to_run, app_path)
        pass

    def openHelp(self):
        os.startfile("Manual_git_report_tool.chm")
        pass

    def scan_action(self):
        self.write_json()
        print "Pressed scan !"
        self.PopUp = ScanPopUp()
        self.PopUp.show()
        pass
    pass

class MakeXML:

    def __init__(self, week_days, date_time, command_path, working_dir):

        # -- Accumulate variables ---
        self.week_days = week_days
        self.date_time = date_time
        self.command_path = command_path
        self.working_dir = working_dir

        self.task = ET.Element("Task", version="1.2", xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task")

        # Generate RegistrationInfo
        self.RegistrationInfo = ET.SubElement(self.task, "RegistrationInfo")
        ET.SubElement(self.RegistrationInfo, "Description").text = "This is a task for auto running  git report generator"

        # Generate Triggers
        self.Triggers = ET.SubElement(self.task, "Triggers")
        self.CalendarTrigger = ET.SubElement(self.Triggers, "CalendarTrigger")
        ET.SubElement(self.CalendarTrigger, "StartBoundary").text = str(date_time)
        ET.SubElement(self.CalendarTrigger, "Enabled").text = "true"
        self.ScheduleByWeek = ET.SubElement(self.CalendarTrigger, "ScheduleByWeek")
        DaysOfWeek = ET.SubElement(self.ScheduleByWeek, "DaysOfWeek")

        if(self.week_days["Sunday"]):
            Sunday = ET.SubElement(DaysOfWeek, "Sunday")
            pass

        if(self.week_days["Monday"]):
            Monday = ET.SubElement(DaysOfWeek, "Monday")
            pass

        if(self.week_days["Tuesday"]):
            Tuesday = ET.SubElement(DaysOfWeek, "Tuesday")
            pass

        if self.week_days["Wednesday"]:
            Wednesday = ET.SubElement(DaysOfWeek, "Wednesday")
            pass

        if self.week_days["Thursday"]:
            Thursday = ET.SubElement(DaysOfWeek, "Thursday")
            pass

        if self.week_days["Friday"]:
            Friday = ET.SubElement(DaysOfWeek, "Friday")
            pass

        if self.week_days["Saturday"]:
            Saturday = ET.SubElement(DaysOfWeek, "Saturday")
            pass

        # Generate Principals
        self.Principals = ET.SubElement(self.task, "Principals")
        self.Principal = ET.SubElement(self.Principals, "Principal", id="Author")
        ET.SubElement(self.Principal, "LogonType").text = "InteractiveToken"
        ET.SubElement(self.Principal, "RunLevel").text = "LeastPrivilege"

        # Generate Settings
        self.Settings = ET.SubElement(self.task, "Settings")
        ET.SubElement(self.Settings, "MultipleInstancesPolicy").text = "IgnoreNew"
        ET.SubElement(self.Settings, "DisallowStartIfOnBatteries").text = "false"
        ET.SubElement(self.Settings, "StopIfGoingOnBatteries").text = "true"
        ET.SubElement(self.Settings, "AllowHardTerminate").text = "true"
        ET.SubElement(self.Settings, "StartWhenAvailable").text = "true"
        ET.SubElement(self.Settings, "RunOnlyIfNetworkAvailable").text = "false"

        self.IdleSettings = ET.SubElement(self.Settings, "IdleSettings")
        ET.SubElement(self.IdleSettings, "StopOnIdleEnd").text = "true"
        ET.SubElement(self.IdleSettings, "RestartOnIdle").text = "false"

        ET.SubElement(self.Settings, "AllowStartOnDemand").text = "true"
        ET.SubElement(self.Settings, "Enabled").text = "true"
        ET.SubElement(self.Settings, "Hidden").text = "false"
        ET.SubElement(self.Settings, "RunOnlyIfIdle").text = "false"
        ET.SubElement(self.Settings, "WakeToRun").text = "false"
        ET.SubElement(self.Settings, "ExecutionTimeLimit").text = "P3D"
        # ET.SubElement(self.Settings, "Priority").text = "7"

        self.Actions = ET.SubElement(self.task, "Actions", Context="Author")
        self.Exec = ET.SubElement(self.Actions, "Exec")
        ET.SubElement(self.Exec, "Command").text = self.command_path
        ET.SubElement(self.Exec, "WorkingDirectory").text = self.working_dir

        self.tree = ET.ElementTree(self.task)
        self.tree.write("config/temco_git_tool.xml")
    pass

def main():
    app = QtGui.QApplication(sys.argv)
    ex = Git_UI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
