نظام إدارة المدرسة

هذا المشروع عبارة عن نظام بسيط لإدارة الطلاب والدروس في مدرسة. يتم تخزين البيانات في قاعدة بيانات SQLite، ويتيح النظام للمستخدم إضافة طلاب، حذفهم، تعديل معلوماتهم، وعرض معلوماتهم.

الميزات:

إضافة طالب: إدخال بيانات الطالب (الرقم، الاسم، الكنية، العمر، الصف، تاريخ التسجيل) والدروس التي يسجل فيها.

حذف طالب: حذف طالب من قاعدة البيانات بناءً على رقمه.

تعديل طالب: تحديث بيانات الطالب والدروس المسجل فيها.

عرض معلومات الطالب: عرض بيانات الطالب والدروس المسجل فيها.

هيكل قاعدة البيانات:

جدول students:

student_number: رقم الطالب (مفتاح أساسي).

name: اسم الطالب.

surname: كنية الطالب.

age: عمر الطالب.

class: الصف الذي يدرس فيه الطالب.

registration_date: تاريخ تسجيل الطالب.

جدول lessons:

student_number: رقم الطالب (مفتاح خارجي).

lesson_name: اسم الدرس.

المتطلبات:

Python 3.x

مكتبة sqlite3 (مضمنة مع Python).

المؤلف:

المهدي القرني


School Management System

The system functions to manage school students together with their lesson scheduling activities. The system stores data within an SQLite database structure while enabling users to execute operations such as student addition and deletion and information updating as well as data details viewing.

Features

Add a student: Enter student details (number, name, surname, age, class, registration date) and the lessons they are enrolled in.

Delete a student: Remove a student from the database based on their number.

Update a student: Modify student details and their enrolled lessons.

View student information: Display student details and their enrolled lessons.

Database Structure

students table:

student_number: Student number (primary key).

name: Student's name.

surname: Student's surname.

age: Student's age.

class: Student's class.

registration_date: Student's registration date.

lessons table:

student_number: Student number (foreign key).

lesson_name: Lesson name.

Requirements

Python 3.x

sqlite3 library (included with Python).

Author
Al Mahdi Al Qarni
