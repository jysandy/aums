import flask
from flask import render_template

"""
******************************************************
~VIEWS
******************************************************
"""

def view_course_wise_att()
    check_login()
    run_view_course_wise_att(flask.g.db, flask.request.form)

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
