import sys
from PyQt6.QtWidgets import QMainWindow, QApplication
from connect_database import ConnectDatabase
from main_ui import Ui_mainWindow
from ql_bandoc import ql_bandoc
from ql_admin import ql_admin
from ql_theloai import ql_theloai
from ql_tacgia import ql_tacgia
from ql_vipham import ql_vipham
from ql_muon_tra import FormQLMuonTra
from ql_sach import FormQLSach
from thongke import FormThongKe


class main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)

        # Creat a database connection object
        self.db = ConnectDatabase()

        self.banDoc_pushButton = self.ui.banDoc_pushButton
        self.thongKe_pushButton = self.ui.thongKe_pushButton
        self.admin_pushButton = self.ui.admin_pushButton
        self.theLoai_pushButton = self.ui.theLoai_pushButton
        self.tacGia_pushButton = self.ui.tacGia_pushButton
        self.viPham_pushButton = self.ui.viPham_pushButton
        self.sach_pushButton = self.ui.sach_pushButton
        self.muonTra_pushButton = self.ui.muonTra_pushButton

        # initialize signal-slot connections
        self.init_signal_slot()

    def init_signal_slot(self):
        self.banDoc_pushButton.clicked.connect(self.bandoc)
        self.admin_pushButton.clicked.connect(self.admin)
        self.theLoai_pushButton.clicked.connect(self.theloai)
        self.tacGia_pushButton.clicked.connect(self.tacgia)
        self.viPham_pushButton.clicked.connect(self.vipham)
        self.sach_pushButton.clicked.connect(self.sach)
        self.muonTra_pushButton.clicked.connect(self.muontra)
        self.thongKe_pushButton.clicked.connect(self.thongke)

    def muontra(self):
        self.muontra_window = FormQLMuonTra()
        self.muontra_window.show()

    def thongke(self):
        self.thongke_window = FormThongKe()
        self.thongke_window.show()

    def bandoc(self):
        self.ql_bandoc_window = ql_bandoc()
        self.ql_bandoc_window.show()

    def admin(self):
        self.ql_admin_window = ql_admin()
        self.ql_admin_window.show()

    def theloai(self):
        self.ql_theloai_window = ql_theloai()
        self.ql_theloai_window.show()

    def tacgia(self):
        self.ql_tacgia_window = ql_tacgia()
        self.ql_tacgia_window.show()

    def vipham(self):
        self.ql_vipham_window = ql_vipham()
        self.ql_vipham_window.show()

    def sach(self):
        self.ql_sach_window = FormQLSach()
        self.ql_sach_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = main()
    window.show()

    sys.exit(app.exec())