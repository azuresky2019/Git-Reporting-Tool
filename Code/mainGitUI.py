import time
import datetime
import os
from subprocess import call, STDOUT

from PyQt4 import QtCore
from PyQt4.QtCore import Qt

from review_info import *
from task_creator import *
import git

sys.path.insert(0, "ui/")

from UIGit import Ui_MainWindowGitUiI
from repo_manage import Ui_repo_manager
from about_ui import Ui_DialogAbout
from error_dialogueUi import Ui_ErrorDialogue
from config_ui import Ui_DialogConfRepo

flag_done_scan = False

class gitDirThread(QtCore.QThread):

    def __init__(self, dir_backup):
        QtCore.QThread.__init__(self)
        self.init_path = str(dir_backup)

    def __del__(self):
        self.wait()

    def is_git_repo(self, path):
        try:
            _ = git.Repo(path).git_dir
            return True
        except git.exc.InvalidGitRepositoryError:
            return False

    def run(self):

        list_dirs = []
        for name in os.listdir(self.init_path):
            path = os.path.join(self.init_path, name)
            if not os.path.isfile(path):
                list_dirs.append(path)

        path_now = os.getcwd()
        all_dirs = len(list_dirs)

        for repo in range(0, all_dirs):

            last_dir_name = list_dirs[repo].split('\\')[-1]     # omit hidden directory

            if not last_dir_name[0] == '.':
                self.emit(QtCore.SIGNAL("tbl_val(QString)"), list_dirs[repo])
                time.sleep(0.1)

        # self.emit(QtCore.SIGNAL("inc_num(int)"), 100)
        self.emit(QtCore.SIGNAL("finished(bool)"), True)
        os.chdir(path_now)

