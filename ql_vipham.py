import sys
from PyQt6.QtWidgets import QWidget, QPushButton, QMainWindow, QApplication, QFrame, QMessageBox, QTableWidgetItem
from PyQt6.QtGui import QIntValidator

from ql_vipham_ui import Ui_ql_viphamWindow
from connect_database import ConnectDatabase


class ql_vipham(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_ql_viphamWindow()
        self.ui.setupUi(self)

        # Creat a database connection object
        self.db = ConnectDatabase()

        # Connect UI elements to class variables
        self.maRow = self.ui.maRow
        self.soLuongRow = self.ui.soLuongRow
        self.noidung = self.ui.noiDung_lineEdit
        self.maBanDoc = self.ui.maBanDoc_comboBox
        self.timBanDoc = self.ui.timBanDoc_lineEdit
        self.maAdmin = self.ui.maAdmin_comboBox
        self.timAdmin = self.ui.timAdmin

        self.them_pushButton = self.ui.them_pushButton
        self.capNhat_pushButton = self.ui.capNhat_pushButton
        self.chon_pushButton = self.ui.chon_pushButton
        self.timKiem_pushButton = self.ui.timKiem_pushButton
        self.clear_pushButton = self.ui.clear_pushButton
        self.xoa_pushButton = self.ui.xoa_pushButton

        self.result_table = self.ui.tableWidget
        self.result_table.setSortingEnabled(False)
        self.button_list = self.ui.groupBox_2.findChildren(QPushButton)

        # initialize signal-slot connections
        self.init_signal_slot()

        self.timKiem_info("none")

    def init_signal_slot(self):
        self.them_pushButton.clicked.connect(self.them_info)
        self.capNhat_pushButton.clicked.connect(self.capNhat_info)
        self.chon_pushButton.clicked.connect(self.chon_info)
        self.timKiem_pushButton.clicked.connect(self.timKiem_info)
        self.clear_pushButton.clicked.connect(self.clear_info)
        self.xoa_pushButton.clicked.connect(self.xoa_info)

        # double click table
        self.result_table.mouseDoubleClickEvent = self.custom_mouse_double_click

        # search BAN DOC
        self.timBanDoc.focusInEvent = self.custom_focus_in_event_bandoc
        self.timBanDoc.returnPressed.connect(self.custom_search_event_bandoc)
        self.timBanDoc.editingFinished.connect(
            self.fill_search_bandoc_combo_box)

        # detect khi có lựa chọn được chọn trên combo box ban doc
        self.maBanDoc.currentIndexChanged.connect(
            self.assign_search_result_bandoc)

        # search ADMIN
        self.timAdmin.focusInEvent = self.custom_focus_in_event_admin
        self.timAdmin.returnPressed.connect(self.custom_search_event_admin)
        self.timAdmin.editingFinished.connect(
            self.fill_search_admin_combo_box)

        # detect khi có lựa chọn được chọn trên combo box admin
        self.maAdmin.currentIndexChanged.connect(self.assign_search_result_admin)

        self.fill_search_admin_combo_box()
        self.fill_search_bandoc_combo_box()

    # QLineEdit tim kiem ban doc
    def custom_focus_in_event_bandoc(self, event):
        self.timBanDoc.clear()

        super().focusInEvent(event)

    # QLineEdit tim kiem ban doc
    def custom_focus_in_event_admin(self, event):
        self.timAdmin.clear()

        super().focusInEvent(event)

    # QComboBox ket qua tim kiem ban doc
    def assign_search_result_bandoc(self):
        if self.maBanDoc.currentIndex() != -1:
            self.timBanDoc.blockSignals(True)
            self.timBanDoc.setText(self.maBanDoc.currentText())
            self.timBanDoc.blockSignals(False)
    
    # QComboBox ket qua tim kiem admin
    def assign_search_result_admin(self):
        if self.maAdmin.currentIndex() != -1:
            self.timAdmin.blockSignals(True)
            self.timAdmin.setText(self.maAdmin.currentText())
            self.timAdmin.blockSignals(False)

    # Khi an enter trong QLineEdit ban doc
    def custom_search_event_bandoc(self):
        self.maBanDoc.showPopup()
        self.fill_search_bandoc_combo_box()

    # Khi an enter trong QLineEdit admin
    def custom_search_event_admin(self):
        self.maAdmin.showPopup()
        self.fill_search_admin_combo_box()
    
    # Result table double click
    def custom_mouse_double_click(self, event):
        self.chon_info()

    def check_ma_ban_doc(self, mabandoc):
        result = self.db.search_bandoc(mabandoc=mabandoc)
        return result

    def check_ma_admin(self, maadmin):
        result = self.db.search_admin(maadmin=maadmin)
        return result

    def fill_search_admin_combo_box(self):
        admin_result = []
        self.maAdmin.blockSignals(True)
        self.maAdmin.setCurrentIndex(-1)
        self.maAdmin.clear()

        if self.timAdmin.text():
            admin_result = self.db.search_admin(
                username=self.timAdmin.text().split("#")[0].strip())
        else:
            admin_result = self.db.search_admin()
        for item in admin_result:
            self.maAdmin.addItem(
                item["USERNAME"] + " #" + str(item["MAADMIN"]), item["MAADMIN"])

        self.maAdmin.setCurrentIndex(-1)
        self.maAdmin.blockSignals(False)

    def fill_search_bandoc_combo_box(self):
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

    def them_info(self):
        self.disable_buttons()

        vipham_info = self.get_data_from_inputs()

        if vipham_info["mabandoc"] and vipham_info["maadmin"] and vipham_info["noidung"]:
            check_mabandoc = self.check_ma_ban_doc(
                mabandoc=vipham_info["mabandoc"])
            check_maadmin = self.check_ma_admin(maadmin=vipham_info["maadmin"])

            if not check_mabandoc:
                QMessageBox.information(
                    self, "Lỗi", "Không có mã bạn đọc.", QMessageBox.StandardButton.Ok)
                self.enable_buttons()
                return

            if not check_maadmin:
                QMessageBox.information(
                    self, "Lỗi", "Không có admin.", QMessageBox.StandardButton.Ok)
                self.enable_buttons()
                return

            add_result = self.db.add_vipham(mabandoc=vipham_info["mabandoc"],
                                            maadmin=vipham_info["maadmin"],
                                            noidung=vipham_info["noidung"])
            QMessageBox.information(
                self, "Successful", "Thêm vi phạm thành công.", QMessageBox.StandardButton.Ok)

            if add_result:
                QMessageBox.information(
                    self, "Lỗi", f"Thêm thất bại: {add_result}, Vui lòng thử lại.", QMessageBox.StandardButton.Ok)

        else:
            QMessageBox.information(
                self, "Lỗi", "Vui lòng nhập đầy đủ thông tin.", QMessageBox.StandardButton.Ok)

        self.timKiem_info("none")
        self.enable_buttons()

    def timKiem_info(self, flag="search"):
        if not flag:
            vipham_info = self.get_data_from_inputs()
            vipham_result = self.db.search_vipham(
                mabandoc=vipham_info["mabandoc"],
                maadmin=vipham_info["maadmin"],
                noidung=vipham_info["noidung"]
            )

            self.show_data(vipham_result)
        else:
            vipham_result = self.db.search_vipham()

            self.show_data(vipham_result)

    def capNhat_info(self):
        new_vipham_info = self.get_data_from_inputs()

        select_row = self.result_table.currentRow()
        if select_row != 1:
            self.MAVIPHAM = int(self.result_table.item(
                select_row, 0).text().strip())
        else:
            QMessageBox.information(
                self, "Lỗi", f"Vui lòng chọn một dòng trên bảng", QMessageBox.StandardButton.Ok)
            return

        if new_vipham_info["mabandoc"] and self.MAVIPHAM:
            update_result = self.db.update_vipham(
                mavipham=self.MAVIPHAM,
                mabandoc=new_vipham_info["mabandoc"],
                maadmin=new_vipham_info["maadmin"],
                noidung=new_vipham_info["noidung"]
            )
            QMessageBox.information(
                self, "Successful", "Cập nhật vi phạm thành công.", QMessageBox.StandardButton.Ok)

            if update_result:
                QMessageBox.information(
                    self, "Lỗi", f"Cập nhật thông tin thất bại: {update_result}, Vui lòng thử lại.", QMessageBox.StandardButton.Ok)
            else:
                self.timKiem_info("none")
                self.enable_buttons()
        else:
            QMessageBox.information(
                self, "Lỗi", f"Vui lòng chọn một dòng trên bảng", QMessageBox.StandardButton.Ok)

    def clear_info(self):
        self.maRow.clear()
        self.soLuongRow.clear()
        self.maBanDoc.clear()
        self.maAdmin.clear()
        self.noidung.clear()

    def chon_info(self):
        select_row = self.result_table.currentRow()
        if select_row != -1:
            self.MAVIPHAM = int(self.result_table.item(
                select_row, 0).text().strip())
            self.maRow.setText("Mã: #" + str(self.MAVIPHAM))
            mabandoc = self.result_table.item(select_row, 1).text().strip()
            maadmin = self.result_table.item(select_row, 2).text().strip()
            noidung = self.result_table.item(select_row, 3).text().strip()

            self.maBanDoc.setCurrentText(mabandoc)
            self.maAdmin.setCurrentText(maadmin)
            self.noidung.setText(noidung)
        else:
            QMessageBox.information(
                self, "Lỗi", "Vui lòng chọn một dòng trên bảng.", QMessageBox.StandardButton.Ok)

    def xoa_info(self):
        select_row = self.result_table.currentRow()
        if select_row != 1:
            selected_option = QMessageBox.warning(
                self, "Cảnh báo", "Bạn có chắc chắn muốn xóa?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)

            if selected_option == QMessageBox.StandardButton.Yes:
                self.MAVIPHAM = self.result_table.item(
                    select_row, 0).text().strip()
                delete_result = self.db.delete_vipham(mavipham=self.MAVIPHAM)
                QMessageBox.information(
                    self, "Successful", "Xóa vi phạm thành công.", QMessageBox.StandardButton.Ok)

                if not delete_result:
                    self.timKiem_info("none")
                else:
                    QMessageBox.information(
                        self, "Thông báo", f"Xóa thất bại: {delete_result}, Vui lòng thử lại.", QMessageBox.StandardButton.Ok)
        else:
            QMessageBox.information(
                self, "Lỗi", "Vui lòng chọn bạn đọc cần xóa.", QMessageBox.StandardButton.Ok)

    def disable_buttons(self):
        for button in self.button_list:
            button.setProperty("enabled", False)

    def enable_buttons(self):
        for button in self.button_list:
            button.setProperty("enabled", True)

    def get_data_from_inputs(self):
        mabandoc = self.maBanDoc.itemData(self.maBanDoc.currentIndex())
        maadmin = self.maAdmin.itemData(self.maAdmin.currentIndex())
        noidung = self.noidung.text().strip()

        vipham_info = {
            "mabandoc": mabandoc,
            "maadmin": maadmin,
            "noidung": noidung
        }

        return vipham_info

    def show_data(self, result):
        if result:
            self.result_table.setRowCount(0)
            self.result_table.setRowCount(len(result))
            self.soLuongRow.setText("Số lượng: " + str(len(result)))

            for row, info in enumerate(result):
                info_list = [
                    info["MAVIPHAM"],
                    info["MABANDOC"],
                    info["MAADMIN"],
                    info["NOIDUNG"],
                    info["NGAYTHEM"],
                ]

                for column, item in enumerate(info_list):
                    cell_item = QTableWidgetItem(str(item))
                    self.result_table.setItem(row, column, cell_item)

        else:
            self.result_table.setRowCount(0)
            return


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = ql_vipham()
    window.show()

    sys.exit(app.exec())
