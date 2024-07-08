import sys
from PyQt6.QtWidgets import QWidget, QPushButton, QMainWindow, QApplication, QFrame, QMessageBox, QTableWidgetItem
from PyQt6.QtGui import QIntValidator
from datetime import datetime
from thongke_ui import Ui_thongKeWindow
from connect_database import ConnectDatabase


class FormThongKe(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_thongKeWindow()
        self.ui.setupUi(self)

        self.db = ConnectDatabase()

        self.soSach = self.ui.soSach
        self.soBanDoc = self.ui.soBanDoc
        self.soViPham = self.ui.soViPham
        self.soTheLoai = self.ui.soTheLoai
        self.soTacGia = self.ui.soTacGia
        self.soLanMuon = self.ui.soMuonTra

        self.viPhamTable = self.ui.viPham_tableWidget
        self.sachChuaTraTable = self.ui.sachChuaTra_tableWidget

        self.soLuongViPham = self.ui.soLuongRow_viPham
        self.soLuongSachChuaTra = self.ui.soLuongRow_sachChuaTra

        self.maTheMuon = self.ui.maSachMuon
        self.maViPham = self.ui.maViPham

        self.ngayTra = self.ui.ngayTra_dateEdit
        self.ngayTra.setDate(datetime.today())

        self.tienPhat = self.ui.tienPhat_lineEdit
        self.tienPhat.setValidator(QIntValidator())

        self.traSachBtn = self.ui.traSach_pushButton
        self.chonTheMuonBtn = self.ui.chonTheMuonBtn
        self.nopPhatBtn = self.ui.nopPhat_pushButton
        self.chonViPhamBtn = self.ui.chonViPhamBtn

        self.fill_table_sach_chua_tra()
        self.fill_table_vi_pham()
        self.fill_so_luong()
        self.init_signal_slot()

    def init_signal_slot(self):
        self.traSachBtn.clicked.connect(self.tra_sach)
        self.nopPhatBtn.clicked.connect(self.nop_phat)
        self.chonViPhamBtn.clicked.connect(self.chon_vi_pham)
        self.chonTheMuonBtn.clicked.connect(self.chon_the_muon)

        self.viPhamTable.mouseDoubleClickEvent = self.custom_mouse_double_click_vipham
        self.sachChuaTraTable.mouseDoubleClickEvent = self.custom_mouse_double_click_themuontra

    # Result table double click
    def custom_mouse_double_click_vipham(self, event):
        self.chon_vi_pham()

    def chon_vi_pham(self):
        select_row = self.viPhamTable.currentRow()
        if select_row != -1:
            maViPham = self.viPhamTable.item(
                select_row, 0).text().strip()
            tienPhat = self.viPhamTable.item(
                select_row, 4).text().strip()
            self.maViPham.setText("Mã: #" + str(maViPham))
            self.tienPhat.setText(tienPhat)
        else:
            QMessageBox.information(
                self, "Cảnh báo", "Chọn vi phạm trước!", QMessageBox.StandardButton.Ok)

    # Result table double click
    def custom_mouse_double_click_themuontra(self, event):
        self.chon_the_muon()

    def chon_the_muon(self):
        select_row = self.sachChuaTraTable.currentRow()
        if select_row != -1:
            maTheMuon = self.sachChuaTraTable.item(
                select_row, 0).text().strip()

            self.maTheMuon.setText("Mã: #" + str(maTheMuon))
        else:
            QMessageBox.information(
                self, "Cảnh báo", "Chọn thẻ mượn trước!", QMessageBox.StandardButton.Ok)

    def tra_sach(self):
        maTheMuon = self.maTheMuon.text()

        if maTheMuon:
            maTheMuon = maTheMuon.split("#")[1].strip()
            ngayTra = self.ngayTra.text()
            self.db.hoanthanh_themuon(maTheMuon, ngayTra)
            self.fill_table_sach_chua_tra()
            self.maTheMuon.clear()
        else:
            QMessageBox.information(
                self, "Cảnh báo", "Chọn thẻ mượn trước!", QMessageBox.StandardButton.Ok)

    def nop_phat(self):
        maViPham = self.maViPham.text()

        if maViPham:
            maViPham = maViPham.split("#")[1].strip()
            tienPhat = self.tienPhat.text()

            if tienPhat:
                self.db.nop_phat(maViPham, tienPhat)
                self.fill_table_vi_pham()
                self.maViPham.clear()
            else:
                QMessageBox.information(
                    self, "Cảnh báo", "Phải nhập tiền phạt!", QMessageBox.StandardButton.Ok)
        else:
            QMessageBox.information(
                self, "Cảnh báo", "Chọn vi phạm trước!", QMessageBox.StandardButton.Ok)

    def fill_table_vi_pham(self):
        result = self.db.search_vipham(tinhtrang="Chưa nộp phạt")
        if result:
            self.viPhamTable.setRowCount(0)
            self.viPhamTable.setRowCount(len(result))
            self.soLuongViPham.setText("Số lượng: " + str(len(result)))

            for row, info in enumerate(result):
                info_list = [
                    info["MAVIPHAM"],
                    info["HOTEN"] + " #" + str(info["MABANDOC"]),
                    info["USERNAME"] + " #" + str(info["MAADMIN"]),
                    info["NOIDUNG"],
                    info["TIENPHAT"],
                    info["TINHTRANG"],
                    info["NGAYTHEM"],
                ]

                for column, item in enumerate(info_list):
                    cell_item = QTableWidgetItem(str(item))
                    self.viPhamTable.setItem(row, column, cell_item)

        else:
            self.viPhamTable.setRowCount(0)
            return

    def fill_table_sach_chua_tra(self):
        the_muon_data = self.db.search_the_muon_tra(tinhTrang="Chưa trả")
        if the_muon_data:
            self.sachChuaTraTable.setRowCount(0)
            self.sachChuaTraTable.setRowCount(len(the_muon_data))
            self.soLuongSachChuaTra.setText(
                "Số lượng: " + str(len(the_muon_data)))

            for row, info in enumerate(the_muon_data):
                sach_muon_list = self.db.get_sach_muon(info["MATHEMUON"])
                sach_muon = ""

                for item in sach_muon_list:
                    sach_muon += item["TENSACH"] + ";"

                info_list = [
                    info["MATHEMUON"],
                    info["HOTEN"] + " #" + str(info["MABANDOC"]),
                    info["USERNAME"],
                    info["NGAYMUON"],
                    info["NGAYTRA"],
                    sach_muon,
                    info["TINHTRANG"],
                    info["NGAYCAPNHAT"],
                    info["NGAYTHEM"]
                ]
                for column, item in enumerate(info_list):
                    cell_item = QTableWidgetItem(str(item))
                    self.sachChuaTraTable.setItem(row, column, cell_item)
        else:
            self.sachChuaTraTable.setRowCount(0)
            return

    def fill_so_luong(self):
        data = self.db.get_all_so_luong()

        self.soSach.setText(str(data["sach"]))
        self.soBanDoc.setText(str(data["bandoc"]))
        self.soTacGia.setText(str(data["tacgia"]))
        self.soTheLoai.setText(str(data["theloai"]))
        self.soLanMuon.setText(str(data["themuontra"]))
        self.soViPham.setText(str(data["vipham"]))

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = FormThongKe()
    window.show()

    sys.exit(app.exec())
