-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 21, 2021 at 05:42 PM
-- Server version: 10.4.19-MariaDB
-- PHP Version: 7.3.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sign_up`
--
CREATE DATABASE IF NOT EXISTS `sign_up` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `sign_up`;

-- --------------------------------------------------------

--
-- Table structure for table `signup`
--

CREATE TABLE `signup` (
  `id` int(10) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `income` int(11) NOT NULL,
  `age` int(100) NOT NULL,
  `states` varchar(60) NOT NULL,
  `kids` varchar(5) NOT NULL,
  `svgAmt` int(100) NOT NULL,
  `Goal1` varchar(200) NOT NULL,
  `cursv1` int(100) NOT NULL,
  `tgsv1` int(100) NOT NULL,
  `Goal2` varchar(200) NOT NULL,
  `cursv2` int(100) NOT NULL,
  `tgsv2` int(100) NOT NULL,
  `HId` varchar(200) NOT NULL,
  `HIr` varchar(200) NOT NULL,
  `TId` varchar(200) NOT NULL,
  `TIr` varchar(100) NOT NULL,
  `FId` varchar(200) NOT NULL,
  `FIr` varchar(100) NOT NULL,
  `CId` varchar(200) NOT NULL,
  `CIr` varchar(200) NOT NULL,
  `2WId` varchar(200) NOT NULL,
  `2Wr` varchar(200) NOT NULL,
  `HOD` varchar(200) NOT NULL,
  `HOR` varchar(200) NOT NULL,
  `newstype` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `signup`
--

INSERT INTO `signup` (`id`, `name`, `email`, `password`, `income`, `age`, `states`, `kids`, `svgAmt`, `Goal1`, `cursv1`, `tgsv1`, `Goal2`, `cursv2`, `tgsv2`, `HId`, `HIr`, `TId`, `TIr`, `FId`, `FIr`, `CId`, `CIr`, `2WId`, `2Wr`, `HOD`, `HOR`, `newstype`) VALUES
(1, 'Hreamb', 'herambpawar1307@gmail.com', '123', 123456, 124, 'kerala', 'yes', 100, 'Bike', 10000, 70000, 'Travels', 2000, 50000, '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', ''),
(4, 'abc', 'herambpawar@gmail.com', '1234', 0, 0, '', '', 100, 'ABC', 300, 0, '', 0, 0, '', '0', '', '0', '', '0', '', '0', '0', '0', '', '0', ''),
(6, 'Test', 'Test@1234', '4567', 0, 0, '', '', 0, '', 0, 0, '', 0, 0, '', '0', '', '0', '', '0', '', '0', '0', '0', '', '0', ''),
(7, 'Aman', 'Aman@gmail.com', '3456', 1234567, 12, 'chhattisgarh', 'no', 0, '', 0, 0, '', 0, 0, '', '0', '', '0', '', '0', '', '0', '0', '0', '', '0', '');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `signup`
--
ALTER TABLE `signup`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `signup`
--
ALTER TABLE `signup`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
