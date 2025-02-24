import sqlite3


conn = sqlite3.connect('school.db')
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS students
             (student_number INTEGER PRIMARY KEY,
              name TEXT,
              surname TEXT,
              age INTEGER,
              class TEXT,
              registration_date TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS lessons_list
             (lesson_id INTEGER PRIMARY KEY AUTOINCREMENT,
              lesson_name TEXT UNIQUE)''')

c.execute('''CREATE TABLE IF NOT EXISTS student_lessons
             (student_number INTEGER,
              lesson_id INTEGER,
              FOREIGN KEY(student_number) REFERENCES students(student_number),
              FOREIGN KEY(lesson_id) REFERENCES lessons_list(lesson_id),
              PRIMARY KEY(student_number, lesson_id))''')
conn.commit()


def display_lessons():
    c.execute("SELECT * FROM lessons_list")
    lessons = c.fetchall()
    print("\nAvailable Lessons:")
    for lesson in lessons:
        print(f"{lesson[0]}: {lesson[1]}")


def add_lesson():
    lesson_name = input("Enter new lesson name: ").strip()
    try:
        c.execute("INSERT INTO lessons_list (lesson_name) VALUES (?)", (lesson_name,))
        conn.commit()
        print("Lesson added successfully!")
    except sqlite3.IntegrityError:
        print("This lesson already exists!")


def update_lesson():
    display_lessons()
    try:
        lesson_id = int(input("Enter lesson ID to update: "))
        new_name = input("Enter new lesson name: ").strip()

        c.execute("UPDATE lessons_list SET lesson_name = ? WHERE lesson_id = ?",
                  (new_name, lesson_id))
        conn.commit()
        print("Lesson updated successfully!" if c.rowcount > 0 else "Lesson not found!")
    except ValueError:
        print("Invalid input!")


def delete_lesson():
    display_lessons()
    try:
        lesson_id = int(input("Enter lesson ID to delete: "))


        c.execute("DELETE FROM student_lessons WHERE lesson_id = ?", (lesson_id,))
        c.execute("DELETE FROM lessons_list WHERE lesson_id = ?", (lesson_id,))
        conn.commit()
        print("Lesson deleted successfully!" if c.rowcount > 0 else "Lesson not found!")
    except ValueError:
        print("Invalid input!")


def add_student():
    try:
        student_number = int(input("Student number: "))
    except ValueError:
        print("Student number must be an integer.")
        return

    if c.execute("SELECT * FROM students WHERE student_number=?", (student_number,)).fetchone():
        print("Student number already exists.")
        return

    name = input("First name: ")
    surname = input("Last name: ")
    try:
        age = int(input("Age: "))
    except ValueError:
        print("Age must be an integer.")
        return
    class_ = input("Class: ")
    reg_date = input("Registration date (YYYY-MM-DD): ")

    display_lessons()
    lessons = []
    while True:
        try:
            lesson_id = input("Enter lesson ID to add (or 'done' to finish): ")
            if lesson_id.lower() == 'done':
                break
            lesson_id = int(lesson_id)

            if c.execute("SELECT * FROM lessons_list WHERE lesson_id=?", (lesson_id,)).fetchone():
                lessons.append(lesson_id)
            else:
                print("Invalid lesson ID!")
        except ValueError:
            print("Please enter a valid number or 'done'")

    try:
        c.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?)",
                  (student_number, name, surname, age, class_, reg_date))

        for lesson_id in lessons:
            c.execute("INSERT INTO student_lessons VALUES (?, ?)",
                      (student_number, lesson_id))

        conn.commit()
        print("Student added successfully!")
    except sqlite3.Error as e:
        print("Error:", e)
        conn.rollback()


def delete_student():
    try:
        student_number = int(input("Enter student number to delete: "))
    except ValueError:
        print("Student number must be an integer.")
        return

    c.execute("DELETE FROM student_lessons WHERE student_number=?", (student_number,))
    c.execute("DELETE FROM students WHERE student_number=?", (student_number,))
    conn.commit()
    print("Student deleted successfully!" if c.rowcount > 0 else "Student not found!")


def update_student():
    try:
        student_number = int(input("Enter student number to update: "))
    except ValueError:
        print("Student number must be an integer.")
        return

    student = c.execute("SELECT * FROM students WHERE student_number=?", (student_number,)).fetchone()
    if not student:
        print("Student not found.")
        return

    print("\nLeave blank to keep current value")
    name = input(f"First name [{student[1]}]: ") or student[1]
    surname = input(f"Last name [{student[2]}]: ") or student[2]
    age = input(f"Age [{student[3]}]: ") or student[3]
    class_ = input(f"Class [{student[4]}]: ") or student[4]
    reg_date = input(f"Registration date [{student[5]}]: ") or student[5]

    try:
        age = int(age)
    except ValueError:
        print("Invalid age value. Update canceled.")
        return


    c.execute('''UPDATE students SET
                name=?, surname=?, age=?, class=?, registration_date=?
                WHERE student_number=?''',
              (name, surname, age, class_, reg_date, student_number))


    display_lessons()
    current_lessons = [row[0] for row in
                       c.execute("SELECT lesson_id FROM student_lessons WHERE student_number=?",
                                 (student_number,)).fetchall()]

    print("\nCurrent enrolled lesson IDs:", current_lessons)
    new_lessons = []
    while True:
        try:
            lesson_id = input("Enter lesson ID to add (or 'done' to finish): ")
            if lesson_id.lower() == 'done':
                break
            lesson_id = int(lesson_id)

            if c.execute("SELECT * FROM lessons_list WHERE lesson_id=?", (lesson_id,)).fetchone():
                new_lessons.append(lesson_id)
            else:
                print("Invalid lesson ID!")
        except ValueError:
            print("Please enter a valid number or 'done'")

    try:
        c.execute("DELETE FROM student_lessons WHERE student_number=?", (student_number,))
        for lesson_id in new_lessons:
            c.execute("INSERT INTO student_lessons VALUES (?, ?)",
                      (student_number, lesson_id))
        conn.commit()
        print("Student updated successfully!")
    except sqlite3.Error as e:
        print("Error:", e)
        conn.rollback()


def show_student():
    try:
        student_number = int(input("Enter student number: "))
    except ValueError:
        print("Student number must be an integer.")
        return

    student = c.execute("SELECT * FROM students WHERE student_number=?", (student_number,)).fetchone()
    if not student:
        print("Student not found.")
        return

    lessons = c.execute('''SELECT l.lesson_name 
                         FROM student_lessons sl
                         JOIN lessons_list l ON sl.lesson_id = l.lesson_id
                         WHERE sl.student_number = ?''',
                        (student_number,)).fetchall()

    print("\nStudent Information:")
    print(f"Number: {student[0]}")
    print(f"Name: {student[1]} {student[2]}")
    print(f"Age: {student[3]}")
    print(f"Class: {student[4]}")
    print(f"Registration Date: {student[5]}")
    print("Enrolled Lessons:", ", ".join([lesson[0] for lesson in lessons]) if lessons else "None")


def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Student Management")
        print("2. Lesson Management")
        print("3. Exit")
        choice = input("Select option: ")

        if choice == '1':
            student_menu()
        elif choice == '2':
            lesson_menu()
        elif choice == '3':
            break
        else:
            print("Invalid choice!")


def student_menu():
    while True:
        print("\nStudent Management:")
        print("a. Add Student")
        print("d. Delete Student")
        print("u. Update Student")
        print("s. Show Student")
        print("b. Back to Main Menu")
        choice = input("Select option: ").lower()

        if choice == 'a':
            add_student()
        elif choice == 'd':
            delete_student()
        elif choice == 'u':
            update_student()
        elif choice == 's':
            show_student()
        elif choice == 'b':
            break
        else:
            print("Invalid choice!")


def lesson_menu():
    while True:
        print("\nLesson Management:")
        print("a. Add Lesson")
        print("u. Update Lesson")
        print("d. Delete Lesson")
        print("l. List Lessons")
        print("b. Back to Main Menu")
        choice = input("Select option: ").lower()

        if choice == 'a':
            add_lesson()
        elif choice == 'u':
            update_lesson()
        elif choice == 'd':
            delete_lesson()
        elif choice == 'l':
            display_lessons()
        elif choice == 'b':
            break
        else:
            print("Invalid choice!")



main_menu()
conn.close()