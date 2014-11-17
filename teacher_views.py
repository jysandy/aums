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
