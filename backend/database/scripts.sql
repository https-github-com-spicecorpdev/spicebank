--Comando que cria automaticamente o número da conta do usuário na tabela.
CREATE SEQUENCE account_number START WITH 0 INCREMENT BY 1 MINVALUE=0 MAXVALUE=999999;

--Comandos que cria a tabela de usuários.
CREATE TABLE users(
    id int not null auto_increment,
    name varchar(16),
    cpf varchar(16),
    password varchar(20),
    agency int default 1,
    account int UNIQUE,
    balance float DEFAULT 0,
    primary key(id)
) ENGINE='InnoDB' DEFAULT CHARACTER SET 'utf8' COLLATE 'utf8_general_ci';

--Comando que cria a tabela do banco.
CREATE TABLE bank(
    id int not null auto_increment,
    balance float not null,
    primary key (id)
) ENGINE='InnoDB' DEFAULT CHARACTER SET 'utf8' COLLATE 'utf8_general_ci';

--Comando para popular a tabela bank.
insert into bank (balance) values(1000);

--Comando para popular a tabela users.
insert into users(name, cpf, password, account, balance) values('User1', '00000000001', '123456', next value for account_number, 100);
insert into users(name, cpf, password, account, balance) values('User2', '00000000002', '123456',  next value for account_number, 150);
insert into users(name, cpf, password, account, balance) values('User3', '00000000003', '123456',  next value for account_number, 200);

--Comando para visualizar todos os dados existentes na tabela users.
Select * from users;

--Comando para visualizar todos os dados existentes na tabela bank.
Select * from bank;