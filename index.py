import sqlite3
from datetime import datetime

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
    while True:
        lesson_name = input("Enter new lesson name: ").strip()
        if not lesson_name.isalpha() or not lesson_name:
            print("Invalid input. Lesson name must be alphabetic and non-empty.")
            continue

        try:
            c.execute("INSERT INTO lessons_list (lesson_name) VALUES (?)", (lesson_name,))
            conn.commit()
            print("Lesson added.")
            break
        except sqlite3.IntegrityError:
            print("Lesson already exists.")


def update_lesson():
    display_lessons()
    while True:
        try:
            lesson_id = int(input("Enter lesson ID to update: "))
            new_name = input("Enter new lesson name: ").strip()
            if not new_name.isalpha() or not new_name:
                print("Invalid input. Lesson name must be alphabetic and non-empty.")
                continue

            if c.execute("SELECT 1 FROM lessons_list WHERE lesson_name = ?", (new_name,)).fetchone():
                print("Lesson name already exists.")
                continue

            c.execute("UPDATE lessons_list SET lesson_name = ? WHERE lesson_id = ?", (new_name, lesson_id))
            conn.commit()
            print("Lesson updated." if c.rowcount > 0 else "Lesson not found.")
            break
        except ValueError:
            print("Invalid input. Lesson ID must be an integer.")


def delete_lesson():
    display_lessons()
    while True:
        try:
            lesson_id = int(input("Enter lesson ID to delete: "))


            c.execute("DELETE FROM student_lessons WHERE lesson_id = ?", (lesson_id,))
            c.execute("DELETE FROM lessons_list WHERE lesson_id = ?", (lesson_id,))
            conn.commit()
            print("Lesson deleted successfully!" if c.rowcount > 0 else "Lesson not found!")
            break
        except ValueError:
            print("Invalid input!")
            continue


def add_student():
    while True:
        try:
            student_number = int(input("Student number: "))
            if len(str(student_number)) != 10:
                print("Student number must be exactly 10 digits.")
                continue
        except ValueError:
            print("Invalid input. Student number must be a 10-digit number.")
            continue

        if c.execute("SELECT * FROM students WHERE student_number=?", (student_number,)).fetchone():
            print("Student number already exists.")
            continue
        break
    while True:
        name = input("First name: ").strip()
        if not name.isalpha() or not name:
            print("Invalid input. Name must be alphabetic and non-empty.")
            continue

        surname = input("Last name: ").strip()
        if not surname.isalpha() or not surname:
            print("Invalid input. Surname must be alphabetic and non-empty.")
            continue

        break

    while True:
        try:
            age = int(input("Age: "))
            if age <= 0:
                print("Invalid age. Must be positive.")
                continue
            break
        except ValueError:
            print("Invalid input. Age must be an integer.")

    while True:
        class_name = input("Class: ").strip()
        reg_date_str = input("Registration date (YYYY-MM-DD): ").strip()

        if not class_name or not reg_date_str:
            print("Invalid input. Class and date cannot be empty.")
            continue

        try:
            reg_date = datetime.strptime(reg_date_str, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")

    display_lessons()
    lessons = []
    while True:
        try:
            lesson_id = input("Enter lesson ID to add (or 'done' to finish): ")
            if lesson_id.lower() == 'done':
                break

            lesson_id = int(lesson_id)
            if c.execute("SELECT 1 FROM lessons_list WHERE lesson_id=?", (lesson_id,)).fetchone():
                lessons.append(lesson_id)

            else:
                print("Invalid lesson ID.")
        except ValueError:
            print("Invalid input. Enter a number or 'done'.")
    reg_date_str = reg_date.isoformat()
    try:
        c.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?)",
                  (student_number, name, surname, age, class_name, reg_date_str))

        for lesson_id in lessons:
            try:
                c.execute("INSERT INTO student_lessons VALUES (?, ?)", (student_number, lesson_id))
            except sqlite3.IntegrityError:
                print(f"Lesson with ID {lesson_id} already added to student.")

        conn.commit()
        print("Student added.")
    except sqlite3.Error as e:
        print("Error:", e)
        conn.rollback()


def delete_student():
    while True:
        try:
            student_number = int(input("Enter student number to delete: "))
            if len(str(student_number)) != 10:
                print("Student number must be exactly 10 digits.")
                continue
            break
        except ValueError:
            print("Student number must be an integer.")
            continue

    c.execute("DELETE FROM student_lessons WHERE student_number=?", (student_number,))
    c.execute("DELETE FROM students WHERE student_number=?", (student_number,))
    conn.commit()
    print("Student deleted successfully!" if c.rowcount > 0 else "Student not found!")


def update_student():
    while True:
        try:
            student_number = int(input("Enter student number to update: "))
            if len(str(student_number)) != 10:
                print("Student number must be exactly 10 digits.")
                continue
            break
        except ValueError:
            print("Student number must be an integer.")
            continue

    student = c.execute("SELECT * FROM students WHERE student_number=?", (student_number,)).fetchone()
    if not student:
        print("Student not found.")
        return

    print("\nLeave blank to keep current value")
    while True:
        name = input(f"First name [{student[1]}]: ").strip() or student[1]
        if not name.isalpha() or name == "":
            print("Invalid input!")
            continue
        surname = input(f"Last name [{student[2]}]: ").strip() or student[2]
        if not surname.isalpha() or surname == "":
            print("Invalid input!")
            continue
        break
    while True:
        age = input(f"Age [{student[3]}]: ") or student[3]
        if age <= 0:
            print("Invalid input!")
            continue
        class_ = input(f"Class [{student[4]}]: ") or student[4]
        if class_ == "":
            print("Invalid input!")
            continue
        reg_date = input(f"Registration date [{student[5]}]: ") or student[5]
        if reg_date == "":
            print("Invalid input!")
            continue
        break
    while True:
        try:
            age = int(age)
            break
        except ValueError:
            print("Invalid age value. Update canceled.")
            continue


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
            if c.execute("SELECT * FROM student_lessons WHERE lesson_id=?", (lesson_id,)).fetchone() or lesson_id in new_lessons:
                print("Lesson already exists.")
            elif c.execute("SELECT * FROM lessons_list WHERE lesson_id=?", (lesson_id,)).fetchone():
                new_lessons.append(lesson_id)
            else:
                print("Invalid lesson ID!")
        except ValueError:
            print("Please enter a valid number or 'done'")

    try:
        for lesson_id in new_lessons:
            c.execute("INSERT INTO student_lessons VALUES (?, ?)",
                      (student_number, lesson_id))
        conn.commit()
        print("Student updated successfully!")
    except sqlite3.Error as e:
        print("Error:", e)
        conn.rollback()


def show_student():
    while True:
        try:
            student_number = int(input("Enter student number: "))
        except ValueError:
            print("Student number must be an integer.")
            continue

        student = c.execute("SELECT * FROM students WHERE student_number=?", (student_number,)).fetchone()
        if not student:
            print("Student not found.")
            continue

        lessons = c.execute('''SELECT l.lesson_name 
                             FROM student_lessons sl
                             JOIN lessons_list l ON sl.lesson_id = l.lesson_id
                             WHERE sl.student_number = ?''',
                            (student_number,)).fetchall()
        break

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