-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 24, 2024 at 10:56 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `web_barang_hilang`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin_login`
--

CREATE TABLE `admin_login` (
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin_login`
--

INSERT INTO `admin_login` (`email`, `password`, `username`) VALUES
('ridhanurrachmat240802@gmail.com', 'qweasdzxc', 'Ridha Nurrachmat');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_item`
--

CREATE TABLE `tbl_item` (
  `item_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `img` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `status` enum('pending','accepted','rejected') DEFAULT 'pending',
  `action_time` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_item_history`
--

CREATE TABLE `tbl_item_history` (
  `history_id` int(11) NOT NULL,
  `item_id` int(11) DEFAULT NULL,
  `title` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `img` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `status` enum('rejected','accepted') NOT NULL,
  `action_time` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_item_history`
--

INSERT INTO `tbl_item_history` (`history_id`, `item_id`, `title`, `description`, `img`, `email`, `status`, `action_time`) VALUES
(7, 13, 'Sepatu', 'Sepatu merk aerostreet dengan warna abu dan coklat sesuai pada gambar, ditemukan di masjid depan amikom. cp : 081347136434', 'sepatu.jpg', 'ridhanurrachmat240802@gmail.com', 'rejected', '2024-12-24 09:06:19'),
(8, 14, 'Sepatu ', 'Sepatu merk aerostreet dengan warna abu dan coklat sesuai pada gambar foto, ditemukan di depan universitas amikom. cp : 081231248348', 'sepatu.jpg', 'ridhanurrachmat@students.amikom.ac.id', 'rejected', '2024-12-24 09:15:37');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_item_user`
--

CREATE TABLE `tbl_item_user` (
  `id` int(11) NOT NULL,
  `item_id` int(11) DEFAULT NULL,
  `title` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `img` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `status` enum('accepted') DEFAULT 'accepted',
  `timestamp_column` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_item_user`
--

INSERT INTO `tbl_item_user` (`id`, `item_id`, `title`, `description`, `img`, `email`, `status`, `timestamp_column`) VALUES
(11, 12, 'Kunci Pintu', 'Deskripsi seperti pada gambar, ditemukan di smoking area depan gedung 4. cp : 08123123123', 'Key_ring.jpg', 'ridhanurrachmat@students.amikom.ac.id', 'accepted', '2024-12-24 09:09:03'),
(12, 15, 'Sepatu', 'Sepatu merk aerostreet dengan warna abu dan coklat sesuai pada foto, ditemukan di masjid depan amikom. cp : 0812317246232', 'sepatu.jpg', 'ridhanurrachmat@students.amikom.ac.id', 'accepted', '2024-12-24 09:19:30');

-- --------------------------------------------------------

--
-- Table structure for table `user_login`
--

CREATE TABLE `user_login` (
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `is_verified` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_login`
--

INSERT INTO `user_login` (`email`, `password`, `username`, `is_verified`) VALUES
('ridhanurrachmat@students.amikom.ac.id', 'qwerty123', 'ridha', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin_login`
--
ALTER TABLE `admin_login`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `tbl_item`
--
ALTER TABLE `tbl_item`
  ADD PRIMARY KEY (`item_id`);

--
-- Indexes for table `tbl_item_history`
--
ALTER TABLE `tbl_item_history`
  ADD PRIMARY KEY (`history_id`);

--
-- Indexes for table `tbl_item_user`
--
ALTER TABLE `tbl_item_user`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_login`
--
ALTER TABLE `user_login`
  ADD PRIMARY KEY (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tbl_item`
--
ALTER TABLE `tbl_item`
  MODIFY `item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `tbl_item_history`
--
ALTER TABLE `tbl_item_history`
  MODIFY `history_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `tbl_item_user`
--
ALTER TABLE `tbl_item_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
