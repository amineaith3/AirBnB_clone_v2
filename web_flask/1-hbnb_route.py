#!/usr/bin/python3
"""script that starts a Flask web application"""


# import Flask class from flask module
from flask import Flask

# creates an instance call app of the class by pass the __name__ variable
appc = Flask(__name__)
appc.url_map.strict_slashes = False


@appc.route('/')
def index():
    """display "Hello HBNB!"

    Return:
        str: texte on the indexe page
    """
    return 'Hello HBNB!'


@appc.route('/hbnb')
def hbnb_route():
    """display "HBNB"

    Returns:
        str: text on the page
    """
    return 'HBNB'


if __name__ == '__main__':
    appc.run(debug=True)
