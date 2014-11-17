import flask
import os
import sqlite3
from contextlib import closing
import admin_views
import student_views
from flask import request, render_template, url_for, redirect, session, g

"""
******************************************************
~CONFIG
******************************************************
"""
app = flask.Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
	DATABASE = os.path.join(app.root_path, "aums.db"),
	DEBUG = True,
	SECRET_KEY = 'kseurh98w5u0293gkjsnfdg8w834',
	ADMIN_USERNAME = 'vendekka',
	ADMIN_PASSWORD = 'vforvendekka'))

"""
******************************************************
~DATABASE INIT
******************************************************
"""
def connect_db():
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

@app.before_request
def before_request():
	flask.g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	if hasattr(flask.g, 'db'):
		flask.g.db.close()

"""
******************************************************
~URLS
******************************************************
"""
admin_views.register_urls(app)
student_views.register_urls(app)


"""
******************************************************
~LOGIN AND LOGOUT
******************************************************
"""
@app.route('/')
def root():
	return redirect(url_for('login'))


@app.route('/login/', methods = ['GET', 'POST'])
def login():
	session.clear()
	if request.method == 'POST':
		if is_admin(request.form):
			session['admin_logged_in'] = True
			return redirect(url_for('admin_home'))
		elif is_teacher(request.form):
			session['teacherid'] = request.form['username']
			return redirect(url_for('teacher_home'))
		elif is_student(request.form):
			session['rno'] = request.form['username']
			return redirect(url_for('student_home'))
		else:
			return redirect(url_for('login'))

	return render_template('login.html')


@app.route('/logout/')
def logout():
	session.clear()
	return redirect(url_for('login'))


def is_admin(form):
	return form['username'] == app.config['ADMIN_USERNAME'] and form['password'] == app.config['ADMIN_PASSWORD']


def is_teacher(form):
	rows = g.db.execute('select * from teacher where teacherid=? and password=?', [ form['username'], form['password'] ]).fetchall()
	return len(rows) == 1


def is_student(form):
	rows = g.db.execute('select * from student where rno=? and password=?', [ form['username'], form['password'] ]).fetchall()
	return len(rows) == 1

"""
******************************************************
~RUN APPLICATION
******************************************************
"""
if __name__ == '__main__':
	if not os.path.isfile(app.config['DATABASE']):
		init_db()
	app.run()