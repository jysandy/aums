import flask
from flask import render_template

"""
******************************************************
~VIEWS
******************************************************
"""
def home():
	check_login()
	return render_template('admin/home.html')

def create_teacher():
	check_login()
	return render_template('admin/create_teacher.html')

def create_teacher_post():
	check_login()
	run_create_teacher_sql(flask.g.db, flask.request.form)
	flask.flash('New teacher successfully created.')
	return flask.redirect(flask.url_for('home'))

#NOTE: The views for viewing and updating a teacher's info are the SAME.
def update_teacher(teacher_id):
	check_login()
	return render_template('admin/update_teacher.html', teacher_info = get_teacher_info(flask.g.db, teacher_id))

def update_teacher_post():
	check_login()
	run_update_teacher_sql(flask.g.db, flask.request.form)
	flask.flask('Teacher info successfully updated.')
	return redirect_to_home()

def view_teacher_list():
	check_login()
	return render_template('admin/teacher_list.html', teacher_list = get_teacher_list(flask.g.db))

def create_student():
	check_login()
	return render_template('admin/create_student.html')

def create_student_post():
	check_login()
	run_create_student_sql(flask.g.db, flask.request.form)
	flask.flash('New student successfully created.')
	return redirect_to_home()

def update_student(student_rno):
	check_login()
	return render_template('admin/update_student.html', student_info = get_student_info(flask.g.db, student_rno))

def update_student_post():
	check_login()
	run_update_student_sql(flask.g.db, flask.request.form)
	flask.flash('Student info successfully updated.')
	return redirect_to_home()

def view_student_list():
	check_login()
	return render_template('admin/view_student_list.html', student_list = get_student_list(flask.g.db))

def create_course():
	check_login()
	return render_template('admin/create_course.html')

def create_course_post():
	check_login()
	run_create_course_sql(flask.g.db, flask.request.form)
	flask.flash('New course successfully created.')
	return redirect_to_home()

def update_course(courseno):
	check_login()
	return render_template('admin/update_course.html', course_info = get_course_info(flask.g.db, courseno))

def update_course_post():
	check_login()
	run_update_course_sql(flask.g.db, flask.request.form)
	flask.flash('Course info successfully updated.')
	return redirect_to_home()

def view_course_list():
	check_login()
	returrn render_template('admin/view_course_list.html', course_list = get_course_list(flask.g.db))

def create_class():
	check_login()
	return render_template('admin/create_class.html')

def create_class_post():
	check_login()
	run_create_class_sql(flask.g.db, flask.request.form)
	flask.flash('New class successfully created.')
	return redirect_to_home()

def update_class(classid):
	check_login()
	return render_template('admin/update_class.html', class_info = get_class_info(flask.g.db, classid))

def update_class_post():
	check_login()
	run_update_class_sql(flask.g.db, flask.request.form)
	flask.flash('Class successfully updated.')
	return redirect_to_home()

def view_class_list():
	check_login()
	return render_template('admin/view_class_list.html', class_list = get_class_list(flask.g.db))

def view_class_courses(classid):
	check_login()
	return render_template('admin/view_class_courses.html', course_teacher_list = get_course_teacher_list(flask.g.db, classid), classid = classid)

def view_class_courses_post():
	check_login()
	run_map_class_sql(flask.g.db, flask.request.form)
	flask.flash('Course mapping successfully created')
	return redirect_to_home()

def delete_confirm(table_name, entry_key):
	check_login()
	return render_template('admin/delete_confirm.html', table_name = table_name, entry_key = entry_key)

def delete_post():
	check_login()
	run_delete_item_sql(flask.g.db, flask.request.form)
	flask.flash('Item successfully deleted.')
	return redirect_to_home()

"""
******************************************************
~UTILITY
******************************************************
"""
def check_login():
	if not flask.session.get('logged_in'):
		flask.abort(401)

def redirect_to_home():
	return flask.redirect(flask.url_for('admin_home'))

