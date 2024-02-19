#!/usr/bin/python3
"""script that starts a Flask web application"""


# import Flask class from flask module
# import render_template for rendering templates to browser
# fetch data from storage engine
from flask import Flask, render_template

from models import storage

# creates an instance called app of the class by passong the __name__ variable
appc = Flask(__name__)
appc.url_map.strict_slashes = False


@appc.teardown_appcontext
def teardown_db(exception=None):
    """removes the current SQLAlchemy Session
    """
    if storage is not None:
        storage.close()


@appc.route('/states_list')
def states_list(n=None):
    """displays a HTML page: inside the tag BODY"""
    states = storage.all('State')
    return render_template('7-states_list.html', states=states)


if __name__ == '__main__':
    appc.run(debug=True)
