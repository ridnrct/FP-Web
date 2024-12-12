-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 12, 2024 at 08:57 PM
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
(1, 3, 'wkwk', 'askdamlskd', 'cat-game-of-thrones-jon-snow-artwork-wallpaper-preview.jpg', 'ridhanurrachmat240802@gmail.com', 'rejected', '2024-12-09 14:51:26'),
(2, 1, 'asd', 'asdasd', '2791085.jpg', 'ridhanurrachmat@students.amikom.ac.id', 'accepted', '2024-12-09 15:03:12'),
(3, 2, 'ntah lagi', 'asd', '2791085.jpg', 'ridhanurrachmat240802@gmail.com', 'accepted', '2024-12-09 15:03:12'),
(4, 4, '123', 'asdasd', '2791085.jpg', 'ridhanurrachmat240802@gmail.com', 'accepted', '2024-12-09 15:06:42'),
(5, 5, 'asd', 'asdasdasd', '2791085.jpg', 'ridhanurrachmat240802@gmail.com', 'accepted', '2024-12-10 15:07:42'),
(6, 6, 'zxc', 'zxczxc', 'cat-game-of-thrones-jon-snow-artwork-wallpaper-preview.jpg', 'ridhanurrachmat240802@gmail.com', 'accepted', '2024-12-10 16:17:12');

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
(6, 7, 'asd', 'asdasdasdasasdasdasdasasdasdasdasasdasdasdasasdasdasdasasdasdasdasasdasdasdasasdasdasdasasdasdasdasasdasdasdasasdasdasdasasdasdasdasasdasdasdasasdasdasdasasdasdasdasasdasdasdasasdasdasdasasdasdasdasasdasdasdasasdasdasdasasdasdasdasasdasdasdasasdasdasdasasdasdasdasasdasdasdasasdasdasdasasdasdasdasasdasdasdas', '2791085.jpg', 'ridhanurrachmat240802@gmail.com', 'accepted', '2024-12-11 14:14:16'),
(7, 8, 'tes', 'asdasdasdas', '2791085.jpg', 'ridhanurrachmat@students.amikom.ac.id', 'accepted', '2024-12-11 14:14:19'),
(8, 9, 'asdasdasd', 'zxczxczx', 'cat-game-of-thrones-jon-snow-artwork-wallpaper-preview.jpg', 'ridhanurrachmat@students.amikom.ac.id', 'accepted', '2024-12-11 14:14:23'),
(9, 10, 'asdadasdasdasd', 'zckjefjshkjdghsdjkgh', '2791085.jpg', 'ridhanurrachmat@students.amikom.ac.id', 'accepted', '2024-12-11 14:14:25'),
(10, 11, 'asdasd', 'kzmckzmcxkzmckzmckzxczxczc', 'cat-game-of-thrones-jon-snow-artwork-wallpaper-preview.jpg', 'ridhanurrachmat@students.amikom.ac.id', 'accepted', '2024-12-11 14:14:28');

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
('ridhanurrachmat@students.amikom.ac.id', 'qwerty121', 'rid', 1);

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
  MODIFY `item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `tbl_item_history`
--
ALTER TABLE `tbl_item_history`
  MODIFY `history_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `tbl_item_user`
--
ALTER TABLE `tbl_item_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
