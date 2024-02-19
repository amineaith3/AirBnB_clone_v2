#!/usr/bin/python3
"""script that start a Flask web application"""


# import Flask class from flask module
# import render_template for rendering templates to browser
from flask import Flask, render_template

# creates an instance called app of the class by passong the __name__ variable
appc = Flask(__name__)
appc.url_map.strict_slashes = False


@appc.route('/')
def index():
    """display "Hello HBNB!"

    Returns:
        str: text on the index page
    """
    return 'Hello HBNB!'


@appc.route('/hbnb')
def hbnb_route():
    """display "HBNB"

    Returns:
        str: text on the page
    """
    return 'HBNB'


@appc.route('/c/<text>')
def c_route(text):
    """display "C", followed by the value of the text variable

    Args:
        text (str): text to be served on the page

    Returns:
        str: text on the page
    """
    return 'C {}'.format(text.replace('_', ' '))


@appc.route('/python', defaults={'text': 'is cool'})
@appc.route('/python/<text>')
def python_route(text):
    """display "Python", followed by the value of the text variable

    Args:
        text (str): text to be served on the page

    Returns:
        str: text on the page
    """
    return 'Python {}'.format(text.replace('_', ' '))


@appc.route('/number/<int:n>')
def number_route(n):
    """display "n is a number" only if n is an integer

    Args:
        n (integer): number to be displayed on page

    Returns:
        str: text on the page
    """
    return '{} is a number'.format(n)


@appc.route('/number_template/<int:n>')
def number_template_route(n):
    """display a HTML page only if n is an integer

    H1 tag: "Number: n" inside the tag BODY

    Args:
        n (integer): number to be displayed on page

    Returns:
        str: text on the page
    """
    return render_template('5-number.html', num=n)


if __name__ == '__main__':
    appc.run(debug=True)
