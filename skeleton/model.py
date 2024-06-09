import sys
import psycopg2
import psycopg2.extras


class Model:
    def __init__(self):
        self.connection = psycopg2.connect("dbname='glecorre' user='glecorre' host='psql.eleves.ens.fr' password='c9Wvl2so'")
        self.connection.autocommit = True
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if (self.connection):
            self.connection.close()

##############################################
######      Queries for tab  PERSONS    ######
##############################################

    # Create a new person.
    def createPerson(self, lastname, firstname, address, phone):
        self.cursor.execute(f"""
        INSERT INTO  Persons(last_name,first_name,phone_number,adress)
        VALUES ({lastname}, {firstname}, {phone},{address}); 
        """)
        self.connection.commit()

    # Return a list of (id, lastname, firstname, address, phone,
    # number of curriculums) corresponding to all persons.
    def listPersons(self):
        self.cursor.execute("""
        SELECT * FROM Persons
        """)
        return self.cursor.fetchall()

    # Delete a person given its ID (beware of the foreign constraints!).
    def deletePerson(self, idPerson):
        self.cursor.execute(f"""
        DELETE FROM Persons
        WHERE id={idPerson};
        """)
        self.connection.commit()

##############################################
######     Queries for  CURRICULUMS     ######
##############################################

    # Create a curriculum.
    def createCurriculum(self, name, secretary, director):
        self.cursor.execute(f"""
        INSERT INTO Curriculums(title, secretary, director)
        VALUES ({name},{secretary},{director})
        """)
        self.connection.commit()

    # Return a list of (id,name of curriculum,director lastname,
    # director firstname, secretary lastname, secretary firstname)
    # corresponding to all curriculums.
    def listCurriculums(self):
        self.cursor.execute("""
        SELECT * FROM Curriculums
        """)
        return self.cursor.fetchall()

    # Delete a curriculum given its ID (beware of the foreign constraints!).
    def deleteCurriculum(self, idCurriculum):
        self.cursor.execute("""
        DELETE FROM Curriculums
        WHERE id={idCurriculum}
        """)
        self.connection.commit()

##############################################
######     Queries for  COURSES         ######
##############################################

    # Create a course.
    def createCourse(self, name, idProfessor):
        self.cursor.execute(f"""
        INSERT INTO Courses(title,teacher)
        VALUES ({name},{idProfessor})
        """)
        self.connection.commit()

    # Return a list of (course id, course name, teacher id,
    # teacher last name, teacher first name) corresponding
    # to all the courses.
    def listCourses(self):
        self.cursor.execute("""
        SELECT * FROM Courses
        """)
        return self.cursor.fetchall()

    # Delete a given course (beware that the course might be registered to
    # curriculum, and have grades that should also be deleted).
    def deleteCourse(self, idCourse):
        self.cursor.execute(f"""
        DELETE FROM Courses
        WHERE id={idCourse}
        """)
        self.connection.commit()


##############################################
###### Queries for tab  CURRICULUM/<ID> ######
##############################################

    # Get the name of a given curriculum.
    def getNameOfCurriculum(self, id):
        self.cursor.execute(f"""
        SELECT title FROM Curriculums
        WHERE id = {id}
        """)
        # suppose that there is a solution
        return self.cursor.fetchall()[0][0]

    # Return the list (course ID, course name, course teacher
    # last name and first name, ECTS) corresponding to the courses
    # registered to a given curriculum.
    def listCoursesOfCurriculum(self, idCurriculum):
        self.cursor.execute(f"""
        SELECT ()
        """)
        return self.cursor.fetchall()

    #  !! HARD !!
    # Return a list (last name, first name, average grade) of students
    # registered to a given curriculum. The
    # average grade is computed as described in the document, but
    # beware that if a student does not have a grade for a validation
    # or is not registered to a course, he should have 0.
    def averageGradesOfStudentsInCurriculum(self, idCurriculum):
        self.cursor.execute(f"""
        SELECT (last name, first name, TODO) 
        FROM (((SELECT * FROM (SELECT Courses JOIN on Validations on Courses.id = Validations.course))
            JOIN (SELECT * FROM Ects WHERE id_curr = {idCurriculum}) 
                on Courses.id = id_courses)
            JOIN (SELECT Persons.id FROM (Persons JOIN Curr_pers on Persons.id = id_pers) WHERE id_curr = {idCurriculum}))

        """, idCurriculum)
        return self.cursor.fetchall()

    # Register a person to a curriculum.
    def registerPersonToCurriculum(self, idPerson, idCurriculum):
        self.cursor.execute(f"""
        INSERT INTO Curr_pers(id_pers, id_curr) VALUES({idPerson, idCurriculum}))
        """)
        self.connection.commit()

    # Register a course to a curriculum.
    def registerCourseToCurriculum(self, idCourse, idCurriculum, ects):
        self.cursor.execute(f"""
        INSERT INTO Curr_courses(id_courses, id_curr) VALUES({idCourse, idCurriculum}));
        INSERT INTO Ects(id_courses, id_curr, nombre) VALUES({idCourse, idCurriculum, ects})
        """)
        self.connection.commit()

    # Unregister a course to a curriculum.
    def deleteCourseFromCurriculum(self, idCourse, idCurriculum):
        self.cursor.execute(f"""
        DELETE FROM Curr_courses
        WHERE id_courses={idCourse} AND id_curr={idCurriculum};
        DELETE FROM Ects
        WHERE id_courses={idCourse} AND id_curr={idCurriculum};
        """)
        self.connection.commit()

