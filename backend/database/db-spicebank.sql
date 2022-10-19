-- Criando estrutura do banco de dados para spicebank
CREATE DATABASE IF NOT EXISTS `spicebank`;
USE `spicebank`;

CREATE SEQUENCE IF NOT EXISTS account_number START WITH 1001 INCREMENT BY 1 MINVALUE=0 MAXVALUE=999999;

CREATE SEQUENCE IF NOT EXISTS agency_number START WITH 1 INCREMENT BY 1 MINVALUE=0 MAXVALUE=999999;

CREATE SEQUENCE IF NOT EXISTS manager_registration_number START WITH 1000 INCREMENT BY 1 MINVALUE=0 MAXVALUE=999999;

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

-- Criando estrutura para tabela spicebank.profile
CREATE TABLE IF NOT EXISTS `profile` (
  `id` int(1) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

INSERT INTO `profile` (`id`, `name`) VALUES
	(1, 'gerente geral'),
	(2, 'gerente regional');

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
  PRIMARY KEY (`idUser`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4;

-- Criando estrutura para tabela spicebank.bank_statement
CREATE TABLE IF NOT EXISTS `bank_statement` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_user` int(11) NOT NULL, 
  `balance` float(11) NOT NULL,
  `deposit` float(11) DEFAULT NULL,
  `withdraw` float(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `operation` varchar(1) not null,
  PRIMARY KEY (`id`),
  constraint `fk_tuser_bank_statement`
  foreign key (`id_user`) references `tuser`(idUser)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `bank`(
    `id` int(11) not null auto_increment,
    `capital` float not null,
    PRIMARY KEY (`id`)
) ENGINE='InnoDB' DEFAULT CHARACTER SET 'utf8' COLLATE 'utf8_general_ci';

INSERT INTO `bank`(capital) VALUES(1000);

-- Criando estrutura para tabela agency
CREATE TABLE IF NOT EXISTS `agency` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `number` int(11) NOT NULL,
  `bank_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  constraint `fk_agency_bank`
  foreign key (`bank_id`) references `bank`(id)
) ENGINE='InnoDB' DEFAULT CHARACTER SET 'utf8' COLLATE 'utf8_general_ci';

-- Criando estrutura para tabela agency_manager
CREATE TABLE IF NOT EXISTS `manager` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_user` int(10) NOT NULL,
  `registration_number` int(12) NOT NULL,
  `work_agency_id` int(11),
  `profile_user` int(1) DEFAULT NULL,
  `bank_id` int(1) NOT NULL,
  PRIMARY KEY (`id`),
  constraint `fk_agency_manager_profile_user`
  foreign key (`profile_user`) references `profile`(`id`),
  constraint `fk_agency_manager_id_user`
  foreign key (`id_user`) references `tuser`(`idUser`),
  constraint `fk_manager_bank`
  foreign key (`bank_id`) references `bank`(`id`)
) ENGINE='InnoDB' DEFAULT CHARACTER SET 'utf8' COLLATE 'utf8_general_ci';


-- Cria agência
INSERT INTO spicebank.agency
(`number`, bank_id)
VALUES(nextval(agency_number), 1);

-- Cria gerente geral
INSERT INTO spicebank.manager
(id_user, registration_number, work_agency_id, profile_user, bank_id)
VALUES(25, NEXTVAL(manager_registration_number), null, 1, 1);

-- Cria gerente Agência
INSERT INTO spicebank.manager
(id_user, registration_number, work_agency_id, profile_user, bank_id)
VALUES(23, NEXTVAL(manager_registration_number), 1, 2, 1);

-- Cria usuário comum
INSERT INTO spicebank.tuser
(nameUser, cpfUser, roadUser, numberHouseUser, districtUser, cepUser, cityUser, stateUser, birthdateUser, genreUser, passwordUser)
VALUES('José', 3, 'fatec', 1, 'fatec', 1, 'fatec', 'fatec', '2022-01-01', 'M', '123');