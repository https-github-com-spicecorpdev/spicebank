-- DROP DATABASE spicebank;

-- Criando estrutura do banco de dados para spicebank
CREATE DATABASE IF NOT EXISTS `spicebank`;
USE `spicebank`;

CREATE SEQUENCE IF NOT EXISTS account_number START WITH 1001 INCREMENT BY 1 MINVALUE=0 MAXVALUE=999999;

CREATE SEQUENCE IF NOT EXISTS agency_number START WITH 2 INCREMENT BY 1 MINVALUE=0 MAXVALUE=999999;

CREATE SEQUENCE IF NOT EXISTS manager_registration_number START WITH 1000 INCREMENT BY 1 MINVALUE=0 MAXVALUE=999999;

-- Criando estrutura para tabela spicebank.taccount
CREATE TABLE IF NOT EXISTS `taccount` (
  `idAccount` int(11) NOT NULL AUTO_INCREMENT,
  `numberAccount` int(11) DEFAULT NULL,
  `totalbalance` float DEFAULT NULL,
  `idAccountUser` int(11) DEFAULT NULL,
  `agencyUser` int(11) DEFAULT NULL,
  is_active bool default true,
  account_type ENUM('CC','CP') default 'CC',
  PRIMARY KEY (`idAccount`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4;

-- Criando estrutura para tabela spicebank.profile
CREATE TABLE IF NOT EXISTS `profile` (
  `id` int(1) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4;

INSERT INTO `profile` (`id`, `name`) VALUES
	(1, 'gerente geral'),
	(2, 'gerente regional');

-- Criando estrutura para tabela spicebank.tuser
CREATE TABLE IF NOT EXISTS `tuser` (
  `idUser` int(11) NOT NULL AUTO_INCREMENT,
  `nameUser` varchar(255) DEFAULT NULL,
  `cpfUser` bigint(12) UNIQUE,
  `roadUser` varchar(255) DEFAULT NULL,
  `numberHouseUser` int(11) DEFAULT NULL,
  `districtUser` varchar(255) DEFAULT NULL,
  `cepUser` bigint(9) DEFAULT NULL,
  `cityUser` varchar(255) DEFAULT NULL,
  `stateUser` varchar(255) DEFAULT NULL,
  `birthdateUser` date DEFAULT NULL,
  `genreUser` varchar(1) DEFAULT NULL,
  `passwordUser` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`idUser`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4;

-- Criando estrutura para tabela spicebank.solicitation
CREATE TABLE IF NOT EXISTS `solicitation` (
	id int(11) NOT NULL AUTO_INCREMENT PRIMARY key,
	id_user int(11) NOT NULL,
	status ENUM('Pendente','Aprovado','Reprovado', 'Em Análise', 'Encerrado'),
	solicitation_type ENUM('Encerrar conta','Abertura de conta','Alteração de dados cadastrais','Confirmação de depósito'),
	created_time datetime NOT NULL default current_timestamp,
	updated_time datetime on update current_timestamp,
	constraint `fk_tuser_solicitation`
  	foreign key (`id_user`) references `tuser`(idUser)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4;

-- Criando estrutura para tabela spicebank.account_solicitation
CREATE TABLE IF NOT EXISTS `account_solicitation` (
	id int(11) NOT NULL AUTO_INCREMENT PRIMARY key,
	id_solicitation int(11) NOT NULL,
	account_type ENUM('Conta Corrente','Conta Poupança') default 'Conta Corrente',
	constraint `fk_solicitation_account_solicitation`
  	foreign key (`id_solicitation`) references `solicitation`(id)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4;

-- Criando estrutura para tabela spicebank.deposit_solicitation
CREATE TABLE IF NOT EXISTS `deposit_solicitation` (
	id int(11) NOT NULL AUTO_INCREMENT PRIMARY key,
	id_solicitation int(11) NOT NULL,
	account_number int(11) NOT NULL,
	deposit_value float NOT NULL,
	constraint `fk_solicitation_open_account_solicitation`
  	foreign key (`id_solicitation`) references `solicitation`(id)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4;

-- Criando estrutura para tabela spicebank.update_user_solicitation
CREATE TABLE IF NOT EXISTS `update_user_solicitation` (
	id int(11) NOT NULL AUTO_INCREMENT PRIMARY key,
	id_solicitation int(11) NOT NULL,
	name varchar(255) DEFAULT NULL,
	road varchar(255) DEFAULT NULL,
	number_house int(11) DEFAULT NULL,
	district varchar(255) DEFAULT NULL,
	cep int(9) DEFAULT NULL,
	city varchar(255) DEFAULT NULL,
	state varchar(255) DEFAULT NULL,
	genre varchar(1) DEFAULT NULL,
	constraint `fk_solicitation_open_user_solicitation`
  	foreign key (`id_solicitation`) references `solicitation`(id)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4;

-- Criando estrutura para tabela spicebank.update_user_solicitation
CREATE TABLE IF NOT EXISTS `account_close_solicitation` (
	id int(11) NOT NULL AUTO_INCREMENT PRIMARY key,
	id_solicitation int(11) NOT NULL,
	id_account int(11) DEFAULT NULL,
	name varchar(255) DEFAULT NULL,
	cpf int(12) DEFAULT NULL,
	birthdate date DEFAULT NULL,
	road varchar(255) DEFAULT NULL,
	number_house int(11) DEFAULT NULL,
	district varchar(255) DEFAULT NULL,
	cep int(9) DEFAULT NULL,
	city varchar(255) DEFAULT NULL,
	state varchar(255) DEFAULT NULL,
	genre varchar(1) DEFAULT NULL,
	constraint `fk_open_user_solicitation_solicitation`
  	foreign key (`id_solicitation`) references `solicitation`(id),
  	constraint `fk_account_account_close_solicitation`
  	foreign key (`id_account`) references `taccount`(idAccount)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4;

-- Criando estrutura para tabela spicebank.bank_statement
CREATE TABLE IF NOT EXISTS `bank_statement` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_user` int(11) NOT NULL, 
  `balance` float(11) NOT NULL,
  `deposit` float(11) DEFAULT NULL,
  `withdraw` float(11) DEFAULT NULL,
  situation enum('Aprovado', 'Reprovado', 'Pendente'),
  created_time datetime NOT NULL default current_timestamp,
  updated_time datetime on update current_timestamp,
  `operation` varchar(1) not null,
  PRIMARY KEY (`id`),
  constraint `fk_tuser_bank_statement`
  foreign key (`id_user`) references `tuser`(idUser)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4;

-- Criando estrutura para tabela spicebank.bank
CREATE TABLE `bank`(
    `id` int(11) not null auto_increment,
    `capital` float not null,
    PRIMARY KEY (`id`)
) ENGINE='InnoDB' DEFAULT CHARACTER SET 'utf8' COLLATE 'utf8_general_ci';

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
  `id_user` INT(11) NOT NULL,
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

-- Cria capital do banco
INSERT INTO `bank`(capital) VALUES(0);

-- Cria agência
INSERT INTO spicebank.agency
(`number`, bank_id)
VALUES(1, 1);

-- Cria agência
INSERT INTO spicebank.agency
(`number`, bank_id)
VALUES(nextval(agency_number), 1);

-- Cria agência
INSERT INTO spicebank.agency
(`number`, bank_id)
VALUES(nextval(agency_number), 1);

-- Cria agência
INSERT INTO spicebank.agency
(`number`, bank_id)
VALUES(nextval(agency_number), 1);

-- Cria usuário comum do gerente geral
INSERT INTO spicebank.tuser
(nameUser, cpfUser, roadUser, numberHouseUser, districtUser, cepUser, cityUser, stateUser, birthdateUser, genreUser, passwordUser)
VALUES('Jose', 10000000001, 'fatec', 1, 'fatec', 1, 'fatec', 'São Paulo', '2022-01-01', 'M', '123');

-- Cria gerente geral
INSERT INTO spicebank.manager
(id_user, registration_number, work_agency_id, profile_user, bank_id)
VALUES(1, NEXTVAL(manager_registration_number), 1, 1, 1);

-- Cria usuário comum do gerente agência
INSERT INTO spicebank.tuser
(nameUser, cpfUser, roadUser, numberHouseUser, districtUser, cepUser, cityUser, stateUser, birthdateUser, genreUser, passwordUser)
VALUES('Ronaldo', 10000000002, 'fatec', 1, 'fatec', 1, 'fatec', 'São Paulo', '2022-01-01', 'M', '123');

-- Cria gerente de agência
INSERT INTO spicebank.manager
(id_user, registration_number, work_agency_id, profile_user, bank_id)
VALUES(2, NEXTVAL(manager_registration_number), 2, 2, 1);

-- Cria usuário comum do gerente agência
INSERT INTO spicebank.tuser
(nameUser, cpfUser, roadUser, numberHouseUser, districtUser, cepUser, cityUser, stateUser, birthdateUser, genreUser, passwordUser)
VALUES('Igor', 10000000003, 'fatec', 1, 'fatec', 1, 'fatec', 'São Paulo', '2022-01-01', 'M', '123');

-- Cria gerente de agência
INSERT INTO spicebank.manager
(id_user, registration_number, work_agency_id, profile_user, bank_id)
VALUES(3, NEXTVAL(manager_registration_number), 3, 2, 1);

-- Cria usuário comum do gerente agência
INSERT INTO spicebank.tuser
(nameUser, cpfUser, roadUser, numberHouseUser, districtUser, cepUser, cityUser, stateUser, birthdateUser, genreUser, passwordUser)
VALUES('Luan', 10000000004, 'fatec', 1, 'fatec', 1, 'fatec', 'São Paulo', '2022-01-01', 'M', '123');

-- Cria gerente de agência
INSERT INTO spicebank.manager
(id_user, registration_number, work_agency_id, profile_user, bank_id)
VALUES(4, NEXTVAL(manager_registration_number), 4, 2, 1);

-- Cria usuário comum
INSERT INTO spicebank.tuser
(nameUser, cpfUser, roadUser, numberHouseUser, districtUser, cepUser, cityUser, stateUser, birthdateUser, genreUser, passwordUser)
VALUES('Aline', 12345678901, 'fatec', 1, 'fatec', 1, 'fatec', 'São Paulo', '2022-01-01', 'F', '123');

-- Cria solicitação abertura de conta usuário comum
INSERT INTO spicebank.solicitation
(id_user, status, solicitation_type, created_time, updated_time)
VALUES(5, 'Pendente', 'Abertura de conta', current_timestamp, null);

-- Cria solicitação abertura de conta usuário comum
insert into spicebank.account_solicitation 
(id_solicitation, account_type)
values (1,'Conta Corrente');

-- Cria conta usuário comum
INSERT INTO spicebank.taccount
(numberAccount, totalbalance, idAccountUser, agencyUser, is_active, account_type)
VALUES(NEXTVAL(account_number), 0, 5, 2, 0, 'CC');

-- Cria usuário comum
INSERT INTO spicebank.tuser
(nameUser, cpfUser, roadUser, numberHouseUser, districtUser, cepUser, cityUser, stateUser, birthdateUser, genreUser, passwordUser)
VALUES('Gabriela', 1000009012, 'fatec', 1, 'fatec', 1, 'fatec', 'São Paulo', '2022-01-01', 'F', '123');

-- Cria solicitação abertura de conta usuário comum
INSERT INTO spicebank.solicitation
(id_user, status, solicitation_type, created_time, updated_time)
VALUES(6, 'Pendente', 'Abertura de conta', current_timestamp, null);

-- Cria solicitação abertura de conta usuário comum
insert into spicebank.account_solicitation 
(id_solicitation, account_type)
values (2,'Conta Corrente');

-- Cria conta usuário comum
INSERT INTO spicebank.taccount
(numberAccount, totalbalance, idAccountUser, agencyUser, is_active, account_type)
VALUES(NEXTVAL(account_number), 0, 6, 3, 0, 'CC');