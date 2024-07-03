import sys
from PyQt6.QtWidgets import QWidget, QPushButton, QMainWindow, QApplication, QFrame, QMessageBox, QTableWidgetItem
from PyQt6.QtGui import QIntValidator

from ql_theloai_ui import Ui_ql_theloaiWindow
from connect_database import ConnectDatabase


class ql_theloai(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_ql_theloaiWindow()
        self.ui.setupUi(self)

        # Creat a database connection object
        self.db = ConnectDatabase()

        # Connect UI elements to class variables
        self.ten = self.ui.tenTheLoai_lineEdit
        
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

        theloai_info = self.get_theloai_info()

        if theloai_info["ten"]:
            check_result = self.check_ten(ten = theloai_info["ten"])

            if check_result:
                QMessageBox.information(self, "Lỗi", "Vui lòng nhập tên thể loại mới.", QMessageBox.StandardButton.Ok)
                self.enable_buttons()
                return
            
            add_result = self.db.add_theloai(ten = theloai_info["ten"])
            QMessageBox.information(self, "Successful", "Thêm thể loại mới thành công.", QMessageBox.StandardButton.Ok)

            if add_result:
                QMessageBox.information(self, "Lỗi", f"Thêm thất bại: {add_result}, Vui lòng thử lại.", QMessageBox.StandardButton.Ok)

        else:
            QMessageBox.information(self, "Lỗi", "Vui lòng nhập tên thể loại.", QMessageBox.StandardButton.Ok)


        self.timKiem_info("none")
        self.enable_buttons()


    def timKiem_info(self, flag = "search"):
        if not flag:
            theloai_info = self.get_theloai_info()
            theloai_result = self.db.search_theloai(    
                ten = theloai_info["ten"]
            )

            self.show_data(theloai_result)
        else:
            theloai_result = self.db.search_theloai()

            self.show_data(theloai_result)


    def capNhat_info(self):
        new_theloai_info = self.get_theloai_info()

        select_row = self.result_table.currentRow()
        if select_row != 1:
            self.MATHELOAI = int(self.result_table.item(select_row, 0).text().strip())
        else:
            QMessageBox.information(self, "Lỗi", f"Vui lòng chọn một dòng trên bảng", QMessageBox.StandardButton.Ok)
            return
            
        if new_theloai_info["ten"] and self.MATHELOAI:
            update_result = self.db.update_theloai(
                matheloai=self.MATHELOAI,
                ten=new_theloai_info["ten"]
            )
            QMessageBox.information(self, "Successful", "Cập nhật thể loại thành công.", QMessageBox.StandardButton.Ok)

            if update_result:
                QMessageBox.information(self, "Lỗi", f"Cập nhật thông tin thất bại: {update_result}, Vui lòng thử lại.", QMessageBox.StandardButton.Ok)
            else:
                self.timKiem_info("none")
                self.enable_buttons()
        else:
            QMessageBox.information(self, "Lỗi", f"Vui lòng chọn một dòng trên bảng", QMessageBox.StandardButton.Ok)



    def clear_info(self):
        self.ten.clear()

    
    def chon_info(self):
        select_row = self.result_table.currentRow()
        if select_row != -1:
            self.MATHELOAI = int(self.result_table.item(select_row, 0).text().strip())
            ten = self.result_table.item(select_row, 1).text().strip()

            self.ten.setText(ten)
        else:
            QMessageBox.information(self, "Lỗi", "Vui lòng chọn một dòng trên bảng.", QMessageBox.StandardButton.Ok)


    def xoa_info(self):
        select_row = self.result_table.currentRow()
        if select_row != 1:
            selected_option = QMessageBox.warning(self, "Cảnh báo", "Bạn có chắc chắn muốn xóa?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)

            if selected_option == QMessageBox.StandardButton.Yes:
                self.MATHELOAI = self.result_table.item(select_row, 0).text().strip()

                delete_result = self.db.delete_theloai(matheloai=self.MATHELOAI)
                QMessageBox.information(self, "Successful", "Xóa thể loại thành công.", QMessageBox.StandardButton.Ok)

                if not delete_result:
                    self.timKiem_info("none")
                else:
                    QMessageBox.information(self, "Thông báo", f"Xóa thất bại: {delete_result}, Vui lòng thử lại.", QMessageBox.StandardButton.Ok)
        else:
            QMessageBox.information(self, "Lỗi", "Vui lòng chọn thể loại cần xóa.", QMessageBox.StandardButton.Ok)
        

    def disable_buttons(self):
        for button in self.button_list:
            button.setProperty("enabled", False)

    def enable_buttons(self):
        for button in self.button_list:
            button.setProperty("enabled", True)

    def get_theloai_info(self):
        ten = self.ten.text().strip()

        theloai_info = {
            "ten": ten
        }

        return theloai_info


    def check_ten(self, ten):
        result = self.db.search_theloai(ten=ten)

        return result

    def show_data(self, result):
        if result:
            self.result_table.setRowCount(0)
            self.result_table.setRowCount(len(result))

            for row, info in enumerate(result):
                info_list = [
                    info["MATHELOAI"],
                    info["TEN"]
                ]

                for column, item in enumerate(info_list):
                    cell_item = QTableWidgetItem(str(item))
                    self.result_table.setItem(row, column, cell_item)

        else:
            self.result_table.setRowCount(0)
            return





if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = ql_theloai()
    window.show()

    sys.exit(app.exec())