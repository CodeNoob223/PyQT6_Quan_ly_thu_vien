import mysql.connector


class ConnectDatabase:
    def __init__(self):
        self.host = 'localhost'
        self.port = 3306
        self.database = 'ql_thuvien'
        self.user = 'root'
        self.password = ''
        self.dbname = 'ql_thuvien'
        self.con = None
        self.cursor = None

    def connect_db(self):
        self.con = mysql.connector.connect(
            host=self.host,
            port=self.port,
            database=self.dbname,
            user=self.user,
            password=self.password
        )

        self.cursor = self.con.cursor(dictionary=True)

    def add_sach(self, matheloai, matacgia, tensach, soluong, vitri, tomtat, anhsach):
        self.connect_db()

        sql = f"""
        INSERT INTO `sach`(`MATHELOAI`, `MATACGIA`, `TENSACH`, `SOLUONG`, `VITRI`, `TOMTAT`, `ANHSACH`, `NGAYCAPNHAT`) VALUES ({matheloai},{matacgia},'{tensach}',{soluong},'{vitri}','{tomtat}','{anhsach}',NOW())
    """
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def update_sach(self, masach, matheloai, matacgia, tensach, soluong, vitri, tomtat, anhsach):
        self.connect_db()

        sql = f"""
        UPDATE `sach` SET `MATHELOAI`={matheloai},`MATACGIA`={matacgia},`TENSACH`='{tensach}',`SOLUONG`={soluong},`VITRI`='{vitri}',`TOMTAT`='{tomtat}',`ANHSACH`='{anhsach}', `NGAYCAPNHAT`= NOW() WHERE `MASACH`={masach}
    """
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def delete_sach(self, masach):
        self.connect_db()
        sql = f"""
        DELETE FROM `sach` WHERE `MASACH`={masach}
    """
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def search_sach(self, masach=None, matheloai=None, matacgia=None, tensach=None, soluong=None, vitri=None, tomtat=None, anhsach=None):
        self.connect_db()
        condition = ""
        if masach:
            condition += f" AND sach.masach = {masach} "
        if matheloai:
            condition += f" AND theloai.matheloai = {matheloai} "
        if matacgia:
            condition += f" AND tacgia.matacgia = {matacgia} "
        if tensach:
            condition += f" AND sach.tensach LIKE '%{tensach}%' "
        if soluong:
            condition += f" AND soLuong >= {soluong}"
        if vitri:
            condition += f" AND vitri LIKE '%{vitri}%' "
        if tomtat:
            condition += f" AND tomtat LIKE '%{tomtat}%' "
        if anhsach:
            condition += f" AND anhsach LIKE '%{anhsach}%' "

        sql = f"SELECT MASACH, TENSACH, sach.MATHELOAI, sach.MATACGIA, SOLUONG, VITRI, TOMTAT, ANHSACH, sach.NGAYTHEM, sach.NGAYCAPNHAT, BUTDANH, TEN FROM sach JOIN tacgia ON sach.MATACGIA = tacgia.MATACGIA JOIN theloai ON sach.MATHELOAI = theloai.MATHELOAI WHERE 1"
        try:
            # Execute the SQL query for searching information
            self.cursor.execute(sql + condition)
            result = self.cursor.fetchall()
            return result
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def get_all_sach(self):
        self.connect_db()
        sql = f"Select * from sach"
        try:
            # Execute the SQL query for searching information
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def get_all_tacgia(self):
        self.connect_db()
        sql = f"Select * from tacgia"
        try:
            # Execute the SQL query for searching information
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def get_all_theloai(self):
        self.connect_db()
        sql = f"Select * from theloai"
        try:
            # Execute the SQL query for searching information
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def get_all_admin(self):
        self.connect_db()
        sql = f"Select MAADMIN, USERNAME from admin"
        try:
            # Execute the SQL query for searching information
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def get_sach_muon(self, maTheMuon):
        self.connect_db()
        sql = f"SELECT sach_muon.MASACH, sach_muon.MATHEMUON, sach_muon.NGAYTRA, sach_muon.NGAYMUON, sach_muon.TINHTRANG, sach.TENSACH, tacgia.BUTDANH FROM sach_muon JOIN sach ON sach_muon.MASACH = sach.MASACH JOIN tacgia ON sach.MATACGIA = tacgia.MATACGIA WHERE sach_muon.mathemuon = {maTheMuon}"
        try:
            # Execute the SQL query for searching information
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def search_the_muon_tra(self, maTheMuon: int = None,
                            maBanDoc: str = None,
                            maAdmin: str = None,
                            ngayMuon: str = None,
                            ngayTra: str = None,
                            tinhTrang: str = None,
                            sachMuon: list[str] = None):
        self.connect_db()
        condition = ""

        if maTheMuon:
            condition += f" AND themuontra.mathemuon = {maTheMuon} "
        if maBanDoc:
            condition += f" AND bandoc.maBanDoc = {maBanDoc} "
        if maAdmin:
            condition += f" AND admin.maAdmin = {maAdmin} "
        if ngayMuon:
            condition += f" AND themuontra.ngayMuon >= '{ngayMuon}' "
        if ngayTra:
            condition += f" AND themuontra.ngayTra >= '{ngayTra}' "
        if tinhTrang:
            condition += f" AND themuontra.tinhTrang = '{tinhTrang}' "
        if sachMuon:
            if len(sachMuon) > 0:
                for tenSach in sachMuon:
                    condition += f" AND EXISTS (SELECT SACH.TENSACH FROM SACH JOIN SACH_MUON ON SACH.MASACH = SACH_MUON.MASACH WHERE SACH_MUON.MATHEMUON = themuontra.MATHEMUON AND SACH.TENSACH LIKE '%{tenSach}%') "

        sql = f"SELECT themuontra.MATHEMUON, bandoc.HOTEN, admin.USERNAME, themuontra.NGAYMUON, themuontra.NGAYTRA, themuontra.TINHTRANG, themuontra.NGAYCAPNHAT, themuontra.NGAYTHEM, bandoc.MABANDOC FROM themuontra JOIN bandoc ON themuontra.MABANDOC = bandoc.MABANDOC JOIN admin ON admin.MAADMIN = themuontra.MAADMIN WHERE 1 "
        try:
            # Execute the SQL query for searching information
            self.cursor.execute(sql + condition)
            result = self.cursor.fetchall()
            return result
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def add_the_muon(self, maBanDoc, maAdmin, ngayTra, ngayMuon, tinhTrang, sachMuon):
        self.connect_db()

        sql = f"INSERT INTO `themuontra`(`MABANDOC`, `MAADMIN`, `NGAYMUON`, `NGAYTRA`, `TINHTRANG`, `NGAYCAPNHAT`) VALUES ({maBanDoc},{maAdmin},'{ngayMuon}','{ngayTra}','{tinhTrang}',NOW())"
        try:
            self.cursor.execute(sql)
            self.con.commit()

            rowid = self.cursor.lastrowid

            for maSach in sachMuon:
                self.add_muon_sach(maSach, rowid, ngayMuon, ngayTra)

        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def update_the_muon(self, maTheMuon, maBanDoc, maAdmin, ngayTra, ngayMuon, tinhTrang):
        self.connect_db()

        sql = f"UPDATE `themuontra` SET `MABANDOC`={maBanDoc},`MAADMIN`={maAdmin},`NGAYMUON`='{ngayMuon}',`NGAYTRA`='{ngayTra}',`TINHTRANG`='{tinhTrang}',`NGAYCAPNHAT`= NOW() WHERE MATHEMUON = {maTheMuon}"
        try:
            self.cursor.execute(sql)
            self.con.commit()

            # for item in sachMuon:
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def hoanthanh_themuon(self, maTheMuon, ngayTra):
        self.connect_db()

        sql = f"UPDATE `themuontra` SET `NGAYTRA`= '{ngayTra}', `TINHTRANG`='Đã trả',`NGAYCAPNHAT`= NOW() WHERE MATHEMUON = {maTheMuon}"
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception as E:
            self.con.rollback()
            print(E)
        
        sql = f"UPDATE `sach_muon` SET `NGAYTRA`= '{ngayTra}', `TINHTRANG`='Đã trả' WHERE MATHEMUON = {maTheMuon}"
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception as E:
            self.con.rollback()
            print(E)
        finally:
            self.con.close()

    def delete_the_muon(self, maTheMuon):
        self.connect_db()

        sql = f"DELETE FROM themuontra WHERE mathemuon = {maTheMuon}"
        try:
            self.cursor.execute(sql)
            self.con.commit()

            # for item in sachMuon:
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def add_muon_sach(self, maSach: int, maTheMuon: int, ngayMuon: str, ngayTra: str):
        self.connect_db()

        sql = f"INSERT INTO sach_muon(MASACH, MATHEMUON, NGAYMUON, NGAYTRA) VALUES ({maSach},{maTheMuon}, '{ngayMuon}', '{ngayTra}')"
        try:
            self.cursor.execute(sql)
            self.con.commit()

            self.dec_sach(maSach)
        except Exception as E:
            self.con.rollback()
            print(E)
            return E
        finally:
            self.con.close()

    def delete_muon_sach(self, maSach, maTheMuon):
        self.connect_db()

        sql = f"DELETE FROM sach_muon WHERE MASACH = {maSach} and MATHEMUON = {maTheMuon}"
        try:
            self.cursor.execute(sql)
            self.con.commit()

            self.inc_sach(maSach)
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def update_muon_sach(self, maSach, maTheMuon, tinhTrang="Đã trả"):
        self.connect_db()

        sql = f"UPDATE sach_muon SET TINHTRANG = '{tinhTrang}', NGAYTRA = NOW() WHERE MASACH = {maSach} and MATHEMUON = {maTheMuon}"
        try:
            self.cursor.execute(sql)
            self.con.commit()

            self.inc_sach(maSach)
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    # giam so luong sach
    def dec_sach(self, maSach: int):
        self.connect_db()
        sql = f"UPDATE `sach` SET `SOLUONG`= SOLUONG - 1 WHERE MASACH = {maSach}"
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()
    # tang so luong sach

    def inc_sach(self, maSach: int):
        self.connect_db()
        sql = f"UPDATE `sach` SET `SOLUONG`= SOLUONG + 1 WHERE MASACH = {maSach}"
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def add_theloai(self, ten):
        self.connect_db()

        sql = f"""
        INSERT INTO `theloai`(`TEN`) VALUES ('{ten}')
    """
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def update_theloai(self, ten, matheloai):
        self.connect_db()

        sql = f"""
        UPDATE `theloai` SET `TEN`='{ten}' WHERE MATHELOAI = {matheloai}
    """
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def delete_theloai(self, matheloai):
        self.connect_db()
        sql = f"""
        DELETE FROM `theloai` WHERE MATHELOAI = {matheloai}
    """
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def search_theloai(self, matheloai=None, ten=None):
        self.connect_db()
        condition = ""
        if matheloai:
            condition += f" AND matheloai = {matheloai} "
        if ten:
            condition += f" AND ten LIKE '%{ten}%' "

        sql = f"SELECT * FROM `theloai` WHERE 1"
        try:
            # Execute the SQL query for searching information
            self.cursor.execute(sql + condition)
            result = self.cursor.fetchall()
            return result
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def add_tacgia(self, butdanh):
        self.connect_db()

        sql = f"""
        INSERT INTO `tacgia`(`BUTDANH`, `NGAYTHEM`) VALUES ('{butdanh}', NOW())
    """
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def update_tacgia(self, butdanh, matacgia):
        self.connect_db()

        sql = f"""
        UPDATE `tacgia` SET `BUTDANH`='{butdanh}', `NGAYTHEM`= NOW() WHERE MATACGIA = {matacgia}
    """
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def delete_tacgia(self, matacgia):
        self.connect_db()
        sql = f"""
        DELETE FROM `tacgia` WHERE MATACGIA = {matacgia}
    """
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def search_tacgia(self, matacgia=None, butdanh=None):
        self.connect_db()
        condition = ""
        if matacgia:
            condition += f" AND matacgia = {matacgia} "
        if butdanh:
            condition += f" AND butdanh LIKE '%{butdanh}%' "

        sql = f"SELECT * FROM `tacgia` WHERE 1"
        try:
            # Execute the SQL query for searching information
            self.cursor.execute(sql + condition)
            result = self.cursor.fetchall()
            return result
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def add_vipham(self, mabandoc, maadmin, noidung, tienphat, tinhtrang):
        self.connect_db()

        sql = f"""
        INSERT INTO `vipham`(`MABANDOC`, `MAADMIN`, `NOIDUNG`, `TIENPHAT`, `TINHTRANG`, `NGAYTHEM`) VALUES ({mabandoc},{maadmin},'{noidung}','{tienphat}','{tinhtrang}',NOW())
    """
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def update_vipham(self, mavipham, mabandoc, maadmin, noidung, tienphat, tinhtrang):
        self.connect_db()

        sql = f"""
        UPDATE `vipham` SET `MABANDOC`={mabandoc},`MAADMIN`={maadmin},`NOIDUNG`='{noidung}', TIENPHAT = '{tienphat}', TINHTRANG = '{tinhtrang}' WHERE `MAVIPHAM`={mavipham}
    """
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def nop_phat(self, mavipham, tienphat):
        self.connect_db()

        sql = f"""
        UPDATE `vipham` SET TIENPHAT = '{tienphat}', TINHTRANG = 'Đã nộp phạt' WHERE `MAVIPHAM`={mavipham}
    """
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def delete_vipham(self, mavipham):
        self.connect_db()
        sql = f"""
        DELETE FROM `vipham` WHERE `MAVIPHAM`={mavipham}
    """
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def search_vipham(self, mavipham=None, mabandoc=None, maadmin=None, noidung=None, tinhtrang=None, tienphat=None):
        self.connect_db()
        condition = ""
        if mavipham:
            condition += f" AND mavipham = {mavipham} "
        if mabandoc:
            condition += f" AND mabandoc = {mabandoc} "
        if maadmin:
            condition += f" AND maadmin = {maadmin} "
        if noidung:
            condition += f" AND noidung LIKE '%{noidung}%' "
        if tinhtrang:
            condition += f" AND tinhtrang = '{tinhtrang}' "
        if tienphat:
            condition += f" AND tienphat >= {tienphat} "

        sql = f"SELECT vipham.MAVIPHAM, vipham.MABANDOC, vipham.MAADMIN, vipham.NOIDUNG, vipham.TIENPHAT, vipham.TINHTRANG, vipham.NGAYTHEM, bandoc.HOTEN, admin.USERNAME FROM vipham JOIN bandoc ON bandoc.MABANDOC = vipham.MABANDOC JOIN admin ON admin.MAADMIN = vipham.MAADMIN WHERE 1 "
        try:
            # Execute the SQL query for searching information
            self.cursor.execute(sql + condition)
            result = self.cursor.fetchall()
            return result
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def add_bandoc(self, hoten, ngaysinh, diachi, sdt):
        self.connect_db()

        sql = f"""
        INSERT INTO `bandoc`(`HOTEN`, `NGAYSINH`, `DIACHI`, `SDT`, `NGAYTHEM`) VALUES ('{hoten}','{ngaysinh}','{diachi}','{sdt}',NOW())
    """
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def update_bandoc(self, mabandoc, hoten, ngaysinh, diachi, sdt):
        self.connect_db()

        sql = f"""
        UPDATE `bandoc` SET `HOTEN`='{hoten}',`NGAYSINH`='{ngaysinh}',`DIACHI`='{diachi}',`SDT`='{sdt}', `NGAYTHEM`= NOW() WHERE `MABANDOC`={mabandoc}
    """
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def delete_bandoc(self, mabandoc):
        self.connect_db()
        sql = f"""
        DELETE FROM `bandoc` WHERE `MABANDOC`={mabandoc}
    """
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def search_bandoc(self, mabandoc=None, hoten=None, ngaysinh=None, diachi=None, sdt=None):
        self.connect_db()
        condition = ""
        if mabandoc:
            condition += f" AND mabandoc = {mabandoc} "
        if hoten:
            condition += f" AND hoten LIKE '%{hoten}%' "
        if ngaysinh:
            condition += f" AND ngaysinh >= '{ngaysinh}' "
        if diachi:
            condition += f" AND diachi LIKE '%{diachi}%' "
        if sdt:
            condition += f" AND sdt LIKE '%{sdt}%'"

        sql = f"SELECT * FROM `bandoc` WHERE 1"
        try:
            # Execute the SQL query for searching information
            self.cursor.execute(sql + condition)
            result = self.cursor.fetchall()
            return result
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def add_admin(self, username, matkhau, role):
        self.connect_db()

        sql = f"""
        INSERT INTO `admin`(`USERNAME`, `MATKHAU`, `ROLE`, `NGAYTHEM`) VALUES ('{username}','{matkhau}','{role}',NOW())
    """
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def update_admin(self, maadmin, username, matkhau, role):
        self.connect_db()

        sql = f"""
        UPDATE `admin` SET `MAADMIN`={maadmin},`USERNAME`='{username}',`MATKHAU`='{matkhau}',`ROLE`='{role}', `NGAYTHEM`= NOW() WHERE `MAADMIN`={maadmin}
    """
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def delete_admin(self, maadmin):
        self.connect_db()
        sql = f"""
        DELETE FROM `admin` WHERE `MAADMIN`={maadmin}
    """
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def search_admin(self, maadmin=None, username=None, matkhau=None, role=None):
        self.connect_db()
        condition = ""
        if maadmin:
            condition += f" AND maadmin LIKE '%{maadmin}%' "
        if username:
            condition += f" AND username LIKE '%{username}%' "
        if matkhau:
            condition += f" AND matkhau LIKE '%{matkhau}%' "
        if role:
            condition += f" AND role = '{role}' "

        sql = f"SELECT * FROM `admin` WHERE 1"
        try:
            # Execute the SQL query for searching information
            self.cursor.execute(sql + condition)
            result = self.cursor.fetchall()
            return result
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def check_login(self, username, matkhau):
        self.connect_db()
        query = "SELECT * FROM admin WHERE username = %s AND matkhau = %s"
        self.cursor.execute(query, (username, matkhau))
        result = self.cursor.fetchone()
        return result is not None

    def get_all_role(self):
        self.connect_db()
        sql = f"Select role from admin group by role"
        try:
            # Execute the SQL query for searching information
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def get_all_so_luong(self):
        self.connect_db()
        data = {}
        data["sach"] = 0
        data["bandoc"] = 0
        data["tacgia"] = 0
        data["theloai"] = 0
        data["themuontra"] = 0
        data["vipham"] = 0
        try:
            sql = f"SELECT COUNT(*) FROM `sach`"
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            data["sach"] = result["COUNT(*)"]
        except Exception as E:
            self.con.rollback()
            print(E)

        try:
            sql = f"SELECT COUNT(*) FROM `bandoc`"
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            data["bandoc"] = result["COUNT(*)"]
        except Exception as E:
            self.con.rollback()
            print(E)

        try:
            sql = f"SELECT COUNT(*) FROM `tacgia`"
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            data["tacgia"] = result["COUNT(*)"]
        except Exception as E:
            self.con.rollback()
            print(E)
        
        try:
            sql = f"SELECT COUNT(*) FROM `theloai`"
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            data["theloai"] = result["COUNT(*)"]
        except Exception as E:
            self.con.rollback()
            print(E)
        
        try:
            sql = f"SELECT COUNT(*) FROM `sach_muon`"
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            data["themuontra"] = result["COUNT(*)"]
        except Exception as E:
            self.con.rollback()
            print(E)

        try:
            sql = f"SELECT COUNT(*) FROM `vipham`"
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            data["vipham"] = result["COUNT(*)"]
            return data
        except Exception as E:
            self.con.rollback()
            print(E)
        finally:
            self.con.close()