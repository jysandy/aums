import flask
from flask import render_template
from util import rows_to_stringdicts



"""
******************************************************
~VIEWS
******************************************************
"""

def home():
    check_login()
    return render_template('teacher/home.html', student_attendance_list = get_course_wise_att(flask.g.db, flask.request.form), student_name = get_student_name(flask.g.db, flask.request.form))

