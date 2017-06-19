import json
import sys
from PyQt4 import QtGui
import os

class Info_review(QtGui.QDialog, QtGui.QWidget):
    def __init__(self, user_info_all):
        super(Info_review, self).__init__()
        self.user_info_all = user_info_all
        try:
            with open("config/dir_list.json", "rb") as dir_lists:
                raw_dir_lst = json.load(dir_lists)
                dir_lists.close()
        except IOError:
            pass

        self.confirmInfoMainLayut = QtGui.QVBoxLayout()

        # --- Table for general information -----
        self.confirmInfoTable = QtGui.QTableWidget()
        if not self.user_info_all["repo_type_github"]:
            self.confirmInfoTable.setRowCount(2)
        else:
            self.confirmInfoTable.setRowCount(8)
        self.confirmInfoTable.setColumnCount(2)

        # --- Table for listing local repository ----
        self.projectMonitorTable = QtGui.QTableWidget()
        self.projectMonitorTable.setRowCount(len(raw_dir_lst))
        self.projectMonitorTable.setColumnCount(1)
        self.projectMonitorTable.setColumnWidth(0, 400)

        # --- Table for listing the days they have checked in the UI ----
        self.dispString = None
        self.labelTopTable = QtGui.QLabel("General Information")
        self.labelTopTableRepoList =QtGui.QLabel("Project Repository being monitored for auto backup.")

        self.buttomButtonLayout = QtGui.QHBoxLayout()
        self.buttomButtonLayout.addStretch(0)

        self.saveButton = QtGui.QPushButton("Confirm and Exit")
        self.saveButton.clicked.connect(self.save_rev_info)

        self.DiscardButton = QtGui.QPushButton("Discard")
        self.DiscardButton.clicked.connect(self.discard_rev_info)

        self.buttomButtonLayout.addWidget(self.saveButton)
        self.buttomButtonLayout.addWidget(self.DiscardButton)

        self.confirmInfoMainLayut.addWidget(self.labelTopTable)
        self.confirmInfoMainLayut.addWidget(self.confirmInfoTable)
        self.confirmInfoMainLayut.addWidget(self.labelTopTableRepoList)
        self.confirmInfoMainLayut.addWidget(self.projectMonitorTable)

        self.confirmInfoTable.setHorizontalHeaderLabels(("Variables", "Value"))

        self.confirmInfoTable.setColumnWidth(1, 300)

        self.confirmInfoTable.setItem(0, 0, QtGui.QTableWidgetItem("User email "))
        self.confirmInfoTable.setItem(0, 1, QtGui.QTableWidgetItem(str(self.user_info_all["email"])))

        self.confirmInfoTable.setItem(1, 0, QtGui.QTableWidgetItem("Root report directory"))
        self.confirmInfoTable.setItem(1, 1, QtGui.QTableWidgetItem(str(self.user_info_all["bckup_dir"])))

        if self.user_info_all["repo_type_github"]:
            self.confirmInfoTable.setItem(2, 0, QtGui.QTableWidgetItem("Git Username"))
            self.confirmInfoTable.setItem(2, 1, QtGui.QTableWidgetItem(str(self.user_info_all["user"])))

            self.confirmInfoTable.setItem(3, 0, QtGui.QTableWidgetItem("Client ID"))
            self.confirmInfoTable.setItem(3, 1, QtGui.QTableWidgetItem(str(self.user_info_all["id"])))

            self.confirmInfoTable.setItem(4, 0, QtGui.QTableWidgetItem("Client Secret"))
            self.confirmInfoTable.setItem(4, 1, QtGui.QTableWidgetItem(str(self.user_info_all["secret"])))

            self.confirmInfoTable.setItem(5, 0, QtGui.QTableWidgetItem("Scheduled time"))
            self.confirmInfoTable.setItem(5, 1, QtGui.QTableWidgetItem(str(self.user_info_all["time"])))

            self.confirmInfoTable.setItem(6, 0, QtGui.QTableWidgetItem("Code matrics project Folder"))
            self.confirmInfoTable.setItem(6, 1, QtGui.QTableWidgetItem(str(self.user_info_all["prj_dir"])))

            self.confirmInfoTable.setItem(7, 0, QtGui.QTableWidgetItem("Programming language, code matrices"))
            self.confirmInfoTable.setItem(7, 1, QtGui.QTableWidgetItem(str(self.user_info_all["pgm_lng"])))

        self.projectMonitorTable.setHorizontalHeaderLabels(["Directory Path"])
        for repo in range(0, len(raw_dir_lst)):
            self.projectMonitorTable.setItem(repo, 0, QtGui.QTableWidgetItem(str(raw_dir_lst[repo])))

        week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        count = 0
        # print json.dumps(self.user_info_all["days"], indent=4)

        for days in range(0, len(week)):
            if self.user_info_all["days"][str(week[days])]:
                count += 1

        self.dispString = "The report will be generated and sent on every: \n"

        if self.user_info_all["days"]["Sunday"]:
            count -= 1
            if count >= 1:
                self.dispString += "Sunday, "
            else:
                self.dispString += "Sunday"

        if self.user_info_all["days"]["Monday"]:
            count -= 1
            if count >= 1:
                self.dispString += "Monday, "
            else:
                self.dispString += " Monday"

        if self.user_info_all["days"]["Tuesday"]:
            count -= 1
            if count >= 1:
                self.dispString += "Tuesday, "
            else:
                self.dispString += " Tuesday"

        if self.user_info_all["days"]["Wednesday"]:
            count -= 1
            if count >= 1:
                self.dispString += "Wednesday, "
            else:
                self.dispString += "Wednesday"

        if self.user_info_all["days"]["Thursday"]:
            count -= 1
            if count >= 1:
                self.dispString += "Thursday, "
            else:
                self.dispString += "Thursday"

        if self.user_info_all["days"]["Friday"]:
            count -= 1
            if count >= 1:
                self.dispString += "Friday, "
            else:
                self.dispString += "Friday "

        if self.user_info_all["days"]["Saturday"]:
            count -= 1
            self.dispString += "Saturday"

        self.dispString += " at " + str(self.user_info_all["time"]) + "."

        self.labelWeekDaysInformation = QtGui.QLabel(self.dispString)
        self.confirmInfoMainLayut.addWidget(self.labelWeekDaysInformation)
        self.confirmInfoMainLayut.addLayout(self.buttomButtonLayout)
        self.setLayout(self.confirmInfoMainLayut)
        self.setGeometry(100, 100, 500, 500)
        self.setFixedSize(500, 500)
        self.setWindowTitle("Confirm inputs")
        # self.setWindowIcon(QtGui.QIcon('github-logo-icon.png'))

    def save_rev_info(self):
        os.system("SCHTASKS /Create /XML config/temco_git_tool.xml /TN TemcoGitReport /F")
        with open("config/config.json", "wb") as save_config:
            json.dump(self.user_info_all, save_config)
            save_config.close()
        sys.exit()
        pass

    def discard_rev_info(self):
        self.close()
        pass
    pass