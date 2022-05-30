from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import dropbox_functions as df
import funcs


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        global IMG_PATH
        IMG_PATH = ''
        MainWindow.setObjectName("CloudApp")
        MainWindow.resize(630, 640)  # Pencere boyutu

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
        self.tree.insertTopLevelItems(0, self.get_tree_item())
        self.tree.setStyleSheet("""
        background-color : rgba(0, 0, 0, 200);
        color: rgb(255,255,255);
                                """)
        palette = QPalette()
        palette.setColor(QPalette.Text, QColor(0, 0, 0))
        self.tree.header().setPalette(palette)

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
        self.tree.clear()
        files, folders = df.dropbox_list_files("")
        items = funcs.get_child_control(files, folders)
        return items

    def Refresh(self):  # Çalıştırma fonksiyonu
        self.tree.clear()
        files, folders = df.dropbox_list_files("")
        items = funcs.get_child_control(files, folders)
        self.tree.insertTopLevelItems(0, items)

    def ParentCheck(self, item, item_dir):
        if item.parent() is not None:
            item_dir.append(item.parent().text(0))
            item_dir = self.ParentCheck(item.parent(), item_dir)
            return item_dir
        else:
            return item_dir

    def DownloadFile(self):
        item_dir = []
        item = self.tree.currentItem()
        item_dir.append(item.text(0))
        item_dir = self.ParentCheck(item, item_dir)
        dir = ""
        for i in range(len(item_dir)):
            add_dir = "/" + item_dir[len(item_dir) - i - 1]
            dir += add_dir
        download_dir = r"C:/CloudApp" + dir.rsplit('/', 1)[0]
        df.dropbox_download_file(dir, download_dir)

    def UploadFile(self):
        fname = QFileDialog.getOpenFileName(None, 'Select File', 'c:\\')
        item_dir = []
        item = self.tree.currentItem()
        if item.text(1) == "folder":
            item_dir.append(item.text(0))

        item_dir = self.ParentCheck(item, item_dir)
        dir = ""
        for i in range(len(item_dir)):
            add_dir = "/" + item_dir[len(item_dir) - i - 1]
            dir += add_dir
        df.dropbox_upload_file(fname[0], dir)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
