import sys
from PyQt6.QtWidgets import QApplication, QPushButton, QMessageBox, QTableWidgetItem, QMainWindow
from PyQt6.QtGui import QIntValidator, QPixmap

from ql_sach_ui import Ui_ql_sachWindow
from connect_database import ConnectDatabase as ConnectDB

class FormQLSach(QMainWindow):
    maSach = 0

    def __init__(self):
        super().__init__()

        # Init the UI from a separate UI file
        self.ui = Ui_ql_sachWindow()
        self.ui.setupUi(self)

        # Create a database connection object
        self.db = ConnectDB()

        # Connect UI elements to class variables
        self.maSach = 0
        self.maRow = self.ui.maRow
        self.soLuongRow = self.ui.soLuongRow
        self.tenSach = self.ui.tenSach_lineEdit
        self.viTri = self.ui.viTri_lineEdit
        self.tomTat = self.ui.tomTat_textEdit
        self.anhSach = self.ui.anhSach_lineEdit

        self.soLuong = self.ui.soLuong_lineEdit
        self.soLuong.setValidator(QIntValidator())

        self.maTheLoai = self.ui.theLoai_comboBox
        self.maTacGia = self.ui.tacGia_comboBox

        self.themBtn = self.ui.them_pushButton
        self.capNhatBtn = self.ui.capNhat_pushButton
        self.chonBtn = self.ui.chon_pushButton
        self.timKiemBtn = self.ui.timKiem_pushButton
        self.lamTrongBtn = self.ui.lamTrong_pushButton
        self.xoaBtn = self.ui.xoa_pushButton
        self.image_label = self.ui.image_label

        self.result_table = self.ui.tableWidget
        self.result_table.setSortingEnabled(False)
        self.buttons_list = self.ui.groupBox_2.findChildren(QPushButton)

        # double click table
        self.result_table.mouseDoubleClickEvent = self.custom_mouse_double_click

        # Initialize signal-slot connections
        self.init_signal_slot()

        # Populate the initial data in the table in the combo-boxes
        self.search_sach(True)
        self.fill_combo_box()

    def init_signal_slot(self):
        # connect buttons to their respective functions
        self.themBtn.clicked.connect(self.add_sach)
        self.capNhatBtn.clicked.connect(self.update_sach)
        self.chonBtn.clicked.connect(self.select_sach_info)
        self.lamTrongBtn.clicked.connect(self.clear_data)
        self.timKiemBtn.clicked.connect(self.search_sach)
        self.xoaBtn.clicked.connect(self.delete_sach)

    # Result table double click
    def custom_mouse_double_click(self, event):
        self.select_sach_info()

    def attach_image(self, path : str):
        mypmap = QPixmap(path)
        self.image_label.setPixmap(mypmap)
        self.image_label.setMask(mypmap.mask())
    
    def add_sach(self):
        self.disable_buttons()
        sach_info = self.get_sach_info()

        if sach_info["soLuong"] < 1:
            QMessageBox.information(
                self, "Cảnh báo", "Số lượng không được nhỏ hơn 1", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
                
            return
        if sach_info["viTri"] == "":
            QMessageBox.information(
                self, "Cảnh báo", "Vị trí không được bỏ trống", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
                
            return
        if sach_info["tenSach"] == "":
            QMessageBox.information(
                self, "Cảnh báo", "Tên sách không được bỏ trống", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
                
            return
        if sach_info["tomTat"] == "":
            QMessageBox.information(
                self, "Cảnh báo", "Tóm tắt không được bỏ trống", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
                
            return
        if sach_info["anhSach"] == "":
            QMessageBox.information(
                self, "Cảnh báo", "Ảnh sách không được bỏ trống", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
                
            return
        if sach_info["maTheLoai"] == "":
            QMessageBox.information(
                self, "Cảnh báo", "Thể loại không được bỏ trống", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
                
            return
        if sach_info["maTacGia"] == "":
            QMessageBox.information(
                self, "Cảnh báo", "Tác giả không được bỏ trống", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
                
            return

        add_result = self.db.add_sach(
            matheloai=sach_info["maTheLoai"],
            matacgia=sach_info["maTacGia"],
            soluong=sach_info["soLuong"],
            tensach=sach_info["tenSach"],
            anhsach=sach_info["anhSach"],
            vitri=sach_info["viTri"],
            tomtat=sach_info["tomTat"]
        )
        QMessageBox.information(self, "Successful", "Thêm sách thành công.", QMessageBox.StandardButton.Ok)

        if add_result:
            QMessageBox.information(
                self, "Cảnh báo", f"Lỗi: {add_result}", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
                
            return
        self.search_sach(True)
        self.enable_buttons()
        

    def get_sach_info(self):
        # Lay thong tin sach tu cac Input
        maSach = self.maSach
        maTheLoai = self.maTheLoai.itemData(self.maTheLoai.currentIndex())
        maTacGia = self.maTacGia.itemData(self.maTacGia.currentIndex())
        tenSach = self.tenSach.text().strip()
        soLuong = self.soLuong.text().strip()
        if soLuong:
            soLuong = int(soLuong)
        else:
            soLuong = 0
        tomTat = self.tomTat.toPlainText()
        viTri = self.viTri.text().strip()
        anhSach = self.anhSach.text().strip()

        sachInfo = {
            "maSach": maSach,
            "maTheLoai": maTheLoai,
            "maTacGia": maTacGia,
            "tenSach": tenSach,
            "soLuong": soLuong,
            "tomTat": tomTat,
            "viTri": viTri,
            "anhSach": anhSach
        }

        return sachInfo

    def update_sach(self):
        self.disable_buttons()
        sach_info = self.get_sach_info()

        if not sach_info["maSach"]:
            QMessageBox.information(
                self, "Cảnh báo", "Mã sách không được bỏ trống", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
            return
        if sach_info["soLuong"] < 1:
            QMessageBox.information(
                self, "Cảnh báo", "Số lượng không được nhỏ hơn 1", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
            return
        if sach_info["viTri"] == "":
            QMessageBox.information(
                self, "Cảnh báo", "Vị trí không được bỏ trống", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
            return
        if sach_info["tenSach"] == "":
            QMessageBox.information(
                self, "Cảnh báo", "Tên sách không được bỏ trống", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
            return
        if sach_info["tomTat"] == "":
            QMessageBox.information(
                self, "Cảnh báo", "Tóm tắt không được bỏ trống", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
            return
        if sach_info["anhSach"] == "":
            QMessageBox.information(
                self, "Cảnh báo", "Ảnh sách không được bỏ trống", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
            return
        if sach_info["maTheLoai"] == "":
            QMessageBox.information(
                self, "Cảnh báo", "Thể loại không được bỏ trống", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
            return
        if sach_info["maTacGia"] == "":
            QMessageBox.information(
                self, "Cảnh báo", "Tác giả không được bỏ trống", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
            return

        add_result = self.db.update_sach(
            masach=sach_info["maSach"],
            matheloai=sach_info["maTheLoai"],
            matacgia=sach_info["maTacGia"],
            soluong=sach_info["soLuong"],
            tensach=sach_info["tenSach"],
            anhsach=sach_info["anhSach"],
            vitri=sach_info["viTri"],
            tomtat=sach_info["tomTat"]
        )
        QMessageBox.information(self, "Successful", "Cập nhật sách thành công.", QMessageBox.StandardButton.Ok)
        if add_result:
            QMessageBox.information(
                self, "Cảnh báo", f"Lỗi: {add_result}", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
            return
        self.search_sach(True)
        self.enable_buttons()

    def delete_sach(self):
        # Function to delete student information
        select_row = self.result_table.currentRow()
        if select_row != -1:
            selected_option = QMessageBox.warning(self, "Cảnh báo", "Bạn có chắc chắn muốn xóa?",
                                                  QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)

            if selected_option == QMessageBox.StandardButton.Yes:
                sach_id = self.result_table.item(
                    select_row, 0).text().strip()

                delete_result = self.db.delete_sach(int(sach_id))
                QMessageBox.information(self, "Successful", "Xóa sách thành công.", QMessageBox.StandardButton.Ok)

                if not delete_result:
                    self.search_sach(True)
                else:
                    QMessageBox.information(self, "Cảnh báo", f"Lỗi: {delete_result}. Vui lòng thử lại.", QMessageBox.StandardButton.Ok)

        else:
            QMessageBox.information(self, "Cảnh báo", "Vui lòng một dòng trên bảng.", QMessageBox.StandardButton.Ok)

    def select_sach_info(self):
        # Function to select and populate student information in the form
        select_row = self.result_table.currentRow()
        if select_row != -1:
            self.maSach = int(self.result_table.item(select_row, 0).text().strip())
            self.maRow.setText("Mã: #" + str(self.maSach))
            tenSach = self.result_table.item(select_row, 1).text().strip()
            maTheLoai = self.result_table.item(select_row, 2).text().strip()
            maTacGia = self.result_table.item(select_row, 3).text().strip()
            soLuong = self.result_table.item(select_row, 4).text().strip()
            viTri = self.result_table.item(select_row, 5).text().strip()
            tomTat = self.result_table.item(select_row, 6).text().strip()
            anhSach = self.result_table.item(select_row, 7).text().strip()

            self.attach_image(anhSach)

            self.tenSach.setText(tenSach)
            self.maTheLoai.setCurrentText(maTheLoai)
            self.maTacGia.setCurrentText(maTacGia)
            self.soLuong.setText(soLuong)
            self.viTri.setText(viTri)
            self.tomTat.setText(tomTat)
            self.anhSach.setText(anhSach)
        else:
            QMessageBox.information(self, "Cảnh báo", "Vui lòng chọn một dòng trên bảng.",
                                    QMessageBox.StandardButton.Ok)

    def clear_data(self):
        self.maSach = 0
        self.maRow.clear()
        self.soLuongRow.clear()
        self.maTheLoai.setCurrentIndex(-1)
        self.maTacGia.setCurrentIndex(-1)
        self.soLuong.clear()
        self.tomTat.clear()
        self.viTri.clear()
        self.tenSach.clear()
        self.anhSach.clear()
        self.attach_image("D:/Designer QLTV/anhSach/placeholder.jpg")
        self.search_sach(True)

    def search_sach(self, emptySearch : bool):
        
        if not emptySearch: 
            sach_info = self.get_sach_info() # Lay thong tin sach tu input
            sach_result = self.db.search_sach(
                anhsach=sach_info["anhSach"],
                masach=sach_info["maSach"],
                matacgia=sach_info["maTacGia"],
                matheloai=sach_info["maTheLoai"],
                soluong=sach_info["soLuong"],
                tensach=sach_info["tenSach"],
                tomtat=sach_info["tomTat"],
                vitri=sach_info["viTri"]
            )

            if type(sach_result) == list:
                self.show_data(sach_result)
            else:
                QMessageBox.information(self, "Lỗi", f"Lỗi: {sach_result}", QMessageBox.StandardButton.Ok)
                return
        else:
            sach_result = self.db.search_sach()
            if type(sach_result) == list:
                self.show_data(sach_result)
            else:
                QMessageBox.information(self, "Lỗi", f"Lỗi: {sach_result}",
                                        QMessageBox.StandardButton.Ok)
                return

    def show_data(self, sach_data_list):
        if sach_data_list:
            self.result_table.setRowCount(0)
            self.result_table.setRowCount(len(sach_data_list))
            self.soLuongRow.setText("Số lượng: " + str(len(sach_data_list)))

            for row, info in enumerate(sach_data_list):
                info_list = [
                    info["MASACH"],
                    info["TENSACH"],
                    info["TEN"],  # the loai
                    info["BUTDANH"],  # ten tac gia
                    info["SOLUONG"],
                    info["VITRI"],
                    info["TOMTAT"],
                    info["ANHSACH"],
                    info["NGAYTHEM"],
                    info["NGAYCAPNHAT"]
                ]

                for column, item in enumerate(info_list):
                    cell_item = QTableWidgetItem(str(item))
                    self.result_table.setItem(row, column, cell_item)
        else:
            self.result_table.setRowCount(0)
            return

    def fill_combo_box(self):
        # Fill the tac gia combobox
        tacGia_result = self.db.get_all_tacgia()
        theLoai_result = self.db.get_all_theloai()

        self.maTacGia.clear()
        self.maTheLoai.clear()

        for item in tacGia_result:
            self.maTacGia.addItem(item['BUTDANH'], item['MATACGIA'])

        for item in theLoai_result:
            self.maTheLoai.addItem(item['TEN'], item['MATHELOAI'])

        self.maTacGia.setCurrentIndex(-1)
        self.maTheLoai.setCurrentIndex(-1)

    def disable_buttons(self):
        for btn in self.buttons_list:
            btn.setProperty('enabled', False)

    def enable_buttons(self):
        for btn in self.buttons_list:
            btn.setProperty('enabled', True)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = FormQLSach()
    window.show()

    sys.exit(app.exec())
