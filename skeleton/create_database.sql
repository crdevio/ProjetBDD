DROP TABLE Ects;
DROP TABLE Notes;
DROP TABLE Curr_pers;
DROP TABLE Curr_courses;
DROP TABLE Validations;
DROP TABLE Courses;
DROP TABLE Curriculums;
DROP TABLE Persons;

CREATE TABLE Persons (
    last_name TEXT,
    first_name TEXT,
    phone_number TEXT,
    adress TEXT,
    id SERIAL PRIMARY KEY 
);

CREATE TABLE Curriculums (
    title TEXT,
    secretary INT REFERENCES Persons(id) ON DELETE CASCADE,
    director INT REFERENCES Persons(id) ON DELETE CASCADE,
    id SERIAL PRIMARY KEY
);

CREATE TABLE Courses (
    title TEXT,
    teacher INT REFERENCES Persons(id) ON DELETE CASCADE,
    id_curriculum INT REFERENCES Curriculums(id) ON DELETE CASCADE,
    id SERIAL PRIMARY KEY 
);  

CREATE TABLE Ects (
    id_courses INT REFERENCES Courses(id) ON DELETE CASCADE,
    id_curr INT REFERENCES Curriculums(id) ON DELETE CASCADE,
    nombre INT
);

CREATE TABLE Curr_pers(
    id_pers INT REFERENCES Persons(id) ON DELETE CASCADE,
    id_curr INT REFERENCES Curriculums(id) ON DELETE CASCADE
);

CREATE TABLE Curr_courses(
    id_curr INT REFERENCES Curriculums(id) ON DELETE CASCADE,
    id_courses INT REFERENCES Courses(id) ON DELETE CASCADE
);

CREATE TABLE Validations (
    title TEXT,
    id SERIAL PRIMARY KEY,
    course INT REFERENCES Courses(id) ON DELETE CASCADE,
    validation_date Date DEFAULT CURRENT_DATE,
    coeff INT
);

CREATE TABLE Notes (
    id_person INT REFERENCES Persons(id) ON DELETE CASCADE,
    id_validation INT REFERENCES Validations(id) ON DELETE CASCADE,
    note INT
);