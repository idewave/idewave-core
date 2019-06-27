-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 29, 2019 at 10:44 PM
-- Server version: 5.7.23-0ubuntu0.16.04.1
-- PHP Version: 7.0.32-0ubuntu0.16.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `wowdb_world`
--

-- --------------------------------------------------------

--
-- Dumping data for table `spell_template`
--

INSERT INTO `spell_template` (`id`, `entry`, `name`, `cost`, `school`, `range`) VALUES
(1, 668, 'Language Common', 0, 0, 0),
(2, 671, 'Language Darnassian', 0, 0, 0),
(3, 815, 'Language Demon Tongue', 0, 0, 0),
(4, 814, 'Language Draconic', 0, 0, 0),
(5, 29932, 'Language Draenei', 0, 0, 0),
(6, 672, 'Language Dwarven', 0, 0, 0),
(7, 7340, 'Language Gnomish', 0, 0, 0),
(8, 17737, 'Language Gutterspeak', 0, 0, 0),
(9, 817, 'Language Old Tongue (NYI)', 0, 0, 0),
(10, 669, 'Language Orcish', 0, 0, 0),
(11, 670, 'Language Taurahe', 0, 0, 0),
(12, 813, 'Language Thalassian', 0, 0, 0),
(13, 816, 'Language Titan', 0, 0, 0),
(14, 7341, 'Language Troll', 0, 0, 0),
(15, 6603, 'Auto Attack', 0, 0, 0),
(16, 20598, 'Human Spirit', 0, 0, 0),
(17, 20600, 'Perception', 0, 0, 0),
(18, 20599, 'Diplomacy', 0, 0, 0),
(19, 20594, 'Stoneform', 0, 0, 0),
(20, 20596, 'Frost Resistance', 0, 0, 0),
(21, 2481, 'Find Treasure', 0, 0, 0),
(22, 20583, 'Nature Resistance', 0, 0, 0),
(23, 20582, 'Quickness', 0, 0, 0),
(24, 21009, 'Shadowmeld Passive', 0, 0, 0),
(25, 20580, 'Shadowmeld', 0, 0, 0),
(26, 20585, 'Wisp Spirit', 0, 0, 0),
(27, 20591, 'Expansive Mind', 0, 0, 0),
(28, 20589, 'Escape Artist', 0, 0, 0),
(29, 20593, 'Engineering Specialization', 0, 0, 0),
(30, 28875, 'Gemcutting', 0, 0, 0),
(31, 28880, 'Gift of the Naaru', 0, 1, 40),
(32, 6562, 'Heroic Presence', 0, 0, 0),
(33, 20579, 'Shadow Resistance', 0, 0, 0),
(34, 20572, 'Blood Fury', 0, 0, 0),
(35, 33697, 'Blood Fury (shaman)', 0, 0, 0),
(36, 33702, 'Blood Fury (warlock)', 0, 0, 0),
(37, 21563, 'Command', 0, 0, 0),
(38, 20576, 'Command (hunter)', 0, 0, 0),
(39, 20575, 'Command (warlock)', 0, 0, 0),
(40, 20573, 'Hardiness', 0, 0, 0),
(41, 20577, 'Cannibalize', 0, 0, 5),
(42, 5227, 'Underwater Breathing', 0, 0, 0),
(43, 7744, 'Will of the Forsaken', 0, 0, 0),
(44, 20552, 'Cultivation', 0, 0, 0),
(45, 20550, 'Endurance', 0, 0, 0),
(46, 20551, 'Nature Resistance (tauren)', 0, 0, 0),
(47, 20549, 'War Stomp', 0, 0, 0),
(48, 20557, 'Beast Slaying', 0, 0, 0),
(49, 26296, 'Berserking (warrior)', 5, 0, 0),
(50, 26297, 'Berserking (rogue)', 10, 0, 0),
(51, 20555, 'Regeneration', 0, 0, 0),
(52, 20554, 'Berserking (caster, 6% of base mana)', 6, 0, 0),
(53, 20558, 'Throwing Specialization', 0, 0, 0),
(54, 28877, 'Arcane Affinity', 0, 0, 0),
(55, 25046, 'Arcane Torrent (rogue)', 0, 6, 0),
(56, 28730, 'Arcane Torrent (caster)', 0, 6, 0),
(57, 822, 'Magic Resistance', 0, 0, 0),
(58, 28734, 'Mana Tap', 0, 6, 30),
(59, 20592, 'Arcane Resistance', 0, 0, 0),
(60, 28878, 'Inspiring Presence', 0, 0, 0);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
