#!/usr/bin/python3
"""script that start a Flask web application"""


# import Flask class from flask module
from flask import Flask

# creates instance call app of the class by pass the __name__ variable
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
        str: texte on the page
    """
    return 'HBNB'


@appc.route('/c/<text>')
def c_route(text):
    """displaye "C", follow by the value of the text variable

    Args:
        text (str): text to be serve on the page

    Return:
        str: text on the page
    """
    return 'C {}'.format(text.replace('_', ' '))


@appc.route('/python', defaults={'text': 'is cool'})
@appc.route('/python/<text>')
def python_route(text):
    """displays "Python", followed by the value of the text variable

    Args:
        text (str): text to be served on the page

    Returns:
        str: text on the page
    """
    return 'Python {}'.format(text.replace('_', ' '))


@appc.route('/number/<int:n>')
def number_route(n):
    """display "n is a number" only if n is  integer

    Args:
        n (integer): number to be display on page

    Return:
        str: text on the page
    """
    return '{} is a number'.format(n)


if __name__ == '__main__':
    appc.run(debug=True)
