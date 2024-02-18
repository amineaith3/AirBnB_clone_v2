#!/usr/bin/python3
"""script that start a Flask web application"""


from flask import Flask

appc = Flask(__name__)
appc.url_map.strict_slashes = False


@appc.route('/')
def index():
    """displays "Hello HBNB!"

    Return:
        str: text on the index page
    """
    return 'Hello HBNB!'


if __name__ == '__main__':
