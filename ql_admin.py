import sys
from PyQt6.QtWidgets import QWidget, QPushButton, QMainWindow, QApplication, QFrame, QMessageBox, QTableWidgetItem
from PyQt6.QtGui import QIntValidator

from ql_admin_ui import Ui_ql_adminWindow
from connect_database import ConnectDatabase


class ql_admin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_ql_adminWindow()
        self.ui.setupUi(self)

        # Creat a database connection object
        self.db = ConnectDatabase()

        # Connect UI elements to class variables
        self.username = self.ui.username_lineEdit
        self.matkhau = self.ui.matkhau_lineEdit
        self.role = self.ui.role_comboBox
        
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
    

    def capNhat_role(self):
        role_result = self.db.get_all_role()

        self.role.clear()

        role_list = [""]
        for item in role_result:
            for k, v in item.items():
                if v != "":
                    role_list.append(v)

        if len(role_list) > 1:
            self.role.addItems(role_list)
    
    def them_info(self):
        self.disable_buttons()

        admin_info = self.get_admin_info()

        if admin_info["username"] and admin_info["matkhau"]:
            check_result = self.check_username(username = admin_info["username"])
            QMessageBox.information(self, "Successful", "Thêm thành công tài khoản admin mới.", QMessageBox.StandardButton.Ok)

            if check_result:
                QMessageBox.information(self, "Lỗi", "Tài khoản đã tồn tại. Vui lòng điền tên tài khoản mới.", QMessageBox.StandardButton.Ok)
                self.enable_buttons()
                return
            
            add_result = self.db.add_admin(username = admin_info["username"],
                                            matkhau = admin_info["matkhau"],
                                            role = admin_info["role"])

            if add_result:
                QMessageBox.information(self, "Lỗi", f"Thêm thất bại: {add_result}, Vui lòng thử lại.", QMessageBox.StandardButton.Ok)

        else:
            QMessageBox.information(self, "Lỗi", "Vui lòng nhập đầy đủ userame và password.", QMessageBox.StandardButton.Ok)


        self.timKiem_info("none")
        self.enable_buttons()


    def timKiem_info(self, flag = "search"):
        if not flag:
            admin_info = self.get_admin_info()
            admin_result = self.db.search_admin(    
                username = admin_info["username"],
                matkhau = admin_info["matkhau"],
                role = admin_info["role"]
            )

            self.show_data(admin_result)
        else:
            admin_result = self.db.search_admin()

            self.show_data(admin_result)


    def capNhat_info(self):
        new_admin_info = self.get_admin_info()

        select_row = self.result_table.currentRow()
        if select_row != 1:
            self.MAADMIN = int(self.result_table.item(select_row, 0).text().strip())
        else:
            QMessageBox.information(self, "Lỗi", f"Vui lòng chọn một dòng trên bảng", QMessageBox.StandardButton.Ok)
            return
            
        if new_admin_info["username"] and self.MAADMIN:
            update_result = self.db.update_admin(
                maadmin=self.MAADMIN,
                username=new_admin_info["username"],
                matkhau=new_admin_info["matkhau"],
                role=new_admin_info["role"]
            )
            QMessageBox.information(self, "Successful", "Cập nhật tài khoản admin thành công.", QMessageBox.StandardButton.Ok)

            if update_result:
                QMessageBox.information(self, "Lỗi", f"Cập nhật thông tin thất bại: {update_result}, Vui lòng thử lại.", QMessageBox.StandardButton.Ok)
            else:
                self.timKiem_info("none")
                self.enable_buttons()
        else:
            QMessageBox.information(self, "Lỗi", f"Vui lòng chọn một dòng trên bảng", QMessageBox.StandardButton.Ok)



    def clear_info(self):
        self.username.clear()
        self.matkhau.clear()
        self.role.clear()

    
    def chon_info(self):
        select_row = self.result_table.currentRow()
        if select_row != -1:
            self.MAADMIN = int(self.result_table.item(select_row, 0).text().strip())
            username = self.result_table.item(select_row, 1).text().strip()
            matkhau = self.result_table.item(select_row, 2).text().strip()
            role = self.result_table.item(select_row, 3).text().strip()

            self.username.setText(username)
            self.matkhau.setText(matkhau)
            self.role.setCurrentText(role)
        else:
            QMessageBox.information(self, "Lỗi", "Vui lòng chọn một dòng trên bảng.", QMessageBox.StandardButton.Ok)


    def xoa_info(self):
        select_row = self.result_table.currentRow()
        if select_row != 1:
            selected_option = QMessageBox.warning(self, "Cảnh báo", "Bạn có chắc chắn muốn xóa?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)

            if selected_option == QMessageBox.StandardButton.Yes:
                self.MAADMIN = self.result_table.item(select_row, 0).text().strip()

                delete_result = self.db.delete_admin(maadmin=self.MAADMIN)
                if not delete_result:
                    self.timKiem_info("none")
                    QMessageBox.information(self, "Successful", "Xóa tài khoản admin thành công.", QMessageBox.StandardButton.Ok)
                else:
                    QMessageBox.information(self, "Thông báo", f"Xóa thất bại: {delete_result}, Vui lòng thử lại.", QMessageBox.StandardButton.Ok)
        else:
            QMessageBox.information(self, "Lỗi", "Vui lòng chọn admin cần xóa.", QMessageBox.StandardButton.Ok)
        

    def disable_buttons(self):
        for button in self.button_list:
            button.setProperty("enabled", False)

    def enable_buttons(self):
        for button in self.button_list:
            button.setProperty("enabled", True)

    def get_admin_info(self):
        username = self.username.text().strip()
        matkhau = self.matkhau.text().strip()
        role = self.role.currentText().strip()

        admin_info = {
            "username": username,
            "matkhau": matkhau,
            "role": role
        }

        return admin_info


    def check_username(self, username):
        result = self.db.search_admin(username=username)

        return result

    def show_data(self, result):
        if result:
            self.result_table.setRowCount(0)
            self.result_table.setRowCount(len(result))

            for row, info in enumerate(result):
                info_list = [
                    info["MAADMIN"],
                    info["USERNAME"],
                    info["MATKHAU"],
                    info["ROLE"],
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

    window = ql_admin()
    window.show()

    sys.exit(app.exec())