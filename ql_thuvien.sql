-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 05, 2024 at 05:07 PM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 7.4.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ql_thuvien`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `MAADMIN` int(11) NOT NULL,
  `MATKHAU` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `ROLE` varchar(30) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'THU_THU',
  `USERNAME` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `NGAYTHEM` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`MAADMIN`, `MATKHAU`, `ROLE`, `USERNAME`, `NGAYTHEM`) VALUES
(1, '1', 'QUAN_TRI', 'Admin123', '2024-06-11'),
(2, '$argon2id$v=19$m=65536,t=4,p=1$Ri5OWTRTdzdSRXR5d3VSZg$y+Yyc9VrKKA2cMccr3x6ByS7BGQ/axB7q3FAXoHDGZY', 'QUAN_TRI', 'TuanMinh', '2023-12-29'),
(3, '$argon2id$v=19$m=65536,t=4,p=1$Ri5OWTRTdzdSRXR5d3VSZg$y+Yyc9VrKKA2cMccr3x6ByS7BGQ/axB7q3FAXoHDGZY', 'THU_THU', 'VanThi', '2023-12-29'),
(5, '12345', 'THU_THU', 'NguyenBo', '2024-06-13');

-- --------------------------------------------------------

--
-- Table structure for table `bandoc`
--

CREATE TABLE `bandoc` (
  `MABANDOC` int(11) NOT NULL,
  `HOTEN` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `NGAYSINH` date NOT NULL,
  `DIACHI` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `SDT` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `NGAYTHEM` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `bandoc`
--

INSERT INTO `bandoc` (`MABANDOC`, `HOTEN`, `NGAYSINH`, `DIACHI`, `SDT`, `NGAYTHEM`) VALUES
(1, 'Nguyễn Văn Bộ', '2003-05-23', 'Việt Nam, Vĩnh Phúc', '0984172055', '2024-06-08'),
(2, 'Vương Minh Quân', '2003-06-12', 'Đống Đa, Hà Nội', '0813344815', '2023-12-29'),
(3, 'Đinh Văn Thi', '2003-01-01', 'Hà Nội', '0123456789', '2024-04-23'),
(4, 'Hoàng Vũ', '2003-01-02', 'Hà Tĩnh', '0123456788', '2024-06-08'),
(14, 'Nguyễn Văn Đức', '2003-02-05', 'Nam Định', '4124214124', '2024-06-08'),
(15, 'Nguyễn Văn Nam', '2003-02-05', 'Nam Định', '4124214124', '2024-06-08'),
(17, 'Hoàng Khắc Vũ', '2003-03-07', 'Hà Tĩnh', '0394182113', '2024-06-08'),
(19, 'Tiến Nghiêm', '2003-01-04', 'Vĩnh Phúc', '123', '2024-06-10'),
(20, 'Vũ Hoàng', '2003-01-04', 'Hà Tĩnh', '123', '2024-06-10'),
(26, 'Quân Bộ', '2000-01-01', 'Hà Nội', '123124', '2024-06-11'),
(33, 'Trương Văn Lượng', '2002-01-01', 'Nghệ An', '6666666666', '2024-06-15'),
(34, 'Nguyễn Tuấn Minh', '2003-01-01', 'Phú Thọ', '231414', '2024-06-18');

-- --------------------------------------------------------

--
-- Table structure for table `sach`
--

CREATE TABLE `sach` (
  `MASACH` int(11) NOT NULL,
  `MATHELOAI` int(11) NOT NULL,
  `MATACGIA` int(11) NOT NULL,
  `TENSACH` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `SOLUONG` int(11) NOT NULL,
  `VITRI` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `TOMTAT` varchar(400) COLLATE utf8_unicode_ci NOT NULL,
  `ANHSACH` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `NGAYTHEM` date NOT NULL DEFAULT current_timestamp(),
  `NGAYCAPNHAT` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `sach`
--

INSERT INTO `sach` (`MASACH`, `MATHELOAI`, `MATACGIA`, `TENSACH`, `SOLUONG`, `VITRI`, `TOMTAT`, `ANHSACH`, `NGAYTHEM`, `NGAYCAPNHAT`) VALUES
(1, 3, 2, 'Anh chàng hiệp sĩ gỗ', 91, 'Dãy C', 'Ở thị trấn Bến Cam, mỗi năm cứ đến ngày gần Tết người ta lại thấy ông lão già ấy. Không ai biết quê quán ông lão ở đâu, họ tên ông lão là gì. Nhưng mỗi năm vào dịp Tết người ta lại thấy ông lão đẩy cái xe bánh gỗ lọc khọc đến, ăn mấy phiên chợ Tết...', 'D:/Designer QLTV/anhSach/anhchanghiepsigo.jpg', '2023-12-28', '2024-06-15'),
(2, 3, 2, 'Làng', 93, 'Dãy A', 'Truyện kể về ông Hai rất yêu làng, yêu nước. Ông Hai phải đi tản cư nên ông rất nhớ làng và yêu làng, ông thường tự hào và khoe về làng Chợ Dầu giàu đẹp của mình, nhất là tinh thần kháng chiến và chính ông là một công dân tích cực.', 'D:/Designer QLTV/anhSach/lang.jpg', '2023-12-28', '2024-06-13'),
(3, 3, 7, 'Chí Phèo', 6, 'Dãy A', 'Chí Phèo là cuốn sách của tác giả Nam Cao, mô tả hình ảnh thực tế đời sống nông thôn Việt Nam trước năm 1945, với sự thiếu vắng chất đầu tư, sự nghèo đói và tàn tệ trên con đường phá sản, bần cùng...', 'D:/Designer QLTV/anhSach/chipheo.jpg', '2023-12-29', '2024-06-17'),
(4, 20, 1, 'Dế mèn phiêu lưu ký', 98, 'Dãy A', 'Dế Mèn phiêu lưu ký là tác phẩm văn xuôi đặc sắc và nổi tiếng nhất của nhà văn Tô Hoài viết về loài vật, dành cho lứa tuổi thiếu nhi.', 'D:/Designer QLTV/anhSach/demenphieuluuky.jpg', '2024-04-22', '2024-06-13'),
(5, 8, 11, 'Số đỏ', 94, 'Dãy B', 'Truyện dài 20 chương và được bắt đầu khi bà Phó Đoan đến chơi ở sân quần vợt nơi Xuân tóc đỏ làm việc. Vô tình Xuân tóc đỏ vì xem trộm 1 cô đầm thay đồ nên bị cảnh sát bắt giam và được bà Phó Đoan bảo lãnh. Sau đó, bà Phó Đoan giới thiệu Xuân đến làm việc', 'D:/Designer QLTV/anhSach/sodo.jpg', '2024-04-23', '2024-06-13'),
(6, 3, 2, 'Vợ nhặt', 91, 'Dãy B', 'Tràng là một người dân sống ngụ cư sống cùng với mẹ già. Anh làm nghề kéo xe bò thuê. Một lần trên đường kéo cái xe bò thóc trên tỉnh anh quen được Thị, Chỉ với bốn bát bánh đúc thị đã đồng ý làm vợ Tràng.', 'D:/Designer QLTV/anhSach/vonhat.jpg', '2024-04-23', '2024-06-13'),
(11, 6, 12, 'Truyện Kiều', 95, 'Dãy C', 'Tai họa đã đột ngột ập đến Vương gia trong lúc người thiếu nữ còn đang thổn thức với mối tình đầu. Thằng bán tơ đã lén chôn một chai rượu vào vườn nhà Kiều rồi vu oan cho Vương ông tội buôn lậu rượu. Ngay lập tức, bọn sai nha xông vào, treo ngược Vương ôn', 'D:/Designer QLTV/anhSach/truyenkieu.jpg', '2024-04-23', '2024-06-13');

-- --------------------------------------------------------

--
-- Table structure for table `sach_muon`
--

CREATE TABLE `sach_muon` (
  `MASACH` int(11) NOT NULL,
  `MATHEMUON` int(11) NOT NULL,
  `NGAYMUON` date NOT NULL DEFAULT current_timestamp(),
  `NGAYTRA` date NOT NULL DEFAULT current_timestamp(),
  `TINHTRANG` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'Chưa trả'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `sach_muon`
--

INSERT INTO `sach_muon` (`MASACH`, `MATHEMUON`, `NGAYMUON`, `NGAYTRA`, `TINHTRANG`) VALUES
(1, 1, '2023-12-29', '2024-07-03', 'Đã trả'),
(2, 1, '2023-12-31', '2024-06-18', 'Đã trả'),
(1, 4, '2024-01-01', '2024-06-18', 'Chưa trả'),
(3, 4, '2024-01-01', '2024-06-18', 'Chưa trả'),
(5, 6, '2024-06-13', '2024-06-18', 'Chưa trả'),
(6, 6, '2024-06-13', '2024-06-18', 'Chưa trả'),
(1, 11, '2024-06-13', '2024-07-03', 'Đã trả'),
(2, 6, '2024-06-15', '2024-06-18', 'Chưa trả'),
(1, 28, '2024-06-18', '2024-06-18', 'Chưa trả'),
(2, 28, '2024-06-18', '2024-06-18', 'Chưa trả'),
(3, 28, '2024-06-18', '2024-06-18', 'Chưa trả'),
(11, 31, '2024-06-19', '2024-07-03', 'Đã trả'),
(6, 31, '2024-06-19', '2024-07-20', 'Đã trả'),
(5, 32, '2024-06-19', '2025-06-19', 'Đã trả'),
(1, 32, '2024-06-19', '2025-06-19', 'Đã trả'),
(4, 33, '2024-06-22', '2024-06-23', 'Đã trả'),
(2, 33, '2024-06-22', '2024-06-23', 'Đã trả');

-- --------------------------------------------------------

--
-- Table structure for table `tacgia`
--

CREATE TABLE `tacgia` (
  `MATACGIA` int(11) NOT NULL,
  `BUTDANH` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `NGAYTHEM` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `tacgia`
--

INSERT INTO `tacgia` (`MATACGIA`, `BUTDANH`, `NGAYTHEM`) VALUES
(1, 'Tô Hoài', '2023-12-28'),
(2, 'Kim Lân', '2023-12-28'),
(4, 'Nguyễn Đình Thi', '2023-12-29'),
(5, 'Hàn Mạc Tử', '2023-12-29'),
(6, 'Nguyễn Đăng Khoa', '2023-12-29'),
(7, 'Nam Cao', '2023-12-29'),
(8, 'Xuân Diệu', '2024-01-03'),
(9, 'Lân Dũng', '2024-01-03'),
(10, 'Văn Thọ', '2024-01-03'),
(11, 'Vũ Trọng Phụng', '2024-04-23'),
(12, 'Nguyễn Du', '2024-04-23'),
(13, 'Nguyễn Văn Bộ', '2024-06-07'),
(14, 'Ngô Tất Tố', '2024-06-15');

-- --------------------------------------------------------

--
-- Table structure for table `theloai`
--

CREATE TABLE `theloai` (
  `MATHELOAI` int(11) NOT NULL,
  `TEN` varchar(50) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `theloai`
--

INSERT INTO `theloai` (`MATHELOAI`, `TEN`) VALUES
(13, 'Bí ẩn'),
(10, 'CNPM'),
(27, 'CNTT'),
(4, 'Cổ tích'),
(19, 'Comic'),
(5, 'Dân gian'),
(9, 'HTTT'),
(15, 'Khoa học'),
(1, 'Kinh dị'),
(12, 'KTĐT'),
(14, 'Lịch sử'),
(16, 'Manga'),
(17, 'Manhua'),
(18, 'Manhwa'),
(11, 'QTKD'),
(8, 'Tiểu thuyết'),
(2, 'Tình cảm'),
(3, 'Truyện ngắn'),
(6, 'Truyện thơ'),
(20, 'Văn xuôi');

-- --------------------------------------------------------

--
-- Table structure for table `themuontra`
--

CREATE TABLE `themuontra` (
  `MATHEMUON` int(11) NOT NULL,
  `MABANDOC` int(11) NOT NULL,
  `MAADMIN` int(11) NOT NULL,
  `NGAYMUON` date NOT NULL DEFAULT current_timestamp(),
  `NGAYTRA` date NOT NULL DEFAULT current_timestamp(),
  `TINHTRANG` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `NGAYCAPNHAT` date NOT NULL DEFAULT current_timestamp(),
  `NGAYTHEM` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `themuontra`
--

INSERT INTO `themuontra` (`MATHEMUON`, `MABANDOC`, `MAADMIN`, `NGAYMUON`, `NGAYTRA`, `TINHTRANG`, `NGAYCAPNHAT`, `NGAYTHEM`) VALUES
(1, 1, 3, '2024-06-18', '2024-06-19', 'Đã trả', '2024-07-03', '2023-12-29'),
(4, 1, 1, '2024-06-18', '2024-06-19', 'Đã trả', '2024-04-25', '2024-01-01'),
(6, 26, 5, '2024-06-18', '2024-06-19', 'Chưa trả', '2024-06-15', '2024-06-13'),
(11, 1, 5, '2024-06-18', '2024-07-03', 'Đã trả', '2024-07-03', '2024-06-13'),
(28, 3, 1, '2024-06-18', '2024-06-19', 'Chưa trả', '2024-06-18', '2024-06-18'),
(31, 4, 1, '2024-06-19', '2024-07-03', 'Đã trả', '2024-07-03', '2024-06-19'),
(32, 26, 5, '2024-06-19', '2025-06-19', 'Đã trả', '2024-06-19', '2024-06-19'),
(33, 3, 1, '2024-06-22', '2024-06-23', 'Đã trả', '2024-06-22', '2024-06-22');

-- --------------------------------------------------------

--
-- Table structure for table `vipham`
--

CREATE TABLE `vipham` (
  `MAVIPHAM` int(11) NOT NULL,
  `MABANDOC` int(11) NOT NULL,
  `MAADMIN` int(11) NOT NULL,
  `NOIDUNG` text COLLATE utf8_unicode_ci NOT NULL,
  `TIENPHAT` int(11) NOT NULL DEFAULT 1000,
  `TINHTRANG` enum('Đã nộp phạt','Chưa nộp phạt') COLLATE utf8_unicode_ci NOT NULL DEFAULT 'Chưa nộp phạt',
  `NGAYTHEM` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `vipham`
--

INSERT INTO `vipham` (`MAVIPHAM`, `MABANDOC`, `MAADMIN`, `NOIDUNG`, `TIENPHAT`, `TINHTRANG`, `NGAYTHEM`) VALUES
(1, 3, 3, 'Làm mất sách', 1000, 'Đã nộp phạt', '2023-12-29'),
(2, 1, 3, 'Làm mất sách', 1000, 'Chưa nộp phạt', '2023-12-29'),
(3, 1, 2, 'Xả rác trong thư viện', 1000, 'Chưa nộp phạt', '2024-04-26'),
(5, 3, 3, 'Làm mất sách', 1000, 'Chưa nộp phạt', '2024-06-08');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`MAADMIN`),
  ADD UNIQUE KEY `USERNAME` (`USERNAME`);

--
-- Indexes for table `bandoc`
--
ALTER TABLE `bandoc`
  ADD PRIMARY KEY (`MABANDOC`);

--
-- Indexes for table `sach`
--
ALTER TABLE `sach`
  ADD PRIMARY KEY (`MASACH`),
  ADD KEY `SACH_THELOAI` (`MATHELOAI`),
  ADD KEY `SACH_TACGIA` (`MATACGIA`);

--
-- Indexes for table `sach_muon`
--
ALTER TABLE `sach_muon`
  ADD KEY `SACH_THEMUONTRA` (`MASACH`,`MATHEMUON`),
  ADD KEY `MATHEMUONTRA` (`MATHEMUON`);

--
-- Indexes for table `tacgia`
--
ALTER TABLE `tacgia`
  ADD PRIMARY KEY (`MATACGIA`);

--
-- Indexes for table `theloai`
--
ALTER TABLE `theloai`
  ADD PRIMARY KEY (`MATHELOAI`),
  ADD UNIQUE KEY `TEN` (`TEN`);

--
-- Indexes for table `themuontra`
--
ALTER TABLE `themuontra`
  ADD PRIMARY KEY (`MATHEMUON`),
  ADD KEY `THEMUONTRA_BANDOC` (`MABANDOC`),
  ADD KEY `THEMUONTRA_ADMIN` (`MAADMIN`);

--
-- Indexes for table `vipham`
--
ALTER TABLE `vipham`
  ADD PRIMARY KEY (`MAVIPHAM`),
  ADD KEY `VIPHAM_ADMIN` (`MAADMIN`),
  ADD KEY `VIPHAM_BANDOC` (`MABANDOC`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `MAADMIN` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `bandoc`
--
ALTER TABLE `bandoc`
  MODIFY `MABANDOC` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `sach`
--
ALTER TABLE `sach`
  MODIFY `MASACH` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `tacgia`
--
ALTER TABLE `tacgia`
  MODIFY `MATACGIA` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `theloai`
--
ALTER TABLE `theloai`
  MODIFY `MATHELOAI` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `themuontra`
--
ALTER TABLE `themuontra`
  MODIFY `MATHEMUON` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `vipham`
--
ALTER TABLE `vipham`
  MODIFY `MAVIPHAM` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `sach`
--
ALTER TABLE `sach`
  ADD CONSTRAINT `sach_ibfk_1` FOREIGN KEY (`MATHELOAI`) REFERENCES `theloai` (`MATHELOAI`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `sach_ibfk_2` FOREIGN KEY (`MATACGIA`) REFERENCES `tacgia` (`MATACGIA`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `sach_muon`
--
ALTER TABLE `sach_muon`
  ADD CONSTRAINT `sach_muon_ibfk_1` FOREIGN KEY (`MASACH`) REFERENCES `sach` (`MASACH`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `sach_muon_ibfk_2` FOREIGN KEY (`MATHEMUON`) REFERENCES `themuontra` (`MATHEMUON`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `themuontra`
--
ALTER TABLE `themuontra`
  ADD CONSTRAINT `themuontra_ibfk_1` FOREIGN KEY (`MAADMIN`) REFERENCES `admin` (`MAADMIN`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `themuontra_ibfk_2` FOREIGN KEY (`MABANDOC`) REFERENCES `bandoc` (`MABANDOC`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `vipham`
--
ALTER TABLE `vipham`
  ADD CONSTRAINT `vipham_ibfk_1` FOREIGN KEY (`MAADMIN`) REFERENCES `admin` (`MAADMIN`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `vipham_ibfk_2` FOREIGN KEY (`MABANDOC`) REFERENCES `bandoc` (`MABANDOC`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
