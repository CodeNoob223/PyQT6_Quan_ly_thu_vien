import sys

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QWidget, QPushButton, QMainWindow, QApplication, QFrame, QMessageBox, QTableWidgetItem
from PyQt6.QtGui import QIntValidator

from ql_bandoc_ui import Ui_ql_bandocWindow
from connect_database import ConnectDatabase


class ql_bandoc(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_ql_bandocWindow()
        self.ui.setupUi(self)

        # Creat a database connection object
        self.db = ConnectDatabase()

        # Connect UI elements to class variables
        self.hoten = self.ui.hoTen_lineEdit
        self.ngaysinh = self.ui.dateEdit
        self.diachi = self.ui.diaChi_lineEdit
        self.sdt = self.ui.soDienThoai_lineEdit
        
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
    
    
    def them_info(self):
        self.disable_buttons()

        bandoc_info = self.get_bandoc_info()

        if bandoc_info["hoten"] and bandoc_info["ngaysinh"] and bandoc_info["diachi"] and bandoc_info["sdt"]:
            add_result = self.db.add_bandoc(hoten = bandoc_info["hoten"],
                                            ngaysinh = bandoc_info["ngaysinh"],
                                            diachi = bandoc_info["diachi"],
                                            sdt = bandoc_info["sdt"])

            if add_result:
                QMessageBox.information(self, "Lỗi", f"Thêm thất bại: {add_result}, Vui lòng thử lại.", QMessageBox.StandardButton.Ok)
            else:
                QMessageBox.information(self, "Successful", "Thêm bạn đọc thành công.", QMessageBox.StandardButton.Ok)


        else:
            QMessageBox.information(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin bạn đọc.", QMessageBox.StandardButton.Ok)


        self.timKiem_info("none")
        self.enable_buttons()


    def timKiem_info(self, flag = "search"):
        if not flag:
            bandoc_info = self.get_bandoc_info()
            bandoc_result = self.db.search_bandoc(    
                hoten = bandoc_info["hoten"],
                ngaysinh = bandoc_info["ngaysinh"],
                diachi = bandoc_info["diachi"],
                sdt = bandoc_info["sdt"]
            )

            self.show_data(bandoc_result)
        else:
            bandoc_result = self.db.search_bandoc()

            self.show_data(bandoc_result)


    def capNhat_info(self):
        new_bandoc_info = self.get_bandoc_info()

        select_row = self.result_table.currentRow()
        if select_row != 1:
            self.MABANDOC = int(self.result_table.item(select_row, 0).text().strip())
        else:
            QMessageBox.information(self, "Lỗi", f"Vui lòng chọn một dòng trên bảng", QMessageBox.StandardButton.Ok)
            return
            
        if new_bandoc_info["hoten"] and self.MABANDOC:
            update_result = self.db.update_bandoc(
                mabandoc=self.MABANDOC,
                hoten=new_bandoc_info["hoten"],
                ngaysinh=new_bandoc_info["ngaysinh"],
                diachi=new_bandoc_info["diachi"],
                sdt=new_bandoc_info["sdt"]
            )
            QMessageBox.information(self, "Successful", "Cập nhật bạn đọc thành công.", QMessageBox.StandardButton.Ok)

            if update_result:
                QMessageBox.information(self, "Lỗi", f"Cập nhật thông tin thất bại: {update_result}, Vui lòng thử lại.", QMessageBox.StandardButton.Ok)
            else:
                self.timKiem_info("none")
                self.enable_buttons()
        else:
            QMessageBox.information(self, "Lỗi", f"Vui lòng chọn một dòng trên bảng", QMessageBox.StandardButton.Ok)



    def clear_info(self):
        self.hoten.clear()
        self.ngaysinh.setDate(QDate.fromString("2000-01-01", "yyyy-MM-dd"))
        self.diachi.clear()
        self.sdt.clear()

    
    def chon_info(self):
        select_row = self.result_table.currentRow()
        if select_row != -1:
            self.MABANDOC = int(self.result_table.item(select_row, 0).text().strip())
            hoten = self.result_table.item(select_row, 1).text().strip()
            ngaysinh = self.result_table.item(select_row, 2).text().strip()
            diachi = self.result_table.item(select_row, 3).text().strip()
            sdt = self.result_table.item(select_row, 4).text().strip()

            self.hoten.setText(hoten)
            qdate = QDate.fromString(ngaysinh, "yyyy-MM-dd")
            self.ngaysinh.setDate(qdate)
            self.diachi.setText(diachi)
            self.sdt.setText(sdt)
        else:
            QMessageBox.information(self, "Lỗi", "Vui lòng chọn một dòng trên bảng.", QMessageBox.StandardButton.Ok)


    def xoa_info(self):
        select_row = self.result_table.currentRow()
        if select_row != 1:
            selected_option = QMessageBox.warning(self, "Cảnh báo", "Bạn có chắc chắn muốn xóa?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)

            if selected_option == QMessageBox.StandardButton.Yes:
                self.MABANDOC = self.result_table.item(select_row, 0).text().strip()
                delete_result = self.db.delete_bandoc(mabandoc=self.MABANDOC)
                QMessageBox.information(self, "Successful", "Xóa bạn đọc thành công.", QMessageBox.StandardButton.Ok)

                if not delete_result:
                    self.timKiem_info("none")
                else:
                    QMessageBox.information(self, "Thông báo", f"Xóa thất bại: {delete_result}, Vui lòng thử lại.", QMessageBox.StandardButton.Ok)
        else:
            QMessageBox.information(self, "Lỗi", "Vui lòng chọn bạn đọc cần xóa.", QMessageBox.StandardButton.Ok)
        

    def disable_buttons(self):
        for button in self.button_list:
            button.setProperty("enabled", False)

    def enable_buttons(self):
        for button in self.button_list:
            button.setProperty("enabled", True)

    def get_bandoc_info(self):
        hoten = self.hoten.text().strip()
        ngaysinh = self.ngaysinh.text().strip()
        diachi = self.diachi.text().strip()
        sdt = self.sdt.text().strip()

        bandoc_info = {
            "hoten": hoten,
            "ngaysinh": ngaysinh,
            "diachi": diachi,
            "sdt": sdt
        }

        return bandoc_info


    def check_hoten(self, hoten):
        result = self.db.search_bandoc(hoten=hoten)

        return result

    def show_data(self, result):
        if result:
            self.result_table.setRowCount(0)
            self.result_table.setRowCount(len(result))

            for row, info in enumerate(result):
                info_list = [
                    info["MABANDOC"],
                    info["HOTEN"],
                    info["NGAYSINH"],
                    info["DIACHI"],
                    info["SDT"],
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

    window = ql_bandoc()
    window.show()

    sys.exit(app.exec())