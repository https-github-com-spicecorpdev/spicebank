CREATE SEQUENCE account_number START WITH 0 INCREMENT BY 1 MINVALUE=0 MAXVALUE=999999;

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

CREATE TABLE bank(
    id int not null auto_increment,
    balance float not null,
    primary key (id)
) ENGINE='InnoDB' DEFAULT CHARACTER SET 'utf8' COLLATE 'utf8_general_ci';

insert into bank (balance) values(1000);
insert into users(name, cpf, password, account, balance) values('Aline', '00000000001', '123456', next value for account_number, 100);
insert into users(name, cpf, password, account, balance) values('Luan', '00000000002', '123456',  next value for account_number, 150);
insert into users(name, cpf, password, account, balance) values('Lena', '00000000003', '123456',  next value for account_number, 200);