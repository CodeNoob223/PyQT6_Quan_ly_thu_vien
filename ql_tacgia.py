import sys
from PyQt6.QtWidgets import QWidget, QPushButton, QMainWindow, QApplication, QFrame, QMessageBox, QTableWidgetItem
from PyQt6.QtGui import QIntValidator

from ql_tacgia_ui import Ui_ql_tacgiaWindow
from connect_database import ConnectDatabase


class ql_tacgia(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_ql_tacgiaWindow()
        self.ui.setupUi(self)

        # Creat a database connection object
        self.db = ConnectDatabase()

        # Connect UI elements to class variables
        self.butdanh = self.ui.butDanh_lineEdit
        
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

        tacgia_info = self.get_tacgia_info()

        if tacgia_info["butdanh"]:
            check_result = self.check_butdanh(butdanh = tacgia_info["butdanh"])

            if check_result:
                QMessageBox.information(self, "Lỗi", "Vui lòng nhập bút danh mới.", QMessageBox.StandardButton.Ok)
                self.enable_buttons()
                return
            
            add_result = self.db.add_tacgia(butdanh = tacgia_info["butdanh"])
            QMessageBox.information(self, "Successful", "Thêm tác giả mới thành công.", QMessageBox.StandardButton.Ok)

            if add_result:
                QMessageBox.information(self, "Lỗi", f"Thêm thất bại: {add_result}, Vui lòng thử lại.", QMessageBox.StandardButton.Ok)

        else:
            QMessageBox.information(self, "Lỗi", "Vui lòng nhập bút danh.", QMessageBox.StandardButton.Ok)


        self.timKiem_info("none")
        self.enable_buttons()


    def timKiem_info(self, flag = "search"):
        if not flag:
            tacgia_info = self.get_tacgia_info()
            tacgia_result = self.db.search_tacgia(    
                butdanh = tacgia_info["butdanh"]
            )

            self.show_data(tacgia_result)
        else:
            tacgia_result = self.db.search_tacgia()

            self.show_data(tacgia_result)


    def capNhat_info(self):
        new_tacgia_info = self.get_tacgia_info()

        select_row = self.result_table.currentRow()
        if select_row != 1:
            self.MATACGIA = int(self.result_table.item(select_row, 0).text().strip())
        else:
            QMessageBox.information(self, "Lỗi", f"Vui lòng chọn một dòng trên bảng", QMessageBox.StandardButton.Ok)
            return
            
        if new_tacgia_info["butdanh"] and self.MATACGIA:
            update_result = self.db.update_tacgia(
                matacgia=self.MATACGIA,
                butdanh=new_tacgia_info["butdanh"]
            )
            QMessageBox.information(self, "Successful", "Cập nhật tác giả thành công.", QMessageBox.StandardButton.Ok)

            if update_result:
                QMessageBox.information(self, "Lỗi", f"Cập nhật thông tin thất bại: {update_result}, Vui lòng thử lại.", QMessageBox.StandardButton.Ok)
            else:
                self.timKiem_info("none")
                self.enable_buttons()
        else:
            QMessageBox.information(self, "Lỗi", f"Vui lòng chọn một dòng trên bảng", QMessageBox.StandardButton.Ok)



    def clear_info(self):
        self.butdanh.clear()

    
    def chon_info(self):
        select_row = self.result_table.currentRow()
        if select_row != -1:
            self.MATACGIA = int(self.result_table.item(select_row, 0).text().strip())
            butdanh = self.result_table.item(select_row, 1).text().strip()

            self.butdanh.setText(butdanh)
        else:
            QMessageBox.information(self, "Lỗi", "Vui lòng chọn một dòng trên bảng.", QMessageBox.StandardButton.Ok)


    def xoa_info(self):
        select_row = self.result_table.currentRow()
        if select_row != 1:
            selected_option = QMessageBox.warning(self, "Cảnh báo", "Bạn có chắc chắn muốn xóa?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)

            if selected_option == QMessageBox.StandardButton.Yes:
                self.MATACGIA = self.result_table.item(select_row, 0).text().strip()

                delete_result = self.db.delete_tacgia(matacgia=self.MATACGIA)
                QMessageBox.information(self, "Successful", "Xóa tác giả thành công.", QMessageBox.StandardButton.Ok)

                if not delete_result:
                    self.timKiem_info("none")
                else:
                    QMessageBox.information(self, "Thông báo", f"Xóa thất bại: {delete_result}, Vui lòng thử lại.", QMessageBox.StandardButton.Ok)
        else:
            QMessageBox.information(self, "Lỗi", "Vui lòng chọn bút danh cần xóa.", QMessageBox.StandardButton.Ok)
        

    def disable_buttons(self):
        for button in self.button_list:
            button.setProperty("enabled", False)

    def enable_buttons(self):
        for button in self.button_list:
            button.setProperty("enabled", True)

    def get_tacgia_info(self):
        butdanh = self.butdanh.text().strip()

        tacgia_info = {
            "butdanh": butdanh
        }

        return tacgia_info


    def check_butdanh(self, butdanh):
        result = self.db.search_tacgia(butdanh=butdanh)

        return result

    def show_data(self, result):
        if result:
            self.result_table.setRowCount(0)
            self.result_table.setRowCount(len(result))

            for row, info in enumerate(result):
                info_list = [
                    info["MATACGIA"],
                    info["BUTDANH"],
                    info["NGAYTHEM"]
                ]

                for column, item in enumerate(info_list):
                    cell_item = QTableWidgetItem(str(item))
                    self.result_table.setItem(row, column, cell_item)

        else:
            self.result_table.setRowCount(0)
            return





if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = ql_tacgia()
    window.show()

    sys.exit(app.exec())