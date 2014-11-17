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
    return render_template('teacher/home.html')

def view_course_list():
	"""
	List of courses which the logged in teacher has registered for.
	"""
	check_login()


"""
******************************************************
~UTILITY
******************************************************
"""
def check_login():
	if not flask.session.get('teacherid'):
		flask.abort(401)

def redirect_to_home():
	check_login()
	return flask.redirect(flask.url_for('teacher_home'))

def register_urls(app):
	app.add_url_rule('/teacher/home/', 'teacher_home', home)

	app.add_url_rule('/teacher/list/course/', 'view_course_list', view_course_list)

def get_course_list():
	return rows_to_stringdicts(db.execute('select * from attendace_course where teacherid=?', [flask.session.get('teacherid')]))