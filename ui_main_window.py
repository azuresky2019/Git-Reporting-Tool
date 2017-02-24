#!/usr/bin/python

import sys
import json
from PyQt4 import QtGui
from PyQt4.Qt import *

# ---- List to store selected paths ----
path_lists = [None] * 20

class MyPopup(QWidget):
    def __init__(self):
        QWidget.__init__(self)

    def manage_repos(self):
        path_1 = QtGui.QPushButton('Browse')
        self.path_1Edit = QtGui.QLineEdit(self)
        if path_lists[0]:
            self.path_1Edit.setText(str(path_lists[0]))
        else:
            self.path_1Edit.setText("Browse for repo 1")
        path_1.clicked.connect(self.get_paths_repo1)

        path_2 = QtGui.QPushButton('Browse')
        self.path_2Edit = QtGui.QLineEdit(self)
        if path_lists[1]:
            self.path_2Edit.setText(str(path_lists[0]))
        else:
            self.path_2Edit.setText("Browse for repo 2")
        path_2.clicked.connect(self.get_paths_repo2)

        path_3 = QtGui.QPushButton('Browse')
        self.path_3Edit = QtGui.QLineEdit(self)
        if path_lists[2]:
            self.path_3Edit.setText(str(path_lists[2]))
        else:
            self.path_3Edit.setText("Browse for repo 3")
        path_3.clicked.connect(self.get_paths_repo3)

        path_4 = QtGui.QPushButton('Browse')
        self.path_4Edit = QtGui.QLineEdit(self)
        if path_lists[3]:
            self.path_4Edit.setText(str(path_lists[3]))
        else:
            self.path_4Edit.setText("Browse for repo 4")
        path_4.clicked.connect(self.get_paths_repo4)

        path_5 = QtGui.QPushButton('Browse')
        self.path_5Edit = QtGui.QLineEdit(self)
        if path_lists[4]:
            self.path_5Edit.setText(str(path_lists[4]))
        else:
            self.path_5Edit.setText("Browse for repo 5")
        path_5.clicked.connect(self.get_paths_repo5)

        path_6 = QtGui.QPushButton('Browse')
        self.path_6Edit = QtGui.QLineEdit(self)
        if path_lists[5]:
            self.path_6Edit.setText(str(path_lists[5]))
        else:
            self.path_6Edit.setText("Browse for repo 6")
        path_6.clicked.connect(self.get_paths_repo6)

        path_7 = QtGui.QPushButton('Browse')
        self.path_7Edit = QtGui.QLineEdit(self)
        if path_lists[6]:
            self.path_7Edit.setText(path_lists[6])
        else:
            self.path_7Edit.setText("Browse for repo 7")
        path_7.clicked.connect(self.get_paths_repo7)

        path_8 = QtGui.QPushButton('Browse')
        self.path_8Edit = QtGui.QLineEdit(self)
        if path_lists[7]:
            self.path_8Edit.setText(path_lists[7])
        else:
            self.path_8Edit.setText("Browse for repo 8")
        path_8.clicked.connect(self.get_paths_repo8)

        path_9 = QtGui.QPushButton('Browse')
        self.path_9Edit = QtGui.QLineEdit(self)
        if path_lists[8]:
            self.path_9Edit.setText(str(path_lists[8]))
        else:
            self.path_9Edit.setText("Browse for repo 9")
        path_9.clicked.connect(self.get_paths_repo9)

        path_10 = QtGui.QPushButton('Browse')
        self.path_10Edit = QtGui.QLineEdit(self)
        if path_lists[9]:
            self.path_10Edit.setText(str(path_lists[9]))
        else:
            self.path_10Edit.setText("Browse for repo 10")
        path_10.clicked.connect(self.get_paths_repo10)

        path_11 = QtGui.QPushButton('Browse')
        self.path_11Edit = QtGui.QLineEdit(self)
        if path_lists[10]:
            self.path_11Edit.setText(str(path_lists[10]))
        else:
            self.path_11Edit.setText("Browse for repo 11")
        path_11.clicked.connect(self.get_paths_repo11)

        path_12 = QtGui.QPushButton('Browse')
        self.path_12Edit = QtGui.QLineEdit(self)
        if path_lists[11]:
            self.path_12Edit.setText(str(path_lists[11]))
        else:
            self.path_12Edit.setText("Browse for repo 12")
        path_12.clicked.connect(self.get_paths_repo12)

        path_13 = QtGui.QPushButton('Browse')
        self.path_13Edit = QtGui.QLineEdit(self)
        if path_lists[12]:
            self.path_13Edit.setText(str(path_lists[12]))
        else:
            self.path_13Edit.setText("Browse for repo 13")
        path_13.clicked.connect(self.get_paths_repo13)

        path_14 = QtGui.QPushButton('Browse')
        self.path_14Edit = QtGui.QLineEdit(self)
        if path_lists[13]:
            self.path_14Edit.setText(path_lists[13])
        else:
            self.path_14Edit.setText("Browse for repo 14")
        path_14.clicked.connect(self.get_paths_repo14)

        path_15 = QtGui.QPushButton('Browse')
        self.path_15Edit = QtGui.QLineEdit(self)
        if path_lists[14]:
            self.path_15Edit.setText(path_lists[14])
        else:
            self.path_15Edit.setText("Browse for repo 15")
        path_15.clicked.connect(self.get_paths_repo15)

        path_16 = QtGui.QPushButton('Browse')
        self.path_16Edit = QtGui.QLineEdit(self)
        if path_lists[15]:
            self.path_16Edit.setText(path_lists[15])
        else:
            self.path_16Edit.setText("Browse for repo 16")
        path_16.clicked.connect(self.get_paths_repo16)

        path_17 = QtGui.QPushButton('Browse')
        self.path_17Edit = QtGui.QLineEdit(self)
        if path_lists[16]:
            self.path_17Edit.setText(path_lists[16])
        else:
            self.path_17Edit.setText("Browse for repo 17")
        path_17.clicked.connect(self.get_paths_repo17)

        path_18 = QtGui.QPushButton('Browse')
        self.path_18Edit = QtGui.QLineEdit(self)
        if path_lists[17]:
            self.path_18Edit.setText(path_lists[17])
        else:
            self.path_18Edit.setText("Browse for repo 18")
        path_18.clicked.connect(self.get_paths_repo18)

        path_19 = QtGui.QPushButton('Browse')
        self.path_19Edit = QtGui.QLineEdit(self)
        if path_lists[18]:
            self.path_19Edit.setText(path_lists[18])
        else:
            self.path_19Edit.setText("Browse for repo 19")
        path_19.clicked.connect(self.get_paths_repo19)

        path_20 = QtGui.QPushButton('Browse')
        self.path_20Edit = QtGui.QLineEdit(self)
        if path_lists[19]:
            self.path_20Edit.setText(path_lists[19])
        else:
            self.path_20Edit.setText("Browse for repo 20")
        path_20.clicked.connect(self.get_paths_repo20)

        apply_button = QtGui.QPushButton("Apply")

        apply_button.clicked.connect(self.apply_paths)

        grid_get_browse = QtGui.QGridLayout()

        grid_get_browse.addWidget(path_1, 1, 0)
        grid_get_browse.addWidget(self.path_1Edit, 1, 1)

        grid_get_browse.addWidget(path_2, 2, 0)
        grid_get_browse.addWidget(self.path_2Edit, 2, 1)

        grid_get_browse.addWidget(path_3, 3, 0)
        grid_get_browse.addWidget(self.path_3Edit, 3, 1)

        grid_get_browse.addWidget(path_4, 4, 0)
        grid_get_browse.addWidget(self.path_4Edit, 4, 1)

        grid_get_browse.addWidget(path_5, 5, 0)
        grid_get_browse.addWidget(self.path_5Edit, 5, 1)

        grid_get_browse.addWidget(path_6, 6, 0)
        grid_get_browse.addWidget(self.path_6Edit, 6, 1)

        grid_get_browse.addWidget(path_7, 7, 0)
        grid_get_browse.addWidget(self.path_7Edit, 7, 1)

        grid_get_browse.addWidget(path_8, 8, 0)
        grid_get_browse.addWidget(self.path_8Edit, 8, 1)

        grid_get_browse.addWidget(path_9, 9, 0)
        grid_get_browse.addWidget(self.path_9Edit, 9, 1)

        grid_get_browse.addWidget(path_10, 10, 0)
        grid_get_browse.addWidget(self.path_10Edit, 10, 1)

        grid_get_browse.addWidget(path_11, 11, 0)
        grid_get_browse.addWidget(self.path_11Edit, 11, 1)

        grid_get_browse.addWidget(path_12, 12, 0)
        grid_get_browse.addWidget(self.path_12Edit, 12, 1)

        grid_get_browse.addWidget(path_13, 13, 0)
        grid_get_browse.addWidget(self.path_13Edit, 13, 1)

        grid_get_browse.addWidget(path_14, 14, 0)
        grid_get_browse.addWidget(self.path_14Edit, 14, 1)

        grid_get_browse.addWidget(path_15, 15, 0)
        grid_get_browse.addWidget(self.path_15Edit, 15, 1)

        grid_get_browse.addWidget(path_16, 16, 0)
        grid_get_browse.addWidget(self.path_16Edit, 16, 1)

        grid_get_browse.addWidget(path_17, 17, 0)
        grid_get_browse.addWidget(self.path_17Edit, 17, 1)

        grid_get_browse.addWidget(path_18, 18, 0)
        grid_get_browse.addWidget(self.path_18Edit, 18, 1)

        grid_get_browse.addWidget(path_19, 19, 0)
        grid_get_browse.addWidget(self.path_19Edit, 19, 1)

        grid_get_browse.addWidget(path_20, 20, 0)
        grid_get_browse.addWidget(self.path_20Edit, 20, 1)

        grid_get_browse.addWidget(apply_button, 21, 0)


        self.setLayout(grid_get_browse)

    def apply_paths(self):
        print path_lists
        self.close()

    def get_paths_repo1(self):
        get_dir_dialog = QtGui.QFileDialog.getExistingDirectory(None,
                                                                'Select repository.',
                                                                'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        print "Obtained direcory is : " + str(get_dir_dialog)
        self.path_1Edit.setText(str(get_dir_dialog))
        path_lists[0] = str(get_dir_dialog)
        pass

    def get_paths_repo2(self):
        get_dir_dialog = QtGui.QFileDialog.getExistingDirectory(None,
                                                                'Select repository.',
                                                                'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        print "Obtained direcory is : " + str(get_dir_dialog)
        # self.path_2Edit.setText(str(get_dir_dialog))
        self.path_2Edit.setText(str(get_dir_dialog))
        path_lists[1] = str(get_dir_dialog)
        pass

    def get_paths_repo3(self):
        get_dir_dialog = QtGui.QFileDialog.getExistingDirectory(None,
                                                                'Select repository.',
                                                                'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        print "Obtained direcory is : " + str(get_dir_dialog)
        self.path_3Edit.setText(str(get_dir_dialog))
        path_lists[2] = str(get_dir_dialog)
        pass

    def get_paths_repo4(self):
        get_dir_dialog = QtGui.QFileDialog.getExistingDirectory(None,
                                                                'Select repository.',
                                                                'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        print "Obtained direcory is : " + str(get_dir_dialog)
        self.path_4Edit.setText(str(get_dir_dialog))
        path_lists[3] = str(get_dir_dialog)
        pass

    def get_paths_repo5(self):
        get_dir_dialog = QtGui.QFileDialog.getExistingDirectory(None,
                                                                'Select repository.',
                                                                'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        print "Obtained direcory is : " + str(get_dir_dialog)
        self.path_5Edit.setText(str(get_dir_dialog))
        path_lists[4] = str(get_dir_dialog)
        pass

    def get_paths_repo6(self):
        get_dir_dialog = QtGui.QFileDialog.getExistingDirectory(None,
                                                                'Select repository.',
                                                                'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        print "Obtained direcory is : " + str(get_dir_dialog)
        self.path_6Edit.setText(str(get_dir_dialog))
        path_lists[5] = str(get_dir_dialog)
        pass

    def get_paths_repo7(self):
        get_dir_dialog = QtGui.QFileDialog.getExistingDirectory(None,
                                                                'Select repository.',
                                                                'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        print "Obtained direcory is : " + str(get_dir_dialog)
        self.path_7Edit.setText(str(get_dir_dialog))
        path_lists[6] = str(get_dir_dialog)
        pass

    def get_paths_repo8(self):
        get_dir_dialog = QtGui.QFileDialog.getExistingDirectory(None,
                                                                'Select repository.',
                                                                'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        print "Obtained direcory is : " + str(get_dir_dialog)
        self.path_8Edit.setText(str(get_dir_dialog))
        path_lists[7] = str(get_dir_dialog)
        pass

    def get_paths_repo9(self):
        get_dir_dialog = QtGui.QFileDialog.getExistingDirectory(None,
                                                                'Select repository.',
                                                                'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        print "Obtained direcory is : " + str(get_dir_dialog)
        self.path_9Edit.setText(str(get_dir_dialog))
        path_lists[8] = str(get_dir_dialog)
        pass

    def get_paths_repo10(self):
        get_dir_dialog = QtGui.QFileDialog.getExistingDirectory(None,
                                                                'Select repository.',
                                                                'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        print "Obtained direcory is : " + str(get_dir_dialog)
        self.path_10Edit.setText(str(get_dir_dialog))
        path_lists[9] = str(get_dir_dialog)
        pass

    def get_paths_repo11(self):
        get_dir_dialog = QtGui.QFileDialog.getExistingDirectory(None,
                                                                'Select repository.',
                                                                'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        print "Obtained direcory is : " + str(get_dir_dialog)
        self.path_11Edit.setText(str(get_dir_dialog))
        path_lists[10] = str(get_dir_dialog)
        pass

    def get_paths_repo12(self):
        get_dir_dialog = QtGui.QFileDialog.getExistingDirectory(None,
                                                                'Select repository.',
                                                                'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        print "Obtained direcory is : " + str(get_dir_dialog)
        self.path_12Edit.setText(str(get_dir_dialog))
        path_lists[11] = str(get_dir_dialog)
        pass

    def get_paths_repo13(self):
        get_dir_dialog = QtGui.QFileDialog.getExistingDirectory(None,
                                                                'Select repository.',
                                                                'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        print "Obtained direcory is : " + str(get_dir_dialog)
        self.path_13Edit.setText(str(get_dir_dialog))
        path_lists[12] = str(get_dir_dialog)
        pass

    def get_paths_repo14(self):
        get_dir_dialog = QtGui.QFileDialog.getExistingDirectory(None,
                                                                'Select repository.',
                                                                'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        print "Obtained direcory is : " + str(get_dir_dialog)
        self.path_14Edit.setText(str(get_dir_dialog))
        path_lists[13] = str(get_dir_dialog)
        pass

    def get_paths_repo15(self):
        get_dir_dialog = QtGui.QFileDialog.getExistingDirectory(None,
                                                                'Select repository.',
                                                                'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        print "Obtained direcory is : " + str(get_dir_dialog)
        self.path_15Edit.setText(str(get_dir_dialog))
        path_lists[14] = str(get_dir_dialog)
        pass

    def get_paths_repo16(self):
        get_dir_dialog = QtGui.QFileDialog.getExistingDirectory(None,
                                                                'Select repository.',
                                                                'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        print "Obtained direcory is : " + str(get_dir_dialog)
        self.path_16Edit.setText(str(get_dir_dialog))
        path_lists[15] = str(get_dir_dialog)
        pass

    def get_paths_repo17(self):
        get_dir_dialog = QtGui.QFileDialog.getExistingDirectory(None,
                                                                'Select repository.',
                                                                'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        print "Obtained direcory is : " + str(get_dir_dialog)
        self.path_17Edit.setText(str(get_dir_dialog))
        path_lists[16] = str(get_dir_dialog)
        pass

    def get_paths_repo18(self):
        get_dir_dialog = QtGui.QFileDialog.getExistingDirectory(None,
                                                                'Select repository.',
                                                                'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        print "Obtained direcory is : " + str(get_dir_dialog)
        self.path_18Edit.setText(str(get_dir_dialog))
        path_lists[17] = str(get_dir_dialog)
        pass

    def get_paths_repo19(self):
        get_dir_dialog = QtGui.QFileDialog.getExistingDirectory(None,
                                                                'Select repository.',
                                                                'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        print "Obtained direcory is : " + str(get_dir_dialog)
        self.path_19Edit.setText(str(get_dir_dialog))
        path_lists[18] = str(get_dir_dialog)
        pass

    def get_paths_repo20(self):
        get_dir_dialog = QtGui.QFileDialog.getExistingDirectory(None,
                                                                'Select repository.',
                                                                'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        print "Obtained direcory is : " + str(get_dir_dialog)
        self.path_20Edit.setText(str(get_dir_dialog))
        path_lists[19] = str(get_dir_dialog)
        pass

class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()

        user_name = QtGui.QLabel('Git Username')
        usr_email = QtGui.QLabel('Email')
        client_id = QtGui.QLabel('Git Client ID')
        client_secret = QtGui.QLabel('Git Client Secret')

        button_apply = QtGui.QPushButton("OK", self)
        button_apply.clicked.connect(self.apply_action)

        button_scan_dir = QtGui.QPushButton("Manage Repos", self)
        button_scan_dir.clicked.connect(self.scan_repos)

        button_finish = QtGui.QPushButton("Cancel", self)
        button_finish.resize(100, 20)
        button_finish.clicked.connect(self.finish_action)

        self.user_nameEdit = QtGui.QLineEdit()
        self.client_idEdit = QtGui.QLineEdit()
        self.client_secretEdit = QtGui.QLineEdit()
        self.usr_emailEdit = QtGui.QLineEdit()
        self.initial_pathEdit = QtGui.QLineEdit()
        self.progress = QtGui.QProgressBar()
        self.progress.resize(300, 20)

        grid = QtGui.QGridLayout()

        grid.addWidget(user_name, 1, 0)
        grid.addWidget(self.user_nameEdit, 1, 1)

        grid.addWidget(usr_email, 2, 0)
        grid.addWidget(self.usr_emailEdit, 2, 1)

        grid.addWidget(client_id, 3, 0)
        grid.addWidget(self.client_idEdit, 3, 1)

        grid.addWidget(client_secret, 4, 0)
        grid.addWidget(self.client_secretEdit, 4, 1)

        grid.addWidget(button_apply, 5, 0)
        grid.addWidget(button_scan_dir, 5, 1)
        grid.addWidget(button_finish, 6, 1)


        self.setLayout(grid)
        self.setGeometry(300, 300, 350, 200)
        self.setFixedSize(350, 200)
        self.setWindowIcon(QtGui.QIcon('github-logo-icon.png'))
        self.setWindowTitle('Git report tool: TemcoNepal')
        self.show()
        pass

    def apply_action(self):
        info_fromUI = {
            "username":str(self.user_nameEdit.text()),
            "user_email":str(self.usr_emailEdit.text()),
            "clint_id":str(self.client_idEdit.text()),
            "client_secret":str(self.client_secretEdit.text()),
            "repo_paths":path_lists
        }
        if not info_fromUI["username"] or not info_fromUI["user_email"] or not info_fromUI["clint_id"] or not info_fromUI["client_secret"]:
            self.error_message()
        with open("config/user_infoUI.json", "wb") as user_ui_json:
            json.dump(info_fromUI, user_ui_json)
            user_ui_json.close()
        pass

    def get_dir(self):
        get_dir_dialog = QtGui.QFileDialog.getExistingDirectory(None,
                                                                'Select initial directory into which repos are cloned:',
                                                                'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        print "Obtained direcory is : " + str(get_dir_dialog)
        self.initial_pathEdit.setText(str(get_dir_dialog))
        pass

    def finish_action(self):
        sys.exit()
        pass

    def scan_repos(self):
        print "Opening a new popup window..."
        self.w = MyPopup()
        self.w.setGeometry(QRect(100, 100, 400, 200))
        self.w.manage_repos()
        self.w.show()
        pass

    def error_message(self):
        error = QtGui.QErrorMessage()
        error.showMessage("Data fields are empty !")
        error.exec_()
        pass

def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
