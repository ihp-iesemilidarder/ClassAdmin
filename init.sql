CREATE USER 'ClassAdmin'@'%' IDENTIFIED BY '12345678';
GRANT ALL PRIVILEGES ON ClassAdmin.* TO 'ClassAdmin'@'%';
FLUSH PRIVILEGES;
CREATE DATABASE ClassAdmin;
use ClassAdmin;
CREATE TABLE server (
	id		INT		AUTO_INCREMENT,
	password	VARCHAR(500)	NOT NULL,
	address		VARCHAR(15)	NOT NULL,
	port		INT(5)		NOT NULL,
	status		VARCHAR(50)	NOT NULL,
	CONSTRAINT 	server_PK 	PRIMARY KEY (id),
	CONSTRAINT port_CK CHECK (port BETWEEN 0 AND 65535),
	CONSTRAINT_address_CK CHECK (address REGEXP "^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$")
);

CREATE TABLE clients (
	id		INT		AUTO_INCREMENT,
	nick		VARCHAR(50)	NOT NULL,
	address		VARCHAR(15)	NOT NULL,
	port		INT(5)		NOT NULL,
	status		VARCHAR(50)	NOT NULL,
	cli_ser_id	INT		NOT NULL,
	CONSTRAINT	clients_PK	PRIMARY KEY (id),
	CONSTRAINT port_CK CHECK (port BETWEEN 0 AND 65535),
	CONSTRAINT address_REGEXP CHECK (address REGEXP "^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$")
);

# CONNECTED, DISCONNECTED, ERROR
CREATE TABLE status (
	name		VARCHAR(50)	NOT NULL,
	CONSTRAINT	status_PK	PRIMARY KEY (name)
);

ALTER TABLE clients ADD CONSTRAINT cli_ser_FK FOREIGN KEY (cli_ser_id) REFERENCES server (id);
ALTER TABLE clients ADD CONSTRAINT cli_status_FK FOREIGN KEY (status) REFERENCES status (name);
ALTER TABLE clients ADD CONSTRAINT ser_status_FK FOREIGN KEY (status) REFERENCES status (name);

INSERT INTO status (name) VALUES ("CONNECTED"),("DISCONNECTED"),("ERROR");

INSERT INTO server (password,port,status) VALUES ("fa585d89c851dd338a70dcf535aa2a92fee7836dd6aff1226583e88e0996293f16bc009c652826e0fc5c706695a03cddce372f139eff4d13959da6f1f5d3eabe",7788,"DISCONNECTED");

INSERT INTO clients (nick,address,port,status,cli_ser_id) VALUES ("PC1","192.168.0.10",10192,"DISCONNECTED",1);
