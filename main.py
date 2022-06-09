from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import dropbox_functions as df
import funcs
import webbrowser

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):

        self.sub_window = SubWindow()
        self.sub_window.show()
        app.exec_()

        global IMG_PATH
        IMG_PATH = ''
        MainWindow.setObjectName("CloudApp")
        MainWindow.resize(630, 650)  # Pencere boyutu

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.photo = QLabel(self.centralwidget)
        self.photo.setGeometry(QRect(20, 20, 550, 550))
        self.photo.setText("")
        self.photo.setScaledContents(True)
        self.photo.setObjectName("photo")
        self.photo.setPixmap(QPixmap('images/logo.png'))

        self.tree = QTreeWidget(self.centralwidget)  # Folder Tree
        self.tree.setGeometry(QRect(20, 20, 550, 550))
        self.tree.setObjectName("tree")
        self.tree.setColumnCount(3)
        self.tree.setHeaderLabels(["Name", "type", "client modified"])
        self.tree.setStyleSheet("""
        background-color : rgba(0, 0, 0, 200);
        color: rgb(255,255,255);
                                """)
        palette = QPalette()
        palette.setColor(QPalette.Text, QColor(0, 0, 0))
        self.tree.header().setPalette(palette)
        self.Refresh()

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.refreshButton = QPushButton(self.centralwidget)  # Calıştırma butonu
        self.refreshButton.setGeometry(QRect(575, 20, 40, 40))
        self.refreshButton.setObjectName("run")
        self.refreshButton.clicked.connect(self.Refresh)
        self.refreshButton.setStyleSheet("""
            background-image: url(images/refresh.ico);
            background-position: center;
            background-repeat: no-repeat;
        """)

        self.deleteButton = QPushButton(self.centralwidget)  # Calıştırma butonu
        self.deleteButton.setGeometry(QRect(575, 65, 40, 40))
        self.deleteButton.setObjectName("run")
        self.deleteButton.clicked.connect(self.deleteFile)
        self.deleteButton.setStyleSheet("""
            background-image: url(images/trash.ico);
            background-position: center;
            background-repeat: no-repeat;
        """)

        self.downloadButton = QPushButton(self.centralwidget)  # Calıştırma butonu
        self.downloadButton.setGeometry(QRect(20, 570, 275, 50))
        self.downloadButton.setObjectName("run")
        self.downloadButton.clicked.connect(self.DownloadFile)

        self.uploadButton = QPushButton(self.centralwidget)  # Calıştırma butonu
        self.uploadButton.setGeometry(QRect(295, 570, 275, 50))
        self.uploadButton.setObjectName("run")
        self.uploadButton.clicked.connect(self.UploadFile)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Cloud App"))
        self.downloadButton.setText(_translate("MainWindow", "Download File"))
        self.uploadButton.setText(_translate("MainWindow", "Upload File"))

    def get_tree_item(self):
        try:
            self.tree.clear()
            files, folders = df.dropbox_list_files("")
            items = funcs.get_child_control(files, folders)
            return items
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("Error")
            msg.exec_()

    def Refresh(self):  # Çalıştırma fonksiyonu
        try:
            self.tree.clear()
            files, folders = df.dropbox_list_files("")
            print(files)
            print(folders)
            items = funcs.get_child_control(files, folders)
            root = QTreeWidgetItem(["/", "root folder"])
            root.setIcon(0, QIcon('images/dropbox.ico'))
            for i in range(len(items)):
                root.addChild(items[i])
            self.tree.insertTopLevelItem(0, root)
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("Error")
            msg.exec_()

    def ParentCheck(self, item, item_dir):
        try:
            if (item.parent() is not None) and item.parent().text(1) == "folder":
                item_dir.append(item.parent().text(0)+"/")
                item_dir = self.ParentCheck(item.parent(), item_dir)
                return item_dir
            else:
                return item_dir
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("Error")
            msg.exec_()

    def DownloadFile(self):
        try:
            item_dir = []
            item = self.tree.currentItem()
            if item.text(1) != "file":
                print("This item not file")
                return
            item_dir.append(item.text(0))
            item_dir = self.ParentCheck(item, item_dir)
            dir = "/"
            for i in range(len(item_dir)):
                add_dir = item_dir[len(item_dir) - i - 1]
                dir += add_dir
            download_dir = r"C:/CloudApp" + dir.rsplit('/', 1)[0]
            df.dropbox_download_file(dir, download_dir)
            print("File Downloaded")
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("Error")
            msg.exec_()

    def UploadFile(self):
        try:
            fname = QFileDialog.getOpenFileName(None, 'Select File', 'c:\\')
            if fname[0] != '':
                item_dir = []
                item = self.tree.currentItem()
                if item.text(1) == "folder":
                    item_dir.append(item.text(0)+"/")
                item_dir = self.ParentCheck(item, item_dir)
                dir = "/"
                for i in range(len(item_dir)):
                    dir += item_dir[len(item_dir) - i - 1]
                df.dropbox_upload_file(fname[0], dir)
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("Error")
            msg.exec_()

    def deleteFile(self):
        try:
            item_dir = []
            item = self.tree.currentItem()
            if item.text(1) != "file":
                print("This item not file")
                return
            item_dir.append(item.text(0))
            item_dir = self.ParentCheck(item, item_dir)
            dir = "/"
            for i in range(len(item_dir)):
                add_dir = item_dir[len(item_dir) - i - 1]
                dir += add_dir
            df.dropbox_delete_file(dir)
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("Error")
            msg.exec_()

class SubWindow(QWidget):
    def __init__(self):
        super(SubWindow, self).__init__()
        self.resize(550, 200)
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("SubWindow", "Get Access Code"))
        # Label
        self.label = QLabel(self)
        self.label.setGeometry(30, 10, 530, 50)
        self.label.setFont(QFont('Arial', 13))
        self.label.setText('Please click the get access code and enter generated access code')

        #Label2
        cl_button = QCommandLinkButton("Get Access Code", self)
        cl_button.setGeometry(30, 60, 160, 50)
        cl_button.clicked.connect(self.openBrowser)

        #TextEdit
        self.acc_code = QTextEdit(self)  # Kullanıcıdan alınan şifreleme anahtarı
        self.acc_code.setGeometry(QRect(200, 60, 320, 50))
        self.acc_code.setFont(QFont('Arial', 13))
        self.acc_code.setPlaceholderText(_translate("SubWindow","Enter Access code here"))

        #Connect_Button
        self.Connect = QPushButton(self)  # Fotoğraf seçme butonu
        self.Connect.setGeometry(QRect(30, 120, 490, 50))
        self.Connect.setText(_translate("SubWindow", "Connect"))
        self.Connect.setFont(QFont('Arial', 20))
        self.Connect.clicked.connect(self.getToken)

    def openBrowser(self):
        try:
            app_key = "e1iey9lzp2uu6jq"
            authorization_url = "https://www.dropbox.com/oauth2/authorize?client_id=%s&response_type=code" % app_key
            webbrowser.open(authorization_url)
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("Error")
            msg.exec_()

    def getToken(self):
        try:
            authorization_code = self.acc_code.toPlainText()
            df.setToken(authorization_code)
            self.close()
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("Error")
            msg.exec_()

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
