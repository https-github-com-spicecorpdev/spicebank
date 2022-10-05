-- --------------------------------------------------------
-- Servidor:                     127.0.0.1
-- Versão do servidor:           10.9.2-MariaDB - mariadb.org binary distribution
-- OS do Servidor:               Win64
-- HeidiSQL Versão:              11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Copiando estrutura do banco de dados para spicebank
CREATE DATABASE IF NOT EXISTS `spicebank` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `spicebank`;

-- Copiando estrutura para tabela spicebank.taccount
CREATE TABLE IF NOT EXISTS `taccount` (
  `idAccount` int(11) NOT NULL AUTO_INCREMENT,
  `numberAccount` int(11) DEFAULT NULL,
  `totalbalance` float DEFAULT NULL,
  `idAccountUser` int(11) DEFAULT NULL,
  `agencyUser` int(11) DEFAULT NULL,
  `statusAccount` int(11) DEFAULT NULL,
  `solicitacao` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idAccount`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4;

-- Copiando dados para a tabela spicebank.taccount: ~3 rows (aproximadamente)
DELETE FROM `taccount`;
/*!40000 ALTER TABLE `taccount` DISABLE KEYS */;
INSERT INTO `taccount` (`idAccount`, `numberAccount`, `totalbalance`, `idAccountUser`, `agencyUser`, `statusAccount`, `solicitacao`) VALUES
	(3, 2146, 209.05, 1, 1, 1, 'aprovado'),
	(11, NULL, NULL, 22, NULL, NULL, 'pendente'),
	(12, 2145, 0, 22, 1, 1, 'aprovado');
/*!40000 ALTER TABLE `taccount` ENABLE KEYS */;

-- Copiando estrutura para tabela spicebank.tagency
CREATE TABLE IF NOT EXISTS `tagency` (
  `idAgency` int(11) NOT NULL AUTO_INCREMENT,
  `accountAgency` int(11) DEFAULT NULL,
  `locAgency` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`idAgency`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;

-- Copiando dados para a tabela spicebank.tagency: ~3 rows (aproximadamente)
DELETE FROM `tagency`;
/*!40000 ALTER TABLE `tagency` DISABLE KEYS */;
INSERT INTO `tagency` (`idAgency`, `accountAgency`, `locAgency`) VALUES
	(1, 3583, 'SJC'),
	(2, 3584, 'Cacapava'),
	(3, 3585, 'SP'),
	(4, 3586, 'Taubate');
/*!40000 ALTER TABLE `tagency` ENABLE KEYS */;

-- Copiando estrutura para tabela spicebank.textract
CREATE TABLE IF NOT EXISTS `textract` (
  `idExtract` int(11) NOT NULL AUTO_INCREMENT,
  `userExtract` int(11) NOT NULL,
  `depositExtract` float DEFAULT NULL,
  `withdrawExtract` float DEFAULT NULL,
  `dateExtract` date DEFAULT NULL,
  PRIMARY KEY (`idExtract`),
  UNIQUE KEY `idtExtract_UNIQUE` (`idExtract`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

-- Copiando dados para a tabela spicebank.textract: ~3 rows (aproximadamente)
DELETE FROM `textract`;
/*!40000 ALTER TABLE `textract` DISABLE KEYS */;
INSERT INTO `textract` (`idExtract`, `userExtract`, `depositExtract`, `withdrawExtract`, `dateExtract`) VALUES
	(1, 1, 359, 0, '2022-09-02'),
	(2, 1, 0, 20, '2022-09-03'),
	(3, 1, 0, 0, '2022-09-03');
/*!40000 ALTER TABLE `textract` ENABLE KEYS */;

-- Copiando estrutura para tabela spicebank.tprofile
CREATE TABLE IF NOT EXISTS `tprofile` (
  `idProfile` int(11) NOT NULL AUTO_INCREMENT,
  `nameProfile` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`idProfile`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

-- Copiando dados para a tabela spicebank.tprofile: ~3 rows (aproximadamente)
DELETE FROM `tprofile`;
/*!40000 ALTER TABLE `tprofile` DISABLE KEYS */;
INSERT INTO `tprofile` (`idProfile`, `nameProfile`) VALUES
	(1, 'gerente geral'),
	(2, 'gerente regional'),
	(3, 'usuario');
/*!40000 ALTER TABLE `tprofile` ENABLE KEYS */;

-- Copiando estrutura para tabela spicebank.tuser
CREATE TABLE IF NOT EXISTS `tuser` (
  `idUser` int(11) NOT NULL AUTO_INCREMENT,
  `nameUser` varchar(255) DEFAULT NULL,
  `cpfUser` int(12) DEFAULT NULL,
  `profileUser` int(1) DEFAULT NULL,
  `roadUser` varchar(255) DEFAULT NULL,
  `districtUser` varchar(255) DEFAULT NULL,
  `numberHouseUser` int(11) DEFAULT NULL,
  `cepUser` int(9) DEFAULT NULL,
  `celUser` int(12) DEFAULT NULL,
  `passwordUser` varchar(255) DEFAULT NULL,
  `genreUser` varchar(1) DEFAULT NULL,
  `birthdateUser` date DEFAULT NULL,
  `emailUser` varchar(50) DEFAULT NULL,
  `cityUser` varchar(255) DEFAULT NULL,
  `stateUser` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`idUser`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4;

-- Copiando dados para a tabela spicebank.tuser: ~15 rows (aproximadamente)
DELETE FROM `tuser`;
/*!40000 ALTER TABLE `tuser` DISABLE KEYS */;
INSERT INTO `tuser` (`idUser`, `nameUser`, `cpfUser`, `profileUser`, `roadUser`, `districtUser`, `numberHouseUser`, `cepUser`, `celUser`, `passwordUser`, `genreUser`, `birthdateUser`, `emailUser`, `cityUser`, `stateUser`) VALUES
	(1, 'Ronaldo', 1234567899, 3, 'Avenida', 'Jardim', 148, 12225485, 1293569874, 'ronaldo', 'M', '1990-04-26', 'fenomeno', NULL, NULL),
	(7, '1', 1, NULL, NULL, NULL, NULL, NULL, NULL, '1', NULL, NULL, NULL, NULL, NULL),
	(8, 'yuri', 123, NULL, NULL, NULL, NULL, NULL, NULL, '1234', NULL, NULL, NULL, NULL, NULL),
	(9, 'yuri', 123, NULL, NULL, NULL, NULL, NULL, NULL, '1234', NULL, NULL, NULL, NULL, NULL),
	(10, 'ric', 12315, NULL, NULL, NULL, NULL, NULL, NULL, '123', NULL, NULL, NULL, NULL, NULL),
	(11, 'eli', 12345, NULL, NULL, NULL, NULL, NULL, NULL, '1234', NULL, NULL, NULL, NULL, NULL),
	(12, '12', 12, NULL, NULL, NULL, NULL, NULL, NULL, '12', NULL, NULL, NULL, NULL, NULL),
	(13, 'yuri', 123, NULL, NULL, NULL, NULL, NULL, NULL, '1234', NULL, NULL, NULL, NULL, NULL),
	(14, 'eli', 124578, NULL, NULL, NULL, NULL, NULL, NULL, '123', NULL, NULL, NULL, NULL, NULL),
	(15, 'a', 1231, NULL, NULL, NULL, NULL, NULL, NULL, '123', NULL, NULL, NULL, NULL, NULL),
	(16, 'yuri', 123, NULL, NULL, NULL, NULL, NULL, NULL, '1234', NULL, NULL, NULL, NULL, NULL),
	(17, '12', 21, NULL, NULL, NULL, NULL, NULL, NULL, '123', NULL, NULL, NULL, NULL, NULL),
	(18, '12', 21, NULL, NULL, NULL, NULL, NULL, NULL, '123', NULL, NULL, NULL, NULL, NULL),
	(19, '12', 1213, NULL, NULL, NULL, NULL, NULL, NULL, '123', NULL, NULL, NULL, NULL, NULL),
	(20, 'abreu', 21, NULL, NULL, NULL, NULL, NULL, NULL, '123', NULL, NULL, NULL, NULL, NULL),
	(21, 'Iago', 123122, NULL, NULL, NULL, NULL, NULL, NULL, '123', NULL, NULL, NULL, NULL, NULL),
	(22, 'Queila', 1232133441, NULL, 'SJC', 'Pernambuco', 32, 11109, 1313, '1234', 'F', '2022-09-28', 'queila@live', NULL, NULL);
/*!40000 ALTER TABLE `tuser` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
