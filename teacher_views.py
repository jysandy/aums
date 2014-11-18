import flask
from flask import render_template
from util import rows_to_stringdicts



"""
******************************************************
~VIEWS
******************************************************
"""
def home():
	"""
	List of courses which the logged in teacher has registered for.
	"""
	check_login()
	return render_template('teacher/home.html', teacher_course_list = get_course_list(flask.g.db))


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

def get_course_list(db):
	query = """select coursename, branch, semester, section from class
	inner join attendance_course
	on class.classid=attendance_course.classid
	inner join course
	on course.courseno=attendance_course.courseno
	where attendance_course.teacherid=?"""
	return rows_to_stringdicts(db.execute(query, [flask.session.get('teacherid')]))
