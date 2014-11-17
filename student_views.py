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
    return render_template('student/home.html', student_attendance_list = get_course_wise_att(flask.g.db), student_name = get_student_name(flask.g.db))


"""
******************************************************
~UTILITY
******************************************************
"""
def check_login():
	if not flask.session.get('rno'):
		flask.abort(401)

def redirect_to_home():
	check_login()
	return flask.redirect(flask.url_for('student_home'))

def register_urls(app):
	app.add_url_rule('/student/home/', 'student_home', home)

def get_student_name(db):
	q = rows_to_stringdicts(db.execute('select name from student where rno=?', [flask.session.get('rno')]))
	return q[0]['name']


def get_course_wise_att(db):
	return rows_to_stringdicts(db.execute('select * from simple_attendance where rno=?', [flask.session.get('rno')]))