##############################################
######   Queries for tab  COURSE/<ID>   ######
##############################################

    # Get the name of a given course.
    def getNameOfCourse(self, id):
        self.cursor.execute(f"""
        SELECT title FROM Courses
        WHERE id = {id}
        """)
        # suppose that there is a solution
        return self.cursor.fetchall()[0][0]

    # Return a list of (id, name, ECTS) of the curriculums in
    # which a given course is registered.
    def listCurriculumsOfCourse(self, idCourse):
        self.cursor.execute(f"""
        SELECT Curriculums.id, Curriculums.title, Ects.nombre  
        FROM Curriculums JOIN (SELECT * FROM Courses WHERE Courses.id = {idCourse}) ON Curriculums.id = id_curriculum
        JOIN Ects ON Ects.id_courses = {idCourse} AND Ects.id_curr = Curriculums.id
        JOIN Curr_courses ON Courses.id = Curr_courses.id_courses
        """)
        return self.cursor.fetchall()

    # Returns a list of (id, date, name, coefficent) for the validations
    # assiociated to a given course.
    def listValidationsOfCourse(self, idCourse):
        self.cursor.execute(f"""
        SELECT id, validation_date, title, coeff
        FROM Validations
        WHERE course = {idCourse} 
        """)
        return self.cursor.fetchall()

    # Return a list (id, last name, first name) of persons that are
    # registered in a curriculum with the given course
    def listStudentsOfCourse(self, idCourse):
        self.cursor.execute(f"""
        SELECT DISTINCT(Persons.id, last_name, first_name)
        FROM Persons
        JOIN Curr_pers ON Persons.id = Curr_pers.id_pers
        JOIN Curr_courses ON Curr_pers.id_curr = Curr_courses.id_curr
        WHERE id_courses = {idCourse}
        """)
        return self.cursor.fetchall()

    # Return a list (id, date, curriculum name, student last name,
    # student first name, validation name, grade, coefficient) of
    # grades for all the validations and students having taken them,
    # sorted by decreasing date of validation.
    def listGradesOfCourse(self, idCourse):
        self.cursor.execute("""
        SELECT 
            Validations.id, Validations.date, Curriculums.title,
            Persons.last_name, Persons.first_name, Validations.title,
            Notes.note, Validations.coefficient
        FROM Notes
        JOIN Validations ON Notes.id_validation = Validations.id
        JOIN Courses ON Validations.course = Courses.id
        JOIN Curriculums ON Courses.id_curriculum = Curriculums.id
        JOIN Persons ON Notes.id_person = Persons.id
        ORDER BY Validations.date DESC
        """)
        return self.cursor.fetchall()

    # Add a validation to a given course.
    def addValidationToCourse(self, name, coef, date, idCourse):
        self.cursor.execute(f"""
        INSERT INTO Validations (title, course, date, coefficient)
        VALUES ({name}, {idCourse}, {date}, {coef})
        """)
        self.connection.commit()

    # Add a grade to a student.
    def addGrade(self, idValidation, idStudent, grade):
        self.cursor.execute(f"""
        INSERT INTO Notes (id_person, id_validation, note)
        VALUES ({idStudent}, {idValidation}, {grade})
        """)
        self.connection.commit()

##############################################
######       Queries for tab            ######
######      COURSE/<ID1>/<ID2           ######
###### corresponding to validations     ######
##############################################

   # Return a list (grade, lastname, firstname) of grades for
   # a given validation.
    def listGradesOfValidation(self, idValidation):
        self.cursor.execute("""
        TODO23
        """, idValidation)
        return self.cursor.fetchall()

    # Get the complete name of a validation given its ID. The
    # complete name of a validation with name "exam" of a course "BDD"
    # is "BDD - exam". You should therefore preppend the name of the
    # course.
    def getNameOfValidation(self, id):
        self.cursor.execute(f"""
        SELECT Courses.title || ' - ' || Validations.title 
        FROM Validations
        JOIN Courses ON Validations.course = Courses.id
        WHERE Validations.id ={id}
        """)
        # suppose that there is a solution
        return self.cursor.fetchall()[0][0]

##############################################
######   Queries for tab  PERSON/<ID>   ######
##############################################

    # Get the name of a person given its ID.
    def getNameOfPerson(self, id):
        self.cursor.execute(f"""
        SELECT first_name || ' ' || last_name FROM Persons WHERE id = {id}
        """)
        # suppose that there is a solution
        return self.cursor.fetchall()[0][0]

    # Return a list (id, date, curriculum name, course name,
    # exam name, grade) of grades for a given student, sorted
    # by decreasing date of validation.
    def listValidationsOfStudent(self, idStudent):
        self.cursor.execute(f"""
        SELECT Validations.id, Validations.date, Curriculums.title, Courses.title, Validations.title, ROUND(Grades.grade::numeric, 2)
        FROM Persons
        JOIN Notes ON Notes.id_person = Persons.id
        JOIN Validations ON Validations.id = Notes.id_validation
        JOIN Curr_Courses ON Curr_Courses.course = Validations.course
        JOIN Curriculums ON Curr_Courses.id_curr = Curriculums.id
        JOIN Courses ON Courses.id = Validations.course
        WHERE Persons.id = {idStudent}
        """)
        return self.cursor.fetchall()

    # !!! HARD !!!
    # Return a list (curriculum name, average grade) of all the
    # curriculum a given student is registered to, where the
    # average grade is computed as before.
    def listCurriculumsOfStudent(self, idStudent):
        self.cursor.execute("""
        TODO27
        """, (idStudent, idStudent))
        return self.cursor.fetchall()