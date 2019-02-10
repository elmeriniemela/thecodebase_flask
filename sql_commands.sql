CREATE DATABASE thecodebase;

show tables;

USE thecodebase;

CREATE TABLE users (
    uid INT(11) AUTO_INCREMENT PRIMARY KEY, 
    username VARCHAR(20), 
    password VARCHAR(100), 
    email VARCHAR(50), 
    settings VARCHAR(32500), 
    tracking VARCHAR(32500), 
    rank INT(3)
);



CREATE TABLE visits (
    visit_id INT(11) AUTO_INCREMENT PRIMARY KEY,
    uid INT,
    time DATETIME,
    remote_addr VARCHAR(45),
    endpoint VARCHAR(50),
    FOREIGN KEY (uid) REFERENCES users(uid)
);

GRANT ALL PRIVILEGES ON *.* TO 'username'@'localhost' IDENTIFIED BY 'password';

SET PASSWORD FOR 'username'@'localhost' = PASSWORD('password');