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
    id SERIAL PRIMARY KEY 
);

CREATE TABLE Curriculums (
    title TEXT,
    secretary INT REFERENCES Persons(id),
    director INT REFERENCES Persons(id),
    id SERIAL PRIMARY KEY
);

CREATE TABLE Courses (
    title TEXT,
    teacher INT REFERENCES Persons(id),
    id_curriculum INT REFERENCES Curriculums(id),
    id SERIAL PRIMARY KEY 
);  

CREATE TABLE Ects (
    id_courses INT REFERENCES Courses(id),
    id_curr INT REFERENCES Curriculums(id),
    nombre INT
);

CREATE TABLE Curr_pers(
    id_pers INT REFERENCES Persons(id),
    id_curr INT REFERENCES Curriculums(id)
);

CREATE TABLE Curr_courses(
    id_curr INT REFERENCES Curriculums(id),
    id_courses INT REFERENCES Courses(id)
);

CREATE TABLE Validations (
    title TEXT,
    id SERIAL PRIMARY KEY,
    course INT REFERENCES Courses(id)
);

CREATE TABLE Notes (
    id_person INT REFERENCES Persons(id),
    id_validation INT REFERENCES Validations(id),
    note INT
);