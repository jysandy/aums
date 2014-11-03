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
	return render_template('admin/create_teacher.html', class_list = get_class_list())

def create_teacher_postback():
	check_login()
	run_create_teacher_sql(flask.g.db, flask.request.form)
	flask.flash('New teacher successfully created.')
	return flask.redirect(flask.url_for('home'))

#NOTE: The views for viewing and updating a teacher's info are the SAME.
def update_teacher(teacher_id):
	check_login()
	return render_template('admin/update_teacher.html', teacher_info = get_teacher_info(teacher_id))

def update_teacher_postback():
	check_login()
	run_update_teacher_sql(flask.g.db, flask.request.form)
	flask.flask('Teacher info successfully updated.')
	return redirect_to_home()

def view_teacher_list():
	check_login()
	return render_template('admin/teacher_list.html', teacher_list = get_teacher_list())

def create_student():
	check_login()
	return render_template('admin/create_student.html')

def create_student_postback():
	check_login()
	run_create_student_sql(flask.g.db, flask.request.form)
	flask.flash('New student successfully created.')
	return redirect_to_home()

def update_student(student_rno):
	check_login()
	return render_template('admin/update_student.html', student_info = get_student_info(student_rno))

def update_student_postback():
	check_login()
	run_update_student_sql(flask.g.db, flask.request.form)
	flask.flash('Student info successfully updated.')
	return redirect_to_home()

def create_course():
	check_login()
	return render_template('admin/create_course.html')

def create_course_postback():
	check_login()
	run_update_course_sql(flask.g.db, flask.request.form)
	flask.flash('New course successfully created.')
	return redirect_to_home()

def update_course(courseno):
	check_login()
	return render_template('admin/update_course.html', course_info = get_course_info(courseno))

def update_course_postback():
	check_login()
	run_update_course_sql(flask.g.db, flask.request.form)
	flask.flash('Course info successfully updated.')
	return redirect_to_home()

def create_class():
	check_login()
	return render_template('admin/create_class.html')

def create_class_postback():
	check_login()
	run_create_class_sql(flask.g.db, flask.request.form)
	flask.flash('New class successfully created.')
	return redirect_to_home()

def update_class(classid):
	check_login()
	return render_template('admin/update_class.html', class_info = get_class_info(classid))

def update_class_postback():
	check_login()
	run_update_class_sql(flask.g.db, flask.request.form)
	flask.flash('Class successfully updated.')
	return redirect_to_home()

def delete_confirm(table_name, entry_key):
	check_login()
	return render_template('admin/delete_confirm.html', table_name = table_name, entry_key = entry_key)

def delete_postback(table_name, entry_key):
	check_login()
	run_delete_item_sql(table_name, entry_key)
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
	return flask.redirect(flask.url_for(('home')))