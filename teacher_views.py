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

def teacher_class_update(aid):
	"""
	RAJIV WRITE YOUR CODE HERE.
	aid is the key of the attendance_course table. You will have to get the students of the corresponding class
	yourself
	"""
	check_login()
	return render_template('teacher/mark_attendance.html', student_list = get_student_list(flask.g.db))


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
	app.add_url_rule('/teacher/class/<aid>/', 'teacher_class_update', teacher_class_update)

def get_course_list(db):
	query = """select coursename, branch, semester, section, aid from class
	inner join attendance_course
	on class.classid=attendance_course.classid
	inner join course
	on course.courseno=attendance_course.courseno
	where attendance_course.teacherid=?"""
	return rows_to_stringdicts(db.execute(query, [flask.session.get('teacherid')]))

def get_teacher_class(db):
	teacher_class = rows_to_stringdicts(db.execute('select classid from teacher where teacherid=?', [flask.session.get('teacherid')]))
	return teacher_class[0]['classid']

def get_student_list(db):
	return rows_to_stringdicts(db.execute('select * from student where classid=?', get_teacher_class(flask.g.db)))

def run_update_attendance_course(db, form):
	db.execute('update attendance_course set total=total+1 where teacherid=? and classid=? and courseno=?', [flask.session.get('teacherid')], get_teacher_class(flask.g.db), ???)

def run_update_student_attendance(db, form):
	db.execute('update att_student set attended=attended+1 where rno=? and aid=(select aid from attendance_course where teacherid=? and classid=? and courseno=?)', ???, [flask.session.get('teacherid')], get_teacher_class(flask.g.db), ???)