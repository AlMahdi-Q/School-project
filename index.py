import sqlite3

# الاتصال بقاعدة البيانات وإنشاء الجداول
conn = sqlite3.connect('school.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS students
             (student_number INTEGER PRIMARY KEY,
              name TEXT,
              surname TEXT,
              age INTEGER,
              class TEXT,
              registration_date TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS lessons
             (student_number INTEGER,
              lesson_name TEXT,
              FOREIGN KEY(student_number) REFERENCES students(student_number),
              PRIMARY KEY(student_number, lesson_name))''')
conn.commit()

def add_student():
    try:
        student_number = int(input("رقم الطالب: "))
    except ValueError:
        print("رقم الطالب يجب أن يكون رقمًا صحيحًا.")
        return

    c.execute("SELECT * FROM students WHERE student_number=?", (student_number,))
    if c.fetchone():
        print("رقم الطالب موجود مسبقًا.")
        return

    name = input("الاسم: ")
    surname = input("الكنية: ")
    try:
        age = int(input("العمر: "))
    except ValueError:
        print("العمر يجب أن يكون رقمًا صحيحًا.")
        return
    class_ = input("الصف: ")
    reg_date = input("تاريخ التسجيل (YYYY-MM-DD): ")

    lessons = []
    while True:
        lesson = input("أدخل اسم الدرس (أو اترك فارغًا لإنهاء): ").strip()
        if not lesson:
            break
        if lesson not in lessons:
            lessons.append(lesson)
        else:
            print("هذا الدرس مضاف مسبقًا.")

    try:
        c.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?)",
                  (student_number, name, surname, age, class_, reg_date))
        for lesson in lessons:
            c.execute("INSERT INTO lessons VALUES (?, ?)", (student_number, lesson))
        conn.commit()
        print("تمت إضافة الطالب بنجاح.")
    except sqlite3.Error as e:
        print("حدث خطأ:", e)
        conn.rollback()

def delete_student():
    try:
        student_number = int(input("رقم الطالب المراد حذفه: "))
    except ValueError:
        print("رقم الطالب يجب أن يكون رقمًا صحيحًا.")
        return

    c.execute("SELECT * FROM students WHERE student_number=?", (student_number,))
    if not c.fetchone():
        print("الطالب غير موجود.")
        return

    try:
        c.execute("DELETE FROM lessons WHERE student_number=?", (student_number,))
        c.execute("DELETE FROM students WHERE student_number=?", (student_number,))
        conn.commit()
        print("تم حذف الطالب بنجاح.")
    except sqlite3.Error as e:
        print("حدث خطأ:", e)
        conn.rollback()

def update_student():
    try:
        student_number = int(input("رقم الطالب المراد تعديله: "))
    except ValueError:
        print("رقم الطالب يجب أن يكون رقمًا صحيحًا.")
        return

    c.execute("SELECT * FROM students WHERE student_number=?", (student_number,))
    student = c.fetchone()
    if not student:
        print("الطالب غير موجود.")
        return

    print("أدخل البيانات الجديدة (اترك الحقل فارغًا للحفاظ على القيمة الحالية):")
    name = input(f"الاسم الحالي ({student[1]}): ") or student[1]
    surname = input(f"الكنية الحالية ({student[2]}): ") or student[2]
    age = input(f"العمر الحالي ({student[3]}): ") or student[3]
    class_ = input(f"الصف الحالي ({student[4]}): ") or student[4]
    reg_date = input(f"تاريخ التسجيل الحالي ({student[5]}): ") or student[5]

    try:
        age = int(age)
    except ValueError:
        print("العمر يجب أن يكون رقمًا صحيحًا.")
        return

    try:
        c.execute('''UPDATE students SET
                     name=?, surname=?, age=?, class=?, registration_date=?
                     WHERE student_number=?''',
                  (name, surname, age, class_, reg_date, student_number))

        print("تحديث الدروس (سيتم استبدال جميع الدروس السابقة):")
        lessons = []
        while True:
            lesson = input("أدخل اسم الدرس (أو اترك فارغًا لإنهاء): ").strip()
            if not lesson:
                break
            if lesson not in lessons:
                lessons.append(lesson)
            else:
                print("هذا الدرس مضاف مسبقًا.")

        c.execute("DELETE FROM lessons WHERE student_number=?", (student_number,))
        for lesson in lessons:
            c.execute("INSERT INTO lessons VALUES (?, ?)", (student_number, lesson))
        conn.commit()
        print("تم تحديث بيانات الطالب بنجاح.")
    except sqlite3.Error as e:
        print("حدث خطأ:", e)
        conn.rollback()

def show_student():
    try:
        student_number = int(input("رقم الطالب المراد عرضه: "))
    except ValueError:
        print("رقم الطالب يجب أن يكون رقمًا صحيحًا.")
        return

    c.execute("SELECT * FROM students WHERE student_number=?", (student_number,))
    student = c.fetchone()
    if not student:
        print("الطالب غير موجود.")
        return

    c.execute("SELECT lesson_name FROM lessons WHERE student_number=?", (student_number,))
    lessons = [row[0] for row in c.fetchall()]

    print("\nمعلومات الطالب:")
    print(f"الرقم: {student[0]}")
    print(f"الاسم: {student[1]}")
    print(f"الكنية: {student[2]}")
    print(f"العمر: {student[3]}")
    print(f"الصف: {student[4]}")
    print(f"تاريخ التسجيل: {student[5]}")
    print("الدروس:", ", ".join(lessons) if lessons else "لا يوجد دروس.")

while True:
    print("\nالرجاء اختيار العملية:")
    print("a - إضافة طالب")
    print("d - حذف طالب")
    print("u - تعديل طالب")
    print("s - عرض طالب")
    print("أي حرف آخر - الخروج")
    choice = input("اختيارك: ").lower()

    if choice == 'a':
        add_student()
    elif choice == 'd':
        delete_student()
    elif choice == 'u':
        update_student()
    elif choice == 's':
        show_student()
    else:
        print("الخروج من البرنامج...")
        break

conn.close()