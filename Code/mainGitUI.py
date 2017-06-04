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

flag_done_scan = False

class gitDirThread(QtCore.QThread):

    def __init__(self, dir_backup):
        QtCore.QThread.__init__(self)
        self.init_path = str(dir_backup)
        # print self.init_path
        # self.thPause = False
        # self.pauseStat = False

    def __del__(self):
        self.wait()

    # def is_git_repo(self, dirt):
    #     os.chdir(dirt)
    #     if call(["git", "branch"], stderr=STDOUT, stdout=(os.devnull, 'w')) != 0:
    #         return False
    #     else:
    #         return True

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

        # repoIndx = 0

        for repo in range(0, all_dirs):
            # if not self.thPause:

                # if self.pauseStat:
                #     self.emit(QtCore.SIGNAL("pauseTh(bool)"), True)

            self.emit(QtCore.SIGNAL("inc_num(int)"), float(repo) / all_dirs * 100)
            if self.is_git_repo(list_dirs[repo]):
                self.emit(QtCore.SIGNAL("tbl_val(QString)"), list_dirs[repo])
            # else:
            #     repoIndx = repo
            #     print repoIndx
            #     break
                pass
        self.emit(QtCore.SIGNAL("inc_num(int)"), 100)
        self.emit(QtCore.SIGNAL("finished(bool)"), True)
        os.chdir(path_now)

