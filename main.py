import psycopg2

# parameters used for database connection - MODIFY AS REQUIRED
dbname = 'A3'
user = 'postgres'
password = 'postgres'
host = 'localhost'
port = '5432'

# Q1 - function that retrieves and displays all records from the students table
def getAllStudents():
    query = 'SELECT * FROM students'
    cursor.execute(query)

    rows = cursor.fetchall()
    print("(student_id, first_name, last_name, email, enrollment_date)")
    for row in rows:
        print(row)

# Q2 - function that inserts a new student record into the students table
def addStudent(first_name, last_name, email, enrollment_date):
    query = f"INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES ('{first_name}', '{last_name}', '{email}', '{enrollment_date}')"
    try:
        cursor.execute(query)
        conn.commit()
    except:
        print('ERROR: Could not insert new student record into students table')

# Q3 - function that updates the email address for a student with the specified student_id
def updateStudentEmail(student_id, new_email):
    query = f"UPDATE students SET email = '{new_email}' WHERE student_id = {student_id}"
    try:
        cursor.execute(query)
        conn.commit()
    except psycopg2.errors.UniqueViolation as e:
        print(f'ERROR! Could not complete email update: {e}')
    except:
        print('ERROR: Could not complete email update')

# Q4 - function that deletes the record of the student with the specified student_id
def deleteStudent(student_id):
    query = f'DELETE FROM students WHERE student_id = {student_id}'
    try:
        cursor.execute(query)
        conn.commit()
    except:
        print('ERROR: Could not delete student\'s record from the students table')

def run():
    configure_table()
    while 1:
        print('Select one of the options below to interact with the database:\n'
              '1 - Retrieve and display all records from the students table\n'
              '2 - Insert a new student record into the students table\n'
              '3 - Update the email address for a student with the specified student_id\n'
              '4 - Delete the record of the student with the specified student_id\n'
              '5 - Exit\n')
        option = int(input())

        if option == 1:
            getAllStudents()
        elif option == 2:
            new_student = input('Enter the fields for the new student in the following space-separated format:\n'
                     'first_name last_name email enrollment_date\n')
            f_name, l_name, email, enrollment = new_student.split()
            addStudent(f_name, l_name, email, enrollment)
        elif option == 3:
            updated_student = input('Enter the student\'s ID and their updated email in the following space-separated format:\n'
                                    'student_id new_email\n')
            id, new_email = updated_student.split()
            updateStudentEmail(id, new_email)
        elif option == 4:
            student = input('Enter the ID of the student to delete:\n')
            deleteStudent(student)
        elif option == 5:
            break

        print('\n----------------------------------------------------------------------------\n')

def configure_table():
    # delete students table if it exists
    cursor.execute("DROP TABLE IF EXISTS students")
    # create new students table
    cursor.execute("CREATE TABLE IF NOT EXISTS students (student_id SERIAL PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL, email TEXT NOT NULL UNIQUE, enrollment_date DATE);")
    # populate students table with initial data
    cursor.execute("INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES ('John', 'Doe', 'john.doe@example.com', '2023-09-01'), ('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'), ('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02');")
    conn.commit()

# establish connection to database
try:
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
except psycopg2.OperationalError as e:
    print(f'Error: {e}')
    exit(1) # if we cannot even connect to the database, there's no point in proceeding with the rest of the application until the user fixes the connection parameters

# create a cursor from the connection
cursor = conn.cursor()

# main program execution
run()

# close the cursor and connection to the database
cursor.close()
conn.close()