#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One of the mechanisms used to store and manage large quantities of
data is databases. There are many types of databases, but the one that
has revolutionized the sector is the database organized according to
the relational model theorized by Codd half a century ago. According
to this model, the data are arranged in tables in direct relation, to
optimize memory requirements, promote data consistency and minimize
errors.

We need to design a set of functions that implements a simple
relational database for a training school, with four tables, namely
students, teachers, courses, and exams. The databases can be of three
sizes: small, medium, and large. The database tables of size dbsize
are in four JSON files <dbsize>_<table name>.json (for example, the
small DB consists of the files small_students.json,
small_teachers.json, small_courses.json, and small_exams.json). The
tables are implemented as lists of dictionaries (see, for example, the
file small_students.json) and have the following structures:
   - students: keys stud_code, stud_name, stud_surname, stud_email
   - teachers: keys teach_code, teach_name, teach_surname, teach_email
   - courses: keys course_code, course_name, teach_code
   - exams: keys exam_code, course_code, stud_code, date, grade.
The relationship between the tables implies that each row in each of
the tables have a reference to another table: an exam (exam_code)
corresponds to a grade given by the teacher (teach_code) to a student
(stud_code) for having taken an exam of a given course (course_code)
in a certain date. Every student can have taken several exams. Every
teacher can be responsible for several courses. However, exactly
one teacher is responsible for every course.

The field stud_code is the primary key for the students table since
it uniquely identifies a student; namely no two students have the same
stud_code. Similarly, teach_code is the primary key for the teachers table,
course_code for the courses table and exam_code for the exams tables.
Thus, they are used to realize the relationships between the tables.

The fields in all tables are never empty.

We must realize some functions to query databases of different sizes.
Then, every function always requires a 'dbsize' string type parameter, which can assume the values 'small,' 'medium,' and 'large.'
The functions are:

    - student_average(stud_code, dbsize), which receives the code of
      a student and returns the average of the grades of the exams
      taken by the student.

    - course_average(course_code, dbsize), which receives the code of
      a course and returns the average grade of the exams for that
      course, taken by all students.

    - teacher_average(teach_code, dbsize), which receives the code of
      a teacher and returns the average grade for all the exams taken
      in all of the teacher's courses.

    - top_students(dbisze), which returns the list of the 'stud_code's
      of those students with an average of taken exams, greater than
      or equal to 28. The stud_codes are sorted in descending order by
      average grade and, in case of a tie, in lexicographic order by
      the student's last name and first name, finally the stud_code
      in ascending order.

    - print_recorded_exams(stud_code, fileout, dbsize), which receives a
      stud_code of a student and saves in fileout the list of the exams
      taken by that student. The rows are sorted in ascending
      order by date of exam taken and, in case of the same date, by
      alphabetical order of the exam names. The file has an initial line
      with the text
"Exams taken by student <stud_surname> <stud_name>, student number <stud_code>",
      while the following lines have the following structure:
"<course_name>\t<date>\t<grade>",
      where the fields are aligned with the longest course name (i.e. all
      dates and grades are vertically aligned). The function returns the
      number of exams taken by the student.

    - print_top_students(fileout, dbsize), which saves in fileout a
      row for each student with an average grade greater than or equal
      to 28. The rows in the file are in descending order by average
      grade and, in case of a tie, in lexicographic order by the
      student's last name and first name.
      The rows in the file have the following structure:
"<stud_surname> <names>\t<average>",
      where the average values are vertically aligned for all rows. The
      function returns the number of rows saved in the file.

    - print_exam_record(exam_code, fileout, dbsize), which receives an
      exam_code of an exam and saves in fileout the information about that
      exam, using the following formula
"The student <stud_surname> <stud_name>, student number <stud_code>, took on <date> the <course_name> exam with the teacher <teach_surname> <teach_name> with grade <grade>."
      The function returns the exam grade associated with the exam_code
      received as input.

