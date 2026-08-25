CREATE DATABASE rate_mm;
USE rate_mm;

	#This is my modules table 
CREATE TABLE modules
(
id INT PRIMARY KEY AUTO_INCREMENT,
mod_code VARCHAR(15) UNIQUE NOT NULL,
mod_name VARCHAR(127) NOT NULL,
prerequisites VARCHAR(255) DEFAULT "None",
corequisites VARCHAR(255) DEFAULT "None",
learning_outcome VARCHAR(2000) NOT NULL DEFAULT 'None',
main_content VARCHAR(2000) NOT NULL DEFAULT 'None',
credits VARCHAR(20) NOT NULL DEFAULT 'None'

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
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    student_email VARCHAR(100) UNIQUE NOT NULL, 
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'ROLE_STUDENT',
    
    -- Context for the UI
    degree_program VARCHAR(100),                
    year_of_study VARCHAR(20),                  
    
    -- Community/Gamification
    helpful_votes INT DEFAULT 0,                
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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


CREATE TABLE reviews (
    id INT PRIMARY KEY AUTO_INCREMENT,
    
    -- 1. The README Rating Requirements (Out of 10)
    difficulty_rating INT NOT NULL CHECK (difficulty_rating BETWEEN 1 AND 10),
    teaching_rating INT NOT NULL CHECK (teaching_rating BETWEEN 1 AND 10),
    content_rating INT NOT NULL CHECK (content_rating BETWEEN 1 AND 10),
    
    -- 2. The Text Content (Separated for the UI)
    pros TEXT,
    cons TEXT,
    general_advice TEXT,
    
    -- 3. UX Features
    is_anonymous BOOLEAN DEFAULT FALSE,
    helpful_votes INT DEFAULT 0,
    
    -- 4. Metadata & Relations
    date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    module_id INT NOT NULL,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE
);


Use rate_mm;

SELECT * FROM modules;
DELETE FROM reviews WHERE id =6; 
SELECT * FROM courses;



Select id from modules where mod_code="APG232";

SELECT id FROM users WHERE username=4492340;





Select mod_name from modules where id=1;

SELECT id FROM courses where course_name="Bachelor of Science in Applied Geology";


SELECT id FROM faculties where fac_name="Law";


 