class RepoManager(QtGui.QDialog, QtGui.QWidget):

    def __init__(self, backup_dir):
        QtGui.QDialog.__init__(self, parent=None)

        self.backup_dir = str(backup_dir)

        self.dialog_repoManager = Ui_DialogConfRepo()
        self.dialog_repoManager.setupUi(self)
        self.setFixedSize(485, 526)

        self.dialog_repoManager.pushButtonDiscard.setEnabled(False)
        self.dialog_repoManager.pushButtonUpdate.setEnabled(False)

        self.connect(self.dialog_repoManager.pushButtonUpdate, QtCore.SIGNAL("clicked()"), self.on_save)
        self.connect(self.dialog_repoManager.pushButtonDiscard, QtCore.SIGNAL("clicked()"), self.close)

        self.dialog_repoManager.tableWidgetMon.setRowCount(0)
        self.dialog_repoManager.tableWidgetNewRepo.setRowCount(0)

        try:
            with open("config/dir_list.json", "rb") as dir_list_file:
                self.current_dir_list = json.load(dir_list_file)
                dir_list_file.close()

            with open("config/config.json", "rb") as config_file:
                self.savedConfig = json.load(config_file)
                self.savedInitDir = self.savedConfig["bckup_dir"]
                config_file.close()
        except:
            self.current_dir_list = []
            self.savedInitDir = []
            pass

        self.gitThread = gitDirThread(self.backup_dir)
        self.gitThread.start()

        self.connect(self.gitThread, QtCore.SIGNAL("tbl_val(QString)"), self.draw_table)

        self.connect(self.gitThread, QtCore.SIGNAL("finished(bool)"), self.scan_finished)

    def draw_table(self, table_item):
        if self.savedInitDir != self.backup_dir:

            row_position = self.dialog_repoManager.tableWidgetMon.rowCount()
            self.dialog_repoManager.tableWidgetMon.insertRow(row_position)

            self.dialog_repoManager.tableWidgetMon.setColumnWidth(1, 430)
            self.dialog_repoManager.tableWidgetMon.setItem(row_position, 1, QtGui.QTableWidgetItem(table_item))

            checkItem = QtGui.QTableWidgetItem()
            checkItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            checkItem.setCheckState(Qt.Checked)
            self.dialog_repoManager.tableWidgetMon.setItem(row_position, 0, checkItem)
            self.dialog_repoManager.tableWidgetMon.setColumnWidth(0, 50)

        else:
            if str(table_item) in self.current_dir_list:
                row_position = self.dialog_repoManager.tableWidgetMon.rowCount()
                self.dialog_repoManager.tableWidgetMon.insertRow(row_position)

                self.dialog_repoManager.tableWidgetMon.setColumnWidth(1, 430)
                self.dialog_repoManager.tableWidgetMon.setItem(row_position, 1, QtGui.QTableWidgetItem(table_item))

                checkItem = QtGui.QTableWidgetItem()
                checkItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                checkItem.setCheckState(Qt.Checked)
                self.dialog_repoManager.tableWidgetMon.setItem(row_position, 0, checkItem)
                self.dialog_repoManager.tableWidgetMon.setColumnWidth(0, 50)

            else:
                row_position = self.dialog_repoManager.tableWidgetNewRepo.rowCount()
                self.dialog_repoManager.tableWidgetNewRepo.insertRow(row_position)

                self.dialog_repoManager.tableWidgetNewRepo.setColumnWidth(1, 430)
                self.dialog_repoManager.tableWidgetNewRepo.setItem(row_position, 1, QtGui.QTableWidgetItem(table_item))

                checkItem = QtGui.QTableWidgetItem()
                checkItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                checkItem.setCheckState(Qt.Unchecked)
                self.dialog_repoManager.tableWidgetNewRepo.setItem(row_position, 0, checkItem)
                self.dialog_repoManager.tableWidgetNewRepo.setColumnWidth(0, 50)

    # def rise_pgrs_bar(self, prgVal):
    #     self.dialog_repoManager.progressBarScanning.setValue(prgVal)
    #     pass

    def scan_finished(self):
        print "Finished scanning !"
        self.gitThread.terminate()
        self.dialog_repoManager.pushButtonDiscard.setEnabled(True)
        self.dialog_repoManager.pushButtonUpdate.setEnabled(True)

    def on_save(self):
        checked_dir_list = []
        for i in range(self.dialog_repoManager.tableWidgetMon.rowCount()):
            if self.dialog_repoManager.tableWidgetMon.item(i, 0).checkState() == Qt.Checked:
                checked_dir_list.append(str((self.dialog_repoManager.tableWidgetMon.item(i, 1)).text()))

        for i in range(self.dialog_repoManager.tableWidgetNewRepo.rowCount()):
            if self.dialog_repoManager.tableWidgetNewRepo.item(i, 0).checkState() == Qt.Checked:
                checked_dir_list.append(str((self.dialog_repoManager.tableWidgetNewRepo.item(i, 1)).text()))

        # print json.dumps(checked_dir_list, indent=4)
        # print len(checked_dir_list)

        with open("config/dir_list.json", "wb") as dir_list_file:
            json.dump(checked_dir_list, dir_list_file)
            dir_list_file.close()

        del checked_dir_list
        self.emit(QtCore.SIGNAL("en_ok(bool)"), True)

        # print self.gitThread.isRunning()
        # self.gitThread.terminate()
        # print self.gitThread.isRunning()

        self.close()
        pass