All averages are rounded to the second decimal place, before any sorting.
All files must have "utf8" encoding.
To easily print aligned rows, consider the format function with the
modifiers for alignment (https://pyformat.info/#string_pad_align)

"""

import json


def file_names(dbsize):
    if dbsize == 'small':
        return {'courses': 'small_courses.json',
                'exams': 'small_exams.json',
                'students': 'small_students.json',
                'teachers': 'small_teachers.json'}
    if dbsize == 'medium':
        return {'courses': 'medium_courses.json',
                'exams': 'medium_exams.json',
                'students': 'medium_students.json',
                'teachers': 'medium_teachers.json'}
    else:
        return {'courses': 'large_courses.json',
                'exams': 'large_exams.json',
                'students': 'large_students.json',
                'teachers': 'large_teachers.json'}


def data(filename):
    with open(filename, encoding='utf-8') as f:
        data = json.load(f)
    return data


def student_average(stud_code, dbsize):
    files = file_names(dbsize)
    exams = data(files['exams'])

    lst = []
    for el in exams:
        if el['stud_code'] == stud_code:
            lst.append(el['grade'])

    return round(sum(lst) / len(lst), 2)


def course_average(course_code, dbsize):
    files = file_names(dbsize)
    exams = data(files['exams'])

    student_counter = 0
    score = 0
    for el in exams:
        if el['course_code'] == course_code:
            score += el['grade']
            student_counter += 1

    return round(score / student_counter, 2)


def teacher_average(teach_code, dbsize):
    files = file_names(dbsize)
    exams = data(files['exams'])
    courses = data(files['courses'])

    score = 0
    count = 0
    for el in courses:
        if el['teach_code'] == teach_code:

            for _ in exams:
                if el['course_code'] == _['course_code']:
                    score += _['grade']
                    count += 1
    return round(score / count, 2)


def top_ts(dbsize):
    files = file_names(dbsize)
    students = data(files['students'])

    all = []
    for el in students:
        if student_average(el['stud_code'], dbsize) >= 28:
            all.append((el['stud_code'], el['stud_name'], el['stud_surname'], student_average(el['stud_code'], dbsize)))

    ids = []
    for i in all:
        ids.append(i[0])

    return all, ids


def top_students(dbsize):
    all = top_ts(dbsize)[0]
    sorted_lst = sorted(sorted(all, key=lambda x: (x[2], x[1], x[0])), key=lambda x: (x[3]), reverse=True)

    ids = []
    for i in sorted_lst:
        ids.append(i[0])

    return ids


def print_recorded_exams(stud_code, dbsize, fileout):
    files = file_names(dbsize)
    students, courses, exams = data(files['students']), data(files['courses']), data(files['exams'])

    exam_history = []
    longest = 0
    for el in exams:
        if el['stud_code'] == stud_code:
            for item in courses:
                if item['course_code'] == el['course_code']:
                    w = len(item['course_name'])
                    if w > longest:
                        longest = w
                    exam_history.append((el['date'], el['grade'], item['course_name']))

    for _ in students:
        if _['stud_code'] == stud_code:
            name, surname = _['stud_name'], _['stud_surname']

    sorted_history = sorted(exam_history, key=lambda x: (x[0], x[2]))
    text_file = open(fileout, 'w', encoding='utf-8')

    text_file.write(f'Exams taken by student {surname} {name}, student number {stud_code}\n')

    for el in sorted_history:
        wL = longest - len(el[2])
        space = wL * ' '
        text_file.write(f"{el[2]}{space}\t{el[0]}\t{el[1]}\n")
    text_file.close()

    return len(sorted_history)


def print_top_students(dbsize, fileout):
    text_file = open(fileout, 'w', encoding='utf-8')
    files = file_names(dbsize)
    students = data(files['students'])

    toppers = top_students(dbsize)

    topper_data = []
    longest = 0
    for el in toppers:
        average = student_average(el, dbsize)
        for item in students:
            if el == item['stud_code']:
                name = item['stud_name']
                surname = item['stud_surname']
                fullname = name + surname
                fn_len = len(fullname)
                if fn_len > longest:
                    longest = fn_len
                topper_data.append((surname, name, average, fn_len))

    for _ in topper_data:
        space = (longest - _[3]) * ' '
        text_file.write(f"{_[0]} {_[1]}{space}\t{_[2]}\n")

    text_file.close()

    return len(topper_data)


def print_exam_record(exam_code, dbsize, fileout):
    files = file_names(dbsize)
    students, courses, exams, teachers = data(files['students']), data(files['courses']), data(files['exams']), data(
        files['teachers'])

    d = {}
    for el in exams:
        if el['exam_code'] == exam_code:
            d['course_code'] = el['course_code']
            d['id'] = el['stud_code']
            d['date'] = el['date']
            d['grade'] = el['grade']

    for i in courses:
        if i['course_code'] == d['course_code']:
            d['course_name'] = i['course_name']
            d['teach_code'] = i['teach_code']

    for j in students:
        if j['stud_code'] == d['id']:
            d['stud_name'] = j['stud_name']
            d['stud_surname'] = j['stud_surname']

    for k in teachers:
        if k['teach_code'] == d['teach_code']:
            d['teach_name'] = k['teach_name']
            d['teach_surname'] = k['teach_surname']
    text_file = open(fileout, 'w', encoding='utf-8')

    text_file.write(
        f"The student {d['stud_name']} {d['stud_surname']}, student number {d['id']}, took on {d['date']} the {d['course_name']} exam with the teacher {d['teach_name']} {d['teach_surname']} with grade {d['grade']}.\n")
    text_file.close()
    return d['grade']