class RepoManager(QtGui.QDialog, QtGui.QWidget):
    def __init__(self, backup_dir):
        QtGui.QDialog.__init__(self, parent=None)
        self.backup_dir = backup_dir
        self.dialog_repoManager = Ui_repo_manager()
        self.dialog_repoManager.setupUi(self)
        self.setFixedSize(472, 371)

        self.gitThread = gitDirThread(self.backup_dir)
        self.gitThread.start()

        # self.connect(self.dialog_repoManager.pushButtonStop, QtCore.SIGNAL("clicked()"), self.stop_scan)
        self.connect(self.dialog_repoManager.pushButtonSave, QtCore.SIGNAL("clicked()"), self.on_save)
        self.connect(self.dialog_repoManager.pushButtonDiscard, QtCore.SIGNAL("clicked()"), self.on_discard)

        self.connect(self.gitThread, QtCore.SIGNAL("tbl_val(QString)"), self.draw_table)
        self.dialog_repoManager.tableWidgetListRepo.setColumnCount(2)
        self.dialog_repoManager.tableWidgetListRepo.setRowCount(0)

        self.connect(self.gitThread, QtCore.SIGNAL("inc_num(int)"), self.rise_pgrs_bar)

        self.connect(self.gitThread, QtCore.SIGNAL("finished(bool)"), self.scan_finished)

        # self.connect(self.gitThread, QtCore.SIGNAL("pauseTh(bool)"), self.thPause)
        # self.emit(QtCore.SIGNAL("pauseTh(bool)"), True)

    def draw_table(self, tble_item):
        row_position = self.dialog_repoManager.tableWidgetListRepo.rowCount()
        self.dialog_repoManager.tableWidgetListRepo.insertRow(row_position)

        self.dialog_repoManager.tableWidgetListRepo.setColumnWidth(1, 430)
        # self.dialog_repoManager.tableWidgetListRepo.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.dialog_repoManager.tableWidgetListRepo.setItem(row_position, 1, QtGui.QTableWidgetItem(tble_item))

        checkItem = QtGui.QTableWidgetItem()
        checkItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        checkItem.setCheckState(Qt.Checked)
        self.dialog_repoManager.tableWidgetListRepo.setItem(row_position, 0, checkItem)
        self.dialog_repoManager.tableWidgetListRepo.setColumnWidth(0, 50)

    def rise_pgrs_bar(self, prgVal):
        self.dialog_repoManager.progressBarScanning.setValue(prgVal)
        pass

    # def thPause(self, thPauseEvnt):
    #     self.gitThread.thPause = thPauseEvnt
    #     self.gitThread.pauseStat = False
    #     pass

    # def stop_scan(self):
        # print ("Thread Status", self.gitThread.isRunning())
        # print ("pauseStat", self.gitThread.pauseStat)
        # print ("thPause", self.gitThread.thPause)

        # self.dialog_repoManager.pushButtonPause.setText("Resume")
        # self.dialog_repoManager.pushButtonDiscard.setEnabled(True)

        # if self.gitThread.isRunning():
        # if self.gitThread.thPause:
        #     self.dialog_repoManager.pushButtonStop.setText("Start")
        #     self.dialog_repoManager.pushButtonDiscard.setEnabled(True)
            # self.gitThread.pauseStat = False
            # self.dialog_repoManager.tableWidgetListRepo.setRowCount(0)
            # self.dialog_repoManager.tableWidgetListRepo.setColumnCount(0)
            # self.gitThread.terminate()
        # else:
        #     self.dialog_repoManager.pushButtonStop.setText("Stop")
        #     self.dialog_repoManager.pushButtonDiscard.setEnabled(False)
        #     for i in reversed(range(self.dialog_repoManager.tableWidgetListRepo.rowCount())):
        #         self.dialog_repoManager.tableWidgetListRepo.removeRow(i)
        #     self.gitThread.start()
        #     self.gitThread.pauseStat = False
        #     pass
        # print "Pressed Stop!"

    def scan_finished(self):
        print "Finished scanning !"
        self.gitThread.terminate()
        self.dialog_repoManager.pushButtonDiscard.setEnabled(True)
        self.dialog_repoManager.pushButtonSave.setEnabled(True)
        # self.dialog_repoManager.pushButtonStop.setEnabled(False)


    def on_save(self):
        checked_dir_list = [None]
        checked_dir_list_json = [None]
        for i in range(self.dialog_repoManager.tableWidgetListRepo.rowCount()):
            if self.dialog_repoManager.tableWidgetListRepo.item(i, 0).checkState() == Qt.Checked:
                checked_dir_list.append((self.dialog_repoManager.tableWidgetListRepo.item(i, 1)).text())

        for dir in range(0, len(checked_dir_list)):
            if checked_dir_list[dir]:
                checked_dir_list_json.append(str(checked_dir_list[dir]))

        del checked_dir_list_json[0]

        del checked_dir_list

        with open("config/dir_list.json", "w") as dir_list_file:
            json.dump(checked_dir_list_json, dir_list_file)
            dir_list_file.close()
        del checked_dir_list_json

        self.mainWindow = Main()
        # self.mainWindow.ui.pushButtonScan.setEnabled(False)
        # global flag_done_scan
        # flag_done_scan = True

        self.emit(QtCore.SIGNAL("en_ok(bool)"), True)

        self.close()

    def on_discard(self):
        # self.mainWindow.ui.pushButtonOK.setEnabled(True)
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

        # self.ui.spinBoxHistory.setMaximum(30)

        self.connect(self.ui.radioButtonGithubTypeRepo, QtCore.SIGNAL("clicked()"), self.on_repotype_github)
        self.connect(self.ui.radioButtonLocalTypeRepo, QtCore.SIGNAL("clicked()"), self.on_repotype_local)

        self.connect(self.ui.pushButtonBrowseBackup, QtCore.SIGNAL("clicked()"), self.on_init_dir_browse)

        self.connect(self.ui.pushButtonExit, QtCore.SIGNAL("clicked()"), self.on_exit)
        self.connect(self.ui.pushButtonOK, QtCore.SIGNAL("clicked()"), self.on_okay)

        self.connect(self.ui.lineEditBackupDir, QtCore.SIGNAL("textChanged(QString)"), self.check_dir)

        self.connect(self.ui.pushButtonScan, QtCore.SIGNAL("clicked()"), self.manage_repo)

        # self.repoMangClass = RepoManager()


        # self.ThreadQt = gitDirThread()

        # self.emit(QtCore.SIGNAL("finished(bool)"), True)


        self.check_dir()

    def check_dir(self):
        if self.ui.lineEditBackupDir.text() and ('\\' in self.ui.lineEditBackupDir.text() and (':' in self.ui.lineEditBackupDir.text())):
            self.ui.pushButtonScan.setEnabled(True)
        else:
            self.ui.pushButtonScan.setEnabled(False)

    def on_repotype_github(self):
        self.ui.labelUserName.setEnabled(True)
        self.ui.lineEditUserName.setEnabled(True)

        self.ui.labelClientID.setEnabled(True)
        self.ui.lineEditClientId.setEnabled(True)

        self.ui.labelClientSecret.setEnabled(True)
        self.ui.lineEditClientSecret.setEnabled(True)

        self.ui.groupBoxInitialBackup.setEnabled(False)

        self.ui.pushButtonOK.setEnabled(True)
        self.ui.pushButtonScan.setEnabled(False)

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
                                                         # 'C:\\', QtGui.QFileDialog.ShowDirsOnly)
                                                         # "C:\Users\Admin", QtGui.QFileDialog.ShowDirsOnly)
                                                         '/', QtGui.QFileDialog.ShowDirsOnly)
        self.ui.lineEditBackupDir.setText(str(self.init_backup_dir))
        pass

    def connect_menu_action(self):
        self.ui.actionExit.triggered.connect(self.close)
        # self.ui.actionManage_Repo.triggered.connect(self.manage_repo)
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
            self.if_no_days_set += 1
        if self.ui.checkBoxMonday.isChecked():
            self.week_days["Monday"] = True
            self.if_no_days_set += 1
        if self.ui.checkBoxTuesday.isChecked():
            self.week_days["Tuesday"] = True
            self.if_no_days_set += 1
        if self.ui.checkBoxWed.isChecked():
            self.week_days["Wednesday"] = True
            self.if_no_days_set += 1
        if self.ui.checkBoxThursday.isChecked():
            self.week_days["Thursday"] = True
            self.if_no_days_set += 1
        if self.ui.checkBoxFriday.isChecked():
            self.week_days["Friday"] = True
            self.if_no_days_set += 1
        if self.ui.checkBoxSat.isChecked():
            self.week_days["Saturday"] = True
            self.if_no_days_set += 1

        if not self.if_no_days_set:
            self.ui.checkBoxMonday.setChecked(True)
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
