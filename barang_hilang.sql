-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 10, 2023 at 09:12 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `barang_hilang`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin_login`
--

CREATE TABLE `admin_login` (
  `email` varchar(30) NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin_login`
--

INSERT INTO `admin_login` (`email`, `username`, `password`) VALUES
('ridha@students.amikom.ac.id', 'Ridha Nurrachmat', '135');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_item`
--

CREATE TABLE `tbl_item` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `img` varchar(255) DEFAULT NULL,
  `email` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_item`
--

INSERT INTO `tbl_item` (`id`, `title`, `description`, `img`, `email`) VALUES
(27, 'Test 7', 'Deskripsi 7', 'Twirl.jpg', 'hana@students.amikom.ac.id'),
(28, 'Test 8', 'Deskripsi 8', 'Liquify_Blank.jpg', 'hana@students.amikom.ac.id'),
(29, 'Test 9', 'Deskripsi 9', 'Liquify.jpg', 'hana@students.amikom.ac.id'),
(30, 'Test 10', 'Deskripsi 10', 'Sunset.jpg', 'hana@students.amikom.ac.id');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_item_user`
--

CREATE TABLE `tbl_item_user` (
  `id` int(15) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `img` varchar(255) NOT NULL,
  `email` varchar(50) NOT NULL,
  `status` varchar(50) NOT NULL,
  `timestamp_column` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_item_user`
--

INSERT INTO `tbl_item_user` (`id`, `title`, `description`, `img`, `email`, `status`, `timestamp_column`) VALUES
(22, 'Test 101', 'Deskripsi 101', 'Sliced.jpg', 'hana@students.amikom.ac.id', 'accepted', '2023-12-10 18:49:26'),
(23, 'Test 3', 'Deskripsi 3', 'Just_Do_Nothing.jpg', 'hana@students.amikom.ac.id', 'accepted', '2023-12-10 18:49:48'),
(24, 'Test 4', 'Deskripsi 4', 'Glitch_Blank.jpg', 'hana@students.amikom.ac.id', 'accepted', '2023-12-10 18:53:12'),
(25, 'Test 5', 'Deskripsi 5', 'Just_Do_Nothing.jpg', 'hana@students.amikom.ac.id', 'accepted', '2023-12-10 19:02:43'),
(26, 'Test 6', 'Deskripsi 6', 'Glitch.jpg', 'hana@students.amikom.ac.id', 'accepted', '2023-12-10 19:11:31');

-- --------------------------------------------------------

--
-- Table structure for table `user_login`
--

CREATE TABLE `user_login` (
  `email` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_login`
--

INSERT INTO `user_login` (`email`, `username`, `password`) VALUES
('hana@students.amikom.ac.id', 'Ma\'rifah Hadaina Faza', '123'),
('indra@students.amikom.ac.id', 'Indra Bagas Pratama', '123123'),
('ridha@students.amikom.ac.id', 'Ridha Nurrachmat', '12345');

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
  ADD PRIMARY KEY (`id`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
