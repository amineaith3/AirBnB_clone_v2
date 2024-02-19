#!/usr/bin/python3
"""script that start a Flask web application"""


# import Flask class from flask module
from flask import Flask

# creates an instance called app of the class by passong the __name__ variable
appc = Flask(__name__)
appc.url_map.strict_slashes = False


@appc.route('/')
def index():
    """display "Hello HBNB!"

    Return:
        str: text on the indexe page
    """
    return 'Hello HBNB!'


@appc.route('/hbnb')
def hbnb_route():
    """display "HBNB"

    Return:
        str: text the page
    """
    return 'HBNB'


@appc.route('/c/<text>')
def c_route(text):
    """displays "C", follow by the value of the text variable

    Args:
        texte (str): text to serv on the page

    Return:
        str: text on the page
    """
    return 'C {}'.format(text.replace('_', ' '))


@appc.route('/python', default={'text': 'is cool'})
@appc.route('/python/<text>')
def python_route(text):
    """display "Python", follow by the value of the text variable

    Args:
        texte (str): text to be serve on the page

    Return:
        str: texte  the page
    """
    return 'Python {}'.format(text.replace('_', ' '))


if __name__ == '__main__':
    appc.run(debug=True)
