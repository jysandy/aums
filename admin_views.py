import flask
from flask import render_template

"""
******************************************************
~VIEWS
******************************************************
"""
def home():
	check_login()
	return render_template('admin/base.html')


def create_teacher():
	check_login()
	return render_template('admin/create_teacher.html')


def create_teacher_post():
	check_login()
	run_create_teacher_sql(flask.g.db, flask.request.form)
	flask.g.db.commit()
	flask.flash('New teacher successfully created.')
	return redirect_to_home()


#NOTE: The views for viewing and updating a teacher's info are the SAME.
def update_teacher(key):
	check_login()
	return render_template('admin/update_teacher.html', teacher_info = get_teacher_info(flask.g.db, key))


def update_teacher_post():
	check_login()
	run_update_teacher_sql(flask.g.db, flask.request.form)
	flask.g.db.commit()
	flask.flask('Teacher info successfully updated.')
	return redirect_to_home()


def view_teacher_list():
	check_login()
	entries = [ { 'title' : row['name'], 'key' : row['teacherid'] } for row in get_teacher_list(flask.g.db) ]
	return render_template('admin/view_list_base.html', entries = entries, table_name = 'teacher', update_url_name = 'update_teacher', 
		create_url_name = 'create_teacher', active_page='view_teacher_list')


def create_student():
	check_login()
	return render_template('admin/create_student.html', class_list = get_class_list(flask.g.db))


def create_student_post():
	check_login()
	run_create_student_sql(flask.g.db, flask.request.form)
	flask.g.db.commit()
	flask.flash('New student successfully created.')
	return redirect_to_home()


def update_student(key):
	check_login()
	print key
	print get_student_info(flask.g.db, key)
	return render_template('admin/update_student.html', student_info = get_student_info(flask.g.db, key))


def update_student_post():
	check_login()
	run_update_student_sql(flask.g.db, flask.request.form)
	flask.g.db.commit()
	flask.flash('Student info successfully updated.')
	return redirect_to_home()


def view_student_list():
	check_login()
	entries = [ { 'title' : row['name'], 'key' : row['rno'] } for row in get_student_list(flask.g.db) ]
	print entries
	return render_template('admin/view_list_base.html', entries = entries, table_name = 'student', 
			update_url_name = 'update_student', create_url_name = 'create_student', active_page = 'view_student_list')


def create_course():
	check_login()
	return render_template('admin/create_course.html')


def create_course_post():
	check_login()
	run_create_course_sql(flask.g.db, flask.request.form)
	flask.g.db.commit()
	flask.flash('New course successfully created.')
	return redirect_to_home()


def update_course(key):
	check_login()
	return render_template('admin/update_course.html', course_info = get_course_info(flask.g.db, key))


def update_course_post():
	check_login()
	run_update_course_sql(flask.g.db, flask.request.form)
	flask.g.db.commit()
	flask.flash('Course info successfully updated.')
	return redirect_to_home()


def view_course_list():
	check_login()
	entries = [ { 'title' : row['coursename'], 'key' : row['courseno'] } for row in get_course_list(flask.g.db) ]
	return render_template('admin/view_list_base.html', entries = entries, table_name = 'course', update_url_name = 'update_course',
			create_url_name = 'create_course', active_page = 'view_course_list')


def create_class():
	check_login()
	return render_template('admin/create_class.html')


def create_class_post():
	check_login()
	run_create_class_sql(flask.g.db, flask.request.form)
	flask.g.db.commit()
	flask.flash('New class successfully created.')
	return redirect_to_home()


def update_class(key):
	check_login()
	return render_template('admin/update_class.html', class_info = get_class_info(flask.g.db, key))


def update_class_post():
	check_login()
	run_update_class_sql(flask.g.db, flask.request.form)
	flask.g.db.commit()
	flask.flash('Class successfully updated.')
	return redirect_to_home()


