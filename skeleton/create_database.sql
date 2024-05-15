DROP TABLE Curriculums;
DROP TABLE Notes;
DROP TABLE Validations;
DROP TABLE Courses;
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
    id SERIAL PRIMARY KEY 
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