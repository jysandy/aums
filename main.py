import flask
import os
import sqlite3
from contextlib import closing

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
	SECRET_KEY = 'kseurh98w5u0293gkjsnfdg8w834'))

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
~VIEWS
******************************************************
"""


"""
******************************************************
~RUN APPLICATION
******************************************************
"""
if __name__ == '__main__':
	app.run()