def view_class_list():
	check_login()
	entries = [ { 'title' : str(row['semester']) + ' sem ' + row['branch'] + '-' + row['section'], 'key' : str(row['classid']) } for row in get_class_list(flask.g.db) ]
	return render_template('admin/view_list_base.html', entries = entries, table_name = 'class', update_url_name = 'update_class',
			create_url_name = 'create_class', active_page = 'view_class_list')


def view_class_courses(key):
	"""
	List of courses for each class. Contains a small form at the end to add a new course.
	"""
	check_login()
	return render_template('admin/view_class_courses.html', course_teacher_list = get_course_teacher_list(flask.g.db, key), classid = key,
			teacher_list = get_teacher_list(flask.g.db), course_list = get_course_list(flask.g.db))


def view_class_courses_post():
	check_login()
	run_map_class_sql(flask.g.db, flask.request.form)
	flask.g.db.commit()
	flask.flash('Course mapping successfully created')
	return redirect_to_home()


def delete_confirm(table_name, entry_key):
	check_login()
	return render_template('admin/delete_confirm.html', table_name = table_name, entry_key = entry_key)


def delete_post():
	check_login()
	run_delete_item_sql(flask.g.db, flask.request.form)
	flask.g.db.commit()
	flask.flash('Item successfully deleted.')
	return redirect_to_home()

"""
******************************************************
~UTILITY
******************************************************
"""
def check_login():
	if not flask.session.get('admin_logged_in'):
		flask.abort(401)


def redirect_to_home():
	return flask.redirect(flask.url_for('admin_home'))


def register_urls(app):
	app.add_url_rule('/admin/home/', 'admin_home', home)

	#Teacher CRUD
	app.add_url_rule('/admin/create/teacher/', 'create_teacher', create_teacher)
	app.add_url_rule('/admin/create/teacher/post/', 'create_teacher_post', create_teacher_post, methods = ['POST'])
	app.add_url_rule('/admin/teacher/<key>/', 'update_teacher', update_teacher)
	app.add_url_rule('/admin/teacher/post/', 'update_teacher_post', update_teacher_post, methods = ['POST'])
	app.add_url_rule('/admin/list/teacher/', 'view_teacher_list', view_teacher_list)

	#Student CRUD
	app.add_url_rule('/admin/create/student/', 'create_student', create_student)
	app.add_url_rule('/admin/create/student/post/', 'create_student_post', create_student_post, methods = ['POST'])
	app.add_url_rule('/admin/student/<key>/', 'update_student', update_student)
	app.add_url_rule('/admin/student/post/', 'update_student_post', update_student_post, methods = ['POST'])
	app.add_url_rule('/admin/list/student/', 'view_student_list', view_student_list)

	#Course CRUD
	app.add_url_rule('/admin/create/course/', 'create_course', create_course)
	app.add_url_rule('/admin/create/course/post/', 'create_course_post', create_course_post, methods = ['POST'])
	app.add_url_rule('/admin/course/<key>/', 'update_course', update_course)
	app.add_url_rule('/admin/course/post/', 'update_course_post', update_course_post, methods = ['POST'])
	app.add_url_rule('/admin/list/course/', 'view_course_list', view_course_list)

	#Class CRUD
	app.add_url_rule('/admin/create/class/', 'create_class', create_class)
	app.add_url_rule('/admin/create/class/post/', 'create_class_post', create_class_post, methods = ['POST'])
	app.add_url_rule('/admin/class/<key>/', 'update_class', update_class)
	app.add_url_rule('/admin/class/post/', 'update_class_post', update_class_post, methods = ['POST'])
	app.add_url_rule('/admin/list/class/', 'view_class_list', view_class_list)

	#Attendance_course
	app.add_url_rule('/admin/class/<key>/courses/', 'view_class_courses', view_class_courses)
	app.add_url_rule('/admin/class/courses_map/post/', 'view_class_courses_post', view_class_courses_post, methods = ['POST'])

	#Deletion
	app.add_url_rule('/admin/delete/<table_name>/<entry_key>/', 'delete_confirm', delete_confirm)
	app.add_url_rule('/admin/delete/post/', 'delete_post', delete_post, methods = ['POST'])


