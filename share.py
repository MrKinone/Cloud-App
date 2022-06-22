from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import dropbox_functions as df

class SubWindowshare(QWidget):
    def __init__(self):
        super(SubWindowshare, self).__init__()
        self.resize(500, 200)
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("SubWindowshare", "Share File"))
        # Label
        self.label = QLabel(self)
        self.label.setGeometry(30, 10, 440, 50)
        self.label.setFont(QFont('Arial', 13))
        self.label.setText('Enter the email of the user you want to share the file with')

        #TextEdit
        self.eMail = QTextEdit(self)
        self.eMail.setGeometry(QRect(30, 60, 440, 40))
        self.eMail.setFont(QFont('Arial', 13))
        self.eMail.setPlaceholderText(_translate("SubWindowshare","Enter e-mail here"))

        #Connect_Button
        self.Connect = QPushButton(self)  # Fotoğraf seçme butonu
        self.Connect.setGeometry(QRect(30, 120, 440, 50))
        self.Connect.setText(_translate("SubWindowshare", "Connect"))
        self.Connect.setFont(QFont('Arial', 20))
        self.Connect.clicked.connect(self.createPublicFolder)

    def createPublicFolder(self):
        try:
            eMailStr = self.eMail.toPlainText()
            df.getusermail()
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("Error")
            msg.exec_()