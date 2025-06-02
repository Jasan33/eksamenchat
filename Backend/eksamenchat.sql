CREATE DATABASE eksamenchat;
USE eksamenchat;

CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) unique,
    email VARCHAR(255),
    password VARBINARY(255)
);