def run_create_teacher_sql(db, form):
	db.execute('insert into teacher values (?, ?, ?)', [form['teacherid'], form['name'], form['password']])
	

def run_update_teacher_sql(db, form):
	db.execute('update teacher set name=?, password=? where teacherid=?', [form['name'], form['password'], form['teacherid']])
	

def run_create_student_sql(db, form):
	db.execute('insert into student values (?, ?, ?, ?)', [form['rno'], form['name'], form['classid'], form['password']])
	insert_att_student_sql(db)
	

def run_update_student_sql(db, form):
	db.execute('update student set name=?, password=? where rno=?', [form['name'], form['password'], form['rno']])
	

def run_create_course_sql(db, form):
	db.execute('insert into course values (?, ?)', [form['courseno'], form['coursename']])
	

def run_update_course_sql(db, form):
	db.execute('update course set coursename=? where courseno=?', [form['coursename'], form['courseno']])
	

def run_create_class_sql(db, form):
	db.execute('insert into class (branch, semester, section) values (?, ?, ?)', [form['branch'], form['semester'], form['section']])
	insert_att_student_sql(db)
	

def run_update_class_sql(db, form):
	db.execute('update class set branch=?, semester=?, section=? where classid=?', [form['branch'], form['semester'], form['section'], form['classid']])
	

def run_map_class_sql(db, form):
	db.execute('insert into attendance_course (teacherid, classid, courseno, total) values (?, ?, ?, 0)', [form['teacherid'], form['classid'], form['courseno']])
	insert_att_student_sql(db)
	

def run_delete_item_sql(db, form):
	key_attribute = {'class':'classid', 'student':'rno', 'course':'courseno', 'teacher':'teacherid', 'attendance_course':'aid'}
	query = "delete from " + form['table_name'] + " where " + key_attribute[form['table_name']] + "=?"
	db.execute(query, [ form['entry_key'] ])
	

def insert_att_student_sql(db):
	statement = """insert into att_student (aid, rno) 
				select attendance_course.aid, student.rno 
				from (attendance_course inner join student 
				on attendance_course.classid=student.classid) 
				where not aid in (select aid from att_student)
				and not rno in (select rno from att_student);"""

	db.execute(statement)
	statement = "update att_student set attended=0 where attended is null"
	db.execute(statement)


def get_teacher_info(db, teacherid):
	return rows_to_stringdicts(db.execute('select * from teacher where teacherid=?', [teacherid]).fetchall())[0]


def get_teacher_list(db):
	return rows_to_stringdicts(db.execute('select teacherid, name from teacher').fetchall())


def get_student_info(db, rno):
	return rows_to_stringdicts(db.execute('select * from student where rno=?', [rno]).fetchall())[0]


def get_student_list(db):
	return rows_to_stringdicts(db.execute('select * from student').fetchall())


def get_course_info(db, courseno):
	return rows_to_stringdicts(db.execute('select * from course where courseno=?', [courseno]).fetchall())[0]


def get_course_list(db):
	return rows_to_stringdicts(db.execute('select * from course').fetchall())


def get_class_info(db, classid):
	return rows_to_stringdicts(db.execute('select * from class where classid=?', [classid]).fetchall())[0]


def get_class_list(db):
	rows = db.execute('select * from class').fetchall()
	return rows_to_stringdicts(rows)


def rows_to_stringdicts(rows):
	new_rows = [dict(zip(row.keys(), [str(x) for x in row])) for row in rows]
	return new_rows


def get_course_teacher_list(db, classid):
	query = """select aid, teacher.name, course.coursename 
			from attendance_course inner join course 
			on attendance_course.courseno=course.courseno 
			inner join teacher 
			on attendance_course.teacherid=teacher.teacherid 
			where classid=?;"""
	return rows_to_stringdicts(db.execute(query, [classid]).fetchall())