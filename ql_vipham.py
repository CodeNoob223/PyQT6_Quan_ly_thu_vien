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
        self.noidung = self.ui.noiDung_lineEdit
        self.mabandoc = self.ui.maBanDoc_lineEdit
        self.maadmin = self.ui.maAdmin_lineEdit
        
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
    
    def check_ma_ban_doc(self, mabandoc):
        result = self.db.search_bandoc(mabandoc=mabandoc)
        return result
    
    def check_ma_admin(self, maadmin):
        result = self.db.search_admin(maadmin=maadmin)
        return result
    
    def them_info(self):
        self.disable_buttons()

        vipham_info = self.get_vipham_info()

        if vipham_info["mabandoc"] and vipham_info["maadmin"] and vipham_info["noidung"]:
            check_mabandoc = self.check_ma_ban_doc(mabandoc = vipham_info["mabandoc"])
            check_maadmin = self.check_ma_admin(maadmin = vipham_info["maadmin"])

            if not check_mabandoc:
                QMessageBox.information(self, "Lỗi", "Không có mã bạn đọc.", QMessageBox.StandardButton.Ok)
                self.enable_buttons()                
                return
            
            if not check_maadmin:
                QMessageBox.information(self, "Lỗi", "Không có admin.", QMessageBox.StandardButton.Ok)
                self.enable_buttons()                
                return
            
            add_result = self.db.add_vipham(mabandoc = vipham_info["mabandoc"],
                                            maadmin = vipham_info["maadmin"],
                                            noidung = vipham_info["noidung"])
            QMessageBox.information(self, "Successful", "Thêm vi phạm thành công.", QMessageBox.StandardButton.Ok)

            if add_result:
                QMessageBox.information(self, "Lỗi", f"Thêm thất bại: {add_result}, Vui lòng thử lại.", QMessageBox.StandardButton.Ok)

        else:
            QMessageBox.information(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin.", QMessageBox.StandardButton.Ok)


        self.timKiem_info("none")
        self.enable_buttons()


    def timKiem_info(self, flag = "search"):
        if not flag:
            vipham_info = self.get_vipham_info()
            vipham_result = self.db.search_vipham(    
                mabandoc = vipham_info["mabandoc"],
                maadmin = vipham_info["maadmin"],
                noidung = vipham_info["noidung"]
            )

            self.show_data(vipham_result)
        else:
            vipham_result = self.db.search_vipham()

            self.show_data(vipham_result)


    def capNhat_info(self):
        new_vipham_info = self.get_vipham_info()

        select_row = self.result_table.currentRow()
        if select_row != 1:
            self.MAVIPHAM = int(self.result_table.item(select_row, 0).text().strip())
        else:
            QMessageBox.information(self, "Lỗi", f"Vui lòng chọn một dòng trên bảng", QMessageBox.StandardButton.Ok)
            return
            
        if new_vipham_info["mabandoc"] and self.MAVIPHAM:
            update_result = self.db.update_vipham(
                mavipham=self.MAVIPHAM,
                mabandoc=new_vipham_info["mabandoc"],
                maadmin=new_vipham_info["maadmin"],
                noidung=new_vipham_info["noidung"]
            )
            QMessageBox.information(self, "Successful", "Cập nhật vi phạm thành công.", QMessageBox.StandardButton.Ok)

            if update_result:
                QMessageBox.information(self, "Lỗi", f"Cập nhật thông tin thất bại: {update_result}, Vui lòng thử lại.", QMessageBox.StandardButton.Ok)
            else:
                self.timKiem_info("none")
                self.enable_buttons()
        else:
            QMessageBox.information(self, "Lỗi", f"Vui lòng chọn một dòng trên bảng", QMessageBox.StandardButton.Ok)



    def clear_info(self):
        self.mabandoc.clear()
        self.maadmin.clear()
        self.noidung.clear()

    
    def chon_info(self):
        select_row = self.result_table.currentRow()
        if select_row != -1:
            self.MAVIPHAM = int(self.result_table.item(select_row, 0).text().strip())
            mabandoc = self.result_table.item(select_row, 1).text().strip()
            maadmin = self.result_table.item(select_row, 2).text().strip()
            noidung = self.result_table.item(select_row, 3).text().strip()

            self.mabandoc.setText(mabandoc)
            self.maadmin.setText(maadmin)
            self.noidung.setText(noidung)
        else:
            QMessageBox.information(self, "Lỗi", "Vui lòng chọn một dòng trên bảng.", QMessageBox.StandardButton.Ok)


    def xoa_info(self):
        select_row = self.result_table.currentRow()
        if select_row != 1:
            selected_option = QMessageBox.warning(self, "Cảnh báo", "Bạn có chắc chắn muốn xóa?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)

            if selected_option == QMessageBox.StandardButton.Yes:
                self.MAVIPHAM = self.result_table.item(select_row, 0).text().strip()
                delete_result = self.db.delete_vipham(mavipham=self.MAVIPHAM)
                QMessageBox.information(self, "Successful", "Xóa vi phạm thành công.", QMessageBox.StandardButton.Ok)

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

    def get_vipham_info(self):
        mabandoc = self.mabandoc.text().strip()
        maadmin = self.maadmin.text().strip()
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