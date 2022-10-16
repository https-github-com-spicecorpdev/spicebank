-- Criando banco de dados para spicebank
CREATE DATABASE IF NOT EXISTS `spicebank`;
USE `spicebank`;

CREATE SEQUENCE IF NOT EXISTS account_number START WITH 1001 INCREMENT BY 1 MINVALUE=0 MAXVALUE=999999;

CREATE SEQUENCE IF NOT EXISTS agency_manager START WITH 1 INCREMENT BY 1 MINVALUE=0 MAXVALUE=999999;

-- Criando estrutura para tabela spicebank.taccount
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

-- Criando estrutura para tabela spicebank.tprofile
CREATE TABLE IF NOT EXISTS `tprofile` (
  `idProfile` int(11) NOT NULL AUTO_INCREMENT,
  `nameProfile` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`idProfile`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;


INSERT INTO `tprofile` (`idProfile`, `nameProfile`) VALUES
	(1, 'gerente geral'),
	(2, 'gerente regional'),
	(3, 'usuario');

-- Criando estrutura para tabela spicebank.tagency
CREATE TABLE IF NOT EXISTS `tagency` (
  `idAgency` int(11) NOT NULL AUTO_INCREMENT,
  `accountAgency` int(11) DEFAULT NULL,
  `idManager` int(11) DEFAULT NULL,
  PRIMARY KEY (idAgency)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;


-- Criando estrutura para tabela spicebank.bank_statement
CREATE TABLE IF NOT EXISTS `bank_statement` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_user` int(11) NOT NULL,
  `balance` int(11) NOT NULL,
  `deposit` float DEFAULT NULL,
  `withdraw` float DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  constraint `fk_tuser_bank_statement`
  foreign key (id_user) references tuser(idUser)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;


-- Criando estrutura para tabela spicebank.tuser
CREATE TABLE IF NOT EXISTS `tuser` (
  `idUser` int(11) NOT NULL AUTO_INCREMENT,
  `nameUser` varchar(255) DEFAULT NULL,
  `cpfUser` int(12) DEFAULT NULL,
  `roadUser` varchar(255) DEFAULT NULL,
  `numberHouseUser` int(11) DEFAULT NULL,
  `districtUser` varchar(255) DEFAULT NULL,
  `cepUser` int(9) DEFAULT NULL,
  `cityUser` varchar(255) DEFAULT NULL,
  `stateUser` varchar(255) DEFAULT NULL,
  `birthdateUser` date DEFAULT NULL,
  `genreUser` varchar(1) DEFAULT NULL,
  `passwordUser` varchar(255) DEFAULT NULL,
  `profileUser` int(1) DEFAULT NULL,
  PRIMARY KEY (`idUser`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4;

-- Criando estrutura para tabela spicebank.tbank
CREATE TABLE `tbank`(
    `id` int unsigned not null auto_increment primary key,
    `capital` float not null,
    `agency` int not null default 1,
    `generalManager` varchar(20) not null
) ENGINE='InnoDB' DEFAULT CHARACTER SET 'utf8' COLLATE 'utf8_general_ci';

INSERT INTO `tbank`(`capital`, `agency`, `generalManager`) VALUES(1000, 1, 'Ronaldo');
