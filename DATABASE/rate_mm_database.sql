CREATE DATABASE rate_mm;
USE rate_mm;

	#This is my modules table 
CREATE TABLE modules
(
id INT PRIMARY KEY AUTO_INCREMENT,
mod_code VARCHAR(15) UNIQUE NOT NULL,
mod_name VARCHAR(127) NOT NULL,
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
password VARCHAR(255) NOT NULL,
role VARCHAR(20) DEFAULT 'ROLE_STUDENT'
);


CREATE TABLE courses
(
id INT PRIMARY KEY AUTO_INCREMENT,
course_code VARCHAR(15) UNIQUE NOT NULL,
course_name VARCHAR (127) NOT NULL,
abbreviation VARCHAR(63) NOT NULL,
duration_years INT NOT NULL,
faculty_id INT NOT NULL,

FOREIGN KEY (faculty_id) REFERENCES faculties(id) ON DELETE CASCADE
);


CREATE TABLE course_modules
(
course_id INT NOT NULL,
    module_id INT NOT NULL,
    year_of_study VARCHAR(20) NOT NULL,    
    
    PRIMARY KEY (course_id, module_id),
    
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE
);


CREATE TABLE reviews
(
    id INT PRIMARY KEY AUTO_INCREMENT,
    rating INT NOT NULL,
    comment_text TEXT NOT NULL,
    date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    module_id INT NOT NULL,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
	FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE
);


Use rate_mm;
SELECT * FROM courses;
SELECT * FROM modules;
SELECT * FROM course_modules;

 
