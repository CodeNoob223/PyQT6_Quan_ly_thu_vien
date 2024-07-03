import sys
from PyQt6.QtWidgets import QWidget, QPushButton, QMainWindow, QApplication, QFrame, QMessageBox, QTableWidgetItem
from login_ui import Ui_loginWindow
from connect_database import ConnectDatabase
from main import main

class login(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_loginWindow()
        self.ui.setupUi(self)

        # Creat a database connection object
        self.db = ConnectDatabase()

        # Connect UI elements to class variables
        self.taikhoan = self.ui.taiKhoan_lineEdit
        self.matkhau = self.ui.matKhau_lineEdit
        
        self.dangNhap_pushButton = self.ui.dangNhap_pushButton
        self.dong_pushButton = self.ui.dong_pushButton

        self.button = self.ui.dangNhap_pushButton.findChildren(QPushButton)
        self.button = self.ui.dong_pushButton.findChildren(QPushButton)

        # initialize signal-slot connections
        self.init_signal_slot()

    def init_signal_slot(self):
        self.dangNhap_pushButton.clicked.connect(self.login)
        self.dong_pushButton.clicked.connect(self.dong)

    def login(self):
        username = self.taikhoan.text()
        matkhau = self.matkhau.text()

        if self.db.check_login(username, matkhau):
            # Nếu đăng nhập thành công, hiển thị file main.ui
            QMessageBox.information(self, "Successful", "Đăng nhập thành công.", QMessageBox.StandardButton.Ok)
            self.main_window = main()
            self.main_window.show()
            self.close()
        else:
            # Nếu đăng nhập thất bại, hiển thị thông báo lỗi
            QMessageBox.information(self, "Đăng nhập thất bại", "Tài khoản hoặc mật khẩu không đúng.", QMessageBox.StandardButton.Ok)

    def dong(self):
        exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = login()
    window.show()

    sys.exit(app.exec())