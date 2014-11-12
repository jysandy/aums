import flask
from flask import render_template

"""
******************************************************
~VIEWS
******************************************************
"""

def view_course_wise_att():
    check_login()
    run_view_course_wise_att(flask.g.db, flask.request.form)

def home():
	check_login()
	return render_template('student/home.html')

"""
******************************************************
~UTILITY
******************************************************
"""
def check_login():
	if not flask.session.get('student_logged_in'):
		flask.abort(401)

def redirect_to_home():
	check_login()
	return flask.redirect(flask.url_for('student_home'))

def register_urls(app):
	app.add_url_rule('/student/home/', 'student_home', home)

def run_view_course_wise_att(db, form):
	db.execute('select * from simple_attendance where student.rno=?', flask.session.rno)