class About(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.dialog_about = Ui_DialogAbout()
        self.dialog_about.setupUi(self)
        self.setFixedSize(307, 123)

        self.connect(self.dialog_about.pushButtonOk, QtCore.SIGNAL("clicked()"), self.close)

class ErrorMsg(QtGui.QDialog):
    def __init__(self, error_msg):
        QtGui.QDialog.__init__(self)
        self.dialogue_error = Ui_ErrorDialogue()
        self.dialogue_error.setupUi(self)
        self.setFixedSize(306, 161)

        self.error_msg = error_msg
        self.dialogue_error.textBrowser.setText(self.error_msg)

        self.connect(self.dialogue_error.pushButton, QtCore.SIGNAL("clicked()"), self.close)

class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        # This is always the same
        self.ui = Ui_MainWindowGitUiI()
        # self.setWindowIcon(QtGui.QIcon("rcs/github-logo-icon.png"))
        self.setFixedSize(500, 470)
        self.ui.setupUi(self)

        self.ui.lineEditClientId.setEchoMode(QtGui.QLineEdit.Password)
        self.ui.lineEditClientSecret.setEchoMode(QtGui.QLineEdit.Password)

        self.init_backup_dir = None
        self.flag_repotype_github = False
        self.week_days = {
            "Sunday": None,
            "Monday": None,
            "Tuesday": None,
            "Wednesday": None,
            "Thursday": None,
            "Friday": None,
            "Saturday": None,
        }

        self.connect_menu_action()
        self.init_form()

        self.connect(self.ui.radioButtonGithubTypeRepo, QtCore.SIGNAL("clicked()"), self.on_repotype_github)
        self.connect(self.ui.radioButtonLocalTypeRepo, QtCore.SIGNAL("clicked()"), self.on_repotype_local)

        self.connect(self.ui.pushButtonBrowseBackup, QtCore.SIGNAL("clicked()"), self.on_init_dir_browse)

        self.connect(self.ui.pushButtonExit, QtCore.SIGNAL("clicked()"), self.on_exit)
        self.connect(self.ui.pushButtonOK, QtCore.SIGNAL("clicked()"), self.on_okay)

        self.connect(self.ui.lineEditBackupDir, QtCore.SIGNAL("textChanged(QString)"), self.check_dir)

        self.connect(self.ui.pushButtonManageRepo, QtCore.SIGNAL("clicked()"), self.manage_repo)

        self.ui.checkBoxMonday.setChecked(True) # Set monday checked initially
        # self.connect(self.ui.pushButtonManageRepo, QtCore.SIGNAL("clicked()"), self.update_repo)

        self.check_dir()

    def check_dir(self):
        if self.ui.lineEditBackupDir.text() and ('\\' in self.ui.lineEditBackupDir.text() and (':' in self.ui.lineEditBackupDir.text())):
            self.ui.pushButtonManageRepo.setEnabled(True)
        else:
            self.ui.pushButtonManageRepo.setEnabled(False)

    def on_repotype_github(self):
        self.ui.labelUserName.setEnabled(True)
        self.ui.lineEditUserName.setEnabled(True)

        self.ui.labelClientID.setEnabled(True)
        self.ui.lineEditClientId.setEnabled(True)

        self.ui.labelClientSecret.setEnabled(True)
        self.ui.lineEditClientSecret.setEnabled(True)

        self.ui.groupBoxInitialBackup.setEnabled(False)

        self.ui.pushButtonOK.setEnabled(True)
        self.ui.pushButtonManageRepo.setEnabled(False)

        self.flag_repotype_github = True
        pass

    def on_repotype_local(self):
        self.ui.labelUserName.setEnabled(False)
        self.ui.lineEditUserName.setEnabled(False)

        self.ui.labelClientID.setEnabled(False)
        self.ui.lineEditClientId.setEnabled(False)

        self.ui.labelClientSecret.setEnabled(False)
        self.ui.lineEditClientSecret.setEnabled(False)

        self.ui.groupBoxInitialBackup.setEnabled(True)

        self.ui.pushButtonOK.setEnabled(False)

        self.check_dir()

        self.flag_repotype_github = False
        pass

    def on_init_dir_browse(self):
        self.init_backup_dir = QtGui.QFileDialog.getExistingDirectory(None,
                                                         'Select initial backup directory.',
                                                         '/', QtGui.QFileDialog.ShowDirsOnly)
        self.ui.lineEditBackupDir.setText(str(self.init_backup_dir))
        pass

    def connect_menu_action(self):
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionManageRpo.triggered.connect(self.manage_repo)
        self.ui.actionManual.triggered.connect(self.on_manual)
        self.ui.actionAbout.triggered.connect(self.on_about)
        pass

    def manage_repo(self):
        self.repo_manage = RepoManager(self.ui.lineEditBackupDir.text())
        self.connect(self.repo_manage, QtCore.SIGNAL("en_ok(bool)"), self.en_okay)
        self.repo_manage.show()
        self.repo_manage.exec_()
        pass

    def on_manual(self):
        os.startfile("Manual_git_report_tool.chm")
        pass

    def on_about(self):
        tool_about = About()
        tool_about.show()
        tool_about.exec_()
        pass

    def en_okay(self):
        self.ui.pushButtonOK.setEnabled(True)
        pass

    def on_okay(self):

        self.manage_scheduler()

        if not self.flag_repotype_github:     # On local repository
            if not self.ui.lineEditEmail.text() or not '@' in self.ui.lineEditEmail.text() \
                    or not '.' in self.ui.lineEditEmail.text():
                error_no_proper_info = ErrorMsg(
                    "Please enter valid email address!")
                error_no_proper_info.show()
                error_no_proper_info.exec_()
            elif not self.ui.lineEditBackupDir.text() or not ':' in self.ui.lineEditBackupDir.text() \
                    or not '\\' in self.ui.lineEditBackupDir.text():
                error_no_proper_info = ErrorMsg(
                    "Please browse for appropriate backup directory! ")
                error_no_proper_info.show()
                error_no_proper_info.exec_()

            else:
                self.acc_info()
                print "Information Okay, Non Github"

        else:                               # On remote repository
            if not self.ui.lineEditUserName.text() or not self.ui.lineEditEmail.text() \
                    or not '@' in self.ui.lineEditEmail.text() or not '.' in self.ui.lineEditEmail.text() \
                    or not self.ui.lineEditClientId.text() or not self.ui.lineEditClientSecret.text() \
                    or not self.ui.lineEditBackupDir.text() or not ':' in self.ui.lineEditBackupDir.text():
                error_no_proper_info = ErrorMsg("Please fill appropriate information!")
                error_no_proper_info.show()
                error_no_proper_info.exec_()

            else:
                print "Information Okay, Github"
                self.acc_info()
        pass

    def on_exit(self):
        sys.exit()
        pass

    def init_form(self):
        try:
            with open('config/config.json', 'rb') as config_file:
                self.config_raw = json.load(config_file)
                config_file.close()
        except IOError:  # If file not found make a dummy dictonary
            self.config_raw = {
                "user": None,
                "email": None,
                "id": None,
                "secret": None,
                "time": None,
                "bckup_dir": None,
                "prj_dir": None,
                "pgm_lng": None,
                "days": {None},
                "repo_type_github":None,
                "history": None,
            }
            pass

        # ------------------ Config user information -----------------
        try:
            self.ui.lineEditBackupDir.setText(self.config_raw["bckup_dir"])
            self.ui.lineEditUserName.setText(self.config_raw["user"])
            self.ui.lineEditEmail.setText(self.config_raw["email"])
            self.ui.lineEditClientId.setText(self.config_raw["id"])
            self.ui.lineEditClientSecret.setText(self.config_raw["secret"])
            self.ui.spinBoxHistory.setValue(self.config_raw["history"])
        except:
            pass

        # --------------- Set current time ---------------------
        time_now = datetime.datetime.now().time()
        time_now_qt = QtCore.QTime(time_now.hour, time_now.minute)
        self.ui.timeEditSetTrig.setTime(time_now_qt)

        # ---------------------- Set day ------------------------
        try:
            if self.config_raw["days"]["Sunday"]:
                self.ui.checkBoxSunday.setChecked(True)
            else:
                self.ui.checkBoxSunday.setChecked(False)
        except:
            pass
        try:
            if self.config_raw["days"]["Monday"]:
                self.ui.checkBoxMonday.setChecked(True)
            else:
                self.ui.checkBoxMonday.setChecked(False)
        except:
            pass
        try:
            if self.config_raw["days"]["Tuesday"]:
                self.ui.checkBoxTuesday.setChecked(True)
            else:
                self.ui.checkBoxTuesday.setChecked(False)
        except:
            pass
        try:
            if self.config_raw["days"]["Wednesday"]:
                self.ui.checkBoxWed.setChecked(True)
            else:
                self.ui.checkBoxWed.setChecked(False)
        except:
            pass
        try:
            if self.config_raw["days"]["Thursday"]:
                self.ui.checkBoxThursday.setChecked(True)
            else:
                self.ui.checkBoxThursday.setChecked(False)
        except:
            pass
        try:
            if self.config_raw["days"]["Friday"]:
                self.ui.checkBoxFriday.setChecked(True)
            else:
                self.ui.checkBoxFriday.setChecked(True)
        except:
            pass
        try:
            if self.config_raw["days"]["Saturday"]:
                self.ui.checkBoxSat.setChecked(True)
            else:
                self.ui.checkBoxSat.setChecked(False)
        except:
            pass
        pass

    def manage_scheduler(self):

        # -- Get current date ------------------
        getTime = self.ui.timeEditSetTrig.time()
        time = str(getTime.hour()).zfill(2) + ':' + str(getTime.minute()).zfill(2)
        time = time + ":00"
        time = time + ".000"
        current_date = str(datetime.datetime.now().date())
        final_date_time = current_date + "T" + time
        # ---------------------------------------

        # ---------- arrange repetation ---------
        self.if_no_days_set = 0
        if self.ui.checkBoxSunday.isChecked():
            self.week_days["Sunday"] = True
        else:
            self.week_days["Sunday"] = False

        if self.ui.checkBoxMonday.isChecked():
            self.week_days["Monday"] = True
        else:
            self.week_days["Monday"] = False

        if self.ui.checkBoxTuesday.isChecked():
            self.week_days["Tuesday"] = True
        else:
            self.week_days["Tuesday"] = False

        if self.ui.checkBoxWed.isChecked():
            self.week_days["Wednesday"] = True
        else:
            self.week_days["Wednesday"] = False

        if self.ui.checkBoxThursday.isChecked():
            self.week_days["Thursday"] = True
        else:
            self.week_days["Thursday"] = False

        if self.ui.checkBoxFriday.isChecked():
            self.week_days["Friday"] = True
        else:
            self.week_days["Friday"] = False

        if self.ui.checkBoxSat.isChecked():
            self.week_days["Saturday"] = True
        else:
            self.week_days["Saturday"] = False

        # -- Arrange app dir --------------------------
        app_file_to_run = "\\app_backend.exe"
        # app_file_to_run = "\\trigger_backend.bat"
        current_path = str(os.getcwd())
        app_file_to_run = current_path + app_file_to_run
        app_path = current_path + '\\'
        # ----------------------------------------------

        MakeXMLSCH(self.week_days, final_date_time, app_file_to_run, app_path)
        pass

    def acc_info(self):

        getTime = self.ui.timeEditSetTrig.time()
        time = str(getTime.hour()) + ':' + str(getTime.minute())
        time = time + ":00"

        dict_all_info = {
            "user": str(self.ui.lineEditUserName.text()),
            "email": str(self.ui.lineEditEmail.text()),
            "id": str(self.ui.lineEditClientId.text()),
            "secret": str(self.ui.lineEditClientSecret.text()),
            "time": time,
            "bckup_dir": str(self.ui.lineEditBackupDir.text()),
            # "prj_dir": str(self.getProjectDirEdit.text()),
            "prj_dir": None,
            # "pgm_lng": str(self.chooseLangueage.currentText()),
            "pgm_lng": None,
            "days": self.week_days,
            "repo_type_github": self.flag_repotype_github,
            "history": self.ui.spinBoxHistory.value()
        }
        # print dict_all_info
        # TODO keep log
        try:
            self.reviewInfo = Info_review(dict_all_info)
            self.reviewInfo.show()
            self.reviewInfo.exec_()
        except UnboundLocalError:
            self.error_not_scanned()
            pass
        pass

def main():
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
    pass


if __name__ == "__main__":
    main()
