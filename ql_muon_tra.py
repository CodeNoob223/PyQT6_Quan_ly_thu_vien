import sys
from PyQt6.QtWidgets import QApplication, QPushButton, QMessageBox, QTableWidgetItem, QMainWindow, QListWidgetItem
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import QDate
from datetime import datetime
from ql_muon_tra_ui import Ui_ql_muonTraWindow
from connect_database import ConnectDatabase as ConnectDB


class FormQLMuonTra(QMainWindow):
    maTheMuon = 0
    sachMuon_list = []

    def __init__(self):
        super().__init__()

        self.ui = Ui_ql_muonTraWindow()
        self.ui.setupUi(self)

        self.db = ConnectDB()

        self.maTheMuon = 0
        self.maTheMuon_Line = self.ui.mathemuon_QLineEdit
        self.maBanDoc = self.ui.maBanDoc_comboBox
        self.timBanDoc = self.ui.timBanDoc_lineEdit
        self.maBanDoc.setValidator(QIntValidator())
        self.maAdmin = self.ui.maAdmin_comboBox

        self.ngayTra = self.ui.ngayTra_dateEdit
        self.ngayMuon = self.ui.ngayMuon_dateEdit
        self.ngayTra.setDate(datetime.today())
        self.ngayMuon.setDate(datetime.today())

        self.sachMuon = self.ui.listSachMuon_listWidget
        self.tinhTrang = self.ui.tinhTrang_comboBox

        self.maSach = self.ui.maSach_comboBox
        self.timSach = self.ui.timKiemSach_lineEdit

        self.maSach.setValidator(QIntValidator())
        self.themSachhBtn = self.ui.them_sach_pushButton
        self.xoaSachhBtn = self.ui.xoa_sach_pushButton
        self.traSachBtn = self.ui.tra_sach_pushButton

        self.themBtn = self.ui.them_pushButton
        self.capNhatBtn = self.ui.capNhat_pushButton
        self.chonBtn = self.ui.chon_pushButton
        self.timKiemBtn = self.ui.timKiem_pushButton
        self.lamTrongBtn = self.ui.lamTrong_pushButton
        self.xoaBtn = self.ui.xoa_pushButton

        self.result_table = self.ui.result_table
        self.result_table.setSortingEnabled(False)
        self.buttons_list = self.ui.groupBox_2.findChildren(QPushButton)

        # Initialize signal-slot connections
        self.init_signal_slot()

        # Populate the initial data in the table in the combo-boxes
        self.search_the_muon_tra(True)
        self.fill_combo_box()

    def init_signal_slot(self):
        # connect buttons to their respective functions
        self.themBtn.clicked.connect(self.add_the_muon_tra)
        self.capNhatBtn.clicked.connect(self.update_the_muon_tra)
        self.chonBtn.clicked.connect(self.select_the_muon_tra)
        self.lamTrongBtn.clicked.connect(self.clear_data)
        self.timKiemBtn.clicked.connect(self.search_the_muon_tra)
        self.xoaBtn.clicked.connect(self.delete_the_muon_tra)
        self.themSachhBtn.clicked.connect(self.muon_sach)
        self.xoaSachhBtn.clicked.connect(self.xoa_sach)
        self.traSachBtn.clicked.connect(self.tra_sach)

        # double click table
        self.result_table.mouseDoubleClickEvent = self.custom_mouse_double_click

        # search BAN DOC
        self.timBanDoc.focusInEvent = self.custom_focus_in_event_bandoc
        self.timBanDoc.returnPressed.connect(self.custom_search_event_bandoc)
        self.timBanDoc.editingFinished.connect(
            self.fill_search_result_combo_box_bandoc)

        # detect khi có lựa chọn được chọn trên combo box ban doc
        self.maBanDoc.currentIndexChanged.connect(
            self.assign_search_result_bandoc)

        # search SACH
        self.timSach.focusInEvent = self.custom_focus_in_event_sach
        self.timSach.returnPressed.connect(self.custom_search_event_sach)
        self.timSach.editingFinished.connect(
            self.fill_search_result_combo_box_sach)

        # detect khi có lựa chọn được chọn trên combo box sach
        self.maSach.currentIndexChanged.connect(self.assign_search_result_sach)

    # QLineEdit tim kiem sach
    def custom_focus_in_event_sach(self, event):
        self.timSach.clear()

        super().focusInEvent(event)

    # QLineEdit tim kiem ban doc
    def custom_focus_in_event_bandoc(self, event):
        self.timBanDoc.clear()

        super().focusInEvent(event)

    # QComboBox ket qua tim kiem ban doc
    def assign_search_result_bandoc(self):
        if self.maBanDoc.currentIndex() != -1:
            self.timBanDoc.blockSignals(True)
            self.timBanDoc.setText(self.maBanDoc.currentText())
            self.timBanDoc.blockSignals(False)

    # QComboBox ket qua tim kiem sach
    def assign_search_result_sach(self):
        if self.maSach.currentIndex() != -1:
            self.timSach.blockSignals(True)
            self.timSach.setText(self.maSach.currentText())
            self.timSach.blockSignals(False)

    # Result table double click
    def custom_mouse_double_click(self, event):
        self.select_the_muon_tra()

    # Khi an enter trong QLineEdit ban doc
    def custom_search_event_bandoc(self):
        self.maBanDoc.showPopup()
        self.fill_search_result_combo_box_bandoc()

    # Khi an enter trong QLineEdit sach
    def custom_search_event_sach(self):
        self.maSach.showPopup()
        self.fill_search_result_combo_box_sach()

    def fill_combo_box(self):
        admin_result = self.db.get_all_admin()

        self.maAdmin.clear()

        for item in admin_result:
            self.maAdmin.addItem(item['USERNAME'], item['MAADMIN'])

        self.maAdmin.setCurrentIndex(-1)

        self.fill_search_result_combo_box_bandoc()
        self.fill_search_result_combo_box_sach()

    def fill_search_result_combo_box_bandoc(self):
        banDoc_result = []
        self.maBanDoc.blockSignals(True)
        self.maBanDoc.setCurrentIndex(-1)
        self.maBanDoc.clear()

        if self.timBanDoc.text():
            banDoc_result = self.db.search_bandoc(
                hoten=self.timBanDoc.text().split("#")[0].strip())
        else:
            banDoc_result = self.db.search_bandoc()
        for item in banDoc_result:
            self.maBanDoc.addItem(
                item["HOTEN"] + " #" + str(item["MABANDOC"]), item["MABANDOC"])

        self.maBanDoc.setCurrentIndex(-1)
        self.maBanDoc.blockSignals(False)

    def fill_search_result_combo_box_sach(self):
        sach_result = []
        self.maSach.blockSignals(True)
        self.maSach.setCurrentIndex(-1)
        self.maSach.clear()

        if self.timSach.text():
            sach_result = self.db.search_sach(
                tensach=self.timSach.text().split("#")[0].strip())
        else:
            sach_result = self.db.search_sach()
        for item in sach_result:
            self.maSach.addItem(
                item["TENSACH"] + " #" + str(item["MASACH"]), item["MASACH"])

        self.maSach.setCurrentIndex(-1)
        self.maSach.blockSignals(False)

    def disable_buttons(self):
        for btn in self.buttons_list:
            btn.setProperty('enabled', False)

    def enable_buttons(self):
        for btn in self.buttons_list:
            btn.setProperty('enabled', True)

    def select_the_muon_tra(self):
        # Function to select and populate student information in the form
        self.clear_data()
        select_row = self.result_table.currentRow()
        if select_row != -1:
            self.maTheMuon = int(self.result_table.item(
                select_row, 0).text().strip())
            self.maTheMuon_Line.setText("Mã: #" + self.maTheMuon)
            maBanDoc = self.result_table.item(select_row, 1).text().strip()
            tenAdmin = self.result_table.item(select_row, 2).text().strip()
            ngayMuon = self.result_table.item(select_row, 3).text().strip()
            ngayTra = self.result_table.item(select_row, 4).text().strip()
            sachMuon = self.db.get_sach_muon(self.maTheMuon)
            tinhTrang = self.result_table.item(select_row, 6).text().strip()

            self.timBanDoc.setText(maBanDoc)
            self.maBanDoc.setCurrentText(maBanDoc)
            self.maAdmin.setCurrentText(tenAdmin)

            qdate = QDate.fromString(ngayTra, "yyyy-MM-dd")
            self.ngayTra.setDate(qdate)

            qdate = QDate.fromString(ngayMuon, "yyyy-MM-dd")
            self.ngayMuon.setDate(qdate)

            self.tinhTrang.setCurrentText(tinhTrang)

            self.sachMuon_list = []
            for item in sachMuon:
                newItem = QListWidgetItem()
                newItem.setText(item["TENSACH"] + " (" + str(item["NGAYMUON"]) +
                                ") - (" + str(item["NGAYTRA"]) + ") " + item["TINHTRANG"])
                newItem.value = item["MASACH"]
                newItem.tinhTrang = item["TINHTRANG"]
                newItem.tenSach = item["TENSACH"]
                newItem.ngayMuonTra = " (" + str(item["NGAYMUON"]) + \
                    ") - (" + str(item["NGAYTRA"]) + ") "
                self.sachMuon_list.append(int(item["MASACH"]))
                self.sachMuon.addItem(newItem)
        else:
            QMessageBox.information(self, "Cảnh báo", "Vui lòng chọn một dòng trên bảng.",
                                    QMessageBox.StandardButton.Ok)

    def get_data_from_inputs(self):
        # Lay thong tin sach tu cac Input
        maTheMuon = self.maTheMuon
        maBanDoc = self.maBanDoc.itemData(self.maBanDoc.currentIndex())

        if maBanDoc:
            maBanDoc = int(maBanDoc)
        else:
            if self.timBanDoc.text():
                maBanDoc = int(self.timBanDoc.text().split("#")[1])
                self.maBanDoc.setCurrentText(self.timBanDoc.text())

        maAdmin = self.maAdmin.itemData(self.maAdmin.currentIndex())
        ngayTra = self.ngayTra.text()
        ngayMuon = self.ngayMuon.text()
        tinhTrang = self.tinhTrang.currentText()

        self.sachMuon_list = []
        sachMuonNames_list = []
        for x in range(self.sachMuon.count()):
            self.sachMuon_list.append(self.sachMuon.item(x).value)
            sachMuonNames_list.append(self.sachMuon.item(x).tenSach)

        the_muon_tra = {
            "maBanDoc": maBanDoc,
            "maTheMuon": maTheMuon,
            "maAdmin": maAdmin,
            "ngayTra": ngayTra,
            "ngayMuon": ngayMuon,
            "tinhTrang": tinhTrang,
            "sachMuon": self.sachMuon_list,
            "sachMuonNames": sachMuonNames_list
        }

        return the_muon_tra

    def check_ma_ban_doc(self, mabandoc):
        result = self.db.search_bandoc(mabandoc=mabandoc)
        return result

    def add_the_muon_tra(self):
        self.disable_buttons()
        data = self.get_data_from_inputs()

        if not data["maBanDoc"]:
            QMessageBox.information(
                self, "Cảnh báo", "Mã bạn đọc không được bỏ trống.", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
            return

        check_result = self.check_ma_ban_doc(mabandoc=data["maBanDoc"])

        if not check_result:
            QMessageBox.information(
                self, "Lỗi", "Không có mã bạn đọc.", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
            return

        if not data["maAdmin"]:
            QMessageBox.information(
                self, "Cảnh báo", "Mã thủ thư không được bỏ trống.", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
            return
        if not data["ngayMuon"]:
            QMessageBox.information(
                self, "Cảnh báo", "Ngày mượn không được bỏ trống.", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
            return
        if not data["ngayTra"]:
            QMessageBox.information(
                self, "Cảnh báo", "Ngày trả không được bỏ trống.", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
            return
        ngayMuon = datetime.strptime(
            data["ngayMuon"] + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        ngayTra = datetime.strptime(
            data["ngayTra"] + " 00:00:00", "%Y-%m-%d %H:%M:%S")

        if ngayTra <= datetime.today():
            QMessageBox.information(
                self, "Cảnh báo", "Ngày trả không nhỏ hơn hoặc bằng hôm nay.", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
            return
        if ngayTra <= ngayMuon:
            QMessageBox.information(
                self, "Cảnh báo", "Ngày trả không nhỏ hơn hoặc bằng ngày mượn.", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
            return
        if not data["sachMuon"]:
            QMessageBox.information(
                self, "Cảnh báo", "Phải mượn ít nhất 1 quyển sách.", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
            return
        QMessageBox.information(
            self, "Successfull", "Thêm lịch sử mượn trả thành công.", QMessageBox.StandardButton.Ok)

        self.db.add_the_muon(maAdmin=data["maAdmin"], maBanDoc=data["maBanDoc"], ngayMuon=data["ngayMuon"],
                             ngayTra=data["ngayTra"], sachMuon=data["sachMuon"], tinhTrang=data["tinhTrang"])
        self.search_the_muon_tra(True)

        self.enable_buttons()

    def update_the_muon_tra(self):
        self.disable_buttons()
        data = self.get_data_from_inputs()
        if not data["maTheMuon"]:
            QMessageBox.information(
                self, "Cảnh báo", "Vui lòng chọn một dòng trên bảng.", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
            return
        if not data["maBanDoc"]:
            QMessageBox.information(
                self, "Cảnh báo", "Mã bạn đọc không được bỏ trống.", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
            return
        if not data["maAdmin"]:
            QMessageBox.information(
                self, "Cảnh báo", "Mã thủ thư không được bỏ trống.", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
            return
        if not data["ngayMuon"]:
            QMessageBox.information(
                self, "Cảnh báo", "Ngày mượn không được bỏ trống.", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
            return
        if not data["ngayTra"]:
            QMessageBox.information(
                self, "Cảnh báo", "Ngày trả không được bỏ trống.", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
            return

        ngayMuon = datetime.strptime(
            data["ngayMuon"] + " 12:00:00", "%Y-%m-%d %H:%M:%S")
        ngayTra = datetime.strptime(
            data["ngayTra"] + " 12:00:00", "%Y-%m-%d %H:%M:%S")

        if ngayTra <= ngayMuon:
            QMessageBox.information(
                self, "Cảnh báo", "Ngày trả không nhỏ hơn hoặc bằng ngày mượn.", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
            return
        QMessageBox.information(
            self, "Successfull", "Sửa lịch sử mượn trả thành công.", QMessageBox.StandardButton.Ok)

        data = self.get_data_from_inputs()

        if data["maTheMuon"] > 0:
            self.db.update_the_muon(maTheMuon=data["maTheMuon"], maAdmin=data["maAdmin"], maBanDoc=data["maBanDoc"],
                                    ngayMuon=data["ngayMuon"], ngayTra=data["ngayTra"], tinhTrang=data["tinhTrang"])
            self.search_the_muon_tra(True)
            self.enable_buttons()
        else:
            QMessageBox.information(
                self, "Cảnh báo", "Vui lòng chọn một dòng trên bảng.", QMessageBox.StandardButton.Ok)

    def delete_the_muon_tra(self):
        select_row = self.result_table.currentRow()
        if select_row != -1:
            selected_option = QMessageBox.warning(self, "Cảnh báo", "Bạn có chắc chắn muốn xóa?",
                                                  QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
            if selected_option == QMessageBox.StandardButton.Yes:
                maTheMuon = self.result_table.item(
                    select_row, 0).text().strip()
                delete_result = self.db.delete_the_muon(int(maTheMuon))
                QMessageBox.information(
                    self, "Successful", "Xóa lịch sử mượn trả thành công.", QMessageBox.StandardButton.Ok)

                if not delete_result:
                    self.search_the_muon_tra("none")
                else:
                    QMessageBox.information(
                        self, "Cảnh báo", f"Lỗi: {delete_result}. Vui lòng thử lại.", QMessageBox.StandardButton.Ok)

        else:
            QMessageBox.information(
                self, "Cảnh báo", "Vui lòng một dòng trên bảng.", QMessageBox.StandardButton.Ok)

    def search_the_muon_tra(self, emptySearch: bool):
        if emptySearch:
            the_muon_data_list = self.db.search_the_muon_tra()
            self.show_data(the_muon_data_list)
        else:
            data = self.get_data_from_inputs()
            list = self.db.search_the_muon_tra(maTheMuon=data["maTheMuon"],
                                               maAdmin=data["maAdmin"],
                                               maBanDoc=data["maBanDoc"],
                                               ngayMuon=data["ngayMuon"],
                                               ngayTra=data["ngayTra"],
                                               tinhTrang=data["tinhTrang"],
                                               sachMuon=data["sachMuonNames"])
            self.show_data(list)

    def show_data(self, the_muon_data):
        if the_muon_data:
            self.result_table.setRowCount(0)
            self.result_table.setRowCount(len(the_muon_data))

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
                    self.result_table.setItem(row, column, cell_item)
        else:
            self.result_table.setRowCount(0)
            return

    def clear_data(self):
        self.maTheMuon = 0
        self.maTheMuon_Line.clear()
        self.sachMuon_list = []
        self.maBanDoc.setCurrentIndex(-1)
        self.timBanDoc.clear()
        self.maAdmin.setCurrentIndex(-1)
        self.tinhTrang.setCurrentIndex(-1)
        self.ngayTra.setDate(QDate.fromString("2000-01-01", "yyyy-MM-dd"))
        self.ngayMuon.setDate(QDate.fromString("2000-01-01", "yyyy-MM-dd"))
        self.sachMuon.clear()
        self.timSach.clear()
        self.fill_search_result_combo_box_sach()

    # Ham sach muon
    def muon_sach(self):
        maSach = self.maSach.itemData(self.maSach.currentIndex())

        if not maSach:
            if self.timSach.text():
                temp = self.timSach.text().split("#")
                if len(temp) > 1:
                    maSach = int(temp[1])
                else:
                    QMessageBox.information(
                        self, "Cảnh báo", "Vui lòng nhập tên sách hợp lệ.", QMessageBox.StandardButton.Ok)
                    return
                self.maSach.setCurrentText(self.timSach.text())
            else:
                QMessageBox.information(
                    self, "Cảnh báo", "Vui lòng nhập mã sách.", QMessageBox.StandardButton.Ok)
                return

        maSach = int(maSach)
        result = self.db.search_sach(masach=maSach)

        if not result:
            QMessageBox.information(
                self, "Lỗi", "Mã sách không tồn tại.", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
            return

        for row, info in enumerate(result):
            if int(info["MASACH"]) not in self.sachMuon_list:
                if self.maTheMuon > 0:
                    self.db.add_muon_sach(maSach=info["MASACH"], maTheMuon=self.maTheMuon, ngayTra=self.ngayTra.text(
                    ), ngayMuon=self.ngayMuon.text())
                newItem = QListWidgetItem()
                newItem.setText(info["TENSACH"])
                newItem.value = info["MASACH"]
                newItem.tenSach = info["TENSACH"]
                self.sachMuon.addItem(newItem)
                self.sachMuon_list.append(int(info["MASACH"]))
        if self.maTheMuon > 0:
            self.search_the_muon_tra(True)

    def xoa_sach(self):
        listItems = self.sachMuon.selectedItems()
        if not listItems:
            QMessageBox.information(
                self, "Cảnh báo", "Chọn sách để xóa!", QMessageBox.StandardButton.Ok)
            return

        for item in listItems:
            self.sachMuon.takeItem(self.sachMuon.row(item))
            self.sachMuon_list.remove(int(item.value))
            if self.maTheMuon > 0:
                self.db.delete_muon_sach(
                    maSach=item.value, maTheMuon=self.maTheMuon)

        if self.maTheMuon > 0:
            self.search_the_muon_tra(True)

    def tra_sach(self):
        if self.maTheMuon > 0:
            listItems = self.sachMuon.selectedItems()
            if not listItems:
                QMessageBox.information(
                    self, "Cảnh báo", "Chọn sách để trả!", QMessageBox.StandardButton.Ok)
                return

            for item in listItems:
                item.tinhTrang = "Đã trả"
                item.setText(item.tenSach + item.ngayMuonTra + item.tinhTrang)
                self.db.update_muon_sach(
                    maSach=item.value, maTheMuon=self.maTheMuon, tinhTrang="Đã trả")

            # Kiem tra lieu tat ca sach da duoc tra chua?
            soSachMuon = len(self.sachMuon_list)
            soSachDaTra = 0

            if soSachMuon > 0:
                for x in range(self.sachMuon.count()):
                    if self.sachMuon.item(x).tinhTrang == "Đã trả":
                        soSachDaTra += 1

                if soSachDaTra == soSachDaTra:
                    self.ngayTra.setDate(datetime.today())
                    data = self.get_data_from_inputs()
                    data["tinhTrang"] = "Đã trả"
                    self.db.update_the_muon(maTheMuon=data["maTheMuon"], maAdmin=data["maAdmin"], maBanDoc=data["maBanDoc"],
                                            ngayMuon=data["ngayMuon"], ngayTra=data["ngayTra"], tinhTrang=data["tinhTrang"])
                    self.tinhTrang.setCurrentText("Đã trả")

            self.search_the_muon_tra(True)
        else:
            QMessageBox.information(
                self, "Cảnh báo", "Chọn thẻ mượn trước!", QMessageBox.StandardButton.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = FormQLMuonTra()
    window.show()

    sys.exit(app.exec())