def register_urls(app):
	app.add_url_rule('/admin/home/', 'admin_home', home)

	#Teacher CRUD
	app.add_url_rule('/admin/create/teacher/', 'create_teacher', create_teacher)
	app.add_url_rule('/admin/create/teacher/post/', 'create_teacher_post', create_teacher_post, methods = ['POST'])
	app.add_url_rule('/admin/teacher/<teacher_id>/', 'update_teacher', update_teacher)
	app.add_url_rule('/admin/teacher/post/', 'update_teacher_post', update_teacher_post, methods = ['POST'])
	app.add_url_rule('/admin/list/teacher/', 'view_teacher_list', view_teacher_list)

	#Student CRUD
	app.add_url_rule('/admin/create/student/', 'create_student', create_student)
	app.add_url_rule('/admin/create/student/post/', 'create_student_post', create_student_post, methods = ['POST'])
	app.add_url_rule('/admin/student/<student_rno>/', 'update_student', update_student)
	app.add_url_rule('/admin/student/post/', 'update_student_post', update_student_post, methods = ['POST'])
	app.add_url_rule('/admin/list/student/', 'view_student_list', view_student_list)

	#Course CRUD
	app.add_url_rule('/admin/create/course/', 'create_course', create_course)
	app.add_url_rule('/admin/create/course/post/', 'create_course_post', create_course_post, methods = ['POST'])
	app.add_url_rule('/admin/course/<courseno>/', 'update_course', update_course)
	app.add_url_rule('/admin/course/post/', 'update_course_post', update_course_post, methods = ['POST'])
	app.add_url_rule('/admin/list/course/', 'view_course_list', view_course_list)

	#Class CRUD
	app.add_url_rule('/admin/create/class/', 'create_class', create_class)
	app.add_url_rule('/admin/create/class/post', 'create_class_post', create_class_post, methods = ['POST'])
	app.add_url_rule('/admin/class/<classid>/', 'update_class', update_class)
	app.add_url_rule('/admin/class/post/', 'update_class_post', update_class_post, methods = ['POST'])
	app.add_url_rule('/admin/list/class/', 'view_class_list', view_class_list)

	#Attendance_course
	app.add_url_rule('/admin/class/<classid>/courses/', 'view_class_courses', view_class_courses)
	app.add_url_rule('/admin/class/courses_map/post/', 'view_class_courses_post', view_class_courses_post)

	#Deletion
	app.add_url_rule('/admin/delete/<table_name>/<entry_key>/', 'delete_confirm', delete_confirm)
	app.add_url_rule('/admin/delete/post/', 'delete_post', delete_post, methods = ['POST'])


def run_create_teacher_sql(db, form):
	db.execute('insert into teacher values (?, ?, ?)', [form['teacherid'], form['name'], form['password']])
	db.commit()

def run_update_teacher_sql(db, form):
	db.execute('update teacher set name=?, password=? where teacherid=?', [form['name'], form['password'], form['teacherid']])
	db.commit()

def run_create_student_sql(db, form):
	db.execute('insert into student values (?, ?, ?, ?)', [form['rno'], form['name'], form['classid'], form['password']])
	db.commit()

def run_update_student_sql(db, form):
	db.execute('update student set name=?, password=? where rno=?', [form['name'], form['password'], form['rno']])
	db.commit()

def run_create_course_sql(db, form):
	db.execute('insert into course values (?, ?)', [form['courseno'], form['coursename']])
	db.commit()

def run_update_course_sql(db, form):
	db.execute('update course set coursename=? where courseno=?', [form['coursename'], form['courseno']])
	db.commit()

def run_create_class_sql(db, form):
	db.execute('insert into class (branch, semester, section) values (?, ?, ?)', [form['branch'], form['semester'], form['section']])
	db.commit()

def run_update_class_sql(db, form):
	db.execute('update class set branch=?, semester=?, section=? where classid=?', [form['branch'], form['semester'], form['section']])
	db.commit()

def run_map_class_sql(db, form):
	db.execute('insert into attendance_course (teacherid, classid, courseno, total) values (?, ?, ?, 0)', [form['teacherid'], form['classid'], form['courseno']])
	db.commit()

def run_delete_item_sql(db, form):
	key_attribute = {'class':'classid', 'student':'rno', 'course':'courseno', 'teacher':'teacherid', 'attendance_course':'aid'}
	db.execute('delete from ? where ?=?', [form['table_name'], key_attribute, form['entry_key']])
	db.commit()

def get_teacher_info(db, teacherid):
	return db.execute('select * from teacher where teacherid=?', [teacherid]).fetchall()

def get_teacher_list(db):
	return db.execute('select teacherid, name from teacher').fetchall()

def get_student_info(db, rno):
	return db.execute('select * from student where rno=?', [rno]).fetchall()

def get_student_list(db):
	return db.execute('select rno, name from student').fetchall()

def get_course_info(db, courseno):
	return db.execute('select * from course where courseno=?', [courseno]).fetchall()

def get_course_list(db):
	return db.execute('select * from course').fetchall()

def get_class_info(db, classid):
	return db.execute('select * from class where classid=?', [classid]).fetchall()

def get_class_list(db):
	return db.execute('select * from class').fetchall()

def get_course_teacher_list(db, classid):
	return db.execute('select aid, teacherid, courseno from attendance_course where classid=?', [classid]).fetchall()