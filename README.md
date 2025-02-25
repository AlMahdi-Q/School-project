نظام إدارة المدرسة

الوصف

هذا المشروع هو نظام إدارة المدارس الذي يسمح للمدراء بإدارة الطلاب والدروس في المدرسة. تم بناء النظام باستخدام لغة بايثون وقاعدة البيانات SQLite لإدارة البيانات. يوفر النظام وظائف لإضافة، تحديث، حذف، وعرض الطلاب والدروس، بالإضافة إلى إدارة العلاقة بين الطلاب والدروس المسجلين فيها.

الميزات

إدارة الطلاب:

إضافة طالب جديد برقم طالب فريد مكون من 10 أرقام.

تحديث معلومات الطالب (الاسم، الكنية، العمر، الصف، تاريخ التسجيل).

حذف طالب.

عرض تفاصيل الطالب والدروس المسجل فيها.

إدارة الدروس:

إضافة درس جديد.

تحديث درس موجود.

حذف درس.

عرض جميع الدروس المتاحة.

قاعدة البيانات:

يستخدم SQLite لتخزين البيانات في ثلاث جداول:

students: لتخزين معلومات الطلاب.

lessons_list: لتخزين الدروس المتاحة.

student_lessons: لإدارة العلاقة المتعددة بين الطلاب والدروس.

كيفية الاستخدام

قم بتنزيل المشروع أو استنساخه من المستودع.

تأكد من تثبيت بايثون 3.x.

قم بتشغيل البرنامج school_management.py.

اتبع القائمة الظاهرة على الشاشة لإجراء العمليات:

اختر إدارة الطلاب لإدارة الطلاب.

اختر إدارة الدروس لإدارة الدروس.

اختر خروج لإغلاق البرنامج.

المتطلبات

بايثون 3.x

SQLite3 (مضمن مع بايثون)

School Management System

Description

This project is a School Management System that allows administrators to manage students and lessons in a school. The system is built using Python and SQLite for database management. It provides functionalities to add, update, delete, and view students and lessons, as well as manage the relationship between students and their enrolled lessons.

Features

Student Management:

Add a new student with a unique 10-digit student number.

Update student information (name, surname, age, class, registration date).

Delete a student.

View student details and enrolled lessons.

Lesson Management:

Add a new lesson.

Update an existing lesson.

Delete a lesson.

View all available lessons.

Database:

Uses SQLite to store data in three tables:

students: Stores student information.

lessons_list: Stores available lessons.

student_lessons: Manages the many-to-many relationship between students and lessons.

How to Use

Clone the repository or download the project files.

Ensure you have Python 3.x installed.

Run the script school_management.py.

Follow the on-screen menu to perform operations:

Choose Student Management to manage students.

Choose Lesson Management to manage lessons.

Choose Exit to close the program.

Requirements

Python 3.x

SQLite3 (included with Python)
