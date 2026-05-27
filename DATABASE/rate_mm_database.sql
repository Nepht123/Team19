CREATE DATABASE rate_mm;
USE rate_mm;

	#This is my modules table 
CREATE TABLE modules
(
id INT PRIMARY KEY AUTO_INCREMENT,
mod_code VARCHAR(15) UNIQUE NOT NULL,
mod_name VARCHAR(127) NOT NULL,
credits INT NOT NULL,
prerequisites VARCHAR(255) DEFAULT "None",
corequisites VARCHAR(255) DEFAULT "None"

);

	#This is my faculties table 
CREATE TABLE faculties
(
id INT PRIMARY KEY AUTO_INCREMENT,
fac_name VARCHAR(63) NOT NULL,
is_available BOOLEAN DEFAULT FALSE,
icon_name VARCHAR(63) NOT NULL
);



	#Here I am creating the users table
CREATE TABLE users
(
id INT PRIMARY KEY AUTO_INCREMENT,
username VARCHAR(50) UNIQUE NOT NULL,
student_email VARCHAR(50) UNIQUE NOT NULL,
password VARCHAR(255) NOT NULL
);

SELECT * FROM users;